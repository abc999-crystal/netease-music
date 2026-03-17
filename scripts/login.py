#!/usr/bin/env python3
"""网易云音乐扫码登录"""
import os
import sys
import time
import json
import subprocess
import warnings
warnings.filterwarnings('ignore', message='.*urllib3.*')

from pathlib import Path
from pyncm import apis, GetCurrentSession, DumpSessionAsString
import qrcode
from PIL import Image

SCRIPT_DIR = Path(__file__).parent
STORAGE_DIR = SCRIPT_DIR / "storage"
COOKIE_FILE = STORAGE_DIR / "cookies.json"
QRCODE_FILE = STORAGE_DIR / "login_qrcode.png"

STORAGE_DIR.mkdir(exist_ok=True)


def load_session():
    if COOKIE_FILE.exists():
        try:
            with open(COOKIE_FILE, 'r') as f:
                cookies = json.load(f)
                GetCurrentSession().cookies.update(cookies)
            
            user_info = apis.login.GetCurrentLoginStatus()
            
            if user_info['code'] == 200 and user_info['profile']:
                return True, user_info['profile']['nickname']
        except Exception:
            pass
    return False, None


def save_session():
    try:
        cookies = GetCurrentSession().cookies.get_dict()
        with open(COOKIE_FILE, 'w') as f:
            json.dump(cookies, f)
        return True
    except Exception:
        return False


def check_login_status():
    is_logged_in, nickname = load_session()
    return {"logged_in": is_logged_in, "nickname": nickname}


def login_via_qrcode():
    print("=" * 50)
    print("网易云音乐扫码登录")
    print("=" * 50)
    
    try:
        result = apis.login.LoginQrcodeUnikey(1)
        if result['code'] != 200:
            print("获取二维码失败")
            return
            
        uuid = result['unikey']
        
        qr_content = f"https://music.163.com/login?codekey={uuid}"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_content)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        img.save(str(QRCODE_FILE))
        print(f"二维码已保存到: {QRCODE_FILE}")
        
        if sys.platform == 'win32':
            os.startfile(QRCODE_FILE)
        else:
            subprocess.run(["open", str(QRCODE_FILE)])
        
        print("请使用网易云音乐 App 扫描二维码登录")
        print("等待扫码中... (按 Ctrl+C 取消)")
        
        max_retries = 60
        for i in range(max_retries):
            result = apis.login.LoginQrcodeCheck(uuid)
            code = result['code']
            
            if code == 800:
                print("二维码已过期，请重新运行登录")
                return
            elif code == 803:
                if 'cookie' in result:
                    apis.login.WriteLoginInfo(result['cookie'])
                
                save_session()
                
                try:
                    user_info = apis.login.GetCurrentLoginStatus()
                    nickname = user_info['profile']['nickname'] if user_info.get('profile') else "用户"
                    print(f"\n登录成功！欢迎回来，{nickname}")
                except Exception:
                    print("\n登录成功！")
                return
            
            time.sleep(2)
            
        print("登录超时，请重试")
        
    except Exception as e:
        print(f"登录失败: {e}")


def main():
    status = check_login_status()
    if status["logged_in"]:
        print(f"已登录，当前用户: {status['nickname']}")
    else:
        login_via_qrcode()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n登录已取消")
        sys.exit(0)
