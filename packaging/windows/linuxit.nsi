Unicode true
!include "MUI2.nsh"
!ifndef VERSION
!error "VERSION is required"
!endif
!ifndef PAYLOAD
!error "PAYLOAD is required"
!endif
!ifndef OUTPUT
!error "OUTPUT is required"
!endif
Name "Linuxit PDF ${VERSION} de desenvolvimento"
OutFile "${OUTPUT}"
InstallDir "$LOCALAPPDATA\Programs\Linuxit PDF\${VERSION}"
RequestExecutionLevel user
SetCompressor /SOLID lzma
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "${PAYLOAD}\LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "PortugueseBR"
Section "Linuxit PDF"
  SetShellVarContext current
  IfFileExists "$INSTDIR\*.*" 0 fresh_install
    IfSilent refuse_existing
    MessageBox MB_ICONSTOP "Escolha uma pasta nova e vazia. Instalações e arquivos existentes são preservados."
  refuse_existing:
    Abort
  fresh_install:
  SetOutPath "$INSTDIR"
  File /r "${PAYLOAD}\*"
  WriteUninstaller "$INSTDIR\uninstall.exe"
  CreateShortcut "$SMPROGRAMS\Linuxit PDF ${VERSION}.lnk" "$INSTDIR\LinuxitPDF.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\LinuxitPDF-${VERSION}" "DisplayName" "Linuxit PDF ${VERSION} de desenvolvimento"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\LinuxitPDF-${VERSION}" "DisplayVersion" "${VERSION}"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\LinuxitPDF-${VERSION}" "UninstallString" '$\"$INSTDIR\uninstall.exe$\"'
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\LinuxitPDF-${VERSION}" "InstallLocation" "$INSTDIR"
  WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\LinuxitPDF-${VERSION}" "NoModify" 1
  WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\LinuxitPDF-${VERSION}" "NoRepair" 1
SectionEnd
Section "Uninstall"
  SetShellVarContext current
  IfFileExists "$INSTDIR\windows-manifest.json" manifest_present
    IfSilent refuse_uninstall
    MessageBox MB_ICONSTOP "O manifesto desta instalação não foi encontrado. Nenhum arquivo foi removido."
  refuse_uninstall:
    Abort
  manifest_present:
  !include "${DELETE_INCLUDE}"
  Delete "$INSTDIR\uninstall.exe"
  RMDir "$INSTDIR"
  Delete "$SMPROGRAMS\Linuxit PDF ${VERSION}.lnk"
  ; ASCII junction created by windows_bootstrap.py for non-ASCII folders.
  ; RMDir on a junction removes only the link, never the target's files.
  ReadRegStr $0 HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\LinuxitPDF-${VERSION}" "AsciiAlias"
  StrCmp $0 "" alias_done
    RMDir "$0"
  alias_done:
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\LinuxitPDF-${VERSION}"
SectionEnd
