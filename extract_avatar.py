#!/usr/bin/env python3
import json
import base64
import re

def extract_avatar_from_json():
    # 读取 JSON 文件
    with open('曾卫明简历.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 获取头像数据
    photo_data = data.get('basic', {}).get('photo', '')
    if not photo_data:
        print('JSON 中没有找到头像数据')
        return
    
    # 检查是否是 base64 数据
    if photo_data.startswith('data:image'):
        # 提取 base64 部分
        match = re.match(r'data:image/(\w+);base64,(.+)', photo_data)
        if match:
            img_format = match.group(1)  # jpeg, png 等
            base64_str = match.group(2)
            
            # 解码并保存
            try:
                img_data = base64.b64decode(base64_str)
                filename = f'avatar.{img_format}'
                
                with open(filename, 'wb') as f:
                    f.write(img_data)
                
                print(f'头像已保存为: {filename}')
                print(f'文件大小: {len(img_data)} 字节')
                
                # 更新 JSON 使用文件路径
                data['basic']['photo'] = filename
                with open('曾卫明简历.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print('JSON 已更新为使用文件路径')
                
            except Exception as e:
                print(f'保存头像失败: {e}')
        else:
            print('无法解析 base64 头像数据')
    else:
        print('头像数据不是 base64 格式')

if __name__ == '__main__':
    extract_avatar_from_json()