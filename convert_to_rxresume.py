#!/usr/bin/env python3
import json
import sys
import os
from datetime import datetime

def convert_magicv_to_rxresume(input_path):
    """将magicv.art的JSON简历转换为rxresu.me格式"""
    
    with open(input_path, 'r', encoding='utf-8') as f:
        magicv_data = json.load(f)
    
    # 提取基本信息
    basic = magicv_data.get('basic', {})
    
    # 构建basics部分
    rx_basics = {
        "name": basic.get('name', ''),
        "label": basic.get('title', ''),
        "email": basic.get('email', ''),
        "phone": basic.get('phone', ''),
        "location": basic.get('location', ''),
        "birthDate": basic.get('birthDate', ''),
        "summary": "",  # 可以后续从customData中提取
        "photo": {
            "url": basic.get('photo', ''),
            "visible": basic.get('photoConfig', {}).get('visible', True)
        }
    }
    
    # 构建sections部分
    rx_sections = {}
    
    # 1. 工作经历 (work)
    work_experiences = []
    for exp in magicv_data.get('experience', []):
        # 解析日期字符串
        date_str = exp.get('date', '')
        start_date, end_date = parse_date_range(date_str)
        
        work_item = {
            "company": exp.get('company', ''),
            "position": exp.get('position', ''),
            "startDate": start_date,
            "endDate": end_date,
            "summary": html_to_text(exp.get('details', '')),
            "highlights": extract_highlights(exp.get('details', ''))
        }
        work_experiences.append(work_item)
    
    if work_experiences:
        rx_sections["work"] = {
            "name": "Work Experience",
            "columns": 1,
            "visible": True,
            "items": work_experiences
        }
    
    # 2. 教育经历 (education)
    educations = []
    for edu in magicv_data.get('education', []):
        edu_item = {
            "institution": edu.get('school', ''),
            "area": edu.get('major', ''),
            "studyType": edu.get('degree', ''),
            "startDate": format_date(edu.get('startDate')),
            "endDate": format_date(edu.get('endDate')),
            "score": edu.get('gpa', ''),
            "courses": []
        }
        educations.append(edu_item)
    
    if educations:
        rx_sections["education"] = {
            "name": "Education",
            "columns": 1,
            "visible": True,
            "items": educations
        }
    
    # 3. 项目经历 (projects)
    projects = []
    for proj in magicv_data.get('projects', []):
        proj_item = {
            "name": proj.get('name', ''),
            "description": html_to_text(proj.get('description', '')),
            "startDate": "",  # 从date字段解析
            "endDate": "",
            "url": "",
            "highlights": []
        }
        
        # 尝试解析日期
        date_str = proj.get('date', '')
        if date_str:
            start_date, end_date = parse_date_range(date_str)
            proj_item["startDate"] = start_date
            proj_item["endDate"] = end_date
        
        projects.append(proj_item)
    
    if projects:
        rx_sections["projects"] = {
            "name": "Projects",
            "columns": 1,
            "visible": True,
            "items": projects
        }
    
    # 4. 技能 (skills)
    skill_content = magicv_data.get('skillContent', '')
    if skill_content:
        # 提取技能列表
        skills_list = extract_skills_from_html(skill_content)
        rx_sections["skills"] = {
            "name": "Skills",
            "columns": 2,
            "visible": True,
            "items": [{"name": skill} for skill in skills_list]
        }
    
    # 5. 自定义部分 (个人优势)
    custom_data = magicv_data.get('customData', {})
    if 'custom-1' in custom_data and custom_data['custom-1']:
        advantages = custom_data['custom-1']
        advantage_items = []
        for adv in advantages:
            advantage_items.append({
                "title": adv.get('title', ''),
                "description": html_to_text(adv.get('description', ''))
            })
        
        rx_sections["custom"] = {
            "name": "Personal Advantages",
            "columns": 1,
            "visible": True,
            "items": advantage_items
        }
    
    # 构建metadata
    rx_metadata = {
        "template": "kendall",
        "layout": [
            ["work", "education"],
            ["projects", "skills"],
            ["custom"]
        ],
        "css": {
            "theme": "default"
        },
        "page": {
            "margin": 18,
            "format": "a4"
        },
        "typography": {
            "fontFamily": "Inter",
            "fontSize": 14
        }
    }
    
    # 构建最终输出
    rx_resume = {
        "basics": rx_basics,
        "sections": rx_sections,
        "metadata": rx_metadata
    }
    
    return rx_resume

