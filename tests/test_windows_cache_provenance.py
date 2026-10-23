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
        script=(ROOT/'packaging/windows/linuxit.nsi').read_text(encoding='utf-8')
        boxes=[line for line in script.splitlines() if 'MessageBox' in line]
        self.assertTrue(boxes)
        self.assertTrue(all('/SD ' in line for line in boxes),boxes)
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
