import subprocess
import ctypes
from ctypes import wintypes

class CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ('Flags', wintypes.DWORD),
        ('Type', wintypes.DWORD),
        ('TargetName', wintypes.LPWSTR),
        ('Comment', wintypes.LPWSTR),
        ('LastWritten', wintypes.FILETIME),
        ('CredentialBlobSize', wintypes.DWORD),
        ('CredentialBlob', ctypes.POINTER(ctypes.c_byte)),
        ('Persist', wintypes.DWORD),
        ('AttributeCount', wintypes.DWORD),
        ('Attributes', ctypes.c_void_p),
        ('TargetAlias', wintypes.LPWSTR),
        ('UserName', wintypes.LPWSTR)
    ]

Advapi32 = ctypes.windll.Advapi32
CredReadW = Advapi32.CredReadW
CredReadW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(ctypes.POINTER(CREDENTIAL))]
CredReadW.restype = wintypes.BOOL

def get_cred(target):
    pCred = ctypes.POINTER(CREDENTIAL)()
    if CredReadW(target, 1, 0, ctypes.byref(pCred)):
        cred = pCred.contents
        b = ctypes.string_at(cred.CredentialBlob, cred.CredentialBlobSize)
        return b.decode('utf-8', errors='ignore')
    return None

tok_ctrl = get_cred('gh:github.com:vyasbilawas-ctrl')
tok_inikhil = get_cred('git:https://github.com')

print("vyasbilawas-ctrl token:", bool(tok_ctrl))
print("inikhil token:", bool(tok_inikhil))

# Check refs on vyasbilawas-ctrl
url_ctrl = f"https://vyasbilawas-ctrl:{tok_ctrl}@github.com/vyasbilawas-ctrl/vyas-astrology.git"
out_ctrl = subprocess.check_output(f'git ls-remote "{url_ctrl}"', shell=True).decode()
print("=== vyasbilawas-ctrl refs ===")
print(out_ctrl)

# Check refs on inikhil
url_inikhil = f"https://inikhilvyas:{tok_inikhil}@github.com/inikhilvyas/vyas-astrology.git"
out_inikhil = subprocess.check_output(f'git ls-remote "{url_inikhil}"', shell=True).decode()
print("=== inikhilvyas refs ===")
print(out_inikhil)

