#!/usr/bin/env python3
"""搜索歌曲"""
import json
import argparse
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


def search(keyword, search_type=1):
    print(f"搜索: {keyword}")
    print("=" * 50)
    
    if not load_session():
        print("未登录，部分功能可能受限")
    
    try:
        session = GetCurrentSession()
        
        if search_type == 1:
            url = f'https://music.163.com/api/search/get?s={keyword}&type=1&limit=20'
            headers = {'Referer': 'https://music.163.com/'}
            result = session.get(url, headers=headers)
            data = result.json()
            
            if data.get('code') == 200:
                songs = data.get('result', {}).get('songs', [])
                if songs:
                    print(f"\n找到 {len(songs)} 首歌曲:\n")
                    for i, song in enumerate(songs, 1):
                        artists = song.get('artists', [])
                        artist_names = ", ".join([a.get('name', '') for a in artists]) if artists else '未知'
                        print(f"{i:2d}. {song.get('name')} - {artist_names} (ID: {song.get('id')})")
                    print("\n使用 play.py --id <歌曲ID> --type song 播放")
                else:
                    print("未找到")
            else:
                print(f"搜索失败: {data.get('message')}")
                
        elif search_type == 1000:
            url = f'https://music.163.com/api/search/get?s={keyword}&type=1000&limit=20'
            headers = {'Referer': 'https://music.163.com/'}
            result = session.get(url, headers=headers)
            data = result.json()
            
            if data.get('code') == 200:
                playlists = data.get('result', {}).get('playlists', [])
                if playlists:
                    print(f"\n找到 {len(playlists)} 个歌单:\n")
                    for i, pl in enumerate(playlists, 1):
                        print(f"{i:2d}. {pl.get('name')} (ID: {pl.get('id')})")
                    print("\n使用 play.py --id <歌单ID> --type playlist 播放")
                else:
                    print("未找到")
    except Exception as e:
        print(f"搜索失败: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('keyword', help='搜索关键词')
    parser.add_argument('--type', '-t', type=int, default=1, choices=[1, 1000])
    args = parser.parse_args()
    search(args.keyword, args.type)
