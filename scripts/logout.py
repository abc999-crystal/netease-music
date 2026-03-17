#!/usr/bin/env python3
"""网易云音乐退出登录"""
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
STORAGE_DIR = SCRIPT_DIR / "storage"
COOKIE_FILE = STORAGE_DIR / "cookies.json"

def logout():
    if COOKIE_FILE.exists():
        COOKIE_FILE.unlink()
        print("✅ 已退出登录")
    else:
        print("❌ 当前未登录")

def main():
    logout()

if __name__ == "__main__":
    main()
