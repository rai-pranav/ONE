"""Unit tests for the one.params module.

NB: `setup` function tested with TestOneSetup class in one.tests.test_one.
"""
import unittest
from unittest import mock
from pathlib import Path
from functools import partial

import one.params as params
from . import util


class TestONEParamUtil(unittest.TestCase):
    """Test class for one.params utility functions"""
    def setUp(self) -> None:
        pass

    def test_key_from_url(self):
        """Test for one.params._key_from_url"""
        key = params._key_from_url('https://sub.domain.org/')
        self.assertEqual(key, 'sub.domain.org')

        key = params._key_from_url('http://www.domain.org/db/?rest=True')
        self.assertEqual(key, 'www.domain.org_db__rest_true')

    def test_get_params_dir(self):
        """Test for one.params.get_params_dir"""
        par_dir = Path('path', 'to', 'params')
        with mock.patch('iblutil.io.params.getfile', new=partial(util.get_file, par_dir)):
            path = params.get_params_dir()
        self.assertIsInstance(path, Path)
        self.assertEqual('path/to/params/.one', path.as_posix())

    def test_get_rest_dir(self):
        """Test for one.params.get_rest_dir"""
        par_dir = Path('path', 'to', 'params')
        url = 'https://sub.domain.net/'
        with mock.patch('iblutil.io.params.getfile', new=partial(util.get_file, par_dir)):
            path1 = params.get_rest_dir()
            path2 = params.get_rest_dir(url)

        expected = ('path', 'to', 'params', '.one', '.rest')
        self.assertCountEqual(expected, path1.parts)

        expected = (*expected, 'sub.domain.net', 'https')
        self.assertCountEqual(expected, path2.parts)

    def test_get_default_client(self):
        """Test for one.params.get_default_client"""
        temp_dir = util.set_up_env()
        self.addCleanup(temp_dir.cleanup)
        with mock.patch('iblutil.io.params.getfile', new=partial(util.get_file, temp_dir.name)):
            self.assertIsNone(params.get_default_client())
            # Copy over caches fixture
            params.setup(silent=True)
            client = params.get_default_client()
            self.assertEqual(client, 'https://openalyx.internationalbrainlab.org')
            # Test with include_schema=False
            client = params.get_default_client(include_schema=False)
            self.assertEqual(client, 'openalyx.internationalbrainlab.org')

    def test_get_cache_dir(self):
        """Test for one.params.get_cache_dir"""
        temp_dir = util.set_up_env()
        cache_dir = Path(temp_dir.name) / 'download_cache'
        assert not cache_dir.exists()
        self.addCleanup(temp_dir.cleanup)
        with mock.patch('iblutil.io.params.getfile', new=partial(util.get_file, temp_dir.name)):
            util.setup_test_params(cache_dir=cache_dir)
            out = params.get_cache_dir()
        self.assertEqual(cache_dir, out)
        self.assertTrue(cache_dir.exists())


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
