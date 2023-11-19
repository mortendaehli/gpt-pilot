import json
import sys
from io import StringIO
from os import getenv
from os.path import expanduser, expandvars, join
import pytest

from pilot.settings import Settings


@pytest.fixture
def expected_config_location():
    xdg_config_home = getenv("XDG_CONFIG_HOME")
    if xdg_config_home:
        return join(xdg_config_home, "gpt-pilot", "config.json")
    elif sys.platform in ["darwin", "linux"]:
        return expanduser("~/.gpt-pilot/config.json")
    elif sys.platform == "win32":
        return expandvars("%APPDATA%\\GPT Pilot\\config.json")
    else:
        raise RuntimeError(f"Unknown platform: {sys.platform}")


def test_settings_initializes_known_variables():
    settings = Settings()
    assert settings.openai_api_key is None
    assert settings.telemetry is None


def test_settings_init_raise_error_on_unknown_variables():
    with pytest.raises(ValueError):
        settings = Settings(unknown="value")


def test_settings_raises_error_when_saving_unknown_variables():
    settings = Settings()

    with pytest.raises(ValueError):
        settings.unknown = "value"


def test_settings_update():
    settings = Settings()
    settings.openai_api_key = "test_key"
    assert settings.openai_api_key == "test_key"


def wtest_settings_to_dict():
    settings = Settings()
    settings.openai_api_key = "test_key"
    assert settings.model_dump() == {
        "openai_api_key": "test_key",
        "telemetry": None,
    }
