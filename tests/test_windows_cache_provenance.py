import importlib.util,pathlib,tempfile,unittest
from unittest.mock import patch
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('windows_builder',ROOT/'scripts/build_windows.py');builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
class WindowsCacheProvenanceTests(unittest.TestCase):
    def test_nsis_target_uses_native_separators_and_unquoted_final_directory(self):
        spec=importlib.util.spec_from_file_location('installer_check',ROOT/'scripts/check_windows_installer.py')
        check=importlib.util.module_from_spec(spec);spec.loader.exec_module(check)
        command=check.install_command('D:/build artifacts/installer.exe','D:/temp/installed app com espaços')
        self.assertEqual(command,'"D:\\build artifacts\\installer.exe" /S /D=D:\\temp\\installed app com espaços')
    def test_nsis_target_is_backslashed_even_when_ntpath_keeps_forward_slashes(self):
        # MSYS2 UCRT64 Python keeps '/' in ntpath.normpath; NSIS then ignored /D= (CI 39895160350).
        spec=importlib.util.spec_from_file_location('installer_check',ROOT/'scripts/check_windows_installer.py')
        check=importlib.util.module_from_spec(spec);spec.loader.exec_module(check)
        with patch.object(check.ntpath,'normpath',side_effect=lambda value:value):
            command=check.install_command('D:/a/dist/installer.exe','D:/a/_temp/installed app com espaços')
        self.assertEqual(command,'D:\\a\\dist\\installer.exe /S /D=D:\\a\\_temp\\installed app com espaços')
        self.assertNotIn('/',command.replace(' /S','').replace(' /D=',''))
        with patch.object(builder.ntpath,'normpath',side_effect=lambda value:value):
            self.assertEqual(builder.native('D:/a/stage'),'D:\\a\\stage')
    def test_installer_message_boxes_never_block_silent_mode(self):
        # Each MessageBox must be reachable only when not silent: an `IfSilent`
        # that skips it has to appear on one of the few lines above it. A plain
        # MessageBox in a /S run blocks forever (CI 39896899395).
        lines=(ROOT/'packaging/windows/linuxit.nsi').read_text(encoding='utf-8').splitlines()
        boxes=[i for i,line in enumerate(lines) if line.strip().startswith('MessageBox')]
        self.assertTrue(boxes)
        for i in boxes:
            guard=any('IfSilent' in lines[j] for j in range(max(0,i-3),i))
            self.assertTrue(guard,f'MessageBox at line {i+1} is not guarded by IfSilent')
    def test_uninstall_lines_use_backslashes_for_nested_files(self):
        # MSYS2 Python emitted 'app/x.py'; NSIS Delete ignored it and left every nested file (CI 39897411096).
        with tempfile.TemporaryDirectory() as folder:
            stage=pathlib.Path(folder)
            (stage/'app'/'vendor').mkdir(parents=True)
            (stage/'app'/'vendor'/'m.py').write_text('x');(stage/'top.txt').write_text('x')
            lines=builder.uninstall_lines(stage)
        self.assertIn('Delete "$INSTDIR\\app\\vendor\\m.py"',lines)
        self.assertIn('Delete "$INSTDIR\\top.txt"',lines)
        self.assertEqual(lines[-2:],['RMDir "$INSTDIR\\app\\vendor"','RMDir "$INSTDIR\\app"'])
        self.assertFalse(any('/' in line for line in lines),lines)
    def _openssl_helpers(self):
        import ast,hashlib,os,shutil
        source=(ROOT/'packaging/windows/windows_bootstrap.py').read_text(encoding='utf-8')
        tree=ast.parse(source)
        wanted=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in ('_short_path','_openssl_path')]
        self.assertEqual(len(wanted),2)
        namespace=dict(os=os,hashlib=hashlib,shutil=shutil,Path=pathlib.Path)
        exec(compile(ast.Module(body=wanted,type_ignores=[]),'windows_bootstrap','exec'),namespace)
        return namespace['_openssl_path']
    def test_openssl_paths_reach_openssl_as_ascii(self):
        # A non-ASCII install folder made cryptography's Rust layer panic at import (CI 39897411096).
        openssl_path=self._openssl_helpers()
        with tempfile.TemporaryDirectory() as folder:
            root=pathlib.Path(folder)
            plain=root/'plain.cnf';plain.write_text('cfg')
            self.assertEqual(openssl_path(plain),str(plain))
            accented=root/'instalação';(accented/'ossl-modules').mkdir(parents=True)
            (accented/'ossl-modules'/'legacy.dll').write_bytes(b'dll')
            cache=root/'cache';cache.mkdir()
            with patch.dict('os.environ',{'LOCALAPPDATA':str(cache),'PROGRAMDATA':'','PUBLIC':''}):
                safe=openssl_path(accented/'ossl-modules')
            self.assertTrue(safe.isascii(),safe)
            self.assertEqual((pathlib.Path(safe)/'legacy.dll').read_bytes(),b'dll')
            with patch.dict('os.environ',{'LOCALAPPDATA':str(root/'usuário'),'PROGRAMDATA':'','PUBLIC':''}):
                self.assertIsNone(openssl_path(accented/'ossl-modules'))
    def test_bootstrap_relaunches_from_an_ascii_alias_and_uninstaller_removes_it(self):
        # Poppler aborted opening any PDF from 'installed app com espaços'; the same
        # installer in an ASCII folder rendered (CI 39899979222).
        source=(ROOT/'packaging/windows/windows_bootstrap.py').read_text(encoding='utf-8')
        self.assertIn("ROOT=Path(os.path.abspath(__file__)).parent",source)
        self.assertNotIn("ROOT=Path(__file__).resolve()",source)
        self.assertIn("LINUXIT_ASCII_ALIAS",source)
        self.assertIn("_winapi.CreateJunction",source)
        script=(ROOT/'packaging/windows/linuxit.nsi').read_text(encoding='utf-8')
        self.assertIn('"AsciiAlias"',script)
        self.assertLess(script.index('"AsciiAlias"'),script.index('DeleteRegKey HKCU'))
        import ast,hashlib,os,json
        tree=ast.parse(source)
        wanted=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('_short_path','_uninstall_key','_ascii_alias')]
        namespace=dict(os=os,hashlib=hashlib,json=json,Path=pathlib.Path,__file__=str(ROOT/'packaging/windows/windows_bootstrap.py'))
        exec(compile(ast.Module(body=wanted,type_ignores=[]),'windows_bootstrap','exec'),namespace)
        plain=pathlib.Path('/opt/linuxit/app')
        self.assertEqual(namespace['_ascii_alias'](plain),plain)
        if os.name!='nt':  # no junction support here: must decline, not crash
            self.assertIsNone(namespace['_ascii_alias'](pathlib.Path('/opt/instalação')))
    def test_bootstrap_never_leaves_legacy_load_to_a_non_ascii_path(self):
        source=(ROOT/'packaging/windows/windows_bootstrap.py').read_text(encoding='utf-8')
        self.assertIn("('OPENSSL_MODULES','lib/ossl-modules')",source)
        self.assertIn("os.environ['CRYPTOGRAPHY_OPENSSL_NO_LEGACY']='1'",source)
        self.assertIn("'lib/ossl-modules'",(ROOT/'scripts/build_windows.py').read_text(encoding='utf-8'))
    def test_missing_install_search_finds_only_complete_installations(self):
        spec=importlib.util.spec_from_file_location('installer_check',ROOT/'scripts/check_windows_installer.py')
        check=importlib.util.module_from_spec(spec);spec.loader.exec_module(check)
        with tempfile.TemporaryDirectory() as folder:
            root=pathlib.Path(folder)
            real=root/'Programs'/'Linuxit PDF'/'0.1.19';real.mkdir(parents=True)
            (real/'windows-manifest.json').write_text('{}');(real/'uninstall.exe').write_bytes(b'')
            payload=root/'payload';payload.mkdir()
            (payload/'windows-manifest.json').write_text('{}')  # staged payload, not an installation
            self.assertEqual(check._find_manifests([root]),[str(real)])
            self.assertEqual(check._find_manifests([root/'absent']),[])
    def test_ci_commit_identity_does_not_require_git_executable(self):
        with patch.dict(builder.os.environ,{'GITHUB_SHA':'a'*40}),patch.object(builder.subprocess,'check_output',side_effect=AssertionError('Git dependency')):
            self.assertEqual(builder.source_revision(),'a'*40)
    def test_malformed_ci_identity_is_never_recorded_as_a_commit(self):
        with patch.dict(builder.os.environ,{'GITHUB_SHA':'main'}),self.assertRaises(ValueError):builder.source_revision()
    def test_arbitrary_cache_path_is_not_automatically_attributed(self):
        self.assertIsNone(builder.cache_group('runtime/lib/unknown.cache'))
        self.assertIsNone(builder.cache_group('runtime/share/mime/packages/source.xml'))
        self.assertEqual(builder.cache_group('runtime/share/mime/mime.cache'),'mime')
    def test_missing_input_owner_is_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            root=pathlib.Path(folder);(root/'bin').mkdir();(root/'bin/glib-compile-schemas.exe').write_bytes(b'generator')
            d=root/'share/glib-2.0/schemas';d.mkdir(parents=True);(d/'own.xml').write_text('schema')
            with self.assertRaisesRegex(ValueError,'without provenance'):builder.cache_inputs(root,{},'schemas')
    def test_generator_and_input_hashes_are_individually_retained(self):
        with tempfile.TemporaryDirectory() as folder:
            root=pathlib.Path(folder);(root/'bin').mkdir();(root/'bin/glib-compile-schemas.exe').write_bytes(b'generator')
            d=root/'share/glib-2.0/schemas';d.mkdir(parents=True);(d/'own.xml').write_text('schema')
            owner={'/ucrt64/bin/glib-compile-schemas.exe':'glib2','/ucrt64/share/glib-2.0/schemas/own.xml':'application'}
            report=builder.cache_inputs(root,owner,'schemas');self.assertEqual(len(report['inputs']),2)
            self.assertEqual({r['package'] for r in report['inputs']},{'glib2','application'});self.assertTrue(all(len(r['sha256'])==64 for r in report['inputs']))
