import unittest
from backend.mcp_client import connect, unpack


class MCPIntegrationTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_stdio_handshake_discovery_and_tools(self):
        async with connect() as session:
            tools = await session.list_tools()
            self.assertEqual({t.name for t in tools.tools},
                             {'lookup_student', 'check_appeal', 'get_appeal_policy'})
            policy = unpack(await session.call_tool('get_appeal_policy', {}))
            self.assertTrue(policy['synthetic'])
            result = unpack(await session.call_tool('lookup_student', {
                'student_id':'1001001', 'full_name':'Alex Rivera', 'term':'Fall 2026'}))
            self.assertTrue(result['matched'])
            result = unpack(await session.call_tool('check_appeal', {
                'student_id':'1001001', 'full_name':'Alex Rivera', 'term':'Fall 2026',
                'circumstances':'Illness', 'academic_impact':'Missed lectures',
                'recovery_plan':'Weekly tutoring', 'category':'Illness', 'documents_available':[]}))
            self.assertFalse(result['complete'])
            self.assertEqual(result['missing_documents'], ['supporting_document'])
            resources = await session.list_resources()
            self.assertIn('hornetflow://policy', [str(r.uri) for r in resources.resources])
            invalid = await session.call_tool('lookup_student', {'student_id': '1001001'})
            self.assertTrue(invalid.isError)
