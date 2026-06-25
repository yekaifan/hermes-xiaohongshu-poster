---
name: xiaohongshu-poster
description: "Xiaohongshu auto poster - generates big-font cards with emoji, uploads to draft box. Zero token cost. Human-like delays."
version: 4.0.0
author: Hermes Agent
platforms: [windows]
prerequisites:
  python_packages: [DrissionPage]
  commands: [chrome]
---

# 小红书自动发帖 v4

## 项目位置
`D:\Hermes agnet\`

## 文件结构
```
D:\Hermes agnet\
├── scripts\
│   └── gen_v4.py              # 当前在用脚本
├── posts\                      # 文章配置（JSON）
│   ├── 4s_free_film.json       # 第一篇：4S店免费膜
│   └── new_car_first.json      # 第二篇：新车落地先做啥
├── assets\                     # 自动生成的配图缓存
├── skills\xiaohongshu-poster\  # 本skill
├── README.md                   # GitHub说明
└── .gitignore
```

## 发帖流程

### 一次性设置
```bash
# 启动Chrome远程调试
"C:/Program Files/Google/Chrome/Application/chrome.exe" \
  --remote-debugging-port=9223 \
  --user-data-dir="C:/Users/OKykf/AppData/Local/Google/Chrome/User Data/XHS_Account1"
```
首次需扫码登录小红书。之后重启浏览器session自动恢复。

### 每次发帖
```bash
python "D:/Hermes agnet/scripts/gen_v4.py" --post-name <配置名>
```
1. 生成4张高清大字卡片
2. 上传到创作者平台
3. 填写标题+正文
4. 保存到草稿箱
5. **用户手动**：打开 `creator.xiaohongshu.com` → 草稿箱 → 发布

### 新建文章
在 `D:\Hermes agnet\posts\` 下创建 `xxx.json`：
```json
{
  "port": 9223,
  "title": "标题（≤20字）",
  "body": "正文内容...",
  "card_cover_title": "封面文字",
  "card_cover_sub": "副标题\\n多行用\\n分隔",
  "card_cover_style": "dark",
  "card2_title": "卡片2",
  "card2_sub": "...",
  "card2_style": "teal",
  "card3_title": "卡片3",
  "card3_sub": "...",
  "card3_style": "orange",
  "card4_title": "卡片4",
  "card4_sub": "...",
  "card4_style": "dark"
}
```

可用配色：`dark` `orange` `teal` `white` `navy`

## 卡片设计硬性规则

| 规则 | 值 | 原因 |
|------|----|------|
| 标题字号 | **48px** 加粗 | 要醒目 |
| 正文字号 | **36px** 加粗 | 不能有小字 |
| 配色 | 白字+深色背景 | 黑字加深底看不见 |
| Emoji | 每图2-4个 | 增加吸引力 |
| 装饰元素 | ❌ 不要 | 无意义 |
| CSS方法 | 全部inline style | 用class可能漏定义 |
| 滚动条 | `overflow:hidden` + `::-webkit-scrollbar{display:none}` | 截图不美观 |
| 清晰度 | `--device-scale-factor=2` | 默认截图模糊 |

## 安全规则

- 每步操作间隔 **3-7秒**随机
- 每天总操作 **≤10次**
- 不 **kill Chrome**
- 不 **p.quit()**
- 个人号不索要微信/电话

## 已知限制

- 发布按钮（`XHS-PUBLISH-BTN`）点击会触发保存草稿而非正式发布
- 需用户手动从草稿箱发布
- 暂无评论回复功能

## 更新记录

- v4.0 - 修复滚动条+清晰度，支持配置文件驱动
- v3.0 - 修复CSS class未定义的bug，全部改用inline style
- v2.0 - 大字版+emu
- v1.0 - 初始版本
