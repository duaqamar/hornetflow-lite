"""Deterministic demo rules shared by UI, MCP and Lambda."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = ('Illness', 'Family circumstances', 'Work or finances', 'Other')


def normalize(value: str) -> str:
    return ' '.join(value.split()).casefold()


def lookup_student(student_id: str, full_name: str, term: str) -> dict:
    """Match a synthetic record. This is not authentication."""
    result = {'matched': False, 'reason_code': 'STUDENT_NOT_FOUND', 'student': None}
    if not all(value.strip() for value in (student_id, full_name, term)):
        return result | {'reason_code': 'MISSING_INPUT'}
    students = json.loads((ROOT / 'data/students.json').read_text())
    for student in students:
        if student['student_id'] != student_id.strip():
            continue
        if normalize(student['full_name']) != normalize(full_name):
            return result | {'reason_code': 'NAME_MISMATCH'}
        if normalize(student['term']) != normalize(term):
            return result | {'reason_code': 'TERM_MISMATCH'}
        return {'matched': True, 'reason_code': 'MATCHED', 'student': student}
    return result


def check_appeal(student_id: str, full_name: str, term: str,
                 circumstances: str = '', academic_impact: str = '',
                 recovery_plan: str = '', category: str = 'Other',
                 documents_available: list[str] | None = None) -> dict:
    """Check packet completeness, never financial aid eligibility or approval."""
    match = lookup_student(student_id, full_name, term)
    fields = dict(student_id=student_id, full_name=full_name, term=term,
                  circumstances=circumstances, academic_impact=academic_impact,
                  recovery_plan=recovery_plan)
    missing = [key for key, value in fields.items() if not value.strip()]
    if category not in CATEGORIES:
        missing.append('valid_category')
    documents = list(documents_available or [])
    missing_documents = (['supporting_document'] if category == 'Illness'
                         and 'supporting_document' not in documents else [])
    reasons = [] if match['matched'] else [match['reason_code']]
    if missing:
        reasons.append('MISSING_FIELDS')
    if missing_documents:
        reasons.append('MISSING_DOCUMENTS')
    return dict(complete=not reasons, missing_fields=missing,
                missing_documents=missing_documents, reason_codes=reasons,
                student=match['student'], category=category,
                documents_available=documents,
                notice='Synthetic demo. Completeness is not an aid decision. Documents are self-reported.')
