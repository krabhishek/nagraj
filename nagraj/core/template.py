from pathlib import Path
from typing import Any, Dict, Union

from cookiecutter.main import cookiecutter
from jinja2 import Environment, FileSystemLoader, Template

from nagraj.config.settings import settings


class TemplateEngine:
    """Template engine abstraction that handles both Cookiecutter and Jinja2."""

    def __init__(self) -> None:
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(settings.template_path)),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render_template(
        self, template_path: Union[str, Path], context: Dict[str, Any]
    ) -> str:
        """Render a single template using Jinja2."""
        template: Template = self.jinja_env.get_template(str(template_path))
        return template.render(**context)

    def generate_project(
        self,
        template_name: str,
        output_dir: Union[str, Path],
        context: Dict[str, Any],
        no_input: bool = True,
    ) -> Path:
        """Generate a project structure using Cookiecutter."""
        template_path = settings.template_path / template_name

        # Extract the inner context if it's wrapped in a cookiecutter namespace
        extra_context = context.get("cookiecutter", context)

        result = cookiecutter(
            str(template_path),
            output_dir=str(output_dir),
            no_input=no_input,
            extra_context=extra_context,
        )
        return Path(result)

    def write_template(
        self,
        template_path: Union[str, Path],
        output_path: Union[str, Path],
        context: Dict[str, Any],
    ) -> None:
        """Render a template and write it to a file."""
        content = self.render_template(template_path, context)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)


# Global template engine instance
template_engine = TemplateEngine()
