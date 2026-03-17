#!/usr/bin/env python3
"""我的歌单"""
import json
import subprocess
import sys
import warnings
warnings.filterwarnings('ignore', message='.*urllib3.*')

from pathlib import Path
from pyncm import GetCurrentSession, apis

SCRIPT_DIR = Path(__file__).parent
STORAGE_DIR = SCRIPT_DIR / "storage"
COOKIE_FILE = STORAGE_DIR / "cookies.json"


def load_session():
    if COOKIE_FILE.exists():
        try:
            with open(COOKIE_FILE) as f:
                cookies = json.load(f)
                GetCurrentSession().cookies.update(cookies)
            return True
        except:
            pass
    return False


def auto_login():
    print("未登录，正在调用扫码登录...")
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "login.py")],
        capture_output=True, text=True
    )
    return load_session()


def get_my_playlists():
    print("=" * 50)
    print("我的歌单")
    print("=" * 50)
    
    if not load_session():
        if not auto_login():
            print("\n登录失败，无法获取歌单")
            return
    
    try:
        user_info = apis.login.GetCurrentLoginStatus()
        if user_info.get('code') != 200:
            print("登录状态失效")
            return
            
        uid = user_info.get('account', {}).get('id')
        
        result = apis.user.GetUserPlaylists(uid)
        
        if result.get('code') == 200:
            playlists = result.get('playlist', [])
            
            if playlists:
                print(f"\n共 {len(playlists)} 个歌单:\n")
                
                created = [p for p in playlists if p.get('creator', {}).get('userId') == uid]
                subscribed = [p for p in playlists if p.get('creator', {}).get('userId') != uid]
                
                if created:
                    print("【我创建的歌单】")
                    for i, pl in enumerate(created, 1):
                        print(f"{i:2d}. {pl.get('name')} ({pl.get('trackCount', 0)}首, ID: {pl.get('id')})")
                
                if subscribed:
                    print("\n【我收藏的歌单】")
                    start = len(created) + 1
                    for i, pl in enumerate(subscribed, start):
                        print(f"{i:2d}. {pl.get('name')} ({pl.get('trackCount', 0)}首, ID: {pl.get('id')})")
                
                print("\n使用 play.py --id <歌单ID> --type playlist 播放")
            else:
                print("\n暂无歌单")
        else:
            print(f"获取失败: {result.get('message')}")
    except Exception as e:
        print(f"获取失败: {e}")


if __name__ == "__main__":
    get_my_playlists()
