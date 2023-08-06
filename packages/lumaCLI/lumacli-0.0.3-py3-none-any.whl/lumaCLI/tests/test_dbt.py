from lumaCLI import app
from typer.testing import CliRunner
from lumaCLI.tests.utils import TESTS_DIR, DUMMY_ENDPOINT


runner = CliRunner()


def test_ingest():
    result = runner.invoke(
        app,
        [
            "dbt",
            "ingest",
            TESTS_DIR,
            "--endpoint",
            DUMMY_ENDPOINT,
        ],
    )
    assert result.exit_code == 0, result.output
