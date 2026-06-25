# 小红书自动发帖工具 (Xiaohongshu Auto Poster)

自动生成大字卡片 → 上传小红书创作者平台 → 保存草稿箱

## 快速开始

### 前置条件
- Windows 系统
- Chrome 浏览器
- Python 3.8+ (需安装 DrissionPage)

### 安装
```bash
pip install DrissionPage
# 或用 uv
uv pip install DrissionPage
```

### 启动浏览器
```bash
# 账号1（个人种草号）
"C:/Program Files/Google/Chrome/Application/chrome.exe" \
  --remote-debugging-port=9223 \
  --user-data-dir="./chrome_profile_account1"
```

打开 `xiaohongshu.com` 扫码登录（仅首次）。

### 发帖
```bash
python scripts/gen_v4.py --post-name <配置名>
```

示例：
```bash
python scripts/gen_v4.py --post-name new_car_first
```

然后打开 `creator.xiaohongshu.com` → 草稿箱 → 发布。

## 目录结构

```
D:\Hermes agnet\
├── scripts\
│   └── gen_v4.py          # 核心发帖脚本（零token消耗）
├── posts\                  # 文章配置（JSON）
│   ├── 4s_free_film.json   # 第一篇：4S店免费膜
│   └── new_car_first.json  # 第二篇：新车落地先做啥
├── assets\                 # 自动生成的配图（按文章分目录）
├── skills\                 # 技能文档
│   └── xiaohongshu-poster\
└── .gitignore
```

## 如何发新帖

### 第一步：新建文章配置
在 `posts/` 下创建 `xxx.json`，格式参考现有文件。

### 第二步：运行脚本
```bash
python scripts/gen_v4.py --post-name xxx
```

脚本自动：
1. 生成4张高清大字卡片（HTML→Chrome headless截图）
2. 上传到小红书创作者平台
3. 填标题+正文
4. 保存到草稿箱

### 第三步：手动发布
打开 `creator.xiaohongshu.com` → 草稿箱 → 检查 → 发布

## 卡片设计规范

| 规则 | 要求 |
|------|------|
| 字号 | 标题48px，正文36px |
| 配色 | 白字 + 深色背景，高对比度 |
| Emoji | 每图2-4个 |
| 装饰 | 不要无用CSS装饰 |
| CSS | 全部inline style，不用class |
| 滚动条 | 已隐藏 |
| 清晰度 | `--device-scale-factor=2` |
| 延迟 | 每步3-7秒随机，防检测 |

## 注意事项

- 标题不超过 **20个字**
- 每天操作不超过 **10次**
- 不在个人号索要微信/电话
- 发布按钮暂时无法自动点击（React组件限制）

## 核心运营知识

### 平台算法五维度
| 维度 | 权重 | 优化方向 |
|------|------|---------|
| 原创度 | 30% | 每个内容必须原创，真实案例+实拍 |
| 互动深度 | 25% | 评论引导，评论加权是点赞的4x |
| 完播率 | 20% | 前3秒钩子，节奏紧凑 |
| 停留时长 | 15% | 干货信息量，分段清晰 |
| 分享率 | 10% | 引发共鸣，实用收藏价值 |

### CES评分
`CES = 点赞x1 + 收藏x1 + 评论x4 + 转发x4 + 关注x8`

### 五大选题（灰灰老师培训）
预算类、对比类、车型类、顾虑类、效果类

### POI指标（蓝V核心）
POI点击率25% → 下单转化60% → 核销率20%续命 → 同城精准度20%

### 合规红线
AI标注、禁私域引流、禁虚假人设、禁洗稿

完整知识手册：`{用户目录}/Desktop/小红书知识库/线下授课/小红书运营知识手册_综合精编版.docx`

## License

MIT
