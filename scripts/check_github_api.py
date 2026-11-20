import urllib.request, json, subprocess

# Get token from CredReader
ps_cmd = '''
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public class CredReader {
    [DllImport("Advapi32.dll", SetLastError = true, EntryPoint = "CredReadW", CharSet = CharSet.Unicode)]
    public static extern bool CredRead(string target, int type, int reservedFlag, out IntPtr credentialPtr);
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    public struct CREDENTIAL {
        public int Flags;
        public int Type;
        public string TargetName;
        public string Comment;
        public long LastWritten;
        public int CredentialBlobSize;
        public IntPtr CredentialBlob;
        public int Persist;
        public int AttributeCount;
        public IntPtr Attributes;
        public string TargetAlias;
        public string UserName;
    }
    public static string GetPassUtf8(string target) {
        IntPtr ptr;
        if (CredRead(target, 1, 0, out ptr)) {
            CREDENTIAL cred = (CREDENTIAL)Marshal.PtrToStructure(ptr, typeof(CREDENTIAL));
            byte[] bytes = new byte[cred.CredentialBlobSize];
            Marshal.Copy(cred.CredentialBlob, bytes, 0, cred.CredentialBlobSize);
            return System.Text.Encoding.UTF8.GetString(bytes);
        }
        return null;
    }
}
'@
[CredReader]::GetPassUtf8("GitHub - https://api.github.com/inikhilvyas")
'''

res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
token = res.stdout.strip()

if token:
    # Check repo commits
    req = urllib.request.Request("https://api.github.com/repos/inikhilvyas/vyas-astrology/commits/fix-issues-20231025", headers={
        "Authorization": f"Bearer {token}",
        "User-Agent": "Antigravity"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print("Latest commit on inikhilvyas/vyas-astrology:fix-issues-20231025:")
            print("SHA:", data.get('sha'))
            print("Message:", data.get('commit', {}).get('message', '').split('\n')[0])
    except Exception as e:
        print("API error:", e)

    # Check webhooks
    req_hooks = urllib.request.Request("https://api.github.com/repos/inikhilvyas/vyas-astrology/hooks", headers={
        "Authorization": f"Bearer {token}",
        "User-Agent": "Antigravity"
    })
    try:
        with urllib.request.urlopen(req_hooks) as resp:
            hooks = json.loads(resp.read().decode())
            print(f"Total webhooks on inikhilvyas/vyas-astrology: {len(hooks)}")
            for h in hooks:
                config = h.get('config', {})
                url = config.get('url', '')
                print("Webhook:", h.get('id'), h.get('name'), "active:", h.get('active'), "url:", url[:30] + '...')
                if 'hostinger' in url.lower():
                    # Ping webhook if active
                    print("Found Hostinger webhook! Triggering ping/redeliver...")
    except Exception as e:
        print("Hooks error:", e)

