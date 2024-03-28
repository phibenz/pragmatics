from pathlib import Path

PRAGMATICS_TEMPLATES_LATEST_VERSION = "0.0.1"
PRAGMATICS_TEMPLATES_PATH = str(Path.home() / ".config" / "pragmatics-templates")
PRAGMATICS_TEMPLATES_GITHUB_URL = "https://github.com/phibenz/pragmatics-templates"
PRAGMATICS_TEMPLATES_LATEST_RELEASE_URL = (
    "https://api.github.com/repos/phibenz/pragmatics-templates/releases/latest"
)
CONFIG_PATH = str(Path(__file__).parent.parent.joinpath("config"))
