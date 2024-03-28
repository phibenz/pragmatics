class ScoreKeeper:
    def __init__(self, model_names: list, templates: list, repetitions: int):
        # get the template_ids
        self.template_ids = []
        for template in templates:
            template_id = str(template).split("/")[-1].split(".")[0]
            self.template_ids.append(template_id)
        self.model_names = model_names
        self.repetitions = repetitions

        self.score = {}
        for model_name in self.model_names:
            self.score[model_name] = {}
            for template_id in self.template_ids:
                self.score[model_name][template_id] = [False] * self.repetitions

    def set_score(
        self, model_name: str, template_id: str, repetition_number: int, value: bool
    ):
        self.score[model_name][template_id][repetition_number - 1] = value

    def accuracy(self):
        accuracy = {}
        for model_name in self.model_names:
            accuracy[model_name] = {}
            model_total_all = 0
            model_correct_all = 0

            model_total_any = 0
            model_correct_any = 0
            for template_id in self.template_ids:
                model_total_all += self.repetitions
                model_correct_all += sum(self.score[model_name][template_id])

                model_total_any += 1
                model_correct_any += (
                    1 if any(self.score[model_name][template_id]) else 0
                )
            # Accuracy over all the repetitions
            accuracy[model_name]["all"] = model_correct_all / model_total_all
            # Accuracy where at least one repetition is correct
            accuracy[model_name]["any"] = model_correct_any / model_total_any
        return accuracy
