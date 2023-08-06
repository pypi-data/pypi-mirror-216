import time
import unittest
import unittest.mock
import torch
from irisml.tasks.create_azure_openai_completion_model import Task


class TestCreateAzureOpenaiCompletionModel(unittest.TestCase):
    def test_simple(self):
        outputs = Task(Task.Config(endpoint='https://example.com/', deployment_name='example_deployment', api_key='example_key')).execute(Task.Inputs())
        self.assertIsInstance(outputs.model, torch.nn.Module)

        with unittest.mock.patch('requests.post') as mock_post:
            mock_post.return_value.json.return_value = {'choices': [{'text': 'test'}], 'usage': {'total_tokens': 10}}
            model_outputs = outputs.model([('test', [])])
            mock_post.assert_called_once()
            self.assertEqual(model_outputs, ['test'])

    def test_multiple_responses(self):
        outputs = Task(Task.Config(endpoint='https://example.com/', deployment_name='example_deployment', api_key='example_key', num_responses=3)).execute(Task.Inputs())
        self.assertIsInstance(outputs.model, torch.nn.Module)

        with unittest.mock.patch('requests.post') as mock_post:
            mock_post.return_value.json.return_value = {'choices': [{'text': 'test'}, {'text': 'test2'}, {'text': 'test3'}], 'usage': {'total_tokens': 10}}
            model_outputs = outputs.model([('test', [])])
            mock_post.assert_called_once()
            self.assertEqual(model_outputs, ['test<|delimiter|>test2<|delimiter|>test3'])

    def test_no_wait_at_first_request(self):
        outputs = Task(Task.Config(endpoint='https://example.com/', deployment_name='example_deployment', api_key='example_key', requests_interval=60)).execute(Task.Inputs())
        self.assertIsInstance(outputs.model, torch.nn.Module)

        with unittest.mock.patch('requests.post') as mock_post:
            mock_post.return_value.json.return_value = {'choices': [{'text': 'test'}], 'usage': {'total_tokens': 10}}
            start_time = time.time()
            outputs.model([('test <|image|>', [])])
            self.assertLess(time.time() - start_time, 1)

    def test_requests_interval(self):
        outputs = Task(Task.Config(endpoint='https://example.com/', deployment_name='example_deployment', api_key='example_key', requests_interval=1)).execute(Task.Inputs())
        self.assertIsInstance(outputs.model, torch.nn.Module)

        with unittest.mock.patch('requests.post') as mock_post:
            mock_post.return_value.json.return_value = {'choices': [{'text': 'test'}], 'usage': {'total_tokens': 10}}
            start_time = time.time()
            outputs.model([('test <|image|>', [])])
            self.assertLess(time.time() - start_time, 1)

            # The second request has to wait for 1 second
            start_time = time.time()
            outputs.model([('test <|image|>', [])])
            self.assertGreater(time.time() - start_time, 1)
