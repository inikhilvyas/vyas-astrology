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
$token = [CredReader]::GetPassUtf8("GitHub - https://api.github.com/inikhilvyas")
if (-not $token) {
    Write-Error "Token not found"
    exit 1
}

$remoteUrl = "https://inikhilvyas:$token@github.com/inikhilvyas/vyas-astrology.git"
# Test with git ls-remote first
$out = git ls-remote $remoteUrl HEAD
if ($LASTEXITCODE -eq 0) {
    Write-Output "SUCCESS: Authenticated to inikhilvyas/vyas-astrology!"
} else {
    Write-Output "FAILED: Could not authenticate with token. Exit code $LASTEXITCODE"
}
