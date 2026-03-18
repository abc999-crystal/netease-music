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


def is_app_running(app_name):
    """检查应用是否在运行"""
    try:
        if sys.platform == "darwin":
            result = subprocess.run(
                ["pgrep", "-f", app_name],
                capture_output=True
            )
            return result.returncode == 0
        elif sys.platform == "win32":
            result = subprocess.run(
                ['tasklist'], capture_output=True, text=True
            )
            return app_name in result.stdout
    except Exception:
        return False
    return False
    
def ensure_app_running(app_name):
    """确保应用已启动"""
    if not is_app_running(app_name):
        print(f"正在启动 {app_name}...")
        if sys.platform == "darwin":
            subprocess.run(["open", "-a", app_name])
        elif sys.platform == "win32":
            subprocess.run(["start", app_name], shell=True)
        # 等待应用启动
        import time
        for _ in range(10):
            time.sleep(1)
            if is_app_running(app_name):
                print("✅ 应用已启动")
                time.sleep(1)  # 额外等待确保完全就绪
                return True
        return False
    return True

def minimize_window():
    """最小化网易云音乐窗口"""
    try:
        if sys.platform == "darwin":
            script = '''
            tell application "System Events"
                tell process "NeteaseMusic"
                    set frontmost to true
                end tell
            end tell
            delay 0.2
            tell application "System Events"
                keystroke "m" using command down
            end tell
            '''
            subprocess.run(["osascript", "-e", script], capture_output=True)
        elif sys.platform == "win32":
            # Windows 下最小化
            ps_script = '''
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}
"@
$hwnd = (Get-Process -Name cloudmusic -ErrorAction SilentlyContinue).MainWindowHandle
if ($hwnd) { [Win32]::ShowWindow($hwnd, 6) }
'''
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
    except Exception:
        pass


def play(id, resource_type='song', minimize=True):
    """播放歌曲或歌单"""
    print("=" * 50)
    print(f"播放 {'歌曲' if resource_type == 'song' else '歌单'}")
    print("=" * 50)
    print(f"资源ID: {id}")
    
    app_name = "NeteaseMusic" if sys.platform == "darwin" else "cloudmusic"
    
    try:
        # 先确保客户端已启动
        if not ensure_app_running(app_name):
            raise Exception("无法启动网易云音乐客户端")
        
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
