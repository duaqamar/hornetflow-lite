import unittest
from unittest.mock import patch
from backend.agent_client import chat, public_reply


class AgentTests(unittest.TestCase):
    def test_filters_model_planning_tags(self):
        self.assertEqual(public_reply('<thinking>private plan</thinking>\nHere are the requirements.'),
                         'Here are the requirements.')

    def test_bedrock_tool_request_executes_real_mcp_and_returns_result(self):
        class FakeBedrock:
            def converse(self, **kwargs):
                if len(kwargs['messages']) == 1:
                    return {'output': {'message': {'role': 'assistant', 'content': [
                        {'toolUse': {'toolUseId': 'policy-1', 'name': 'get_appeal_policy', 'input': {}}}]}}}
                tool_result = kwargs['messages'][-1]['content'][0]['toolResult']
                assert tool_result['content'][0]['json']['synthetic']
                return {'output': {'message': {'role': 'assistant', 'content': [
                    {'text': 'This is the synthetic demo policy.'}]}}}
        initial = [{'role': 'user', 'content': [{'text': 'What is the policy?'}]}]
        with patch('backend.agent_client.runtime', return_value=FakeBedrock()):
            result = chat(initial, {})
        self.assertEqual(result['tool_calls'], [{'name': 'get_appeal_policy', 'status': 'success'}])
        self.assertIn('synthetic', result['reply'])
        self.assertEqual(len(initial), 1, 'Input history must not mutate on a failed/retried turn')
