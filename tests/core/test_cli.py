from tests.core.mockup import DummyAwsCli


def test_cli_app_should_returns_stats() -> None:
    app = DummyAwsCli()
    app.list()
