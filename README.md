<div align="center">

<img src="./static/pragmatics-logo.png" alt="pragmaticslogo"/>

[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/projectdiscovery/pragmatics/issues)
[![Latest Release](https://img.shields.io/github/release/phibenz/pragmatics)](https://github.com/phibenz/pragmatics/releases)
![GitHub top language](https://img.shields.io/github/languages/top/phibenz/pragmatics)
![GitHub last commit](https://img.shields.io/github/last-commit/phibenz/pragmatics)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

<p class="align center">
<h4><code>pragmatics</code> is an open-source template engine for testing large language models. </h4>
</p>
</div>

---

Use `pragmatics` to query a language model based on a template and then evaluate the response. This is useful for testing the capabilities of language models in a variety of domains, including programming, security, and general knowledge. `pragmatics` implements various custom checks, which allow you to evaluate the quality of the response, including code compilation, code execution, and more.

Check out the [pragmatics-templates](https://github.com/phibenz/pragmatics-templates) repository containing templates for testing language models.

Please note, that this project is not intended for rigorous evaluation of model capabilities or for determining which model is more capable, knowledgeable, factual, biased, harmful, aligned, or helpful.

This project is highly inspired by [Nicholas Carlinis](https://nicholas.carlini.com/) Github repository [Yet Another Applied LLM Benchmark](https://github.com/carlini/yet-another-applied-llm-benchmark/tree/main) as well as [nuclei](https://github.com/projectdiscovery/nuclei). Most of the inital templates were adapted from his repository. More to come soon.


| :construction:  **Disclaimer**  :construction:  |
|---------------------------------|
| **This project is in active development**. Expect breaking changes with releases. |


```
$ python3 pragmatics.py -t code/python/ -m gpt-4-0125-preview claude-3-opus-20240229 gemini-1.0-pro mistral-large-latest -r 5 -o ./output/result --workers 4
                                            __  _
    ____  _________ _____ _____ ___  ____ _/ /_(_)_________
   / __ \/ ___/ __ `/ __ `/ __ `__ \/ __ `/ __/ / ___/ ___/
  / /_/ / /  / /_/ / /_/ / / / / / / /_/ / /_/ / /__(__  )
 / .___/_/   \__,_/\__, /_/ /_/ /_/\__,_/\__/_/\___/____/   v0.0.0
/_/               /____/
                                        phibenz.github.io

[+] Selected models: 4
[+] pragmatics-templates version 0.0.0 up-to-date
[+] Selected templates: 5

❌ [c-convert-sqrt-from-python][gemini-1.0-pro] (1/5)
❌ [c-weird-expression][gemini-1.0-pro] (1/5)
✅ [c-crc32][claude-3-opus-20240229] (1/5)
[...]
❌ [c-rref][mistral-large-latest] (5/5)
❌ [c-weird-expression][gpt-4-0125-preview] (5/5)
✅ [c-convert-dp-from-python][claude-3-opus-20240229] (5/5)

+-------------------------------------------------------+
|                 Pragmatics Leaderboard                |
+-------------------------------------------------------+
| Rank | Model                  | Acc (All) | Acc (Any) |
+------+------------------------+-----------+-----------+
|    1 | claude-3-opus-20240229 |    56.00% |    60.00% |
|    2 |   mistral-large-latest |    44.00% |    60.00% |
|    3 |     gpt-4-0125-preview |    44.00% |    60.00% |
|    4 |         gemini-1.0-pro |     8.00% |    40.00% |
+------+------------------------+-----------+-----------+
```

## Setup
### API Keys
Set your API keys in `./config/api-keys.yaml`:
```yaml
openai: "sk-xxx"
anthropic: "sk-ant-xxx"
mistralai: "xxx"
googleai: "AIxxx"
```
You can use [./config/api-keys.yaml.example](./config/api-keys.yaml.example) as a template. 
```bash 
cp ./config/api-keys.yaml.example ./config/api-keys.yaml
```

| :warning:  **WARNING**  :warning: |
|---------------------------------|
|**USAGE AT YOUR OWN RISK**. It is **HIGHLY** recommended to use docker, since `pragmatics` will blindly execute code provided by the language model. This includes (over)writing files, executing code, and more. If the model decides to provide malicious code, such as `rm -rf /` it could be executed on your machine. | 

### Docker
Make sure that docker is [installed](https://docs.docker.com/engine/install/) on your machine.
You can run the pragmatics docker image with the following command:
```shell
docker run -it --rm \
    -v $(pwd)/config:/pragmatics/config \
    -v $(pwd)/output:/pragmatics/output \
    phibenz/pragmatics:latest \
    -t code/python/python-hello-world.yaml -m gpt-3.5-turbo-0125 --output ./output
```

Build the docker image with:
```bash
docker build -t pragmatics .
```

### Local
If you are bold/insane enough, you can run `pragmatics` outside of docker. NOT RECOMMENDED! Make sure you have python 3.8 or higher installed on your machine. You can install the required dependencies with:
```bash
pip install -r requirements.txt
```

## Usage
```
Pragmatics: A benchmarking tool for language models

options:
  -h, --help                    show this help message and exit
  -t, --templates               List of template or template directory to run
  -m, --models                  Models to evaluate (specific model or vendor)
  -r, --repetitions             Number of repetitions
  --workers                     Number of workers
  --timeout                     Timeout for each job
  --silent                      Do not print the banner
  --log-level                   Log level (debug,info,warning,error,critical)
  --list-models                 List available models
  --skip-clean-up               Skip clean up
  --skip-leaderboard            Skip leaderboard
  -o, --output                  Path to the output folder to save the results
  --download-templates          Download the latest templates
  --pragmatics-templates-path   Overwrite path to the pragmatics-templates folder 
                                (default: ~/pragmatics-templates)
```
### Models
To see a list of available models use the `--list-models` flag, or have a look in the [config/models](./config/models) folder:
```
python3 pragmatics.py --list-models --silent
Available models:
  - open-mistral-7b
  - open-mixtral-8x7b
  - mistral-small-latest
  - mistral-medium-latest
  - mistral-large-latest
  - gpt-4-0125-preview
  - gpt-4-turbo-preview
  - gpt-4-1106-preview
  - gpt-4-0613
  - gpt-4-32k-0613
  - gpt-3.5-turbo-0125
  - gpt-3.5-turbo-1106
  - claude-3-haiku-20240307
  - claude-3-sonnet-20240229
  - claude-3-opus-20240229
  - gemini-1.0-pro
```

### Examples
With the following command, you can run the template [`python-hello-world.yaml`](https://github.com/phibenz/pragmatics-templates/blob/dev/code/python/python-hello-world.yaml) with the model `gpt-3.5-turbo-0125`. 
```bash
python3 pragmatics.py -t code/python/python-hello-world.yaml -m gpt-3.5-turbo-0125
```

Run all templates in the [`code/c/`](https://github.com/phibenz/pragmatics-templates/tree/dev/code/c) directory with the anthropic models, and save the results in the `./output/antrhropic-c` directory.
```bash
python3 pragmatics.py -t code/c/ -m anthropic -o ./output/anthropic-c
```

Use multiple workers to run the templates in parallel.
```bash
python3 pragmatics.py -t code/c/ -m gemini-1.0-pro -o ./output/multi-workers --workers 4
```

## Output
For each job, an emoji indicates the status of the job.
```
✅ - The job was successfully evaluated
❌ - The job was not successfully evaluated
💀 - The job failed, likely a code or model issue. You should investigate.
⏳ - The job timed out (see --timeout flag)
```
Afterwards the template-id, the model and the repetition number are indicated.
```
⏳ [c-crc32][gemini-1.0-pro] (2/5)
❌ [c-rref][gpt-4-0125-preview] (3/5)
✅ [c-crc32][claude-3-opus-20240229] (3/5)
```
If you specify the `--output` flag, the results are saved in the specified directory. Please note, if you specify an exisiting folder, the results are overwritten and updated. Several files are created:

`score.json`: The results are saved in the following format:
```json
{
    "model": {
        "template-id": [
            true, # These are the results of the evaluations x repetitions
            false,
            true,
            false,
            false
        ],
        [...]
    }
    [...]
}
```

`accuracy.json`: The accuracy of the models are saved in the following format:
```json
{
    "model": {
        "all": 0.6, # The accuracy of the model over all templates & repetitions
        "any": 0.6666666666666666 # The accuracy of the model, where at least one repetition per template is correct
    },
    [...]
}
```

`leaderboard.json`: The [leaderboard](./output/latest/leaderboard.txt), as shown at end of the run is stored in this file. 

Additionally, for each model, template, and repetition a json file is created, storing information about the job, the response and the evaluation.

For example here is the log for a model, that prints "hello world" and evaluates the output:
```json
{"type": "language_model", "name": "AnthropicModel", "input": [{"role": "user", "content": "Write a python program that prints the string \"hello world\". Print only the code."}], "output": "print(\"hello world\")", "success": true, "error": null, "args": {"model": "claude-3-opus-20240229", "api_key": "api-key-redacted"}}
{"type": "processor", "name": "ExtractCodeProcessor", "input": "print(\"hello world\")", "output": "print(\"hello world\")", "success": true, "error": null, "args": {}}
{"type": "processor", "name": "PythonRunProcessor", "input": "print(\"hello world\")", "output": "hello world", "success": true, "error": null, "args": {}}
{"type": "evaluator", "name": "WordEvaluator", "input": "hello world", "output": "True", "success": true, "error": null, "args": {"patterns": ["hello world"], "condition": "and"}}
{"type": "template_job:final_eval", "name": "TemplateJob", "input": [true], "output": true, "success": true, "error": null, "args": {"query_evaluators_condition": "and"}}
{"type": "template_job:clean_up", "name": "TemplateJob", "input": "/tmp/pragmatics/python-hello-world", "output": null, "success": true, "error": null, "args": {}}

```

## Templates
Have a look at the collection of already exisiting templates in the [pragmatics-templates](https://github.com/phibenz/pragmatics-templates) repository. The easiest way to get started is to copy one of the exising templates and modify it. 

For example, here is a [template](https://github.com/phibenz/pragmatics-templates/blob/dev/code/python/python-string-length.yaml), that queries the model to write a simple python function and then evaluates the output of the model, by running the function with input arguments and comparing the output to the expected output:

```yaml
id: python-string-length

info:
  name: Python String Length Function 
  author: phibenz
  difficulty: easy
  description: Write a python function that returns the input string and appends its length.
  tags:
    - code
    - python

query:
  - name: question
    text: |-
      Write a python function that returns the input string and appends its length. 
      Call the function "print_length".
      For example if you input "hello world", the function returns "hello world 11".
      Print only the code.

    processors:
      - type: extract-code
      - type: python-compile
        fn-name: print_length

    evaluators:
      - type: python-fn
        fn-name: print_length
        args: 
          - "hello world"
        output: "hello world 11"

      - type: python-fn
        fn-name: print_length
        args: 
          - "test"
        output: "test 4"
```

## Contributing
This project is far from finished. Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.
