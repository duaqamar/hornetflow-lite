import unittest
from backend.validation import check_appeal, lookup_student


class ValidationTests(unittest.TestCase):
    def valid(self, **changes):
        values = dict(student_id='1001001', full_name='Alex Rivera', term='Fall 2026',
                      circumstances='Illness', academic_impact='Missed classes',
                      recovery_plan='Meet advisor weekly', category='Illness',
                      documents_available=['supporting_document'])
        return check_appeal(**(values | changes))

    def test_complete_appeal(self):
        self.assertTrue(self.valid()['complete'])

    def test_missing_document(self):
        result = self.valid(documents_available=[])
        self.assertFalse(result['complete'])
        self.assertIn('supporting_document', result['missing_documents'])

    def test_unknown_student_exposes_no_record(self):
        result = lookup_student('missing', 'Alex Rivera', 'Fall 2026')
        self.assertFalse(result['matched'])
        self.assertIsNone(result['student'])

    def test_mismatch_blocks_packet(self):
        for changes in ({'full_name': 'Wrong Name'}, {'term': 'Spring 2026'}):
            self.assertFalse(self.valid(**changes)['complete'])

    def test_missing_narrative(self):
        self.assertIn('recovery_plan', self.valid(recovery_plan='  ')['missing_fields'])

    def test_normalizes_name_and_term(self):
        self.assertTrue(self.valid(full_name=' alex rivera ', term=' fall 2026 ')['complete'])

    def test_unknown_category_rejected(self):
        self.assertFalse(self.valid(category='override')['complete'])

    def test_nonmedical_category_does_not_need_medical_document(self):
        self.assertTrue(self.valid(category='Other', documents_available=[])['complete'])