def parse_date_range(date_str):
    """解析日期范围字符串，如'2024/2- 2025/11'"""
    if not date_str:
        return "", ""
    
    # 清理空格
    date_str = date_str.replace(' ', '')
    
    # 尝试多种分隔符
    separators = ['-', '~', '—', '–', 'to']
    
    for sep in separators:
        if sep in date_str:
            parts = date_str.split(sep)
            if len(parts) == 2:
                start_date = format_date_string(parts[0])
                end_date = format_date_string(parts[1])
                return start_date, end_date
    
    # 如果没有分隔符，假设是单个日期
    return format_date_string(date_str), ""

def format_date_string(date_str):
    """格式化日期字符串为YYYY-MM-DD格式"""
    if not date_str:
        return ""
    
    # 尝试解析多种格式
    date_str = date_str.strip()
    
    # 处理中文日期格式
    date_str = date_str.replace('年', '-').replace('月', '-').replace('日', '')
    
    # 尝试解析
    try:
        # 如果是年份
        if len(date_str) == 4 and date_str.isdigit():
            return f"{date_str}-01-01"
        
        # 如果是YYYY/MM格式
        if '/' in date_str:
            parts = date_str.split('/')
            if len(parts) == 2:
                year = parts[0]
                month = parts[1].zfill(2)
                return f"{year}-{month}-01"
            elif len(parts) == 3:
                year = parts[0]
                month = parts[1].zfill(2)
                day = parts[2].zfill(2)
                return f"{year}-{month}-{day}"
        
        # 如果是YYYY-MM格式
        if '-' in date_str:
            parts = date_str.split('-')
            if len(parts) == 2:
                year = parts[0]
                month = parts[1].zfill(2)
                return f"{year}-{month}-01"
            elif len(parts) == 3:
                return date_str
        
        # 尝试其他格式
        return date_str
    except:
        return date_str

def format_date(date_str):
    """格式化ISO日期字符串"""
    if not date_str:
        return ""
    
    try:
        # 如果是ISO格式
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d')
    except:
        return date_str

def html_to_text(html):
    """简单的HTML到文本转换"""
    if not html:
        return ""
    
    # 移除HTML标签
    import re
    text = re.sub(r'<[^>]+>', ' ', html)
    
    # 合并空格
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def extract_highlights(html):
    """从HTML中提取要点"""
    if not html:
        return []
    
    # 查找列表项或段落
    import re
    highlights = []
    
    # 查找<li>标签
    li_matches = re.findall(r'<li[^>]*>(.*?)</li>', html, re.DOTALL)
    if li_matches:
        for match in li_matches:
            highlights.append(html_to_text(match))
    
    # 如果没有<li>，查找<p>标签
    if not highlights:
        p_matches = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
        for match in p_matches:
            text = html_to_text(match)
            if text and len(text) > 10:  # 过滤太短的段落
                highlights.append(text)
    
    return highlights[:5]  # 最多返回5个要点

def extract_skills_from_html(html):
    """从HTML中提取技能列表"""
    if not html:
        return []
    
    # 提取文本
    text = html_to_text(html)
    
    # 查找技能关键词
    skills = []
    
    # 常见技能关键词
    skill_keywords = [
        '3ds Max', 'Vray', 'SketchUp', 'SU', '酷家乐', 'AutoCAD', 
        'Illustrator', 'AI', 'Photoshop', 'PS', 'Python', 'AI编程',
        '空间建模', '渲染', '施工图', '效果图', '品牌视觉', '橱窗设计',
        'DP点', '陈列道具', '工程量预决算', '模块化', '标准化'
    ]
    
    for keyword in skill_keywords:
        if keyword in text:
            skills.append(keyword)
    
    # 如果没有找到关键词，返回通用技能
    if not skills:
        skills = ['空间设计', '工程管理', '品牌形象开发', '施工监理', '成本控制']
    
    return skills

def main():
    if len(sys.argv) < 2:
        print("用法: python convert_to_rxresume.py <输入JSON文件> [输出JSON文件]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        # 默认输出文件名
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_rxresume.json"
    
    if not os.path.exists(input_file):
        print(f"错误: 文件 '{input_file}' 不存在")
        sys.exit(1)
    
    try:
        print(f"正在转换: {input_file}")
        rx_resume = convert_magicv_to_rxresume(input_file)
        
        # 保存转换后的JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(rx_resume, f, ensure_ascii=False, indent=2)
        
        print(f"转换完成! 输出文件: {output_file}")
        print(f"\n基本信息:")
        print(f"  姓名: {rx_resume['basics'].get('name', 'N/A')}")
        print(f"  职位: {rx_resume['basics'].get('label', 'N/A')}")
        print(f"  工作经历: {len(rx_resume['sections'].get('work', {}).get('items', []))} 项")
        print(f"  教育经历: {len(rx_resume['sections'].get('education', {}).get('items', []))} 项")
        print(f"  项目经历: {len(rx_resume['sections'].get('projects', {}).get('items', []))} 项")
        
    except Exception as e:
        print(f"转换过程中出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()