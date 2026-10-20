param(
    [Parameter(Mandatory=$true)][string]$MarkdownPath,
    [Parameter(Mandatory=$true)][string]$HtmlPath
)
$ErrorActionPreference = 'Stop'
$reportSource = (Resolve-Path -LiteralPath $MarkdownPath).Path
$reportTarget = [System.IO.Path]::GetFullPath($HtmlPath)
$reportWorkspace = Split-Path -Parent $PSScriptRoot
if (-not $reportTarget.StartsWith($reportWorkspace + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'The HTML output must stay in the authorized repository.'
}
if (Test-Path -LiteralPath $reportTarget) { throw 'Preserve the earlier HTML; use a new output path.' }
$renderedReport = ConvertFrom-Markdown -LiteralPath $reportSource
$reportHead = @'
<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Linuxit PDF — relatório completo de trabalho e pendências — 19/10/2026</title>
<style>
:root{color-scheme:light;--ink:#20202a;--muted:#5d6170;--accent:#563b91;--line:#d7d9e0;--paper:#fff;--soft:#f5f5f8}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.65 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1180px;padding:32px 36px 100px;margin:auto}h1{font-size:2.15rem;line-height:1.2;letter-spacing:-.025em}h2{font-size:1.65rem;border-top:2px solid var(--line);padding-top:30px;margin-top:52px;scroll-margin-top:88px}h3{font-size:1.3rem;margin-top:32px}h4{font-size:1.1rem;margin-top:26px}h5{font-size:1rem;margin-top:24px}a{color:var(--accent);overflow-wrap:anywhere}p,li{overflow-wrap:anywhere}li{margin:5px 0}code{font-family:Consolas,monospace;font-size:.88em;background:var(--soft);padding:1px 4px;border-radius:3px;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:var(--soft);border:1px solid var(--line);padding:16px;border-radius:5px;font-size:12px;line-height:1.55}pre code{padding:0;background:none}table{border-collapse:collapse;table-layout:fixed;width:100%;font-size:13px;margin:20px 0 28px}td,th{border:1px solid var(--line);padding:9px;text-align:left;vertical-align:top;overflow-wrap:anywhere}th{background:#eeebf5;font-weight:650}tr:nth-child(even) td{background:#fafafd}details{border:1px solid var(--line);padding:12px 15px;border-radius:5px;margin:16px 0}summary{cursor:pointer;color:var(--accent);font-weight:600;overflow-wrap:anywhere}details[open]>summary{margin-bottom:12px}.toolbar{position:sticky;top:0;z-index:10;background:#f5f3fa;border-bottom:1px solid var(--line);padding:10px 24px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}.toolbar span{font-size:13px;color:var(--muted)}button{border:1px solid #bcb5cf;background:white;color:var(--accent);border-radius:5px;padding:8px 12px;cursor:pointer;font:600 13px system-ui}button:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid #aa8de0;outline-offset:3px}.reading-note{background:#f5f3fa;border-left:4px solid var(--accent);padding:15px 20px;color:var(--muted);font-size:14px}blockquote{border-left:3px solid var(--line);margin-left:0;padding-left:18px;color:var(--muted)}
@media(max-width:700px){main{padding:20px 16px 70px}h1{font-size:1.7rem}h2{font-size:1.35rem}table{font-size:11px}td,th{padding:5px}.toolbar{padding:8px 12px}}
@media print{.toolbar{display:none}main{max-width:none;padding:0}body{font-size:10pt}h2{break-before:page}h3,h4,h5,summary{break-after:avoid}pre{font-size:7pt}table{font-size:7pt}a{color:inherit}details{border:0;padding:0}th{background:#eee!important}}
</style></head><body>
<nav class="toolbar" aria-label="Controles de leitura"><button type="button" onclick="setAllDetails(true)">Expandir todos os anexos</button><button type="button" onclick="setAllDetails(false)">Recolher anexos</button><a href="#sec-1">Início</a><a href="#sec-13">Por que demora</a><a href="#sec-14">O que falta</a><span>Arquivo completo, sem bibliotecas ou recursos externos. Ctrl+F para buscar.</span></nav>
<main><p class="reading-note">Este arquivo contém o relatório integral e seus anexos. Os blocos extensos começam recolhidos para facilitar a navegação; o conteúdo está incorporado. Expanda os anexos para pesquisar todos os registros ou imprimir seu conteúdo. Os links do GitHub servem apenas para conferência.</p>
'@
$reportTail = @'
</main><script>function setAllDetails(open){document.querySelectorAll('details').forEach(function(item){item.open=open;});}</script></body></html>
'@
[System.IO.File]::WriteAllText($reportTarget, $reportHead + $renderedReport.Html + $reportTail, [System.Text.UTF8Encoding]::new($false))
Get-Item -LiteralPath $reportTarget | Select-Object FullName,Length
