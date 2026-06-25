---
name: xiaohongshu-poster
description: "Xiaohongshu auto poster - generates big-font cards with emoji, uploads to draft box. Zero token cost. Human-like delays."
version: 3.0.0
author: Hermes Agent
platforms: [windows]
prerequisites:
  python_packages: [DrissionPage]
  commands: [chrome]
---

# 小红书自动发帖 v3

## 项目位置
`D:\Hermes agnet\` (GitHub: `项目名/hermes-xiaohongshu-poster`)

## 文件结构
```
├── scripts/gen_v4.py       # 当前脚本
├── posts/                   # 文章配置JSON
├── assets/                  # 生成图片缓存
├── skills/                  # 本文档
└── README.md
```

## 使用方法
```bash
python "D:/Hermes agnet/scripts/gen_v4.py" --post-name <配置名>
```
1. 生成4张大字卡片 (隐藏滚动条, scale-factor=2高清晰)
2. 上传到创作者平台
3. 填标题+正文
4. 保存草稿箱 → 用户手动发布

## 核心运营知识速查

### 算法五维度
原创30% + 互动25% + 完播20% + 停留15% + 分享10%

### CES评分
点赞x1 + 收藏x1 + 评论x4 + 转发x4 + 关注x8

### 五大选题
预算类 | 对比类 | 车型类 | 顾虑类 | 效果类

### POI指标（蓝V）
POI点击率25% → 下单转化60% → 核销率20% → 同城精准度20%

### 合规红线
AI标注 → 禁私域引流 → 禁虚假人设 → 禁洗稿

## 完整知识手册
桌面 → 小红书知识库 → 线下授课 → 小红书运营知识手册_综合精编版.docx
