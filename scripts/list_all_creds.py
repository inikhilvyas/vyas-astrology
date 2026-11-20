import subprocess

ps_code = '''
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public class CredLister {
    [DllImport("Advapi32.dll", SetLastError = true, EntryPoint = "CredEnumerateW", CharSet = CharSet.Unicode)]
    public static extern bool CredEnumerate(string filter, int flag, out int count, out IntPtr pCredentials);
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
    public static void ListAll() {
        int count;
        IntPtr pCreds;
        if (CredEnumerate(null, 0, out count, out pCreds)) {
            for (int i = 0; i < count; i++) {
                IntPtr pCred = Marshal.ReadIntPtr(pCreds, i * IntPtr.Size);
                CREDENTIAL c = (CREDENTIAL)Marshal.PtrToStructure(pCred, typeof(CREDENTIAL));
                Console.WriteLine("Target: " + c.TargetName + " | User: " + c.UserName);
            }
        }
    }
}
'@
[CredLister]::ListAll()
'''

res = subprocess.run(["powershell", "-Command", ps_code], capture_output=True, text=True)
print(res.stdout)

