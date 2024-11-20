import boto3
from routes import is_code_valid
import time

mturk = boto3.client('mturk', region_name='us-east-1')

def get_submitted_assignments(hit_id: int):
    list_assignments = mturk.list_assignments_for_hit(
        HITId=hit_id, 
        AssignmentStatuses=['Submitted']
    )
    return list_assignments['Assignments']

def validate_assignment(assignment):
    if is_code_valid(assignment['WorderId'], assignment['Answer']):
        mturk.approve_assignment(
            AssignmentId=assignment['AssignmentId'])
    else:
        mturk.reject_assignment(
            AssignmentId=assignment['AssignmentId'], 
            RequesterFeedback="Invalid confirmation code."
        )

def process_submissions(hit_id):
    while True:
        assignments = get_submitted_assignments(hit_id)

        for assignment in assignments:
            validate_assignment(assignment)

        time.sleep(600)

