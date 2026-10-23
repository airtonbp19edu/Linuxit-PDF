"""Explicit, single-endpoint RFC3161 transport; trust remains a separate step."""
import hashlib
import json
from pathlib import Path
import ssl
import tempfile
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener, HTTPSHandler

from local_files import publish_copy

MAX_RESPONSE=1024*1024


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args):
        return None


def fetch_timestamp_response(path,request):
    """Send only a prepared digest/nonce after explicit opt-in, never the PDF.

    A successful download is not signature/CA validation. The unchanged existing
    import step must authenticate the TSA and publish the timestamped PDF.
    """
    from asn1crypto import tsp
    from pdf_preservation import _read, MAX_FILE
    from pdf_changes import _require, _sha
    _require(isinstance(request,dict) and set(request)=={'source_sha256','folder','destination','url','confirmed'},
             'Pedido de consulta TSA inválido.')
    _require(request['confirmed'] is True,'Confirme o envio deste pedido à TSA escolhida.')
    url=request['url']
    _require(isinstance(url,str) and 0<len(url)<=2048 and not any(ord(c)<=32 or ord(c)==127 for c in url),
             'URL TSA inválida.')
    try:
        endpoint=urlsplit(url)
        _require(endpoint.scheme=='https' and endpoint.hostname and endpoint.username is None and
                 endpoint.password is None and not endpoint.fragment and endpoint.port!=0,
                 'Use uma URL HTTPS explícita, sem credenciais embutidas ou fragmento.')
    except ValueError:
        raise ValueError('URL HTTPS da TSA inválida.') from None
    source=Path(path).resolve();identity=_sha(source)
    _require(identity==request['source_sha256'],'O PDF mudou; prepare outro pedido TSA.')
    destination=Path(request['destination'])
    if destination.exists():raise FileExistsError('Escolha um arquivo novo para a resposta TSA.')
    folder=Path(request['folder'])
    manifest=json.loads(_read(folder/'manifest.json',16384))
    query_raw=_read(folder/'timestamp.tsq',16384)
    pending=_read(folder/'document.pending',MAX_FILE)
    _require(manifest.get('schema')=='linuxit-timestamp-pending-v1' and
             manifest.get('source_sha256')==identity and manifest.get('query_sha256')==hashlib.sha256(query_raw).hexdigest()
             and manifest.get('pending_sha256')==hashlib.sha256(pending).hexdigest()
             and pending.startswith(_read(source,MAX_FILE)), 'Preparação TSA alterada ou pertence a outro PDF.')
    query=tsp.TimeStampReq.load(query_raw,strict=True)
    left,right=manifest.get('left'),manifest.get('right')
    _require(type(left) is int and type(right) is int and 0<left<right<len(pending), 'Reserva TSA inválida.')
    _require(query['nonce'].native is not None and query['message_imprint']['hash_algorithm']['algorithm'].native=='sha256'
             and query['message_imprint']['hashed_message'].native==hashlib.sha256(pending[:left]+pending[right:]).digest(),
             'Nonce ou resumo do pedido TSA inválido.')
    message=Request(url,data=query_raw,method='POST',headers={'Content-Type':'application/timestamp-query',
                    'Accept':'application/timestamp-reply','User-Agent':'Linuxit-PDF'})
    # No implicit proxy, cookies, authentication, redirects or retry to other hosts.
    opener=build_opener(ProxyHandler({}),NoRedirect(),HTTPSHandler(context=ssl.create_default_context()))
    try:
        with opener.open(message,timeout=20) as response:
            _require(response.status==200 and response.headers.get_content_type()=='application/timestamp-reply',
                     'A TSA não devolveu uma resposta RFC3161 válida.')
            encoded=response.read(MAX_RESPONSE+1)
    except (HTTPError,URLError,OSError):
        raise ValueError('Consulta TSA falhou; confira a URL HTTPS e tente novamente explicitamente.') from None
    _require(0<len(encoded)<=MAX_RESPONSE,'Resposta TSA vazia ou acima do limite de 1 MiB.')
    answer=tsp.TimeStampResp.load(encoded,strict=True)
    _require(answer.dump()==encoded and answer['status']['status'].native in ('granted','granted_with_mods'),
             'A TSA não concedeu um carimbo DER válido.')
    info=answer['time_stamp_token']['content']['encap_content_info']['content'].parsed
    _require(info['nonce'].native==query['nonce'].native and
             info['message_imprint']['hash_algorithm']['algorithm'].native=='sha256' and
             info['message_imprint']['hashed_message'].native==query['message_imprint']['hashed_message'].native,
             'A resposta TSA pertence a outro pedido.')
    with tempfile.TemporaryDirectory(prefix='linuxit-tsa-response-') as directory:
        staged=Path(directory)/'response.tsr';staged.write_bytes(encoded)
        publish_copy(staged,destination,lambda:_require(_sha(source)==identity,'O PDF mudou durante a consulta.'))
    return dict(schema='linuxit-timestamp-response-v1',path=str(destination),source_sha256=identity,
                response_sha256=hashlib.sha256(encoded).hexdigest(),network_used=True,query_matches=True,
                complete=False,trust_assessed=False,pades_lta_claimed=False)
