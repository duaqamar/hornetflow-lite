import unittest
from backend.packet import build_packet, draft_statement


class PacketTests(unittest.TestCase):
    def test_refuses_unmatched_student(self):
        with self.assertRaises(ValueError):
            build_packet({'student_id':'missing', 'full_name':'Alex', 'term':'Fall 2026'}, 'Statement', True)

    def test_refuses_unreviewed_statement(self):
        with self.assertRaises(ValueError):
            build_packet({}, 'Statement', False)

    def test_export_is_labeled_and_uses_reviewed_statement(self):
        fields = dict(student_id='1001001', full_name='Alex Rivera', term='Fall 2026',
                      circumstances='Family duties', academic_impact='Missed lectures',
                      recovery_plan='Weekly tutoring', category='Other', documents_available=[])
        packet = build_packet(fields, 'My edited statement.', True)
        self.assertIn('My edited statement.', packet)
        self.assertIn('DEMO', packet)
        self.assertIn('Complete for demo review', packet)
        self.assertNotIn('approved', packet.lower())

    def test_draft_only_uses_provided_details(self):
        text = draft_statement(dict(circumstances='Family duties', academic_impact='Missed lectures', recovery_plan='Tutoring'))
        self.assertIn('Family duties', text)
        self.assertNotIn('diagnosis', text)
