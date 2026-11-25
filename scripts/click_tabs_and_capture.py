import subprocess
import time
import os
import ctypes
import win32gui
import win32ui
from PIL import Image

def capture_window_to_file(hwnd, filename):
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)

    ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    im.save(filename)
    print(f"Captured: {filename}")

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

def click_at(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.1)
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.3)

def run():
    exe_path = os.path.abspath("artifacts/vyas_astra.exe")
    proc = subprocess.Popen([exe_path])
    time.sleep(2.0)

    hwnd = win32gui.FindWindow("VYAS_ASTRA_DESKTOP_MAIN", None)
    if not hwnd:
        print("Window not found")
        proc.kill()
        return

    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    print(f"Window Rect: ({left}, {top}, {right}, {bot})")

    # Click Tab 2 (Dasha): approx left + 650, top + 72
    click_at(left + 650, top + 72)
    capture_window_to_file(hwnd, "artifacts/desktop_tab2_dasha_verified.png")

    # Click Tab 3 (Verdict): approx left + 830, top + 72
    click_at(left + 830, top + 72)
    capture_window_to_file(hwnd, "artifacts/desktop_tab3_verdict_verified.png")

    # Click Tab 1 (Planets): approx left + 470, top + 72
    click_at(left + 470, top + 72)
    capture_window_to_file(hwnd, "artifacts/desktop_tab1_planets_verified.png")

    proc.kill()
    print("Verification complete!")

if __name__ == '__main__':
    run()

