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

$token = [CredReader]::GetPassUtf8("gh:github.com:vyasbilawas-ctrl")
if (-not $token) {
    $token = [CredReader]::GetPassUtf8("git:https://github.com")
}

if (-not $token) {
    Write-Error "Token for vyasbilawas-ctrl not found"
    exit 1
}

Write-Output "Found token for vyasbilawas-ctrl, proceeding to push..."
$tokenEncoded = [System.Uri]::EscapeDataString($token)
$remoteUrl = "https://vyasbilawas-ctrl:$tokenEncoded@github.com/vyasbilawas-ctrl/vyas-astrology.git"

Write-Output "Pushing main to origin/main..."
$res1 = git push $remoteUrl main:main 2>&1
$res1 | ForEach-Object { $_ -replace $token, "[REDACTED]" }

Write-Output "Pushing main to origin/master..."
$res2 = git push $remoteUrl main:master 2>&1
$res2 | ForEach-Object { $_ -replace $token, "[REDACTED]" }

Write-Output "FINISHED PUSH TO ORIGIN MAIN AND MASTER!"
