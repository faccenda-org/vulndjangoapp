"""
Utility functions that use vulnerable dependencies.
DO NOT USE IN PRODUCTION.
"""
import requests
import yaml
from PIL import Image
from io import BytesIO


def fetch_remote_image(url: str) -> Image.Image:
    """
    Fetch an image from a remote URL using requests.

    VULNERABLE: Uses requests 2.25.0 which has CVE-2021-33503 (SSRF vulnerability)
    allowing attackers to control redirect locations.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))


def process_image(image_path: str) -> dict:
    """
    Process an image file and return its metadata.

    VULNERABLE: Uses Pillow 9.3.0 which has CVE-2023-50447 (arbitrary code execution)
    via crafted image files.
    """
    try:
        with Image.open(image_path) as img:
            return {
                'format': img.format,
                'size': img.size,
                'mode': img.mode,
                'width': img.width,
                'height': img.height,
            }
    except Exception as e:
        return {'error': str(e)}


def load_yaml_config(yaml_string: str) -> dict:
    """
    Load YAML configuration from a string.

    VULNERABLE: Uses PyYAML 5.3.1 which has CVE-2020-14343 (arbitrary code execution)
    via unsafe yaml.load() usage.
    """
    # Using unsafe yaml.load instead of yaml.safe_load (intentional vulnerability)
    return yaml.load(yaml_string, Loader=yaml.FullLoader)


def make_api_request(url: str, params: dict = None) -> dict:
    """
    Make an API request to an external service.

    VULNERABLE: Uses requests 2.25.0 with SSRF vulnerability.
    """
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {'error': str(e)}
