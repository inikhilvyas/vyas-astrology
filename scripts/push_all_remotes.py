import ctypes, ctypes.wintypes
import subprocess
import sys

CRED_TYPE_GENERIC = 1
class CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ('Flags', ctypes.wintypes.DWORD),
        ('Type', ctypes.wintypes.DWORD),
        ('TargetName', ctypes.wintypes.LPWSTR),
        ('Comment', ctypes.wintypes.LPWSTR),
        ('LastWritten', ctypes.wintypes.FILETIME),
        ('CredentialBlobSize', ctypes.wintypes.DWORD),
        ('CredentialBlob', ctypes.c_void_p),
        ('Persist', ctypes.wintypes.DWORD),
        ('AttributeCount', ctypes.wintypes.DWORD),
        ('Attributes', ctypes.c_void_p),
        ('TargetAlias', ctypes.wintypes.LPWSTR),
        ('UserName', ctypes.wintypes.LPWSTR),
    ]

advapi32 = ctypes.windll.advapi32
CredRead = advapi32.CredReadW
CredRead.argtypes = [ctypes.wintypes.LPWSTR, ctypes.wintypes.DWORD, ctypes.wintypes.DWORD, ctypes.POINTER(ctypes.POINTER(CREDENTIAL))]
CredRead.restype = ctypes.wintypes.BOOL
CredFree = advapi32.CredFree
CredFree.argtypes = [ctypes.c_void_p]

def get_cred(target):
    pcred = ctypes.POINTER(CREDENTIAL)()
    if CredRead(target, CRED_TYPE_GENERIC, 0, ctypes.byref(pcred)):
        blob = ctypes.string_at(pcred.contents.CredentialBlob, pcred.contents.CredentialBlobSize)
        username = pcred.contents.UserName
        CredFree(pcred)
        try:
            pwd = blob.decode('utf-8')
        except:
            pwd = blob.decode('utf-16-le', errors='ignore')
        pwd = pwd.replace('\x00', '').strip()
        if username:
            username = username.replace('\x00', '').strip()
        return username, pwd
    return None, None

u1, t1 = get_cred('gh:github.com:vyasbilawas-ctrl')
u2, t2 = get_cred('git:https://github.com')

print(f"Token vyasbilawas-ctrl: {bool(t1)}, Token inikhilvyas: {bool(t2)}")

# 1. Push to origin (vyasbilawas-ctrl)
origin_url = f"https://{u1}:{t1}@github.com/vyasbilawas-ctrl/vyas-astrology.git"
for branch in ['main', 'master', 'fix-issues-20231025']:
    print(f"Pushing to origin:{branch} ...")
    res = subprocess.run(['git', 'push', origin_url, f'main:{branch}'], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"SUCCESS pushing to origin:{branch}")
    else:
        print(f"FAIL pushing to origin:{branch}:\n{res.stderr}")

# 2. Push to inikhil (inikhilvyas)
inikhil_url = f"https://{u2}:{t2}@github.com/inikhilvyas/vyas-astrology.git"
for branch in ['main', 'master']:
    print(f"Pushing to inikhil:{branch} ...")
    res = subprocess.run(['git', 'push', inikhil_url, f'main:{branch}'], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"SUCCESS pushing to inikhil:{branch}")
    else:
        print(f"FAIL pushing to inikhil:{branch}:\n{res.stderr}")

print("=== ALL PUSHES COMPLETED! ===")

