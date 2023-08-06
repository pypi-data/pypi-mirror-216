import dataclasses
import logging
import time
from typing import Dict, List, Optional, Tuple
from azure.identity import DefaultAzureCredential
import requests
import tenacity
import torch.utils.data
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Create a model that generates text using Azure OpenAI completion API.

    This task calls Azure OpenAI completion API.
    https://docs.microsoft.com/en-us/azure/cognitive-services/openai-gpt/quickstart

    The model interface is:
    - Input: (str, [])
    - Output: str

    Config:
        endpoint (str): Azure endpoint
        deployment_name (str): Azure deployment name
        api_key (str): Azure API key
        temperature (float): Temperature parameter for text generation
        top_p (float): Top p parameter for text generation
        max_tokens (int): Maximum number of tokens to generate
        requests_interval (int): Interval between requests in seconds
    """
    VERSION = '0.2.0'

    @dataclasses.dataclass
    class Config:
        endpoint: str
        deployment_name: str
        api_key: Optional[str] = None
        temperature: float = 0.0
        top_p: float = 1.0
        max_tokens: int = 100
        requests_interval: int = 0
        num_responses: int = 1
        response_delimiter: str = '<|delimiter|>'

    @dataclasses.dataclass
    class Outputs:
        model: torch.nn.Module

    def execute(self, inputs):
        self._check_configs()
        model = OpenAITextCompletionModel(self.config.endpoint, self.config.deployment_name, self.config.api_key, self.config.temperature, self.config.top_p,
                                          self.config.max_tokens, self.config.requests_interval, self.config.num_responses, self.config.response_delimiter)

        return self.Outputs(model)

    def dry_run(self, inputs):
        self._check_configs()
        return self.Outputs(FakeModel())

    def _check_configs(self):
        if not self.config.endpoint:
            raise ValueError("Endpoint is not set")

        if not self.config.endpoint.startswith('https://'):
            raise ValueError("Endpoint must start with https://")

        if not self.config.deployment_name:
            raise ValueError("Deployment name is not set")


def _should_retry(exception):
    if isinstance(exception, requests.exceptions.RequestException):
        response = getattr(exception, 'response', None)
        if response and (response.status_code == 429 or response.status_code >= 500):
            return True
        if isinstance(exception, requests.exceptions.ConnectionError):
            return True
    return False


class SerializableCredential:
    def __init__(self):
        self._credential = DefaultAzureCredential()

    def get_token(self, *args, **kwargs):
        return self._credential.get_token(*args, **kwargs)

    def __getstate__(self):
        return {}

    def __setstate__(self, _):
        self.__init__()


class OpenAIClientBase:
    def __init__(self, endpoint, deployment_name, api_key, temperature, max_tokens, num_responses, delimiter):
        self._url = f'{endpoint}/openai/deployments/{deployment_name}' + self.get_url()
        self._api_key = api_key
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._num_responses = num_responses
        self._delimiter = delimiter
        self._credential = None if self._api_key else SerializableCredential()
        self._auth_token_cache = None

    def get_url(self) -> str:
        raise NotImplementedError

    def make_request_body(self, inputs) -> Dict:
        raise NotImplementedError

    def parse_response(self, response_json) -> Tuple[str, int]:
        raise NotImplementedError

    @tenacity.retry(wait=tenacity.wait_exponential(multiplier=2, min=30, max=128), stop=tenacity.stop_after_attempt(20), retry=tenacity.retry_if_exception(_should_retry))
    def post(self, inputs):
        response = None
        response_json = None
        request_body = self.make_request_body(inputs)
        request_body['temperature'] = self._temperature
        request_body['max_tokens'] = self._max_tokens
        request_body['n'] = self._num_responses
        try:
            # Use a long timeout because the API can take a long time to respond
            headers = {'api-key': self._api_key} if self._api_key else {'Authorization': f'Bearer {self._get_auth_token()}'}
            response = requests.post(self._url, headers=headers, json=request_body, timeout=120)
            response.raise_for_status()
            returned_text, total_tokens = self.parse_response(response.json())
        except Exception as e:
            if response is not None:
                logger.error(f"Failed to POST to {self._url}: {response.status_code} {response.content} {repr(e)}")
            else:
                logger.exception(f"Failed to POST to {self._url}")

            if response_json:
                logger.error(f"Response JSON: {response_json}")
            raise

        return returned_text, total_tokens

    def _get_auth_token(self):
        if not self._auth_token_cache or time.time() > self._auth_token_cache.expires_on:
            self._auth_token_cache = self._credential.get_token('https://cognitiveservices.azure.com/.default')
        return self._auth_token_cache.token


class OpenAICompletionClient(OpenAIClientBase):
    def __init__(self, endpoint, deployment_name, api_key, temperature, max_tokens, num_responses, delimiter, top_p):
        super().__init__(endpoint, deployment_name, api_key, temperature, max_tokens, num_responses, delimiter)
        self._top_p = top_p

    def get_url(self):
        return '/completions?api-version=2023-03-15-preview'

    def make_request_body(self, inputs):
        assert isinstance(inputs, str)
        return {'prompt': inputs, 'top_p': self._top_p}

    def parse_response(self, response_body):
        texts = [t['text'].strip() for t in response_body['choices']]
        text = self._delimiter.join(texts)
        total_tokens = response_body['usage']['total_tokens']
        return text, total_tokens


class OpenAITextCompletionModel(torch.nn.Module):
    def __init__(self, endpoint, deployment_name, api_key, temperature, top_p, max_tokens, requests_inverval, num_responses, delimiter):
        super().__init__()
        self._client = OpenAICompletionClient(endpoint, deployment_name, api_key, temperature, max_tokens, num_responses, delimiter, top_p=top_p)
        self._requests_inverval = requests_inverval
        self._last_request_timestamp = None

    def forward(self, inputs: List[Tuple[str, List[torch.Tensor]]]) -> List[str]:
        assert isinstance(inputs, list)
        texts = []
        for prompt, prompt_images in inputs:
            if prompt_images:
                raise ValueError("This model does not support images")

            if self._last_request_timestamp:
                time.sleep(max(0, self._requests_inverval - (time.time() - self._last_request_timestamp)))

            try:
                result, _ = self._client.post(prompt)
                self._last_request_timestamp = time.time()
            except Exception:
                logger.exception(f"Failed to generate text for prompt: {repr(prompt)}")
                result = ''
            texts.append(result)
            logger.info(f"Generated text: {repr(result)}")
        return texts

    def __getstate__(self):
        return {'client': self._client, 'requests_inverval': self._requests_inverval}

    def __setstate__(self, state):
        super().__init__()
        self._client = state['client']
        self._requests_inverval = state['requests_inverval']
        self._last_request_timestamp = None


class FakeModel(torch.nn.Module):
    def forward(self, inputs):
        return [''] * len(inputs)
