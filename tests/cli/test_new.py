"""Tests for the 'new' command."""

from pathlib import Path

from click.testing import CliRunner

from nagraj.cli.main import cli


def test_new_project_creates_structure(
    cli_runner: CliRunner, temp_project_dir: Path
) -> None:
    """Test that 'new' command creates the expected project structure."""
    result = cli_runner.invoke(
        cli,
        [
            "new",
            "test_project",
            "-o",
            str(temp_project_dir),
            "-a",
            "Test Author",
            "--debug",
        ],
    )
    if result.exit_code != 0:
        print(f"Debug output: {result.output}")
    assert result.exit_code == 0

    project_dir = temp_project_dir / "test_project"
    assert project_dir.exists()

    # Check basic structure
    assert (project_dir / "src").is_dir()
    assert (project_dir / "src" / "shared").is_dir()
    assert (project_dir / "src" / "domains").is_dir()
    assert (project_dir / "pyproject.toml").is_file()
    assert (project_dir / ".nagraj.yaml").is_file()

    # Check base classes
    base_dir = project_dir / "src" / "shared" / "base"
    assert base_dir.is_dir()
    assert (base_dir / "base_entity.py").is_file()
    assert (base_dir / "base_value_object.py").is_file()
    assert (base_dir / "base_aggregate_root.py").is_file()
    assert (base_dir / "base_domain_event.py").is_file()


def test_new_project_with_description(
    cli_runner: CliRunner, temp_project_dir: Path
) -> None:
    """Test that 'new' command handles project description."""
    description = "Test project description"
    result = cli_runner.invoke(
        cli,
        [
            "new",
            "test_project",
            "-o",
            str(temp_project_dir),
            "-d",
            description,
            "-a",
            "Test Author",
            "--debug",
        ],
    )
    if result.exit_code != 0:
        print(f"Debug output: {result.output}")
    assert result.exit_code == 0

    # Check if description is in pyproject.toml
    pyproject = temp_project_dir / "test_project" / "pyproject.toml"
    content = pyproject.read_text()
    assert description in content


def test_new_project_fails_on_existing_directory(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'new' command fails if project directory exists."""
    result = cli_runner.invoke(
        cli,
        [
            "new",
            sample_project.name,
            "-o",
            str(sample_project.parent),
            "--debug",
        ],
    )
    assert result.exit_code != 0
    assert "already exists" in result.output.lower()
