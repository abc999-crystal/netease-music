# netease-music

A Claude Code skill for controlling NetEase Cloud Music via official API. Supports QR code login, daily recommendations, playlist management, song search and playback control. Enables AI Agent to control NetEase Cloud Music playback through natural language.

> **Note**: This skill is published to Ant internal tnpm registry as `@antskill/netease-music`

## Features

| Feature | Description |
|---------|-------------|
| QR Login | Scan QR code to login to NetEase Cloud Music |
| Logout | Clear local login status |
| Status Check | View current login status and user info |
| Daily Recommendations | Get today's recommended songs |
| My Playlists | Get user created and favorited playlists |
| Song Search | Search songs or playlists by keyword |
| Playback Control | Play specific songs or playlists |

## Installation

### Global Installation (Recommended)

```bash
tnpm install -g @antskill/netease-music
```

### Project-Level Installation

```bash
tnpm install @antskill/netease-music
```

## Usage

After installation, the skill will automatically activate in these scenarios:

### 1. QR Login

```
Help me login to NetEase Cloud Music
```

### 2. Logout

```
Logout NetEase
Exit NetEase login
```

### 3. Check Login Status

```
Check NetEase login status
```

### 4. Daily Recommendations

```
What songs are recommended today?
Show me daily recommendations
```

### 5. Search Songs

```
Search Jay Chou's songs
Find some G.E.M. songs
```

### 6. View Playlists

```
Show my playlists
View my favorites
```

### 7. Play Music

```
Play a song for me
Play Jay Chou's Rice Fragrance
Play my favorite playlist
```

**Auto Login**: All operations requiring login will automatically trigger QR code login. Users don't need to explicitly say "login to NetEase".

## First-Time Usage

1. **Install skill**: Run `tnpm install -g @antskill/netease-music`
2. **Trigger any feature**: Tell AI what you want to do (e.g., "Play Jay Chou's song")
3. **Auto login**: If not logged in, AI will show QR code for scanning
4. **Start using**: After login, you can use all features

## Data Privacy

- Login status is only stored locally in `scripts/storage/cookies.json`
- All API calls go directly to NetEase Cloud Music official servers
- No third-party data transmission
- Delete `storage/` directory to clear all data

## Platform Compatibility

| Feature | macOS | Windows | Linux |
|---------|-------|---------|-------|
| QR Login | ✅ | ✅ | ✅ |
| API Calls | ✅ | ✅ | ✅ |
| Client Playback | ✅ | ✅ | ⚠️ |
| Web Playback | ✅ | ✅ | ✅ |

- macOS: Primary test platform, full support
- Windows: Requires NetEase Cloud Music client installed
- Linux: May need to configure URL opening method

## Local Development

```bash
# Clone project
git clone https://github.com/abc999-crystal/netease-music.git
cd netease-music

# Local install for testing
node install-skill.js

# Publish to tnpm
tnpm login
tnpm publish
```

## FAQ

**Q: Do I need to login every time?**  
A: No. Login status is stored locally and remains valid until `cookies.json` is deleted.

**Q: No response after scanning QR code?**  
A: Please scan within 30 seconds. If timeout, run login again.

**Q: Playback only works on macOS?**  
A: Priority to use client playback. If client unavailable, automatically opens web version which works on all platforms.

**Q: How to clear login status?**  
A: Delete `scripts/storage/cookies.json` file.

**Q: Search results not accurate?**  
A: Try searching after login, some content requires login for accurate results.

## Dependencies

- `pyncm` - NetEase Cloud Music Python API
- `qrcode` - QR code generation
- `Pillow` - Image processing
- `requests` - HTTP requests

## License

MIT
