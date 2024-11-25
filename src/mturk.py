import xml.etree.ElementTree as ET
import asyncio
from uuid import UUID

from src.clients import SUPABASE_CLIENT, MTURK_CLIENT

async def validate_turk_responses(hit_ids: list[str]):
    while True:
        copied_hit_ids = []
        copied_hit_ids = hit_ids.copy()

        for hit_id in copied_hit_ids:
            assignments = get_submitted_assignments(hit_id)
            for assignment in assignments:
                validate_assignment(assignment)

        await asyncio.sleep(300)

def is_code_valid(workerId, code):
    try:
        _ = UUID(code, version=4)
    except ValueError:
        return False
    
    res = (SUPABASE_CLIENT.table("verification")
           .select('*')
           .eq("code", code)
           .eq("mturkid", workerId)).execute()
    if not res:
        return False
    (SUPABASE_CLIENT.table("verification")
     .delete()
     .eq("code", code)
     .eq("mturkid", workerId)).execute()
    return True

def get_submitted_assignments(hit_id: int):
    list_assignments = MTURK_CLIENT.list_assignments_for_hit(
        HITId=hit_id, 
        AssignmentStatuses=['Submitted']
    )
    return list_assignments['Assignments']

def validate_assignment(assignment):
    answer_xml = assignment['Answer']
    root = ET.fromstring(answer_xml)
    answer = ""
    # Define the namespace
    namespace = {'ns': 'http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionFormAnswers.xsd'}

    # Find all Answer elements using the namespace
    for answer_field in root.findall('.//ns:Answer', namespace):
        question_id = answer_field.find('ns:QuestionIdentifier', namespace).text
        if question_id != 'surveycode':
            continue
        answer = answer_field.find('ns:FreeText', namespace).text

    if is_code_valid(assignment['WorkerId'], answer):
        MTURK_CLIENT.approve_assignment(
            AssignmentId=assignment['AssignmentId'])
        return
    
    MTURK_CLIENT.reject_assignment(
        AssignmentId=assignment['AssignmentId'], 
        RequesterFeedback="Invalid confirmation code."
    )