# 曾卫明个人简历网站

这是一个个人简历网站项目，包含静态版本和 JSON 动态加载版本。

## 🌐 在线访问

- **静态版本**: https://bullshitai52.github.io/my/
- **JSON 动态版本**: https://bullshitai52.github.io/my/resume-json.html

## 📁 项目结构

```
cadname/
├── index.html              # 静态简历页面
├── resume-json.html        # JSON 动态简历页面
├── 曾卫明简历.json         # 完整的简历数据 (JSON 格式)
├── style.css              # 样式文件
├── script.js              # 交互脚本
├── convert_to_rxresume.py # 简历格式转换脚本
├── vercel.json            # Vercel 部署配置
├── .github/               # GitHub Actions 工作流
│   └── workflows/
│       ├── deploy.yml     # Vercel 部署工作流
│       ├── deploy-gh-pages.yml # GitHub Pages 工作流
│       └── static.yml     # 简化版 Pages 工作流
├── .env.example           # 环境变量示例文件
├── .gitignore            # Git 忽略规则
└── README.md             # 项目说明文件
```

## 🔧 使用方法

### 1. 头像功能

#### HTML 静态版本 (`index.html`)
- **上传头像**: 点击"更换头像"按钮，选择本地图片文件
- **自动保存**: 头像会保存到浏览器本地存储，下次访问时自动加载
- **支持格式**: JPG、PNG、GIF 等图片格式
- **大小限制**: 最大 2MB
- **默认头像**: 使用 Unsplash 的默认头像

#### JSON 动态版本 (`resume-json.html`)
- **自动加载**: 从 `曾卫明简历.json` 文件的 `basic.photo` 字段加载头像
- **支持格式**: 
  - Base64 编码图片（如 `data:image/jpeg;base64,...`）
  - 外部图片 URL（如 `https://example.com/photo.jpg`）
- **当前数据**: JSON 中已包含 base64 编码的头像

### 2. 更新简历内容

#### 方法一：更新 JSON 文件（推荐）
编辑 `曾卫明简历.json` 文件，然后推送到 GitHub：
```bash
git add 曾卫明简历.json
git commit -m "更新简历内容"
git push origin main
```

网站会自动更新，JSON 版本会显示最新内容。

#### 方法二：更新 HTML 文件
直接编辑 `index.html` 文件中的内容。

### 2. 本地预览
在浏览器中打开 `index.html` 或 `resume-json.html` 文件即可预览。

### 3. 部署更新
推送到 `main` 分支后，GitHub Pages 会自动部署：
```bash
git push origin main
```

## 📋 文件说明

### 主要文件
- **`index.html`**: 静态简历页面，内容直接写在 HTML 中
- **`resume-json.html`**: 动态简历页面，从 `曾卫明简历.json` 加载数据
- **`曾卫明简历.json`**: 完整的简历数据，包含：
  - 基本信息（姓名、职位、联系方式）
  - 教育经历
  - 工作经历（8条记录）
  - 项目经历（4个项目）
  - 专业技能
  - 个人优势

### 辅助文件
- **`convert_to_rxresume.py`**: 将 magicv.art 格式的 JSON 转换为 rxresu.me 格式
- **`vercel.json`**: Vercel 平台部署配置
- **`.github/workflows/`**: 自动部署工作流

### 配置文件
- **`.env.example`**: 环境变量示例（不包含真实密钥）
- **`.env`**: 本地环境变量（**不要上传到 GitHub**）
- **`.gitignore`**: 指定不需要版本控制的文件

## 🚀 部署方式

### GitHub Pages（当前使用）
自动部署到：https://bullshitai52.github.io/my/

### Vercel（备选）
如果需要部署到 Vercel：
1. 访问 https://vercel.com
2. 导入 GitHub 仓库 `bullshitAI52/my`
3. 点击部署

## 🔄 更新流程

1. **编辑简历内容**
   - 更新 `曾卫明简历.json` 文件
   - 或更新 `index.html` 文件

2. **提交更改**
   ```bash
   git add .
   git commit -m "更新描述"
   git push origin main
   ```

3. **等待部署**
   - GitHub Pages 会自动部署（约1-2分钟）
   - 访问网站查看更新

## ⚠️ 注意事项

1. **不要上传 `.env` 文件**
   - `.env` 包含敏感信息（API 密钥等）
   - 使用 `.env.example` 作为模板
   - `.gitignore` 已排除 `.env` 文件

2. **JSON 文件编码**
   - 使用 UTF-8 编码
   - 确保 JSON 格式正确

3. **图片处理**
   - 当前 JSON 中的照片使用 base64 编码
   - 如需更换照片，可更新 base64 数据或使用外部链接

## 📞 联系方式

如有问题或需要帮助，请联系：
- 邮箱: 64920093@qq.com
- 电话: 18059867695

---

**最后更新**: 2025-12-30  
**部署状态**: ✅ 正常