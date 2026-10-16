"""Optional Bedrock Agent function action-group adapter (not deployed)."""
import json
from backend.validation import check_appeal, lookup_student


def lambda_handler(event, context):
    tools = {'lookup_student': lookup_student, 'check_appeal': check_appeal}
    name = event.get('function', '')
    arguments = {item['name']: item['value'] for item in event.get('parameters', [])}
    try:
        if isinstance(arguments.get('documents_available'), str):
            arguments['documents_available'] = json.loads(arguments['documents_available'])
        result = tools[name](**arguments)
        body = {'TEXT': {'body': json.dumps(result)}}
        function_response = {'responseBody': body}
    except (KeyError, TypeError, ValueError):
        function_response = {'responseState': 'REPROMPT', 'responseBody': {
            'TEXT': {'body': 'Invalid function or arguments. Ask for the missing information.'}}}
    return {'messageVersion': '1.0', 'response': {
        'actionGroup': event['actionGroup'], 'function': name,
        'functionResponse': function_response}}
