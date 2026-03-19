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


def is_app_running(app_name):
    """检查应用是否在运行"""
    try:
        if sys.platform == "darwin":
            result = subprocess.run(["pgrep", "-f", app_name], capture_output=True)
            return result.returncode == 0
        elif sys.platform == "win32":
            result = subprocess.run(['tasklist'], capture_output=True, text=True)
            return app_name in result.stdout
    except Exception:
        return False
    return False


def ensure_app_running(app_name):
    """确保应用已启动"""
    if is_app_running(app_name):
        return True

    print(f"正在启动 {app_name}...")
    if sys.platform == "darwin":
        subprocess.run(["open", "-a", app_name])
    elif sys.platform == "win32":
        subprocess.run(["start", app_name], shell=True)

    import time
    for _ in range(10):
        time.sleep(1)
        if is_app_running(app_name):
            print("✅ 应用已启动")
            time.sleep(1)
            return True
    return False


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


def click_menu_item(menu_item_name):
    """点击菜单项"""
    if not ensure_app_running("NeteaseMusic"):
        print("❌ 无法启动网易云音乐")
        return False

    script = f'''
tell application "NeteaseMusic"
    activate
end tell
delay 0.3
tell application "System Events"
    tell process "NeteaseMusic"
        tell menu "控制" of menu bar item "控制" of menu bar 1
            click menu item "{menu_item_name}"
        end tell
    end tell
end tell
delay 0.3
tell application "System Events"
    keystroke "m" using command down
end tell
'''
    try:
        subprocess.run(["osascript", "-e", script], capture_output=True)
        return True
    except Exception as e:
        print(f"AppleScript 失败: {e}")
        return False


def click_submenu_item(menu_name, submenu_item_name):
    """点击子菜单项"""
    if not ensure_app_running("NeteaseMusic"):
        print("❌ 无法启动网易云音乐")
        return False

    script = f'''
tell application "NeteaseMusic"
    activate
end tell
delay 0.3
tell application "System Events"
    tell process "NeteaseMusic"
        tell menu "控制" of menu bar item "控制" of menu bar 1
            click menu item "{menu_name}"
        end tell
    end tell
end tell
delay 0.2
tell application "System Events"
    tell process "NeteaseMusic"
        tell menu "控制" of menu bar item "控制" of menu bar 1
            tell menu "{menu_name}" of menu item "{menu_name}"
                click menu item "{submenu_item_name}"
            end tell
        end tell
    end tell
end tell
delay 0.5
tell application "System Events"
    keystroke "m" using command down
end tell
'''
    try:
        subprocess.run(["osascript", "-e", script], capture_output=True)
        return True
    except Exception as e:
        print(f"AppleScript 失败: {e}")
        return False


def next_track():
    """下一首"""
    print("切换到下一首...")
    if sys.platform == "darwin":
        return click_menu_item("下一个")
    return _send_command("next")


def previous_track():
    """上一首"""
    print("切换到上一首...")
    if sys.platform == "darwin":
        return click_menu_item("上一个")
    return _send_command("previous")


def pause():
    """暂停播放"""
    print("暂停播放...")
    if sys.platform == "darwin":
        return click_menu_item("暂停")
    return _send_command("pause")


def resume():
    """继续播放"""
    print("继续播放...")
    if sys.platform == "darwin":
        return click_menu_item("播放")
    return _send_command("resume")


def volume_up(step=25):
    """增加音量"""
    print(f"增加音量 {step}%...")
    if sys.platform == "darwin":
        for i in range(step // 2):
            click_menu_item("升高音量")
        return True
    return _send_command("volumeup", step)


def volume_down(step=25):
    """降低音量"""
    print(f"降低音量 {step}%...")
    if sys.platform == "darwin":
        for i in range(step // 2):
            click_menu_item("降低音量")
        return True
    return _send_command("volumedown", step)


def loop_off():
    """关闭循环播放"""
    print("关闭循环播放...")
    if sys.platform == "darwin":
        return click_submenu_item("循环播放", "关")
    return False


def loop_one():
    """单曲循环"""
    print("开启单曲循环...")
    if sys.platform == "darwin":
        return click_submenu_item("循环播放", "单曲")
    return False


def loop_all():
    """全部循环"""
    print("开启全部循环...")
    if sys.platform == "darwin":
        return click_submenu_item("循环播放", "全部")
    return False


def shuffle():
    """随机播放"""
    print("切换随机播放...")
    if sys.platform == "darwin":
        return click_menu_item("随机播放")
    return False


def _send_command(cmd, value=None):
    """发送命令到网易云音乐客户端 (Windows 备用)"""
    if sys.platform != "win32":
        return False

    app_name = "cloudmusic"
    if not ensure_app_running(app_name):
        print(f"❌ 无法启动 {app_name}")
        return False

    try:
        command = {"cmd": cmd}
        if value is not None:
            command["value"] = value

        json_str = json.dumps(command, separators=(",", ":"))
        encoded = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
        app_url = f"orpheus://{encoded}"
        os.startfile(app_url)
        return True
    except Exception as e:
        print(f"❌ 发送命令失败: {e}")
        return False


def play(id, resource_type='song', minimize=True):
    """播放歌曲或歌单"""
    print("=" * 50)
    print(f"播放 {'歌曲' if resource_type == 'song' else '歌单'}")
    print("=" * 50)
    print(f"资源ID: {id}")

    app_name = "NeteaseMusic" if sys.platform == "darwin" else "cloudmusic"

    try:
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
    if len(sys.argv) < 2:
        print("用法: play.py <action> [options]")
        print("\n操作类型:")
        print("  play <id> [--type song|playlist]  播放歌曲或歌单")
        print("  next                            下一首")
        print("  previous                        上一首")
        print("  pause/resume                    暂停/继续播放")
        print("  volume-up/volume-down           音量调节")
        print("  loop-off/loop-one/loop-all      循环模式")
        print("  shuffle                         随机播放")
        sys.exit(1)

    action = sys.argv[1]

    if action == 'play':
        parser = argparse.ArgumentParser(description='播放歌曲或歌单')
        parser.add_argument('id', help='资源ID')
        parser.add_argument('--type', choices=['song', 'playlist'], default='song')
        parser.add_argument('--no-minimize', action='store_true')
        args = parser.parse_args(sys.argv[2:])
        play(args.id, args.type, not args.no_minimize)
    elif action == 'next':
        next_track()
    elif action == 'previous':
        previous_track()
    elif action == 'pause':
        pause()
    elif action == 'resume':
        resume()
    elif action == 'volume-up':
        volume_up()
    elif action == 'volume-down':
        volume_down()
    elif action == 'loop-off':
        loop_off()
    elif action == 'loop-one':
        loop_one()
    elif action == 'loop-all':
        loop_all()
    elif action in ('shuffle', 'shuffle-on', '随机播放'):
        shuffle()
    else:
        print(f"未知操作: {action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
