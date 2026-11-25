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

class NMHDR(ctypes.Structure):
    _fields_ = [
        ("hwndFrom", ctypes.c_void_p),
        ("idFrom", ctypes.c_size_t),
        ("code", ctypes.c_uint)
    ]

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

    # TCM_SETCURSEL = 0x130C
    # Set to tab 5 (Phal Kathan)
    win32gui.SendMessage(hwnd_tab, 0x130C, 5, 0)

    # Send WM_NOTIFY with TCN_SELCHANGE (code = -551 = 0xFFFFFDD9)
    TCN_SELCHANGE = 0xFFFFFFFF - 551 + 1
    nmhdr = NMHDR()
    nmhdr.hwndFrom = hwnd_tab
    nmhdr.idFrom = 117 # ID_TAB_CONTROL
    nmhdr.code = TCN_SELCHANGE

    ctypes.windll.user32.SendMessageW(hwnd, win32con.WM_NOTIFY, 117, ctypes.byref(nmhdr))
    time.sleep(1)

    capture_window(hwnd, "artifacts/tab5_phal_kathan.png")

    proc.kill()
    print("Verification of Tab 5 complete.")

if __name__ == "__main__":
    main()

