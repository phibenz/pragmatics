import shutil
import logging
from pathlib import Path
from multiprocessing import Process, Queue

from src.utils import load_yaml_file, get_model
from src.processor_engine import ProcessorEngine
from src.evaluation_engine import EvaluationEngine


logger = logging.getLogger(__name__)


class TemplateJob:
    def __init__(
        self,
        template_path: str,
        model_name: str,
        repetition_number: int,
        skip_clean_up: bool = False,
        timeout: int = 120,
        output: str = None,
    ):
        # Initialize the template job
        self.storage = {}
        self.template_path = template_path
        self.template = None
        self.model = get_model(model_name)
        self.repetition_number = repetition_number
        self.skip_clean_up = skip_clean_up
        self.timeout = timeout

        self._load_template()
        self.job_info = []

        if output:
            self._get_output_path(
                base_path=output,
                model_name=self.model.model,
                template_id=self.template["id"],
                rep_num=repetition_number,
            )
            # Create the output path
            Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)
        else:
            self.output_path = None

        # Query
        assert "query" in self.template, "No queries found in the template"

        self.query_results = []
        if "query-evaluators-condition" in self.template:
            self.query_evaluators_condition = self.template[
                "query-evaluators-condition"
            ]
        else:
            self.query_evaluators_condition = "and"

        # For job info
        self.module_type = "template_job"
        self.module_name = str(self.__class__.__name__)

    def _get_output_path(
        self, base_path: str, model_name: str, template_id: str, rep_num: int
    ) -> str:
        filename = str(rep_num) + ".json"
        output_path = Path(base_path) / model_name / template_id / filename
        self.output_path = str(output_path)

    def _load_template(self):
        self.template = load_yaml_file(self.template_path)

    def info(self):
        return self.job_info

    def run(self):
        self.messages = []
        error_base = f"template_path: {self.template_path}, model: {self.model.model}, repetition: {self.repetition_number}, "

        if "setup" in self.template:
            for setup_args in self.template["setup"]:
                try:
                    setup_engine = ProcessorEngine([setup_args])
                    setup_engine.set_module_type("setup")
                    code = None
                    if "code" in setup_args:
                        code = setup_args["code"]
                    answer, success = setup_engine(code)
                    setup_info = setup_engine.info()
                    self.job_info.extend(setup_info)
                except Exception as e:
                    error = (
                        error_base
                        + f"module: {self.setup_engine.__class__}, Error in setup: {e}"
                    )
                    logger.error(error)
                    return False, False

        # Global system prompt
        if "system" in self.template:
            self.model.add_system_prompt(self.template["system"])

        for q in self.template["query"]:
            # TODO: Handle {{ANSWER}} processing, ref. test_temp/query_engine.py; pre-processor?
            answer, success = self.model.process_query(q)
            model_info = self.model.info()
            logger.debug(f"Model answered: {answer}")
            self.job_info.extend(model_info)
            if not success:
                return False, False

            if "processors" in q:
                logger.debug(f"Running processors: {q['processors']}")
                processor_engine = ProcessorEngine(q["processors"])
                # Process the answer
                answer, success = processor_engine(answer)
                processor_info = processor_engine.info()
                self.job_info.extend(processor_info)
                if not success:
                    # An error in the processor is likely due to a wrong answer, hence final_success=True
                    return False, True

            if "evaluators" in q:
                logger.debug(f"Running evaluators: {q['evaluators']}")
                if "evaluators-condition" in q:
                    evaluators_condition = q["evaluators-condition"]
                else:
                    evaluators_condition = "and"
                eval_engine = EvaluationEngine(q["evaluators"], evaluators_condition)
                # Evaluate the answer
                result, success = eval_engine(answer)
                self.query_results.append(result)
                eval_info = eval_engine.info()
                self.job_info.extend(eval_info)

        # Final evaluation
        if self.query_evaluators_condition == "and":
            final_result = all(self.query_results)
        elif self.query_evaluators_condition == "or":
            final_result = any(self.query_results)
        else:
            raise ValueError(
                f"Evaluators condition {self.query_evaluators_condition} not supported"
            )
        self.job_info.extend(
            [
                {
                    "type": self.module_type + ":final_eval",
                    "name": self.module_name,
                    "input": self.query_results,
                    "output": final_result,
                    "success": True,
                    "error": None,
                    "args": {
                        "query_evaluators_condition": self.query_evaluators_condition
                    },
                }
            ]
        )

        if not self.skip_clean_up:
            # Clean up checks if a project folder was created and deletes it
            project_path = Path("/tmp/pragmatics") / self.template["id"]
            if project_path.is_dir():
                shutil.rmtree(project_path)
            self.job_info.extend(
                [
                    {
                        "type": self.module_type + ":clean_up",
                        "name": self.module_name,
                        "input": str(project_path),
                        "output": None,
                        "success": True,
                        "error": None,
                        "args": {},
                    }
                ]
            )

        final_success = True
        return final_result, final_success
