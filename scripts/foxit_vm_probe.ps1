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
$prefix='/Linuxit/Probe/'+$RunId
# VirtualBox includes the terminating NUL in its 64-byte property-name limit.
# Check the receipt too: a short numeric chunk can fit while /Count cannot.
$receiptName=$prefix+'/Result/'+$Id+'/Count'
if($Action -notin @('capture','ack-control') -and [Text.Encoding]::UTF8.GetByteCount($receiptName) -ge 64){
    throw 'Diagnostic receipt property exceeds 63 bytes; use a shorter RunId/Id. No guest action issued.'
}
if([Text.Encoding]::UTF8.GetByteCount($prefix+'/VisualControl') -ge 64){throw 'Diagnostic RunId is too long'}
$folder=Join-Path $OutputRoot $RunId
New-Item -ItemType Directory -Path $folder -Force | Out-Null
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
    param([switch]$ReserveDiagnosticSlots)
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
    if($ReserveDiagnosticSlots){
        $properties=@(Invoke-VBox -Arguments @('guestproperty','enumerate',$VMName))
        $propertyCount=@($properties | Where-Object {$_ -match '^/[^=]+\s+='}).Count
        if($propertyCount -lt 1){throw 'Cannot verify diagnostic property capacity; no guest action issued'}
        # 64 slots for one bounded response, plus Host and Command if new.
        $capacity=[ordered]@{created_at=(Get-Date).ToString('o');property_count=$propertyCount;maximum_properties=256;response_slots_reserved=64;host_command_slots_reserved=2}
        $capacity | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $folder ($Id+'-transport.json')) -Encoding UTF8
        if($propertyCount+66 -gt 256){throw 'Insufficient diagnostic property capacity; archive verified results of stopped collectors before retrying. No guest action issued.'}
    }
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
    Check-Host -ReserveDiagnosticSlots
    Invoke-VBox -Arguments @('guestproperty','set',$VMName,($prefix+'/Command'),($Id+':'+$Action),'--flags','RDONLYGUEST') | Out-Null
    Write-Output ('Issued '+$Id+':'+$Action+'; read separately after completion.')
}
