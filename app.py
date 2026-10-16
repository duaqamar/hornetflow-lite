"""HornetFlow Lite — local student appeal workspace."""
import os
import streamlit as st
from backend.agent_client import DEFAULT_MODEL, chat
from backend.mcp_client import call_tool
from backend.packet import build_packet, draft_statement
from backend.validation import CATEGORIES

st.set_page_config(page_title='HornetFlow · Financial aid appeals', page_icon='🌿', layout='wide')


def invalidate():
    for key in ('validation', 'statement', 'reviewed'):
        st.session_state.pop(key, None)


def identity_changed():
    invalidate()
    st.session_state.pop('conversation', None)
    st.session_state.pop('aws_messages', None)
    st.session_state.pop('tool_calls', None)


def load_demo():
    identity_changed()
    st.session_state.update(student_id='1001001', full_name='Alex Rivera', term='Fall 2026',
                            circumstances='A period of illness made it difficult to attend classes.',
                            academic_impact='I missed several lectures and fell behind on assignments.',
                            recovery_plan='I will meet my advisor weekly and attend tutoring twice a week.',
                            category='Illness', supporting=False)


def reset():
    st.session_state.clear()


with st.sidebar:
    st.markdown('### 🌿 HornetFlow')
    st.caption('STUDENT SERVICES · WORKSHOP DEMO')
    st.divider()
    st.markdown('**Your appeal, one step at a time.**')
    st.write('Gather your details, see what is missing, and leave with a statement you have reviewed.')
    st.button('Load fictional demo student', on_click=load_demo, use_container_width=True)
    st.button('Start a new session', on_click=reset, use_container_width=True)
    st.divider()
    ai_enabled = st.toggle('Enable AWS AI assistant', value=True)
    st.caption('Intake checks use the custom local MCP server in either mode.')
    with st.expander('AI settings'):
        model_id = st.text_input('Bedrock model ID', value=os.getenv('BEDROCK_MODEL_ID', DEFAULT_MODEL))
        st.caption('AWS profile: hackathon · Region: us-east-1')
    st.info('Fictional records and policy. No appeal is submitted. Use synthetic information only.')

st.caption('HORNETFLOW LITE / FINANCIAL AID')
st.title('A clearer path to your appeal.')
st.write('Turn your circumstances and next steps into a packet you can review with confidence.')
intake, assistant = st.columns([1.15, 1], gap='large')

with intake:
    st.subheader('1. Your details')
    st.caption('Demo: Alex Rivera · 1001001 · Fall 2026. Lookup is not identity verification.')
    left, right = st.columns(2)
    with left:
        student_id = st.text_input('Student ID', key='student_id', on_change=identity_changed, max_chars=30)
    with right:
        full_name = st.text_input('Full name', key='full_name', on_change=identity_changed, max_chars=100)
    st.session_state.setdefault('term', 'Fall 2026')
    term = st.text_input('Appeal term', key='term', on_change=identity_changed, max_chars=60)
    category = st.selectbox('Circumstance category', CATEGORIES, key='category', on_change=invalidate)
    circumstances = st.text_area('What happened?', key='circumstances', on_change=invalidate,
                                 placeholder='Share only what you want included in your statement.', max_chars=5000)
    academic_impact = st.text_area('How did it affect your studies?', key='academic_impact',
                                   on_change=invalidate, max_chars=5000)
    recovery_plan = st.text_area('What is your recovery plan?', key='recovery_plan', on_change=invalidate,
                                 placeholder='For example, advisor check-ins and a weekly study schedule.', max_chars=5000)
    supporting = st.checkbox('I have a supporting document available', key='supporting', on_change=invalidate)
    st.caption('Required for Illness under the synthetic demo policy. This does not upload or verify a file.')

fields = dict(student_id=student_id, full_name=full_name, term=term, category=category,
              circumstances=circumstances, academic_impact=academic_impact,
              recovery_plan=recovery_plan,
              documents_available=['supporting_document'] if supporting else [])

