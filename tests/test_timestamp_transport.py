"""Opt-in transport, request binding and an actual synthetic HTTPS endpoint."""
from datetime import datetime,timezone,timedelta
from email.message import Message
from http.server import BaseHTTPRequestHandler,HTTPServer
import hashlib
import ipaddress
from pathlib import Path
import os
import ssl
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from asn1crypto import cms,tsp
from pdf_preservation import prepare_document_timestamp
from timestamp_transport import fetch_timestamp_response
from test_redaction_apply import fixture


class Reply:
    def __init__(self,raw,content_type='application/timestamp-reply'):
        self.raw=raw;self.status=200;self.headers=Message();self.headers['Content-Type']=content_type
    def read(self,size):return self.raw[:size]
    def __enter__(self):return self
    def __exit__(self,*args):return False


class TimestampTransportTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.source=self.root/'source.pdf';self.source.write_bytes(fixture())
        self.identity=hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.folder=self.root/'pending'
        prepare_document_timestamp(self.source,dict(source_sha256=self.identity,folder=str(self.folder)))
        self.query=tsp.TimeStampReq.load((self.folder/'timestamp.tsq').read_bytes())
        self.destination=self.root/'response.tsr'
        self.request=dict(source_sha256=self.identity,folder=str(self.folder),destination=str(self.destination),
                          url='https://tsa.example.invalid/stamp',confirmed=True)

    def answer(self,nonce=None,wrong_imprint=False):
        imprint=self.query['message_imprint'].native
        if wrong_imprint:imprint['hashed_message']=b'\0'*32
        info=tsp.TSTInfo(dict(version='v1',policy='1.2.3.4',message_imprint=imprint,serial_number=1,
                             gen_time=datetime.now(timezone.utc),nonce=self.query['nonce'].native if nonce is None else nonce))
        # Deliberately unsigned structural token: transport cannot establish trust.
        token=cms.ContentInfo({'content_type':'signed_data','content':dict(version='v3',digest_algorithms=[{'algorithm':'sha256'}],
            encap_content_info={'content_type':'tst_info','content':info},signer_infos=[])})
        return tsp.TimeStampResp({'status':{'status':'granted'},'time_stamp_token':token}).dump()

    def test_matching_download_sends_query_only_and_does_not_claim_trust(self):
        encoded=self.answer()
        with patch('timestamp_transport.build_opener') as make:
            make.return_value.open.return_value=Reply(encoded)
            result=fetch_timestamp_response(self.source,self.request)
        sent=make.return_value.open.call_args.args[0]
        self.assertEqual(sent.data,(self.folder/'timestamp.tsq').read_bytes())
        self.assertNotIn(b'%PDF',sent.data)
        self.assertEqual(self.destination.read_bytes(),encoded)
        self.assertFalse(result['trust_assessed']);self.assertFalse(result['complete'])
        self.assertTrue(result['network_used']);self.assertTrue(result['query_matches'])
        self.assertEqual(hashlib.sha256(self.source.read_bytes()).hexdigest(),self.identity)

    def test_wrong_nonce_or_imprint_never_publishes(self):
        for encoded in (self.answer(nonce=self.query['nonce'].native+1),self.answer(wrong_imprint=True)):
            with self.subTest(encoded=hashlib.sha256(encoded).hexdigest()),patch('timestamp_transport.build_opener') as make:
                make.return_value.open.return_value=Reply(encoded)
                with self.assertRaises(ValueError):fetch_timestamp_response(self.source,self.request)
                self.assertFalse(self.destination.exists())

    def test_no_implicit_network_or_unsafe_endpoint(self):
        for change in ({'confirmed':False},{'url':'http://tsa.example.invalid/'},
                       {'url':'https://user:password@tsa.example.invalid/'},{'url':'https://tsa.example.invalid/#fragment'}):
            with self.subTest(change=change),patch('timestamp_transport.build_opener') as make:
                with self.assertRaises(ValueError):fetch_timestamp_response(self.source,dict(self.request,**change))
                make.assert_not_called()

    def test_changed_pending_and_existing_destination_are_preserved(self):
        self.destination.write_bytes(b'existing')
        with patch('timestamp_transport.build_opener') as make:
            with self.assertRaises(FileExistsError):fetch_timestamp_response(self.source,self.request)
            make.assert_not_called()
        self.assertEqual(self.destination.read_bytes(),b'existing');self.destination.unlink()
        (self.folder/'timestamp.tsq').write_bytes(b'altered')
        with patch('timestamp_transport.build_opener') as make:
            with self.assertRaises(ValueError):fetch_timestamp_response(self.source,self.request)
            make.assert_not_called()

    def test_bad_media_oversize_and_redirect_refused(self):
        for reply in (Reply(self.answer(),'text/html'),Reply(b'x'*(1024*1024+1))):
            with patch('timestamp_transport.build_opener') as make:
                make.return_value.open.return_value=reply
                with self.assertRaises(ValueError):fetch_timestamp_response(self.source,self.request)
                self.assertFalse(self.destination.exists())
        with patch('timestamp_transport.build_opener') as make:
            make.return_value.open.side_effect=HTTPError(self.request['url'],302,'redirect',{},None)
            with self.assertRaises(ValueError):fetch_timestamp_response(self.source,self.request)
            self.assertEqual(make.return_value.open.call_count,1)

    def test_actual_https_to_explicit_loopback_tsa(self):
        from cryptography import x509
        from cryptography.hazmat.primitives import hashes,serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
        name=x509.Name([x509.NameAttribute(x509.NameOID.COMMON_NAME,'Linuxit synthetic TLS')])
        now=datetime.now(timezone.utc)
        cert=(x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
            .serial_number(1).not_valid_before(now-timedelta(minutes=1)).not_valid_after(now+timedelta(hours=1))
            .add_extension(x509.SubjectAlternativeName([x509.IPAddress(ipaddress.ip_address('127.0.0.1'))]),critical=False)
            .add_extension(x509.BasicConstraints(ca=True,path_length=None),critical=True).sign(key,hashes.SHA256()))
        certfile=self.root/'tls.pem';certfile.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
        keyfile=self.root/'tls-key.pem';keyfile.write_bytes(key.private_bytes(serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
        observed=[];encoded=self.answer()
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_POST(self):
                observed.append((self.path,self.headers['Content-Type'],self.rfile.read(int(self.headers['Content-Length']))))
                self.send_response(200);self.send_header('Content-Type','application/timestamp-reply')
                self.send_header('Content-Length',str(len(encoded)));self.end_headers();self.wfile.write(encoded)
        server=HTTPServer(('127.0.0.1',0),Handler)
        context=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);context.load_cert_chain(str(certfile),str(keyfile))
        server.socket=context.wrap_socket(server.socket,server_side=True)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        trusted=ssl.create_default_context(cafile=str(certfile))
        try:
            with patch('timestamp_transport.ssl.create_default_context',return_value=trusted):
                result=fetch_timestamp_response(self.source,dict(self.request,url=f'https://127.0.0.1:{server.server_port}/chosen-tsa'))
        finally:server.shutdown();server.server_close();thread.join(3)
        self.assertEqual(observed,[('/chosen-tsa','application/timestamp-query',(self.folder/'timestamp.tsq').read_bytes())])
        self.assertEqual(self.destination.read_bytes(),encoded);self.assertFalse(result['trust_assessed'])
