import io
import zipfile
import requests


import logging
from pathlib import Path

from src.utils import load_model_config
from src.constants import (
    CONFIG_PATH,
    PRAGMATICS_TEMPLATES_PATH,
    PRAGMATICS_TEMPLATES_LATEST_VERSION,
    PRAGMATICS_TEMPLATES_LATEST_RELEASE_URL,
)


logger = logging.getLogger(__name__)


class ConfigEngine:
    def __init__(
        self,
        template_path: str,
    ) -> None:

        if template_path is not None:
            self.template_path = Path(template_path)
        else:
            self.template_path = Path(PRAGMATICS_TEMPLATES_PATH)

        self.config_path = Path(CONFIG_PATH)
        assert self.config_path.is_dir(), f"Config path {self.config_path} not found"

        self.model_config = load_model_config(self.config_path)

        self.pragmatics_templates_latest_release_url = (
            PRAGMATICS_TEMPLATES_LATEST_RELEASE_URL
        )

    def check_template_folder(self):
        return Path(self.template_path).is_dir()

    def get_latest_remote_template_version(self):
        # response = requests.get(self.pragmatics_templates_latest_release_url)
        # response.raise_for_status()
        # latest_release = response.json()
        # return latest_release["tag_name"]
        return PRAGMATICS_TEMPLATES_LATEST_VERSION

    def get_local_template_version(self):
        if not self.template_path.is_dir():
            return "x.x.x"

        version_path = Path(self.template_path) / "version.py"
        if not version_path.is_file():
            return "0.0.0"

        with open(self.template_path / "version.py", "r") as f:
            version = f.read().strip().split("=")[-1].strip().strip('"')
        return version

    def check_template_version(self):
        local_version = self.get_local_template_version()
        remote_version = self.get_latest_remote_template_version()
        return local_version == remote_version

    def download_templates(self):
        remote_version = self.get_latest_remote_template_version()
        download_str = f"Downloading pragmatics-templates v{remote_version} to: {self.template_path}"

        logger.info(download_str)
        print(download_str)

        response = requests.get(self.pragmatics_templates_latest_release_url)
        response.raise_for_status()

        # Download the zipball
        zip_url = response.json()["zipball_url"]
        zip_response = requests.get(zip_url)
        zip_response.raise_for_status()

        # Extract the zipball
        z = zipfile.ZipFile(io.BytesIO(zip_response.content))
        for zf in z.filelist:
            # remove the trailing directory: "phibenz-pragmatics-templates-<hash>/"
            zf.filename = "/".join(zf.filename.split("/", 1)[1:])
            if zf.filename == "":
                continue
            z.extract(zf, self.template_path)

    def get_all_models(self):
        all_models = []
        for vendor in self.model_config:
            all_models += self.model_config[vendor]["models"]
        return all_models

    def get_all_vendors(self):
        return list(self.model_config.keys())

    def get_selected_models(self, model_names: list = []):
        if len(model_names) == 0:
            return self.get_all_models()
        selected_models = []
        for model_name in model_names:
            if model_name in self.get_all_vendors():
                selected_models += self.model_config[model_name]["models"]
            elif model_name in self.get_all_models():
                selected_models.append(model_name)
            else:
                raise ValueError(f"Model {model_name} not supported")
        return selected_models

    def get_all_templates(self):
        templates = self.template_path.glob("**/*.yaml")
        templates = [str(t) for t in templates]
        return templates

    def get_selected_templates(self, templates: list = []):
        all_templates = self.get_all_templates()
        all_templates_relative = [
            str(Path(t).relative_to(self.template_path)) for t in all_templates
        ]

        if len(templates) == 0:
            return all_templates
        selected_templates = []
        for template in templates:
            template = Path(template)
            # Consider absolute path variations
            if template.is_absolute():
                # Check if the full path includes the template path
                if self.template_path in Path(template).parents:
                    selected_templates.append(str(template))
                # Template from a different path, which is a folder
                elif template.is_dir():
                    folder_templates = template.glob("**/*.yaml")
                    folder_templates = [str(t) for t in folder_templates]
                    selected_templates += folder_templates
                # Template from a different path
                else:
                    if Path(template).suffix == ".yaml":
                        selected_templates.append(template)
                    else:
                        raise ValueError(f"Template {str(template)} not yaml file")
            # Relative path and template exists
            elif not template.is_absolute():
                if (self.template_path / template).is_dir():
                    subfolder_templates = (self.template_path / template).glob(
                        "**/*.yaml"
                    )
                    subfolder_templates = [str(t) for t in subfolder_templates]
                    selected_templates += subfolder_templates
                elif str(template) in all_templates_relative:
                    selected_templates.append(str(self.template_path / template))
                else:
                    raise ValueError(f"Template {str(template)} not found")
            else:
                raise ValueError(f"Template {str(template)} not found")
        return list(set(selected_templates))
