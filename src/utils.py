import yaml
import json
from pathlib import Path


def load_yaml_file(path):
    with open(path, "r") as f:
        yaml_file = yaml.safe_load(f)
    return yaml_file


def conditional_evaluation(condition, matches):
    if condition == "and":
        return all(matches)
    elif condition == "nand":
        return not all(matches)
    elif condition == "or":
        return any(matches)
    elif condition == "nor":
        return not any(matches)
    else:
        raise ValueError(f"Condition {condition} not supported")


def load_model_config(config_path=None):
    if not config_path:
        config_path = Path(__file__).parent.parent / "config"
    api_keys_config = config_path / "api-keys.yaml"
    model_config = {}
    assert api_keys_config.is_file(), "API Keys file not found"
    api_keys_yaml = load_yaml_file(api_keys_config)

    model_config_files = (config_path / "models").glob("*.yaml")
    for model_config_file in model_config_files:
        model = load_yaml_file(model_config_file)
        vendor = model["vendor"]
        models = [m["name"] for m in model["models"]]
        if vendor not in model_config.keys():
            model_config[vendor] = {}
            model_config[vendor]["models"] = models

    for vendor in model_config:
        assert vendor in api_keys_yaml, "API Key for {} not found".format(vendor)
        model_config[vendor]["api_key"] = api_keys_yaml[vendor]
    return model_config


def get_model(model_name):
    model_config = load_model_config()
    # Select the model based on the model name
    for vendor in model_config:
        if model_name in model_config[vendor]["models"]:
            if vendor == "openai":
                from src.models.openai import OpenAIModel

                model = OpenAIModel(model_name, model_config[vendor]["api_key"])
            elif vendor == "anthropic":
                from src.models.anthropic import AnthropicModel

                model = AnthropicModel(model_name, model_config[vendor]["api_key"])
            elif vendor == "mistralai":
                from src.models.mistralai import MistralAIModel

                model = MistralAIModel(model_name, model_config[vendor]["api_key"])
            elif vendor == "googleai":
                from src.models.googleai import GoogleAIModel

                model = GoogleAIModel(model_name, model_config[vendor]["api_key"])
            else:
                raise ValueError(f"Vendor {vendor} not supported")
    return model


def update_and_save_dict_to_json(
    new_dict: dict,
    save_path: str,
):
    if Path(save_path).is_file():
        with open(save_path, "r") as f:
            loaded_dict = json.load(f)

        # Go through the keys of the new dict
        for model_key in new_dict.keys():
            # Check if the key is in the new dict
            if model_key in loaded_dict.keys():
                for template_key in new_dict[model_key].keys():
                    # Update the value of the key in the loaded dict
                    loaded_dict[model_key][template_key] = new_dict[model_key][
                        template_key
                    ]
            else:
                # If the key is not in the new dict, add the key and value to the new dict
                loaded_dict[model_key] = new_dict[model_key]
    else:
        loaded_dict = new_dict

    with open(save_path, "w") as f:
        json.dump(loaded_dict, f, indent=4)

    return loaded_dict


def calculate_accuracy(score):
    model_names = score.keys()
    accuracy = {}
    for model_name in model_names:
        accuracy[model_name] = {}
        model_total_all = 0
        model_correct_all = 0

        model_total_any = 0
        model_correct_any = 0

        for template_id in score[model_name].keys():
            repetitions = len(score[model_name][template_id])
            model_total_all += repetitions
            model_correct_all += sum(score[model_name][template_id])

            model_total_any += 1
            model_correct_any += 1 if any(score[model_name][template_id]) else 0
        # Accuracy over all the repetitions
        accuracy[model_name]["all"] = model_correct_all / model_total_all
        # Accuracy where at least one repetition is correct
        accuracy[model_name]["any"] = model_correct_any / model_total_any
    return accuracy


def generate_leaderboard(accuracy):
    accuracy = sorted(accuracy.items(), key=lambda x: x[1]["all"], reverse=True)
    max_name_length = max(len(acc[0]) for acc in accuracy)

    leaderboard_str = ""
    leaderboard_str += "+---------------------------------------------------------+\n"
    leaderboard_str += "|                  Pragmatics Leaderboard                 |\n"
    leaderboard_str += "+---------------------------------------------------------+\n"
    leaderboard_str += (
        "| Rank | Model"
        + " " * (max_name_length - len("Model"))
        + " | Acc (All) | Acc (Any) |\n"
    )
    leaderboard_str += (
        "+------+-" + "-" * max_name_length + "-+-----------+-----------+\n"
    )

    for i, (model_name, accs) in enumerate(accuracy, start=1):
        acc_all = accs["all"] * 100
        acc_any = accs["any"] * 100
        leaderboard_str += f"| {i:4d} | {model_name:>{max_name_length}} | {acc_all:8.2f}% | {acc_any:8.2f}% |\n"
    leaderboard_str += (
        "+------+-" + "-" * max_name_length + "-+-----------+-----------+\n"
    )
    return leaderboard_str
