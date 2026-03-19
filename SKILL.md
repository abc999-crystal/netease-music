---
name: netease-music
description: 网易云音乐控制 skill。基于网易云音乐官方 API 实现，支持扫码登录、获取每日推荐、歌单管理、歌曲搜索和播放控制。让 AI Agent 可以通过自然语言控制网易云音乐播放。
allowed-tools: Bash
---

# 网易云音乐控制 Skill

通过网易云音乐 API 控制音乐播放。当用户请求播放音乐、搜索歌曲、查看每日推荐、管理歌单等操作时，使用此 skill。

**自动登录**：所有需要登录的操作会自动触发扫码登录，用户无需单独说"登录网易云"。

## 功能列表

| 功能 | 说明 |
|------|------|
| 扫码登录 | 启动二维码登录流程 |
| 退出登录 | 清除本地登录状态 |
| 检查状态 | 查看当前登录状态和用户信息 |
| 每日推荐 | 获取今日推荐歌曲列表 |
| 我的歌单 | 获取用户创建和收藏的歌单 |
| 搜索歌曲 | 按关键词搜索歌曲或歌单 |
| 播放歌曲/歌单 | 播放指定歌曲或歌单 |
| 播放控制 | 上一首/下一首、暂停/继续播放 |
| 音量调节 | 增加/降低音量 |
| 循环模式 | 关闭循环/单曲循环/全部循环 |
| 随机播放 | 开启/关闭随机播放 |

## 使用方式

### 1. 登录操作

```bash
~/.claude/skills/netease-music/scripts/login.py
```

扫码登录，登录状态保存在 `storage/cookies.json`。

### 2. 退出登录

```bash
~/.claude/skills/netease-music/scripts/logout.py
```

清除本地保存的登录状态。

### 3. 检查状态

```bash
~/.claude/skills/netease-music/scripts/status.py
```

会显示当前登录状态。

### 4. 每日推荐

```bash
~/.claude/skills/netease-music/scripts/daily_recommend.py
```

### 5. 我的歌单

```bash
~/.claude/skills/netease-music/scripts/my_playlists.py
```

### 6. 搜索歌曲

```bash
~/.claude/skills/netease-music/scripts/search.py "关键词"

# 搜索歌单
~/.claude/skills/netease-music/scripts/search.py "关键词" --type 1000
```

### 7. 播放歌曲/歌单

```bash
# 播放单曲（默认会最小化客户端窗口）
~/.claude/skills/netease-music/scripts/play.py play <歌曲ID>

# 播放歌单
~/.claude/skills/netease-music/scripts/play.py play <歌单ID> --type playlist
```

### 8. 播放控制

```bash
# 上一首
~/.claude/skills/netease-music/scripts/play.py previous

# 下一首
~/.claude/skills/netease-music/scripts/play.py next

# 暂停播放
~/.claude/skills/netease-music/scripts/play.py pause

# 继续播放
~/.claude/skills/netease-music/scripts/play.py resume
```

### 9. 音量调节

```bash
# 增加音量（默认 25%）
~/.claude/skills/netease-music/scripts/play.py volume-up

# 降低音量（默认 25%）
~/.claude/skills/netease-music/scripts/play.py volume-down
```

### 10. 循环模式

```bash
# 关闭循环
~/.claude/skills/netease-music/scripts/play.py loop-off

# 单曲循环
~/.claude/skills/netease-music/scripts/play.py loop-one

# 全部循环
~/.claude/skills/netease-music/scripts/play.py loop-all
```

### 11. 随机播放

```bash
# 切换随机播放
~/.claude/skills/netease-music/scripts/play.py shuffle
```

**特性**：播放成功后会自动唤起网易云音乐客户端，并默认最小化窗口，提供更好的体验。

## 使用示例

### 扫码登录
**User**: "帮我登录网易云音乐"  
**Action**: 运行 login.py，显示二维码，提示用户扫码

### 退出登录
**User**: "退出网易云登录"  
**Action**: 运行 logout.py，清除登录状态

### 今日推荐
**User**: "今天有什么推荐歌曲"  
**Action**: 运行 daily_recommend.py，返回推荐歌曲列表

### 搜索播放
**User**: "播放周杰伦的歌"  
**Action**: 
1. search.py "周杰伦"
2. 用户选择歌曲后，play.py play <歌曲ID>

### 播放控制
**User**: "切歌"  
**Action**: 运行 play.py next

**User**: "暂停"  
**Action**: 运行 play.py pause

**User**: "继续播放"  
**Action**: 运行 play.py resume

**User**: "音量调大"  
**Action**: 运行 play.py volume-up

**User**: "开启单曲循环"  
**Action**: 运行 play.py loop-one

**User**: "开启随机播放"  
**Action**: 运行 play.py shuffle

## 依赖

- Python 3.10+
- pyncm
- qrcode
- pillow
