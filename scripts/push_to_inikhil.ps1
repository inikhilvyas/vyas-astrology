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

Write-Output "Pushing main to inikhil/master..."
$res1 = git push $remoteUrl main:master 2>&1
$res1 | ForEach-Object { $_ -replace $token, "[REDACTED]" }

Write-Output "Pushing main to inikhil/fix-issues-20231025..."
$res0 = git push $remoteUrl main:fix-issues-20231025 2>&1
$res0 | ForEach-Object { $_ -replace $token, "[REDACTED]" }

Write-Output "Pushing main to inikhil/main..."
$res2 = git push $remoteUrl main:main 2>&1
$res2 | ForEach-Object { $_ -replace $token, "[REDACTED]" }

$originUrl = "https://inikhilvyas:$token@github.com/vyasbilawas-ctrl/vyas-astrology.git"
Write-Output "Pushing main to origin/main..."
$res3 = git push $originUrl main:main 2>&1
$res3 | ForEach-Object { $_ -replace $token, "[REDACTED]" }

Write-Output "Pushing main to origin/master..."
$res4 = git push $originUrl main:master 2>&1
$res4 | ForEach-Object { $_ -replace $token, "[REDACTED]" }

Write-Output "FINISHED PUSH TO BOTH INIKHIL AND ORIGIN!"
