import subprocess
import time
import os
import ctypes
from ctypes import wintypes
import win32gui
import win32ui
import win32con
from PIL import Image

class NMHDR(ctypes.Structure):
    _fields_ = [
        ("hwndFrom", wintypes.HWND),
        ("idFrom", wintypes.UINT),
        ("code", wintypes.INT),
    ]

def capture_window_to_file(hwnd, filename):
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top
    if w <= 0 or h <= 0:
        return

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)

    result = ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)
    if not result:
        ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1
    )

    im.save(filename)
    print(f"Captured: {filename} ({w}x{h})")

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

def run():
    exe_path = os.path.abspath("artifacts/vyas_astra.exe")
    proc = subprocess.Popen([exe_path])
    time.sleep(2.0)

    hwnd = win32gui.FindWindow("VYAS_ASTRA_DESKTOP_MAIN", None)
    if not hwnd:
        print("Window not found!")
        proc.kill()
        return

    capture_window_to_file(hwnd, "artifacts/desktop_tab0_charts.png")

    TCM_SETCURSEL = 0x130C
    WM_NOTIFY = 0x004E
    TCN_SELCHANGE = -551

    tab_hwnd = win32gui.FindWindowEx(hwnd, None, "SysTabControl32", None)
    if tab_hwnd:
        tab_id = win32gui.GetDlgCtrlID(tab_hwnd)
        # Tab 1: Planets
        win32gui.SendMessage(tab_hwnd, TCM_SETCURSEL, 1, 0)
        hdr = NMHDR(tab_hwnd, tab_id, TCN_SELCHANGE)
        win32gui.SendMessage(hwnd, WM_NOTIFY, tab_id, ctypes.addressof(hdr))
        time.sleep(0.5)
        capture_window_to_file(hwnd, "artifacts/desktop_tab1_planets.png")

        # Tab 2: Dasha
        win32gui.SendMessage(tab_hwnd, TCM_SETCURSEL, 2, 0)
        hdr = NMHDR(tab_hwnd, tab_id, TCN_SELCHANGE)
        win32gui.SendMessage(hwnd, WM_NOTIFY, tab_id, ctypes.addressof(hdr))
        time.sleep(0.5)
        capture_window_to_file(hwnd, "artifacts/desktop_tab2_dasha.png")

        # Tab 3: Verdict
        win32gui.SendMessage(tab_hwnd, TCM_SETCURSEL, 3, 0)
        hdr = NMHDR(tab_hwnd, tab_id, TCN_SELCHANGE)
        win32gui.SendMessage(hwnd, WM_NOTIFY, tab_id, ctypes.addressof(hdr))
        time.sleep(0.5)
        capture_window_to_file(hwnd, "artifacts/desktop_tab3_verdict.png")

    # Test MAXIMIZE
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    time.sleep(1.0)
    if tab_hwnd:
        win32gui.SendMessage(tab_hwnd, TCM_SETCURSEL, 0, 0)
        hdr = NMHDR(tab_hwnd, tab_id, TCN_SELCHANGE)
        win32gui.SendMessage(hwnd, WM_NOTIFY, tab_id, ctypes.addressof(hdr))
        time.sleep(0.5)
    capture_window_to_file(hwnd, "artifacts/desktop_maximized_charts.png")

    proc.kill()
    print("All captures completed successfully!")

if __name__ == '__main__':
    run()
