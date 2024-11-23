import argparse
import datetime
import boto3
#from routes import is_code_valid
import time
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import os
from clients import SUPABASE_CLIENT


def is_code_valid(workerId, code):
    res = SUPABASE_CLIENT.table("verification").select(1).eq("code", code).eq("mturkid", workerId).execute()
    if not res:
        return False
    SUPABASE_CLIENT.table("verification").delete().eq("code", code).eq("mturkid", workerId).execute()
    return True
    #return code in ['a', 'b', '123456']

mturk = boto3.client('mturk', region_name='us-east-1', endpoint_url='https://mturk-requester-sandbox.us-east-1.amazonaws.com')

def get_submitted_assignments(hit_id: int):
    list_assignments = mturk.list_assignments_for_hit(
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
        if question_id == 'surveycode':
            answer = answer_field.find('ns:FreeText', namespace).text
            print("\n\n\nanswer: " + answer + "\n\n\n")
    if is_code_valid(assignment['WorkerId'], answer):
        print(assignment['AssignmentId'])
        mturk.approve_assignment(
            AssignmentId=assignment['AssignmentId'])
    else:
        mturk.reject_assignment(
            AssignmentId=assignment['AssignmentId'], 
            RequesterFeedback="Invalid confirmation code."
        )

def main():
    load_dotenv('../.env')
    print("POLLING!!!")
    while True:
        for hit_id in hits:
            assignments = get_submitted_assignments(hit_id)
            print(assignments)
            for assignment in assignments:
                validate_assignment(assignment)

        time.sleep(600)

def disable_and_delete_all_hits():
    try:
        # List all HITs in your account
        response = mturk.list_hits()
        hits = response['HITs']

        for hit in hits:
            hit_id = hit['HITId']
            print(f"Processing HIT: {hit_id}")

            # Disable the HIT by setting its expiration date to the past
            mturk.update_expiration_for_hit(
                HITId=hit_id,
                ExpireAt=datetime.datetime(2000, 1, 1)  # Expire immediately
            )
            print(f"HIT {hit_id} disabled (expired).")

            # Delete the HIT
            try:
                mturk.delete_hit(HITId=hit_id)
                print(f"HIT {hit_id} deleted successfully.")
            except mturk.exceptions.RequestError as e:
                for ass in mturk.list_assignments_for_hit(HITId=hit_id, AssignmentStatuses=['Submitted']):
                    mturk.reject_assignment(AssignmentId=ass['AssignmentId'], RequesterFeedback="Invalid confirmation code.")
                print(f"Could not delete HIT {hit_id}. Reason: {e}")

    except Exception as e:
        print(f"Error occurred: {e}")



if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Validate worker's survey code.")
    
    # # Add command-line arguments
    # parser.add_argument('hit_id', type=str, help='ID of the worker')
    # args = parser.parse_args()
    # disable_and_delete_all_hits()
    # main()
    #print([x['HITId'] for x in mturk.list_hits()['HITs']])
    print('hi')