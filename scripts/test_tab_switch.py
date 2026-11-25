import subprocess
import time
import os
import win32gui
import win32ui
import win32con
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

    win32gui.SendMessage(hwnd, win32con.WM_PRINT, saveDC.GetSafeHdc(),
                         win32con.PRF_CHILDREN | win32con.PRF_CLIENT | win32con.PRF_OWNED)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    im.save(filename)
    print(f"Captured: {filename}")

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

def test_clicks():
    exe_path = os.path.abspath("artifacts/vyas_astra.exe")
    proc = subprocess.Popen([exe_path])
    time.sleep(2.0)

    hwnd = win32gui.FindWindow("VYAS_ASTRA_DESKTOP_MAIN", None)
    tab_hwnd = win32gui.FindWindowEx(hwnd, None, "SysTabControl32", None)

    # Click Tab 1: Planets (approx x=220 inside tab)
    lparam = (15 << 16) | 220
    win32gui.SendMessage(tab_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
    win32gui.SendMessage(tab_hwnd, win32con.WM_LBUTTONUP, 0, lparam)
    time.sleep(0.5)
    capture_window_to_file(hwnd, "artifacts/desktop_tab1_planets_real.png")

    # Click Tab 2: Dasha (approx x=420 inside tab)
    lparam = (15 << 16) | 420
    win32gui.SendMessage(tab_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
    win32gui.SendMessage(tab_hwnd, win32con.WM_LBUTTONUP, 0, lparam)
    time.sleep(0.5)
    capture_window_to_file(hwnd, "artifacts/desktop_tab2_dasha_real.png")

    # Click Tab 3: Verdict (approx x=620 inside tab)
    lparam = (15 << 16) | 620
    win32gui.SendMessage(tab_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
    win32gui.SendMessage(tab_hwnd, win32con.WM_LBUTTONUP, 0, lparam)
    time.sleep(0.5)
    capture_window_to_file(hwnd, "artifacts/desktop_tab3_verdict_real.png")

    proc.kill()
    print("Done tab click test!")

if __name__ == '__main__':
    test_clicks()

