#!/usr/bin/env python3
"""Real CUPS held-job/cancellation against an isolated loopback CI scheduler."""
import argparse,json,os,socket,subprocess,sys,time
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'app'))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    if args.output.exists():parser.error('Preserve earlier evidence')
    if not sys.platform.startswith('linux') or os.geteuid()!=0:parser.error('Run only inside the ephemeral Linux CI container as root')
    from pdf_dependency import configure_pdf_library
    configure_pdf_library()
    from pypdf import PdfWriter
    import cups_backend as cups
    work=(ROOT/'analysis-local'/('cups-queue-'+str(time.time_ns()))).resolve();work.mkdir(parents=True)
    for folder in ('etc','state','cache','spool','tmp','logs'):(work/folder).mkdir()
    with socket.socket() as probe:probe.bind(('127.0.0.1',0));port=probe.getsockname()[1]
    files=work/'cups-files.conf';config=work/'cupsd.conf'
    files.write_text('\n'.join(['SystemGroup root','User lp','Group lp','ServerBin /usr/lib/cups','DataDir /usr/share/cups',
        *[directive+' '+str(work/folder) for directive,folder in [('ServerRoot','etc'),('StateDir','state'),('CacheDir','cache'),('RequestRoot','spool'),('TempDir','tmp')]],
        'AccessLog '+str(work/'logs/access_log'),'ErrorLog '+str(work/'logs/error_log'),'PageLog '+str(work/'logs/page_log')])+'\n')
    config.write_text(f'''Listen 127.0.0.1:{port}
Browsing Off
WebInterface No
DefaultEncryption Never
LogLevel warn
PreserveJobHistory Yes
PreserveJobFiles Yes
<Location />
  Order deny,allow
  Allow localhost
</Location>
<Location /admin>
  AuthType None
  Order deny,allow
  Allow localhost
</Location>
<Policy default>
  <Limit All>
    Order deny,allow
    Allow localhost
  </Limit>
</Policy>
''')
    env={**os.environ,'CUPS_SERVER':f'127.0.0.1:{port}','LC_ALL':'C','LANG':'C'}
    report=dict(schema='linuxit-cups-queue-probe-v1',passed=False,checks={},physical_printer=False,foxit_executed=False,server_loopback_only=True,errors=[])
    with (work/'cupsd.log').open('wb') as log:
        process=subprocess.Popen(['/usr/sbin/cupsd','-f','-c',str(config),'-s',str(files)],stdout=log,stderr=log)
        try:
            deadline=time.monotonic()+15
            while time.monotonic()<deadline:
                if process.poll() is not None:raise RuntimeError('Private cupsd exited during startup; inspect its private log')
                try:
                    with socket.create_connection(('127.0.0.1',port),timeout=.3):break
                except OSError:time.sleep(.1)
            else:raise RuntimeError('Private CUPS scheduler did not listen in time')
            printer='LinuxitSynthetic'
            # cups-daemon provides IPP; socket is shipped by the larger cups package.
            # The indefinite hold below prevents any connection to this dummy URI.
            subprocess.run(['lpadmin','-p',printer,'-E','-v','ipp://127.0.0.1:9/printers/synthetic','-m','raw'],env=env,check=True,capture_output=True,timeout=20)
            fixture=work/'synthetic.pdf';writer=PdfWriter();writer.add_blank_page(100,100);writer.write(fixture)
            with patch.dict(os.environ,{'CUPS_SERVER':env['CUPS_SERVER']}):
                receipt=cups.print_file(printer,str(fixture),dict(printer_options={'job-hold-until':'indefinite'}))
                identifier=cups.submitted_job_id(receipt,printer)
                if not identifier:raise RuntimeError('CUPS did not return a recognized own job receipt')
                report['checks']['real_submission_receipt']=True
                report['checks']['held_job_in_pending_queue']=identifier in cups.pending_jobs()
                cups.cancel_job(identifier)
                report['checks']['cancelled_job_absent_from_pending']=identifier not in cups.pending_jobs()
                report['checks']['no_physical_backend_used']=True
                report['own_job_id']=identifier
            report['passed']=all(report['checks'].values()) and len(report['checks'])==4
        except Exception as exc:
            detail=(getattr(exc,'stderr',b'') or b'').decode('utf-8','replace')[:2000]
            report['errors'].append(type(exc).__name__+': '+str(exc)+(' · '+detail if detail else ''))
        finally:
            process.terminate()
            try:process.wait(timeout=10)
            except subprocess.TimeoutExpired:process.kill();process.wait(timeout=5)
    report['private_logs']=work.relative_to(ROOT).as_posix()
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report));return 0 if report['passed'] else 1


if __name__=='__main__':raise SystemExit(main())
