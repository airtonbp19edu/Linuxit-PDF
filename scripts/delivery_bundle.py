"""Resolve an own published bundle, locally or in a hash-verified release cache."""
import hashlib,json,os,re,tempfile,urllib.request
from pathlib import Path


def digest(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def resolve_bundle(root,manifest,download=False):
    root=Path(root);artifact=manifest['artifact'];version=manifest['version']
    expected=f'LinuxitPDF-{version}-x86_64.flatpak'
    if not re.fullmatch(r'\d+\.\d+\.\d+',version) or artifact['file']!=expected or not re.fullmatch('[0-9a-f]{64}',artifact['sha256']) or type(artifact['bytes']) is not int or not 0<artifact['bytes']<=512*1024**2:
        raise ValueError('Invalid own bundle metadata')
    local=root/'releases'/expected
    if local.is_file():target=local
    else:
        distribution=manifest.get('distribution',{})
        tag='v'+version+'-devel'
        url='https://github.com/airtonbp19edu/Linuxit-PDF/releases/download/'+tag+'/'+expected
        if distribution!={'storage':'github_release_asset','tag':tag,'download_url':url}:
            raise ValueError('Missing local bundle or invalid pinned own GitHub release URL')
        target=root/'analysis-local/delivery-downloads'/artifact['sha256']/expected
        if not target.exists():
            if not download:raise ValueError('Fetch the published bundle before the read-only audit')
            target.parent.mkdir(parents=True,exist_ok=True)
            descriptor,name=tempfile.mkstemp(prefix='.download-',dir=target.parent);temporary=Path(name)
            try:
                total=0;identity=hashlib.sha256()
                request=urllib.request.Request(url,headers={'User-Agent':'Linuxit-delivery-verifier'})
                with os.fdopen(descriptor,'wb') as output,urllib.request.urlopen(request,timeout=90) as response:
                    while block:=response.read(1024*1024):
                        total+=len(block)
                        if total>artifact['bytes']:raise ValueError('Download exceeds published size')
                        identity.update(block);output.write(block)
                    output.flush();os.fsync(output.fileno())
                if total!=artifact['bytes'] or identity.hexdigest()!=artifact['sha256']:raise ValueError('Published download identity differs')
                # Exclusive publication, never overwrite a different cached artifact.
                if os.name=='nt':os.rename(temporary,target)
                else:os.link(temporary,target)
            finally:temporary.unlink(missing_ok=True)
    if target.is_symlink() or target.stat().st_size!=artifact['bytes'] or digest(target)!=artifact['sha256']:
        raise ValueError('Bundle bytes/hash do not match published identity')
    return target


def manifest_for_file(root,name):
    match=re.fullmatch(r'LinuxitPDF-(\d+\.\d+\.\d+)-x86_64\.flatpak',name)
    if not match:raise ValueError('Unexpected checksum filename')
    manifest=json.loads((Path(root)/'releases'/('manifest-'+match[1]+'.json')).read_text(encoding='utf-8'))
    if manifest['artifact']['file']!=name:raise ValueError('Historical manifest identity differs')
    return manifest
