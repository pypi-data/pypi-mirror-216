import dataclasses
import logging
import time
import typing
import requests
import tenacity
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Call Azure OpenAI Text Completion API.

    Config:
        endpoint (str): Azure endpoint. Starts with https://
        deployment_name (str): Azure deployment name
        api_key (str): Azure API key
        max_tokens (int): Maximum number of tokens to generate
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        prompts: typing.List[str]

    @dataclasses.dataclass
    class Config:
        endpoint: str
        deployment_name: str
        api_key: str
        max_tokens: int = 100
        requests_interval: int = 0

    @dataclasses.dataclass
    class Outputs:
        texts: typing.List[str]
        total_tokens: int

    def execute(self, inputs):
        self._check_config()
        client = Task.OpenAIClient(self.config.endpoint, self.config.deployment_name, self.config.api_key, self.config.max_tokens)
        texts = []
        total_tokens = 0
        for i, t in enumerate(inputs.prompts):
            start_time = time.time()

            try:
                result, num_tokens = client.post(t)
            except Exception:
                logger.exception(f"Failed to generate text {i}. Skipping.")
                result = ''
                num_tokens = 0

            texts.append(result)
            total_tokens += num_tokens
            logger.info(f"Generated text {i}: {repr(result)} (prompt={repr(t)}, {num_tokens} tokens, {time.time() - start_time} seconds)")
            time.sleep(self.config.requests_interval)

        logger.info(f"Generated {len(texts)} texts. ({total_tokens} tokens)")
        return self.Outputs(texts=texts, total_tokens=total_tokens)

    def dry_run(self, inputs):
        self._check_config()
        return self.Outputs(texts=['dry run'] * len(inputs.prompts), total_tokens=0)

    def _check_config(self):
        if not self.config.endpoint:
            raise ValueError("Endpoint is not set")

        if not self.config.endpoint.startswith('https://'):
            raise ValueError("Endpoint must start with https://")

        if not self.config.deployment_name:
            raise ValueError("Deployment name is not set")

        if not self.config.api_key:
            raise ValueError("API key is not set")

    class OpenAIClient:
        def __init__(self, endpoint, deployment_name, api_key, max_tokens, api_version='2023-03-15-preview'):
            self._url = f'{endpoint}/openai/deployments/{deployment_name}/completions?api-version={api_version}'
            self._api_key = api_key
            self._max_tokens = max_tokens

        @tenacity.retry(wait=tenacity.wait_exponential(multiplier=2, min=4, max=64), stop=tenacity.stop_after_attempt(10))
        def post(self, prompt):
            request_body = {'prompt': prompt, 'max_tokens': self._max_tokens}
            response = None
            response_json = None
            try:
                response = requests.post(self._url, headers={'api-key': self._api_key}, json=request_body)
                response.raise_for_status()
                response_json = response.json()
                returned_text = response_json['choices'][0]['text'].strip()
                total_tokens = response_json['usage']['total_tokens']
            except Exception:
                if response is not None:
                    logger.error(f"Failed to POST to {self._url}: {response.status_code} {response.content}")
                else:
                    logger.exception(f"Failed to POST to {self._url}")

                if response_json:
                    logger.error(f"Response JSON: {response_json}")
                raise

            return returned_text, total_tokens
