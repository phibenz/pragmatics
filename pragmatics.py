import sys
import json
from pathlib import Path

import logging.config

from src.config_engine import ConfigEngine
from src.template_runner import TemplateRunner
from src.template_test import TemplateTest

from src.argument_parser import parse_args
from src.utils import (
    generate_leaderboard,
    update_and_save_dict_to_json,
    calculate_accuracy,
)
from src.constants import PRAGMATICS_TEMPLATES_GITHUB_URL
from src.version import __version__

logger = logging.getLogger(__name__)


def print_banner():
    print(
        f"""
                                            __  _          
    ____  _________ _____ _____ ___  ____ _/ /_(_)_________
   / __ \/ ___/ __ `/ __ `/ __ `__ \/ __ `/ __/ / ___/ ___/
  / /_/ / /  / /_/ / /_/ / / / / / / /_/ / /_/ / /__(__  ) 
 / .___/_/   \__,_/\__, /_/ /_/ /_/\__,_/\__/_/\___/____/   v{__version__}
/_/               /____/                                   
                                        phibenz.github.io
    """
    )


def main():
    # Parse the arguments
    args = parse_args()
    # Set the log level based on args.log_level
    logging.basicConfig(stream=sys.stdout, level=args.log_level.upper())

    if not args.silent:
        print_banner()

    config_engine = ConfigEngine(
        template_path=args.pragmatics_templates_path,
    )

    # List the models
    if args.list_models:
        model_names = config_engine.get_all_models()
        print("Available models:")
        for model in model_names:
            print(f"  - {model}")
        sys.exit(0)

    # Check the models
    model_names = config_engine.get_selected_models(args.models)
    model_msg = "Selected models: {}".format(len(model_names))
    print("[+] " + model_msg)
    if len(model_names) == 0:
        logger.error("No models found")
        sys.exit(1)

    # Download/Update pragmatics-templates data
    if args.download_templates:
        # If not the latest version, or folder does not exist donwload
        if (
            not config_engine.check_template_version()
            or not config_engine.check_template_folder()
        ):
            config_engine.download_templates()
            return 0

    # Check the templates version;
    pragmatics_templates_remote_version = (
        config_engine.get_latest_remote_template_version()
    )
    pragmatics_templates_local_version = config_engine.get_local_template_version()
    if not config_engine.check_template_folder():
        logger.error(
            "pragmatics-templates folder not found. Donwload the latest version with --download-templates flag. Check out the templates at {}".format(
                PRAGMATICS_TEMPLATES_GITHUB_URL
            )
        )
        sys.exit(1)
    elif pragmatics_templates_remote_version != pragmatics_templates_local_version:
        template_vesion_str = (
            "Installed version of pragmatics-templates: {pragmatics_templates_local_version}. Latest version: {pragmatics_templates_remote_version}\n"
            "Download the latest version with --download-templates flag.\n",
            "Check out the templates at {}".format(PRAGMATICS_TEMPLATES_GITHUB_URL),
        )
        print(template_vesion_str)
        logger.info(template_vesion_str)
    else:
        template_vesion_str = "pragmatics-templates version {} up-to-date".format(
            pragmatics_templates_remote_version
        )
        print("[+] " + template_vesion_str)
        logger.info(template_vesion_str)

    # TODO: Check the API Keys to LLMs

    # Select the templates
    templates = config_engine.get_selected_templates(args.templates)
    template_msg = "Selected templates: {}".format(len(templates))
    print("[+] " + template_msg)
    logger.info(template_msg)
    if len(templates) == 0:
        logger.error("No templates found")
        sys.exit(1)

    # Repetitions
    repetitions_msg = "Repetitions: {}".format(args.repetitions)
    print("[+] " + repetitions_msg)
    logger.info(repetitions_msg)

    # Tofal jobs
    total_jobs = len(model_names) * len(templates) * args.repetitions
    total_jobs_msg = "Total jobs: {}".format(total_jobs)
    print("[+] " + total_jobs_msg)
    logger.info(total_jobs_msg)

    print()

    # TODO: Test template engine
    # test_template = TestTemplate()
    # test_template.test_template()

    # Initialize the template engine
    template_engine = TemplateRunner(
        templates=templates,
        model_names=model_names,
        repetitions=args.repetitions,
        workers=args.workers,
        timeout=args.timeout,
        output=args.output,
        skip_clean_up=args.skip_clean_up,
    )
    _score = template_engine.run()

    # Score
    if args.output:
        score_path = Path(args.output) / "score.json"
        _score = update_and_save_dict_to_json(_score, score_path)
    score = _score

    # Accuracy
    accuracy = calculate_accuracy(score)
    if args.output:
        accuracy_path = Path(args.output) / "accuracy.json"
        with open(accuracy_path, "w") as f:
            json.dump(accuracy, f, indent=4)

    # Leaderboard
    leaderboard_str = generate_leaderboard(accuracy)
    if not args.skip_leaderboard:
        print("\n" + leaderboard_str)

    if args.output:
        leaderboard_path = Path(args.output) / "leaderboard.txt"
        with open(leaderboard_path, "w") as f:
            f.write(leaderboard_str)


if __name__ == "__main__":
    main()
