"""Produce reviewable text without inventing student circumstances."""
from backend.validation import check_appeal


def draft_statement(fields: dict) -> str:
    return ('To the Financial Aid Appeals Committee,\n\n'
            'I am requesting review of my financial aid appeal.\n\n'
            f"Circumstances\n{fields.get('circumstances', '').strip()}\n\n"
            f"Academic impact\n{fields.get('academic_impact', '').strip()}\n\n"
            f"Recovery plan\n{fields.get('recovery_plan', '').strip()}\n\n"
            'Thank you for reviewing my request.')


def build_packet(fields: dict, statement: str, reviewed: bool) -> str:
    if not reviewed or not statement.strip():
        raise ValueError('Review and confirm your statement before exporting.')
    result = check_appeal(**fields)
    student = result['student']
    if not student:
        raise ValueError('Match your demo student record before exporting.')
    status = 'Complete for demo review' if result['complete'] else 'Incomplete draft'
    remaining = result['missing_fields'] + result['missing_documents']
    return (f'HORNETFLOW — DEMO FINANCIAL AID APPEAL\nStatus: {status}\n\n'
            f"Student: {student['full_name']} ({student['student_id']})\n"
            f"Term: {student['term']}\nProgram: {student['program']}\n"
            f"Category: {result['category']}\n\nREVIEWED PERSONAL STATEMENT\n{statement.strip()}\n\n"
            'CHECKLIST\nRemaining items: ' + (', '.join(remaining) or 'None') + '\n'
            'Self-reported documents: ' + (', '.join(result['documents_available']) or 'None') + '\n\n'
            'Synthetic workshop policy and records. No documents were uploaded or authenticated.\n'
            'This packet is not an aid decision and has not been submitted.\n'
            'Check actual university requirements and use its official submission process.\n')
