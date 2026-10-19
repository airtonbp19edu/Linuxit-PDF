# Run as a limited interactive task in the prepared, disposable Windows guest.
# Guest properties carry diagnostics and a small fixed command set, never code.
[CmdletBinding()]
param([Parameter(Mandatory=$true)][ValidatePattern('^[A-Za-z0-9-]+$')][string]$RunId)
$ErrorActionPreference='Stop'
$ProgressPreference='SilentlyContinue'
$vbox=Join-Path $env:SystemRoot 'System32\VBoxControl.exe'
$prefix='/Linuxit/Probe/'+$RunId
$root=Join-Path 'C:\Linuxit\Results' $RunId
New-Item -ItemType Directory -Path $root -Force | Out-Null
$expected='90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6'
function Read-Property([string]$Name){
    $raw=@(& $vbox guestproperty get $Name 2>$null) -join "`n"
    if($LASTEXITCODE -eq 0 -and $raw -match '(?m)^Value: (.+)$'){return $Matches[1].Trim()}
    return $null
}
function Publish([string]$Id,$Value){
    $json=$Value | ConvertTo-Json -Depth 12
    [IO.File]::WriteAllText((Join-Path $root ($Id+'.json')),$json,[Text.UTF8Encoding]::new($false))
    $encoded=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($json))
    $parts=[int][Math]::Ceiling($encoded.Length/800.0)
    if([Text.Encoding]::UTF8.GetByteCount($prefix+'/Result/'+$Id+'/Count') -ge 64){throw 'Diagnostic receipt property exceeds 63 bytes'}
    if($parts+1 -gt 64){throw 'Diagnostic response exceeds the reserved 64 property slots; full report preserved on disk'}
    for($i=0;$i -lt $parts;$i++){
        $chunk=$encoded.Substring($i*800,[Math]::Min(800,$encoded.Length-$i*800))
        & $vbox guestproperty set ($prefix+'/Result/'+$Id+'/'+$i) $chunk | Out-Null
        if($LASTEXITCODE -ne 0){throw 'Diagnostic property transport failed'}
    }
    & $vbox guestproperty set ($prefix+'/Result/'+$Id+'/Count') ([string]$parts) | Out-Null
    if($LASTEXITCODE -ne 0){throw 'Diagnostic receipt transport failed; full report preserved on disk'}
}
function Check-Offline {
    $hostValue=Read-Property ($prefix+'/Host')
    if(-not $hostValue){throw 'No current host containment record'}
    $hostRecord=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($hostValue)) | ConvertFrom-Json
    if($hostRecord.run_id -ne $RunId -or -not $hostRecord.verified_offline){throw 'Host containment not approved for this run'}
    if(([DateTimeOffset]::Now-[DateTimeOffset]::Parse($hostRecord.created_at)).TotalHours -gt 2){throw 'Stale containment record'}
    $adapters=@(Get-NetAdapter | Select-Object Name,Status)
    if(@($adapters | Where-Object Status -eq 'Up').Count){throw 'Guest network adapter is connected'}
    $mappings=@(Get-SmbMapping -ErrorAction SilentlyContinue)
    if($mappings.Count){throw 'Guest has SMB mappings'}
    return @{host=$hostRecord;adapters=$adapters;smb_mappings=$mappings}
}
$identity=[Security.Principal.WindowsIdentity]::GetCurrent()
$principal=[Security.Principal.WindowsPrincipal]::new($identity)
$elevated=$principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
$session=(Get-Process -Id $PID).SessionId
if($elevated -or $session -eq 0){Publish 'startup' @{status='failed';error='Limited interactive token required';elevated=$elevated;session=$session};exit 1}
Publish 'startup' @{status='ready';user=$identity.Name;elevated=$elevated;session=$session;created_at=(Get-Date).ToString('o')}
$seen=@{}
$deadline=[DateTime]::UtcNow.AddHours(2)
while([DateTime]::UtcNow -lt $deadline){
    $request=Read-Property ($prefix+'/Command')
    if($request -and $request -match '^([A-Za-z0-9-]+):(preflight|launch|collect|stop)$'){
        $id=$Matches[1];$action=$Matches[2]
        if(-not $seen.ContainsKey($id)){
            $seen[$id]=$true
            $report=[ordered]@{schema='linuxit-guest-probe-v1';run_id=$RunId;id=$id;action=$action;created_at=(Get-Date).ToString('o');status='running';elevated=$elevated;session=$session}
            try {
                if([Text.Encoding]::UTF8.GetByteCount($prefix+'/Result/'+$id+'/Count') -ge 64){throw 'Diagnostic receipt property exceeds 63 bytes; guest action refused'}
                $report.containment=Check-Offline
                $hash=(Get-FileHash 'C:\Linuxit\Reference\FoxitPDFReader.exe' -Algorithm SHA256).Hash.ToLowerInvariant()
                $report.reference_sha256=$hash
                if($hash -ne $expected){throw 'Reference identity mismatch'}
                if($action -eq 'preflight'){
                    $denied=@{}
                    foreach($name in @('Reference','Input','Protocol')){
                        $probe=Join-Path ('C:\Linuxit\'+$name) ('.linuxit-write-probe-'+$RunId)
                        try {[IO.File]::WriteAllText($probe,'permission probe');$denied[$name]=$false;Remove-Item -LiteralPath $probe -Force}
                        catch [UnauthorizedAccessException] {$denied[$name]=$true}
                    }
                    $report.write_denied=$denied
                    if(-not $denied.Reference -or -not $denied.Input -or -not $denied.Protocol){throw 'Input directories are writable'}
                    $report.inputs=@(Get-ChildItem 'C:\Linuxit\Input' -File | ForEach-Object {@{name=$_.Name;bytes=$_.Length;sha256=(Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}})
                    $marker=[IO.File]::ReadAllText('C:\Linuxit\Input\controle.txt')
                    if(-not $marker.Contains('LINUXIT_RUNTIME_PROBE')){throw 'Control marker mismatch'}
                    $control=Start-Process -FilePath "$env:SystemRoot\System32\notepad.exe" -ArgumentList 'C:\Linuxit\Input\controle.txt' -PassThru
                    $report.control_pid=$control.Id
                    $report.visual_control_observed=$false
                }
                if($action -eq 'launch'){
                    if((Read-Property ($prefix+'/VisualControl')) -ne 'observed'){throw 'Visual runtime control has not been acknowledged'}
                    if(Get-Process FoxitPDFReader -ErrorAction SilentlyContinue){throw 'Reference is already running'}
                    $process=Start-Process -FilePath 'C:\Linuxit\Reference\FoxitPDFReader.exe' -WorkingDirectory 'C:\Linuxit\Reference' -PassThru
                    $report.launched_pid=$process.Id
                    $report.functional_success=$null
                }
                if($action -eq 'collect'){
                    $report.processes=@(Get-Process FoxitPDFReader,FoxitPDFReaderUpdateService,notepad -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,SessionId,Responding,MainWindowTitle)
                    $report.printers=@(Get-Printer -ErrorAction SilentlyContinue | Select-Object Name,Type,PortName,DriverName)
                    $report.outputs=@(Get-ChildItem 'C:\Linuxit\Results' -File -Recurse | Where-Object {$_.FullName -notlike ($root+'\*')} | ForEach-Object {@{path=$_.FullName;bytes=$_.Length;sha256=(Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}})
                }
                $report.status='completed'
            } catch {$report.status='failed';$report.error=$_.Exception.Message}
            $report.finished_at=(Get-Date).ToString('o')
            Publish $id $report
            if($action -eq 'stop'){break}
        }
    }
    Start-Sleep -Seconds 2
}
