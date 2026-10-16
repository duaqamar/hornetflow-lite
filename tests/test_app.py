"""Exercise the actual Streamlit workflow, including stale-data resets."""
import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest


class AppFlowTests(unittest.TestCase):
    def test_review_download_and_identity_reset(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py'), default_timeout=40).run()
        self.assertEqual(len(app.exception), 0)
        next(b for b in app.button if b.label == 'Load fictional demo student').click().run()
        self.assertEqual(app.text_input(key='student_id').value, '1001001')
        next(b for b in app.button if b.label == 'Check my appeal packet').click().run()
        self.assertTrue(any('needs' in x.value for x in app.warning))
        app.checkbox(key='supporting').check().run()
        self.assertNotIn('validation', app.session_state)
        next(b for b in app.button if b.label == 'Check my appeal packet').click().run()
        self.assertTrue(any('requirements are present' in x.value for x in app.success))
        next(b for b in app.button if b.label == 'Create my statement draft').click().run()
        self.assertIn('statement', app.session_state)
        app.checkbox(key='reviewed').check().run()
        self.assertTrue(app.session_state['reviewed'])
        app.text_area(key='statement').set_value('My edited statement.').run()
        self.assertFalse(app.session_state['reviewed'])
        app.text_input(key='student_id').set_value('missing').run()
        self.assertNotIn('statement', app.session_state)
        self.assertNotIn('validation', app.session_state)
        self.assertEqual(app.session_state['conversation'], [])
        self.assertEqual(len(app.exception), 0)
