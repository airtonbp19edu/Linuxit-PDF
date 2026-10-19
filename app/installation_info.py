"""Local installation diagnostics and handoff to the platform package manager."""
import configparser,os,platform
from pathlib import Path
from version import VERSION

APP_ID='io.github.airtonbp19edu.LinuxitPDF'


def installation_info(flatpak_info=None):
    path=Path('/.flatpak-info') if flatpak_info is None else Path(flatpak_info)
    result=dict(version=VERSION,system=platform.system(),architecture=platform.machine(),
                installation='source_or_system_package',app_id=None,branch=None,
                update_command=None,remote_update_checked=False)
    try:
        if path.is_file() and path.stat().st_size<=65536:
            parser=configparser.ConfigParser(interpolation=None);parser.read(path,encoding='utf-8')
            if parser.get('Application','name',fallback='')==APP_ID:
                result.update(installation='flatpak',app_id=APP_ID,
                    branch=parser.get('Instance','branch',fallback='devel'),
                    update_command='flatpak update '+APP_ID)
    except (OSError,configparser.Error,UnicodeError):pass
    return result
