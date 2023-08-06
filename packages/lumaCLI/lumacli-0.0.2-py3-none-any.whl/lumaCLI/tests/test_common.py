from lumaCLI.tests.utils import MANIFEST_JSON
from lumaCLI.common import validate_json, json_to_dict


def test_validate_json():
    is_json = validate_json(json_path=MANIFEST_JSON)
    assert is_json


def test_validate_json_to_dict():
    dict_data = json_to_dict(json_path=MANIFEST_JSON)
    assert isinstance(dict_data, dict)
