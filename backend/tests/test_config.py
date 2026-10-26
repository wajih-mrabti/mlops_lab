from app.config import Settings


def test_settings_are_loaded_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("APP_NAME", "modelops-lab-test")
    monkeypatch.setenv("ENVIRONMENT", "testing")

    settings = Settings()

    assert settings.app_name == "modelops-lab-test"
    assert settings.environment == "testing"
