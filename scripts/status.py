#!/usr/bin/env python3
"""
网易云音乐状态检查脚本
检查当前登录状态和用户信息
"""
import os
import sys
from pathlib import Path
from pyncm import GetCurrentSession, SetCurrentSession, LoadSessionFromString, apis

SCRIPT_DIR = Path(__file__).parent
SESSION_FILE = SCRIPT_DIR / ".session"


def check_status():
    """检查登录状态"""
    print("=" * 50)
    print("网易云音乐登录状态")
    print("=" * 50)
    
    if not SESSION_FILE.exists():
        print("\n未登录或登录状态已过期")
        print("请运行 login.py 进行扫码登录")
        return
    
    try:
        with open(SESSION_FILE, "r") as f:
            session_str = f.read()
        
        session = LoadSessionFromString(session_str)
        SetCurrentSession(session)
        
        try:
            user_info = apis.login.GetLoginStatus()
            
            if user_info.get('code', -1) == 200:
                profile = user_info.get('data', {}).get('profile', {})
                print(f"\n已登录")
                print(f"用户名: {profile.get('nickname', '未知')}")
                print(f"用户ID: {profile.get('userId', '未知')}")
                print(f"等级: {profile.get('level', '未知')}")
            else:
                print("\n登录状态已过期")
                print("请重新运行 login.py 扫码登录")
                
        except Exception as e:
            print(f"\n获取用户信息失败: {e}")
            print("可能需要重新登录")
            
    except Exception as e:
        print(f"\n加载登录状态失败: {e}")
        print("请运行 login.py 重新登录")


def main():
    check_status()


if __name__ == "__main__":
    main()