with intake:
    if st.button('Check my appeal packet', type='primary', use_container_width=True):
        try:
            with st.spinner('Checking your packet through HornetFlow MCP…'):
                st.session_state.validation = call_tool('check_appeal', fields)
        except Exception:
            st.error('The local MCP check did not finish. Try again; no successful result was assumed.')
            st.session_state.pop('validation', None)
    result = st.session_state.get('validation')
    if result:
        if result['complete']:
            st.success('All demo intake requirements are present. Review your statement next.')
        else:
            st.warning('Your packet needs a few more details.')
            for reason in result['reason_codes']:
                if reason not in ('MISSING_FIELDS', 'MISSING_DOCUMENTS'):
                    st.write('• Student record: ' + reason.replace('_', ' ').lower())
            for item in result['missing_fields'] + result['missing_documents']:
                st.write('• Add ' + item.replace('_', ' '))
        if result['student']:
            st.caption('Matched fictional record: ' + result['student']['full_name'] + ' · ' + result['student']['program'])
            if st.button('Create my statement draft', use_container_width=True):
                st.session_state.statement = draft_statement(fields)
                st.session_state.reviewed = False
    st.subheader('2. Review & download')
    if 'statement' in st.session_state:
        statement = st.text_area('Edit your personal statement', key='statement', height=300,
                                 on_change=lambda: st.session_state.update(reviewed=False))
        reviewed = st.checkbox('I reviewed this statement and confirm it reflects my circumstances.', key='reviewed')
        if reviewed and statement.strip():
            try:
                packet = build_packet(fields, statement, reviewed)
                st.download_button('Download demo appeal packet', packet, 'hornetflow-appeal.txt',
                                   mime='text/plain', use_container_width=True)
                st.caption('Incomplete packets are labeled as drafts. Completeness is not an aid decision.')
            except ValueError as error:
                st.warning(str(error))
    else:
        st.info('Check your student details, then create a statement draft. You can edit every word before exporting.')

with assistant:
    st.subheader('Your appeal guide')
    st.caption('AWS Bedrock + custom MCP tools' if ai_enabled else 'AI paused · local MCP checks remain available')
    st.session_state.setdefault('conversation', [])
    st.session_state.setdefault('aws_messages', [])
    with st.container(height=530):
        with st.chat_message('assistant'):
            st.write('Hi! I can explain the demo requirements and help you describe your situation. Start with your details on the left, or ask what an appeal needs.')
        for message in st.session_state.conversation:
            with st.chat_message(message['role']):
                st.write(message['text'])
    prompt = st.chat_input('Ask about your appeal…', disabled=not ai_enabled, max_chars=4000)
    if prompt:
        incoming = st.session_state.aws_messages + [{'role': 'user', 'content': [{'text': prompt}]}]
        try:
            with st.spinner('Your guide is thinking…'):
                response = chat(incoming, fields, model_id)
            st.session_state.aws_messages = response['messages']
            st.session_state.conversation.extend([{'role': 'user', 'text': prompt},
                                                 {'role': 'assistant', 'text': response['reply']}])
            st.session_state.tool_calls = response['tool_calls']
            st.rerun()
        except Exception as error:
            st.error('AWS chat is unavailable. Your form is preserved; MCP checks and downloads still work.')
            st.caption('Check your Workshop Studio credentials, network and model access.')
            with st.expander('Error details'):
                st.code(type(error).__name__ + ': ' + str(error)[:500])
    if st.session_state.get('tool_calls'):
        with st.expander('Tools used in the last reply'):
            for call in st.session_state.tool_calls:
                st.write(call['name'] + ' · ' + call['status'])
    with st.expander('Read the synthetic demo policy'):
        from backend.validation import ROOT
        st.markdown((ROOT / 'data/demo-policy.md').read_text())
