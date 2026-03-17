#!/usr/bin/env python3
"""网易云音乐播放脚本"""
import os
import sys
import json
import base64
import argparse
import subprocess
import warnings
warnings.filterwarnings('ignore', message='.*urllib3.*')

from pathlib import Path


def minimize_window():
    """最小化网易云音乐窗口"""
    try:
        if sys.platform == "darwin":
            # 使用 AppleScript 最小化网易云音乐
            script = '''
            tell application "System Events"
                set frontmost of process "cloudmusic" to true
            end tell
            tell application "网易云音乐"
                activate
                set visible of front window to false
            end tell
            '''
            subprocess.run(["osascript", "-e", script], capture_output=True)
        elif sys.platform == "win32":
            # Windows 下最小化
            subprocess.run(['powershell', '-Command', 
                '(Get-Process -Name "cloudmusic" -ErrorAction SilentlyContinue).MainWindowHandle | ForEach-Object { [Win32]::ShowWindow($_, 6) }'],
                capture_output=True)
    except Exception:
        pass


def play(id, resource_type='song', minimize=True):
    """播放歌曲或歌单"""
    print("=" * 50)
    print(f"播放 {'歌曲' if resource_type == 'song' else '歌单'}")
    print("=" * 50)
    print(f"资源ID: {id}")
    
    try:
        command = {"type": resource_type, "id": str(id), "cmd": "play"}
        json_str = json.dumps(command, separators=(",", ":"))
        encoded = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
        app_url = f"orpheus://{encoded}"
        
        print(f"\n尝试唤起网易云音乐客户端...")
        
        if sys.platform == "win32":
            os.startfile(app_url)
        else:
            ret = subprocess.run(["open", app_url], capture_output=True)
            if ret.returncode != 0:
                raise FileNotFoundError("macOS open failed")
        
        print("✅ 已发送播放指令")
        
        # 等待一下让客户端启动
        import time
        time.sleep(1)
        
        if minimize:
            minimize_window()
            print("✅ 已最小化客户端窗口")
        
        return True
        
    except (OSError, FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"⚠️ 无法唤起客户端: {e}")
        print("尝试使用网页版...")
        
        web_type = "song" if resource_type == "song" else "playlist"
        web_url = f"https://music.163.com/#/{web_type}?id={id}"
        
        if sys.platform == "win32":
            os.startfile(web_url)
        else:
            subprocess.run(["open", web_url])
        
        print(f"已在浏览器中打开: {web_url}")
        return True
    
    except Exception as e:
        print(f"❌ 播放失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='网易云音乐播放')
    parser.add_argument('--id', required=True, help='资源ID')
    parser.add_argument('--type', choices=['song', 'playlist'], default='song',
                       help='资源类型: song=歌曲, playlist=歌单')
    parser.add_argument('--no-minimize', action='store_true',
                       help='不最小化客户端窗口')
    
    args = parser.parse_args()
    play(args.id, args.type, not args.no_minimize)


if __name__ == "__main__":
    main()
