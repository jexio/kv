"""Tasks for maintaining the project.
Execute 'invoke --list' for guidance on using Invoke
"""
import platform
from pathlib import Path

from invoke import call, task
from invoke.context import Context
from invoke.runners import Result


ROOT_DIR = Path(__file__).parent
SOURCE_DIR = ROOT_DIR.joinpath("kv")
TG_SOURCE_DIR = ROOT_DIR.joinpath("tg")
TEST_DIR = ROOT_DIR.joinpath("tests")
PYTHON_TARGETS = (
    SOURCE_DIR,
    TG_SOURCE_DIR,
    TEST_DIR,
    Path(__file__),
)
PYTHON_TARGETS_STR = " ".join([str(p) for p in PYTHON_TARGETS])
PERFLINT_WARNINGS = ("W8205",)
PERFLINT_WARNINGS_STR = ",".join(PERFLINT_WARNINGS)


def _run(c: Context, command: str) -> Result:
    """Run a task."""
    return c.run(command, pty=platform.system() != "Windows")


# flake8: noqa: P103
@task()
def clean_build(c):
    # type: (Context) -> None
    """Clean up files from package building."""
    _run(c, "rm -fr build/")
    _run(c, "rm -fr dist/")
    _run(c, "rm -fr .eggs/")
    _run(c, "find . -name '*.egg-info' -exec rm -fr {} +")
    _run(c, "find . -name '*.egg' -exec rm -f {} +")


# flake8: noqa: P103
@task()
def clean_python(c):
    # type: (Context) -> None
    """Clean up python file artifacts."""
    _run(c, "find . -name '*.pyc' -exec rm -f {} +")
    _run(c, "find . -name '*.pyo' -exec rm -f {} +")
    _run(c, "find . -name '*~' -exec rm -f {} +")
    _run(c, "find . -name '__pycache__' -exec rm -fr {} +")


@task()
def clean_tests(c):
    # type: (Context) -> None
    """Clean up files from testing."""
    _run(c, "rm -fr .pytest_cache")


@task(pre=[clean_build, clean_python, clean_tests])
def clean(c):
    # type: (Context) -> None
    """Run all clean sub-tasks."""


@task()
def install_hooks(c):
    # type: (Context) -> None
    """Install pre-commit hooks."""
    _run(c, "poetry run pre-commit install")


@task()
def hooks(c):
    # type: (Context) -> None
    """Run pre-commit hooks."""
    _run(c, "poetry run pre-commit run --all-files")


@task(name="format", help={"check": "Checks if source is formatted without applying changes"})
def format_(c, check=False):
    # type: (Context, bool) -> None
    """Format code."""
    isort_options = ["--check-only", "--diff"] if check else []
    _run(c, f"poetry run isort {' '.join(isort_options)} {PYTHON_TARGETS_STR}")
    black_options = ["--diff", "--check"] if check else ["--quiet"]
    _run(c, f"poetry run black {' '.join(black_options)} {PYTHON_TARGETS_STR}")


@task()
def flake8(c):
    # type: (Context) -> None
    """Run flake8."""
    _run(c, f"poetry run flakeheaven lint {PYTHON_TARGETS_STR}")


@task()
def perflint(c):
    # type: (Context) -> None
    """Run perflint."""
    _run(c, f"poetry run perflint {PYTHON_TARGETS_STR} --disable={PERFLINT_WARNINGS_STR} --ignore={TEST_DIR}")


@task()
def safety(c):
    # type: (Context) -> None
    """Run safety."""
    _run(
        c,
        "poetry export --with dev --format=requirements.txt --without-hashes | "
        "poetry run safety check --stdin --full-report",
    )


@task(pre=[flake8, safety, perflint, call(format_, check=True)])
def lint(c):
    # type: (Context) -> None
    """Run all linting."""


@task()
def mypy(c):
    # type: (Context) -> None
    """Run mypy."""
    _run(c, f"poetry run mypy {PYTHON_TARGETS_STR}")


@task()
def tests(c):
    # type: (Context) -> None
    """Run tests."""
    _run(c, f"poetry run pytest {TEST_DIR} {SOURCE_DIR}")


@task()
def interrogate(c):
    # type: (Context) -> None
    """Interrogate a codebase for docstring coverage."""
    _run(c, f"poetry run interrogate -v {PYTHON_TARGETS_STR}")


@task()
def version(c):
    # type: (Context) -> None
    """Bump version."""
    _run(c, "poetry run cz bump --dry-run")
