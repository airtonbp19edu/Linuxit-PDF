# Host-side diagnostics. This script never connects a VM network or adds shares.
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[A-Za-z0-9-]+$')][string]$RunId,
    [Parameter(Mandatory=$true)][ValidateSet('preflight','launch','collect','stop','read','capture','ack-control')][string]$Action,
    [ValidatePattern('^[A-Za-z0-9-]+$')][string]$Id='preflight',
    [string]$VMName='Windows 10',
    [string]$VBox='C:\Program Files\Oracle\VirtualBox\VBoxManage.exe',
    [string]$OutputRoot=(Join-Path $PSScriptRoot '..\analysis-local')
)
$ErrorActionPreference='Stop'
$folder=Join-Path $OutputRoot $RunId
New-Item -ItemType Directory -Path $folder -Force | Out-Null
$prefix='/Linuxit/Probe/'+$RunId
function Invoke-VBox([string[]]$Arguments){
    $result=@(& $VBox @Arguments 2>&1 | ForEach-Object {$_.ToString()})
    if($LASTEXITCODE -ne 0){throw ($result -join "`n")}
    return $result
}
function Read-Property([string]$Name){
    $raw=@(Invoke-VBox -Arguments @('guestproperty','get',$VMName,$Name)) -join "`n"
    if($raw -match '(?m)^Value: (.+)$'){return $Matches[1].Trim()}
    return $null
}
function Check-Host {
    $raw=@(Invoke-VBox -Arguments @('showvminfo',$VMName,'--machinereadable'))
    $raw | Set-Content -LiteralPath (Join-Path $folder ($Id+'-host.txt')) -Encoding UTF8
    $values=@{}
    foreach($line in $raw){if($line -match '^([^=]+)=(.*)$'){$values[$Matches[1]]=$Matches[2].Trim('"')}}
    $shares=@($values.Keys | Where-Object {$_ -match '^SharedFolderName'})
    $connected=@(1..8 | Where-Object {$values['nic'+$_] -and $values['nic'+$_] -ne 'none' -and $values['cableconnected'+$_] -ne 'off'})
    $api=New-Object -ComObject VirtualBox.VirtualBox
    $session=New-Object -ComObject VirtualBox.Session
    $locked=$false
    try {$api.FindMachine($VMName).LockMachine($session,1);$locked=$true;$usb=@($session.Console.USBDevices).Count}
    finally {if($locked){$session.UnlockMachine()}}
    $verified=$values.VMState -eq 'running' -and $connected.Count -eq 0 -and $shares.Count -eq 0 -and $usb -eq 0 -and $values.clipboard -eq 'disabled' -and $values.draganddrop -eq 'disabled' -and $values.vrde -eq 'off' -and $values.audio_in -eq 'off' -and $values.audio_out -eq 'off'
    $record=[ordered]@{schema='linuxit-host-containment-v1';run_id=$RunId;created_at=(Get-Date).ToString('o');verified_offline=$verified;connected_adapters=$connected.Count;shared_folders=$shares.Count;captured_usb_devices=$usb;clipboard=$values.clipboard;draganddrop=$values.draganddrop;vrde=$values.vrde;audio_in=$values.audio_in;audio_out=$values.audio_out}
    $json=$record | ConvertTo-Json
    $json | Set-Content -LiteralPath (Join-Path $folder ($Id+'-host.json')) -Encoding UTF8
    if(-not $verified){throw 'Host containment failed; no guest action issued'}
    $encoded=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($json))
    Invoke-VBox -Arguments @('guestproperty','set',$VMName,($prefix+'/Host'),$encoded,'--flags','RDONLYGUEST') | Out-Null
}
if($Action -eq 'read'){
    $count=Read-Property ($prefix+'/Result/'+$Id+'/Count')
    if(-not $count -or [int]$count -lt 1 -or [int]$count -gt 1000){throw 'Guest report is not ready'}
    $encoded=''
    for($i=0;$i -lt [int]$count;$i++){$chunk=Read-Property ($prefix+'/Result/'+$Id+'/'+$i);if(-not $chunk){throw 'Missing report chunk'};$encoded+=$chunk}
    $json=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($encoded))
    $parsed=$json | ConvertFrom-Json
    [IO.File]::WriteAllText((Join-Path $folder ($Id+'-guest.json')),$json,[Text.UTF8Encoding]::new($false))
    $json
} elseif($Action -eq 'capture'){
    Invoke-VBox -Arguments @('controlvm',$VMName,'screenshotpng',(Join-Path ([IO.Path]::GetFullPath($folder)) ($Id+'.png'))) | Out-Null
    Get-FileHash -LiteralPath (Join-Path $folder ($Id+'.png')) -Algorithm SHA256 | Select-Object Hash,Path
} elseif($Action -eq 'ack-control'){
    Check-Host
    Invoke-VBox -Arguments @('guestproperty','set',$VMName,($prefix+'/VisualControl'),'observed','--flags','RDONLYGUEST') | Out-Null
} else {
    Check-Host
    Invoke-VBox -Arguments @('guestproperty','set',$VMName,($prefix+'/Command'),($Id+':'+$Action),'--flags','RDONLYGUEST') | Out-Null
    Write-Output ('Issued '+$Id+':'+$Action+'; read separately after completion.')
}
