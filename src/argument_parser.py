import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Pragmatics: A benchmarking tool for language models"
    )
    parser.add_argument(
        "-t",
        "--templates",
        type=str,
        nargs="+",
        default=[],
        help="List of template or template directory to run",
    )
    parser.add_argument(
        "-m",
        "--models",
        type=str,
        nargs="+",
        default=[],
        help="Models to evaluate (specific model or vendor)",
    )
    parser.add_argument(
        "-r",
        "--repetitions",
        type=int,
        default=1,
        help="Number of repetitions",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of workers",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Timeout for each job",
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Do not print the banner",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="warning",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Log level ()",
    )
    parser.add_argument(
        "--skip-clean-up",
        action="store_true",
        help="Skip clean up",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available models",
    )
    # Display
    parser.add_argument(
        "--skip-leaderboard",
        action="store_true",
        help="Skip leaderboard display",
    )

    # TODO
    # Template Filtering
    # parser.add_argument(
    #     "--tags",
    #     type=str,
    #     nargs="+",
    #     default=[],
    #     help="templates to run based on tags"
    # )
    # Output
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Path to the output folder to save the results",
    )
    # TODO
    # Configurations
    # parser.add_argument(
    #     "-c",
    #     "--config",
    #     type=str,
    #     help="Path to the configuration file",
    # )
    # Download templates
    parser.add_argument(
        "--download-templates",
        action="store_true",
        help="Download the latest templates",
    )
    parser.add_argument(
        "--pragmatics-templates-path",
        type=str,
        help="Overwrite path to the pragmatics-templates folder (default: ~/.config/pragmatics-templates)",
    )

    args = parser.parse_args()
    # Deduplicate
    args.models = list(set(args.models))
    args.templates = list(set(args.templates))
    # args.tags = list(set(args.tags))
    return args
