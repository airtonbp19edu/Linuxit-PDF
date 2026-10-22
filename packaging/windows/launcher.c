/* Linuxit PDF per-user launcher. No elevation, service or machine-wide PATH. */
#define UNICODE
#define _UNICODE
#include <windows.h>
#include <shellapi.h>
#include <wchar.h>
#include <stdlib.h>

int WINAPI wWinMain(HINSTANCE instance,HINSTANCE previous,PWSTR ignored,int show) {
    wchar_t root[32768],python[32768],bootstrap[32768];
    if(!GetModuleFileNameW(NULL,root,32768))return 2;
    wchar_t *end=wcsrchr(root,L'\\');if(!end)return 2;*end=0;
    _snwprintf(python,32768,L"%ls\\runtime\\bin\\pythonw.exe",root);
    _snwprintf(bootstrap,32768,L"%ls\\windows_bootstrap.py",root);
    int argc;wchar_t **argv=CommandLineToArgvW(GetCommandLineW(),&argc);if(!argv)return 2;
    size_t capacity=2*(wcslen(python)+wcslen(bootstrap)+32);
    for(int i=1;i<argc;i++)capacity+=2*wcslen(argv[i])+4;
    wchar_t *command=calloc(capacity,sizeof(wchar_t));if(!command){LocalFree(argv);return 2;}
    _snwprintf(command,capacity,L"\"%ls\" -B -I \"%ls\"",python,bootstrap);
    for(int i=1;i<argc;i++){
        wcscat(command,L" \"");wchar_t *out=command+wcslen(command);size_t slashes=0;
        for(const wchar_t *in=argv[i];;in++){
            if(*in==L'\\'){slashes++;continue;}
            if(*in==L'\"' || !*in){for(size_t n=0;n<slashes*2;n++)*out++=L'\\';}
            else{for(size_t n=0;n<slashes;n++)*out++=L'\\';}
            slashes=0;if(!*in)break;if(*in==L'\"')*out++=L'\\';*out++=*in;
        }
        *out++=L'\"';*out=0;
    }
    STARTUPINFOW startup={sizeof(startup)};PROCESS_INFORMATION process={0};
    BOOL ok=CreateProcessW(python,command,NULL,NULL,FALSE,0,NULL,root,&startup,&process);
    free(command);LocalFree(argv);
    if(!ok){MessageBoxW(NULL,L"Não foi possível iniciar o runtime do Linuxit PDF.",L"Linuxit PDF",MB_OK|MB_ICONERROR);return 3;}
    CloseHandle(process.hThread);CloseHandle(process.hProcess);return 0;
}
