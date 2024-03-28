import json
import pebble
import logging

# from concurrent.futures import TimeoutError
from concurrent.futures._base import TimeoutError

from src.score_keeper import ScoreKeeper
from src.template_job import TemplateJob

logger = logging.getLogger(__name__)


class TemplateRunner:
    def __init__(
        self,
        templates: list,
        model_names: list,
        repetitions: int,
        workers: int,
        timeout: int = 120,
        output: str = None,
        skip_clean_up: bool = False,
    ):
        self.templates = templates
        self.model_names = model_names
        self.repetitions = repetitions
        self.workers = workers
        self.timeout = timeout
        self.output = output
        self.skip_clean_up = skip_clean_up

        self.score_keeper = ScoreKeeper(
            model_names=model_names, templates=templates, repetitions=repetitions
        )
        # Threading
        self.job_dicts_blocks = []

    def prepare_job_args(self):
        for rep_num in range(1, self.repetitions + 1):
            for model_idx, _ in enumerate(self.model_names):
                job_dicts = []
                for tmp_idx, template_path in enumerate(self.templates):
                    # Try to keep model diversity in the job block high
                    model_name = self.model_names[
                        (model_idx + tmp_idx) % len(self.model_names)
                    ]
                    job_dict = {
                        "template_path": template_path,
                        "model_name": model_name,
                        "repetition_number": rep_num,
                    }
                    job_dicts.append(job_dict)
                self.job_dicts_blocks.append(job_dicts)

    def run_job(self, job_dict):
        # Construct the job
        job = TemplateJob(
            template_path=job_dict["template_path"],
            model_name=job_dict["model_name"],
            repetition_number=job_dict["repetition_number"],
            skip_clean_up=self.skip_clean_up,
            timeout=self.timeout,
            output=self.output,
        )

        result, success = job.run()

        job_dict["result"] = result
        job_dict["success"] = success
        job_dict["job_info"] = job.info()
        job_dict["template_id"] = job.template["id"]
        job_dict["output_path"] = job.output_path
        return job_dict

    def task_done(self, future):
        try:
            job_dict = future.result()
            job_dict["is_timeout"] = False
        except TimeoutError:
            job_dict = future.job_dict
            job_dict["is_timeout"] = True
            job_dict["result"] = False
            job_dict["success"] = False
            # Approximate the template id
            job_dict["template_id"] = (
                job_dict["template_path"].split("/")[-1].split(".")[0]
            )

        # Skip writing the score if the job timed out
        if not job_dict["is_timeout"]:
            # Storing results
            self.score_keeper.set_score(
                model_name=job_dict["model_name"],
                template_id=job_dict["template_id"],
                repetition_number=job_dict["repetition_number"],
                value=job_dict["result"],
            )
            # Writing output results
            if self.output:
                with open(job_dict["output_path"], "w") as f:
                    for info in job_dict["job_info"]:
                        info_json = json.dumps(info)
                        f.write(info_json + "\n")
        # Displaying results
        if job_dict["is_timeout"]:
            display_result = "⏳"
        elif not job_dict["success"]:
            display_result = "💀"
        elif job_dict["result"]:
            display_result = "✅"
        else:
            display_result = "❌"

        print(
            "{} [{}][{}] ({}/{})".format(
                display_result,
                job_dict["template_id"],
                job_dict["model_name"],
                job_dict["repetition_number"],
                self.repetitions,
            )
        )

    def run(self):
        self.prepare_job_args()
        for job_dicts_block in self.job_dicts_blocks:
            worker_jobs = []
            pool = pebble.ProcessPool(max_workers=self.workers)
            with pool:
                for job_dict in job_dicts_block:
                    # execute the task
                    future = pool.schedule(
                        self.run_job, args=(job_dict,), timeout=self.timeout
                    )
                    future.job_dict = job_dict
                    future.add_done_callback(self.task_done)
                    worker_jobs.append(future)
                for future in worker_jobs:
                    try:
                        future.result()
                    except TimeoutError as e:
                        pass
        # Return the score
        return self.score_keeper.score
