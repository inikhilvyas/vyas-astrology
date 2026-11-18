import ctypes, ctypes.wintypes
import subprocess

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
        # remove null bytes
        clean_blob = blob.replace(b'\x00', b'')
        try:
            pwd = clean_blob.decode('utf-8')
        except:
            pwd = clean_blob.decode('latin-1')
        return username, pwd.strip()
    return None, None

u2, t2 = get_cred('git:https://github.com')
print(f"Token inikhilvyas clean: {bool(t2)}, length: {len(t2)}")

inikhil_url = f"https://{u2}:{t2}@github.com/inikhilvyas/vyas-astrology.git"
for branch in ['main', 'master']:
    print(f"Pushing to inikhil:{branch} ...")
    res = subprocess.run(['git', 'push', inikhil_url, f'main:{branch}'], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"SUCCESS pushing to inikhil:{branch}")
    else:
        print(f"FAIL pushing to inikhil:{branch}:\n{res.stderr}")

print("=== INIKHIL PUSH COMPLETED! ===")

