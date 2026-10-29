from pathlib import Path


class TemplateEngine:
    def available_templates(self) -> list[dict]:
        return [{"name": "python-fastapi", "version": "1.0.0", "description": "Standard Python API service"}]

    def render(self, template_name: str, variables: dict) -> dict:
        if template_name != "python-fastapi":
            raise ValueError("unknown template")
        required = {"service_name", "owner", "image"}
        missing = required - variables.keys()
        if missing:
            raise ValueError(f"missing template variables: {', '.join(sorted(missing))}")
        template_dir = Path(__file__).resolve().parents[1] / "templates" / template_name
        if not template_dir.exists():
            raise ValueError("template directory not found")
        return {"template": template_name, "directory": str(template_dir), "variables": variables}
