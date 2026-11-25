import subprocess
import time
import win32gui
import win32con
import win32ui
import ctypes
from PIL import Image

def capture_window(hwnd, out_path):
    rect = win32gui.GetWindowRect(hwnd)
    w = rect[2] - rect[0]
    h = rect[3] - rect[1]

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)

    result = ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)
    if not result:
        result = ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    img = Image.frombuffer('RGBA', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRA', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    img.save(out_path)
    print(f"Captured {out_path} ({w}x{h})")

def main():
    print("Launching artifacts/vyas_astra.exe...")
    proc = subprocess.Popen(["artifacts/vyas_astra.exe"])
    time.sleep(3)

    hwnd = win32gui.FindWindow("VYAS_ASTRA_DESKTOP_MAIN", None)
    if not hwnd:
        print("ERROR: Window not found!")
        proc.kill()
        return

    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    time.sleep(1)

    hwnd_tab = win32gui.FindWindowEx(hwnd, None, "SysTabControl32", None)
    print("Tab control hwnd:", hwnd_tab)

    tab_rect = win32gui.GetWindowRect(hwnd_tab)
    print("Tab rect:", tab_rect)

    tabs = [
        ("tab0_shodashvarga.png", 0, tab_rect[0] + 70, tab_rect[1] + 15),
        ("tab1_planets_panchang.png", 1, tab_rect[0] + 220, tab_rect[1] + 15),
        ("tab2_ashtakavarga.png", 2, tab_rect[0] + 400, tab_rect[1] + 15),
        ("tab3_kp_jaimini.png", 3, tab_rect[0] + 590, tab_rect[1] + 15),
        ("tab4_dasha.png", 4, tab_rect[0] + 760, tab_rect[1] + 15),
        ("tab5_phal_kathan.png", 5, tab_rect[0] + 930, tab_rect[1] + 15)
    ]

    for name, idx, screen_x, screen_y in tabs:
        print(f"Switching to tab {idx} at screen ({screen_x}, {screen_y})...")
        client_x = screen_x - tab_rect[0]
        client_y = screen_y - tab_rect[1]
        lParam = (client_y << 16) | (client_x & 0xFFFF)
        win32gui.SendMessage(hwnd_tab, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        time.sleep(0.05)
        win32gui.SendMessage(hwnd_tab, win32con.WM_LBUTTONUP, 0, lParam)
        time.sleep(0.6)

        capture_window(hwnd, f"artifacts/{name}")

    proc.kill()
    print("Verification complete.")

if __name__ == "__main__":
    main()
