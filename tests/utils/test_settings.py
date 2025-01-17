import pytest

from pilot.settings import Settings


def test_settings_init_raise_error_on_unknown_variables():
    with pytest.raises(ValueError):
        _ = Settings(unknown="value")


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
