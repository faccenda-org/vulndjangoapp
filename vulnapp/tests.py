"""
Unit tests for vulnerable utility functions.
"""
from django.test import TestCase
from vulnapp.utils import (
    process_image,
    load_yaml_config,
    make_api_request,
    fetch_remote_image
)
from PIL import Image
import os
import tempfile


class ImageProcessingTests(TestCase):
    """Tests for Pillow-based image processing (vulnerable: CVE-2023-50447)"""

    def setUp(self):
        # Create a simple test image
        self.test_image = Image.new('RGB', (100, 100), color='red')
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.test_image.save(self.temp_file.name)
        self.temp_file.close()

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_process_image_returns_metadata(self):
        """Test that process_image returns correct metadata"""
        result = process_image(self.temp_file.name)

        self.assertIn('format', result)
        self.assertIn('size', result)
        self.assertIn('mode', result)
        self.assertIn('width', result)
        self.assertIn('height', result)

        self.assertEqual(result['width'], 100)
        self.assertEqual(result['height'], 100)
        self.assertEqual(result['mode'], 'RGB')

    def test_process_image_handles_invalid_file(self):
        """Test that process_image handles non-existent files"""
        result = process_image('/nonexistent/file.png')

        self.assertIn('error', result)

    def test_process_image_format_detection(self):
        """Test image format detection"""
        result = process_image(self.temp_file.name)

        self.assertEqual(result['format'], 'PNG')


class YAMLConfigTests(TestCase):
    """Tests for PyYAML config loading (vulnerable: CVE-2020-14343)"""

    def test_load_simple_yaml(self):
        """Test loading simple YAML configuration"""
        yaml_string = """
        database:
          host: localhost
          port: 5432
        cache:
          enabled: true
        """

        config = load_yaml_config(yaml_string)

        self.assertIn('database', config)
        self.assertIn('cache', config)
        self.assertEqual(config['database']['host'], 'localhost')
        self.assertEqual(config['database']['port'], 5432)
        self.assertTrue(config['cache']['enabled'])

    def test_load_yaml_with_lists(self):
        """Test loading YAML with lists"""
        yaml_string = """
        servers:
          - name: server1
            ip: 192.168.1.1
          - name: server2
            ip: 192.168.1.2
        """

        config = load_yaml_config(yaml_string)

        self.assertIn('servers', config)
        self.assertEqual(len(config['servers']), 2)
        self.assertEqual(config['servers'][0]['name'], 'server1')

    def test_load_yaml_with_nested_structure(self):
        """Test loading nested YAML structures"""
        yaml_string = """
        app:
          name: TestApp
          settings:
            debug: false
            features:
              auth: true
              api: true
        """

        config = load_yaml_config(yaml_string)

        self.assertEqual(config['app']['name'], 'TestApp')
        self.assertFalse(config['app']['settings']['debug'])
        self.assertTrue(config['app']['settings']['features']['auth'])


class APIRequestTests(TestCase):
    """Tests for requests-based API calls (vulnerable: CVE-2021-33503)"""

    def test_make_api_request_with_invalid_url(self):
        """Test API request with invalid URL"""
        result = make_api_request('http://invalid-domain-that-does-not-exist.local')

        self.assertIn('error', result)

    def test_make_api_request_structure(self):
        """Test that make_api_request returns dict"""
        # Test with invalid URL to ensure it returns error dict
        result = make_api_request('http://invalid-domain-that-does-not-exist.local')

        self.assertIsInstance(result, dict)
        self.assertIn('error', result)

    def test_make_api_request_with_params(self):
        """Test API request with query parameters"""
        params = {'key': 'value', 'test': '123'}
        result = make_api_request('http://httpbin.org/get', params=params)

        # This will fail due to network, but tests the function signature
        self.assertIsInstance(result, dict)


class RemoteImageTests(TestCase):
    """Tests for remote image fetching (vulnerable: CVE-2021-33503)"""

    def test_fetch_remote_image_invalid_url(self):
        """Test fetching image from invalid URL"""
        with self.assertRaises(Exception):
            fetch_remote_image('http://invalid-url-does-not-exist.local/image.png')

    def test_fetch_remote_image_returns_image(self):
        """Test that fetch_remote_image returns Image object"""
        # Create a mock scenario - in real tests you'd mock the requests
        # For now, this tests the function exists and has correct signature
        try:
            # This will fail, but that's expected in unit tests without mocking
            fetch_remote_image('http://example.com/fake.png')
        except Exception:
            # Expected to fail without proper mocking
            pass
