# flake8: noqa
import unittest
import re
import importlib

# Damn you dash separated module names!!!
LinterModule = importlib.import_module('SublimeLinter-contrib-mypy.linter')
Linter = LinterModule.Mypy
regex = Linter.regex


class TestRegex(unittest.TestCase):

    def assertMatch(self, string, expected):
        match = re.match(regex, string)
        self.assertIsNotNone(match)
        self.assertEqual(match.groupdict(), expected)

    def assertMatchIsNone(self, string):
        self.assertIsNone(re.match(regex, string))

    def test_no_matches(self):
        self.assertMatchIsNone('')
        self.assertMatchIsNone('foo')

    def test_matches(self):
        self.assertMatch(
            '/path/to/package/module.py:18:4: error: No return value expected', {
                'file': '/path/to/package/module.py',
                'error': 'error',
                'line': '18',
                'col': '4',
                'warning': None,
                'message': 'No return value expected'})

        self.assertMatch(
            '/path/to/package/module.py:40: error: "dict" is not subscriptable, use "typing.Dict" instead', {
                'file': '/path/to/package/module.py',
                'error': 'error',
                'line': '40',
                'col': None,
                'warning': None,
                'message': '"dict" is not subscriptable, use "typing.Dict" instead'})

    def test_tmp_files_that_have_no_file_extension(self):
        self.assertMatch(
            '/tmp/yoeai32h2:6:0: error: Cannot find module named \'PackageName.lib\'', {
                'file': '/tmp/yoeai32h2',
                'error': 'error',
                'line': '6',
                'col': '0',
                'warning': None,
                'message': 'Cannot find module named \'PackageName.lib\''})

    # def test_pyi_are_excluded(self):
    #     self.assertMatchIsNone('/home/code/.local/lib/mypy/typeshed/stdlib/1and3/logging/handlers.pyi:86:4: error: Return type becomes "Any" due to an unfollowed import')
