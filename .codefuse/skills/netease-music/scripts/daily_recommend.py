#!/usr/bin/env python3
"""每日推荐"""
import json
import subprocess
import sys
import warnings
warnings.filterwarnings('ignore', message='.*urllib3.*')

from pathlib import Path
from pyncm import GetCurrentSession

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


def get_daily_recommend():
    print("=" * 50)
    print("今日推荐歌曲")
    print("=" * 50)
    
    if not load_session():
        if not auto_login():
            print("\n登录失败，无法获取每日推荐")
            return
    
    try:
        session = GetCurrentSession()
        url = 'https://music.163.com/api/v1/discovery/recommend/songs?total=true&offset=0&limit=20'
        headers = {'Referer': 'https://music.163.com/'}
        
        result = session.get(url, headers=headers)
        data = result.json()
        
        if data.get('code') == 200:
            songs = data.get('recommend', [])
            if songs:
                print(f"\n🎵 今日推荐 ({len(songs)}首):\n")
                for i, song in enumerate(songs[:10], 1):
                    artists = song.get('artists', [])
                    artist_names = ", ".join([a.get('name', '') for a in artists]) if artists else '未知'
                    print(f"{i:2d}. {song.get('name')} - {artist_names} (ID: {song.get('id')})")
                print("\n使用 play.py --id <歌曲ID> --type song 播放")
            else:
                print("\n暂无推荐")
        else:
            print(f"获取失败: {data.get('message')}")
    except Exception as e:
        print(f"获取失败: {e}")


if __name__ == "__main__":
    get_daily_recommend()
