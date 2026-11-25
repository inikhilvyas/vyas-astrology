import subprocess
import time
import win32gui
import win32con
import win32ui
import ctypes
from PIL import Image

class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_int),
        ("top", ctypes.c_int),
        ("right", ctypes.c_int),
        ("bottom", ctypes.c_int)
    ]

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

    num_tabs = win32gui.SendMessage(hwnd_tab, 0x1304, 0, 0) # TCM_GETITEMCOUNT = 0x1304
    print("Total tab count:", num_tabs)

    tab_names = [
        "tab0_shodashvarga.png",
        "tab1_planets_panchang.png",
        "tab2_ashtakavarga.png",
        "tab3_kp_jaimini.png",
        "tab4_dasha.png",
        "tab5_phal_kathan.png"
    ]

    for idx in range(num_tabs):
        r = RECT()
        res = ctypes.windll.user32.SendMessageW(hwnd_tab, 0x130A, idx, ctypes.byref(r)) # TCM_GETITEMRECT
        cx = (r.left + r.right) // 2
        cy = (r.top + r.bottom) // 2
        print(f"Tab {idx} exact rect: ({r.left}, {r.top}, {r.right}, {r.bottom}), clicking at ({cx}, {cy})...")

        lParam = (cy << 16) | (cx & 0xFFFF)
        win32gui.SendMessage(hwnd_tab, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        time.sleep(0.05)
        win32gui.SendMessage(hwnd_tab, win32con.WM_LBUTTONUP, 0, lParam)
        time.sleep(0.7)

        name = tab_names[idx] if idx < len(tab_names) else f"tab_{idx}.png"
        capture_window(hwnd, f"artifacts/{name}")

    proc.kill()
    print("All tabs exact verification complete.")

if __name__ == "__main__":
    main()

