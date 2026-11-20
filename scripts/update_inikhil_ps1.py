with open('scripts/push_to_inikhil.ps1', 'r', encoding='utf-8') as f:
    c = f.read()

target = 'Write-Output "Pushing main to inikhil/main..."'
replacement = '''Write-Output "Pushing main to inikhil/fix-issues-20231025..."
$res0 = git push $remoteUrl main:fix-issues-20231025 2>&1
$res0 | ForEach-Object { $_ -replace $token, "[REDACTED]" }

Write-Output "Pushing main to inikhil/main..."'''

if target in c:
    c = c.replace(target, replacement)
    with open('scripts/push_to_inikhil.ps1', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated push_to_inikhil.ps1")

