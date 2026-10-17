#!/usr/bin/env python3
"""Prepare synthetic stage-10 inputs and an offline Sandbox config; never launch Foxit."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app/vendor'))
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

TARGET_SHA256 = '90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6'
PASSWORD = 'linuxit-sintetico'


def sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def host_readiness():
    """Capability hints only: installed binary does not prove a working guest."""
    result = {'platform': sys.platform, 'edition_id': None,
              'sandbox_executable_present': False, 'sandbox_supported_edition': None,
              'runtime_verified': False, 'original_launched': False}
    if sys.platform == 'win32':
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r'SOFTWARE\Microsoft\Windows NT\CurrentVersion') as key:
            result['edition_id'] = winreg.QueryValueEx(key, 'EditionID')[0]
        result['sandbox_supported_edition'] = result['edition_id'] in {
            'Professional', 'ProfessionalN', 'ProfessionalEducation',
            'ProfessionalWorkstation', 'Enterprise', 'EnterpriseN',
            'EnterpriseS', 'EnterpriseSN', 'Education', 'EducationN'}
        result['sandbox_executable_present'] = (
            Path(os.environ.get('SystemRoot', r'C:\Windows')) /
            'System32/WindowsSandbox.exe').is_file()
    result['status'] = 'prepared_not_executed'
    if result['sandbox_supported_edition'] is False:
        result['status'] = 'blocked_unsupported_windows_edition'
    elif not result['sandbox_executable_present']:
        result['status'] = 'blocked_no_windows_sandbox_executable'
    return result


def numbered_pdf(path, count, mixed=False):
    writer = PdfWriter()
    for index in range(count):
        width, height = ((595, 842) if not mixed or index % 2 == 0 else (420, 595))
        page = writer.add_blank_page(width, height)
        font = DictionaryObject({NameObject('/Type'): NameObject('/Font'),
                                 NameObject('/Subtype'): NameObject('/Type1'),
                                 NameObject('/BaseFont'): NameObject('/Helvetica')})
        page[NameObject('/Resources')] = DictionaryObject({
            NameObject('/Font'): DictionaryObject({NameObject('/F1'): font})})
        stream = DecodedStreamObject()
        stream.set_data((f'BT /F1 16 Tf 40 {height - 60} Td '
                         f'(PAGE {index + 1:03d} alvo) Tj ET\n').encode('ascii'))
        page[NameObject('/Contents')] = writer._add_object(stream)
        if mixed and index % 3 == 2:
            page.rotate(90)
    writer.add_metadata({'/Title': 'Linuxit - corpus sintetico etapa 10'})
    writer.write(path)


def build_corpus(folder):
    folder.mkdir()
    shutil.copyfile(ROOT / 'testes/fixtures/busca-escopos.pdf', folder / 'busca-escopos.pdf')
    numbered_pdf(folder / 'geometria.pdf', 8, mixed=True)
    numbered_pdf(folder / 'busca-longa.pdf', 250)
    writer = PdfWriter()
    writer.append(folder / 'geometria.pdf')
    # Synthetic known password only; RC4 exercises the dialog without an AES dependency.
    writer.encrypt(PASSWORD, algorithm='RC4-128')
    writer.write(folder / 'com-senha.pdf')
    writer = PdfWriter()
    writer.append(folder / 'geometria.pdf')
    writer.add_attachment('nota-sintetica.txt', b'Anexo sintetico: alvo\n')
    writer.write(folder / 'com-anexo.pdf')
    (folder / 'invalido.pdf').write_bytes(b'%PDF-1.7\nINVALID SYNTHETIC INPUT\n%%EOF\n')
    (folder / 'vazio.pdf').write_bytes(b'')
    (folder / 'controle.txt').write_text('LINUXIT_RUNTIME_PROBE\nControle de interface do ambiente isolado.\n', encoding='utf-8')
    return [{'name': p.name, 'size': p.stat().st_size, 'sha256': sha256(p)}
            for p in sorted(folder.iterdir()) if p.is_file()]


def sandbox_config(reference, inputs, results):
    config = ET.Element('Configuration')
    for key in ('vGPU', 'Networking', 'AudioInput', 'VideoInput',
                'PrinterRedirection', 'ClipboardRedirection'):
        ET.SubElement(config, key).text = 'Disable'
    ET.SubElement(config, 'ProtectedClient').text = 'Enable'
    ET.SubElement(config, 'MemoryInMB').text = '4096'
    mappings = ET.SubElement(config, 'MappedFolders')
    for host, guest, readonly in (
        (reference, r'C:\Linuxit\Reference', True),
        (inputs, r'C:\Linuxit\Input', True),
        (results, r'C:\Linuxit\Results', False),
    ):
        mapping = ET.SubElement(mappings, 'MappedFolder')
        ET.SubElement(mapping, 'HostFolder').text = str(host)
        ET.SubElement(mapping, 'SandboxFolder').text = guest
        ET.SubElement(mapping, 'ReadOnly').text = str(readonly).lower()
    # A GUI control is opened first; the original is never launched automatically.
    ET.SubElement(ET.SubElement(config, 'LogonCommand'), 'Command').text = (
        r'notepad.exe C:\Linuxit\Input\controle.txt')
    ET.indent(config)
    return ET.tostring(config, encoding='unicode') + '\n'


def prepare(reference, output):
    reference, output = reference.resolve(strict=True), output.resolve()
    if reference == ROOT or reference.is_relative_to(ROOT):
        raise ValueError('Keep the proprietary reference outside the checkout')
    if output.is_relative_to(reference) or reference.is_relative_to(output):
        raise ValueError('Reference and campaign directories must not overlap')
    # Never overwrite prior observations, and never expose an existing results tree.
    if output.exists():
        raise FileExistsError('Use a new campaign directory')
    target = reference / 'FoxitPDFReader.exe'
    if sha256(target) != TARGET_SHA256:
        raise ValueError('Unrecognized original binary')
    # Reparse points could expose additional host folders through the reference map.
    for item in [reference, *reference.rglob('*')]:
        if item.is_symlink() or (hasattr(item, 'is_junction') and item.is_junction()):
            raise ValueError('Reference must not contain symbolic links or junctions')
    output.mkdir(parents=True)
    inputs, results = output / 'input', output / 'results'
    results.mkdir()
    fixtures = build_corpus(inputs)
    scenarios = json.loads((ROOT / 'testes/cenarios-dinamicos.json').read_text(encoding='utf-8'))
    shutil.copyfile(ROOT / 'testes/cenarios-dinamicos.json', inputs / 'cenarios.json')
    shutil.copyfile(ROOT / 'docs/ETAPA-10.md', inputs / 'roteiro.md')
    shutil.copyfile(ROOT / 'testes/cenarios-interface.json', inputs / 'cenarios-interface.json')
    shutil.copyfile(ROOT / 'docs/ETAPA-11.md', inputs / 'roteiro-interface.md')
    report = {'schema': 'linuxit-dynamic-campaign-v1',
              'target_sha256': TARGET_SHA256, 'readiness': host_readiness(),
              'fixtures': fixtures, 'original_launched': False,
              'functional_equivalence_verified': False,
              'observations': [{'id': case['id'], 'status': 'not_run',
                                'observed': None, 'evidence': []}
                               for case in scenarios['cases']]}
    (output / 'campaign.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (output / 'foxit-offline.wsb').write_text(sandbox_config(reference, inputs, results), encoding='utf-8')
    if sha256(target) != TARGET_SHA256:
        raise ValueError('Reference changed during preparation')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True, help='New private campaign directory')
    args = parser.parse_args()
    try:
        report = prepare(args.reference, args.output)
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc) + '\n')
    print(json.dumps({'readiness': report['readiness'], 'fixtures': len(report['fixtures']),
                      'cases_not_run': len(report['observations']), 'original_launched': False}))


if __name__ == '__main__':
    main()
