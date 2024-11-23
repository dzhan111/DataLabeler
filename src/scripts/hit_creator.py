import boto3, datetime
from dotenv import load_dotenv

load_dotenv('../.env')

mturk = boto3.client('mturk', region_name='us-east-1', endpoint_url='https://mturk-requester-sandbox.us-east-1.amazonaws.com')

for i in range(5):
    response = mturk.create_hit(
        Title = 'Colorful Captioner ' + str(i+1),
        Description = 'Dense image captioner to create training data for multimodal LLMs',
        Keywords = 'survey, image',
        Reward = '0.01',
        MaxAssignments = 50,
        LifetimeInSeconds = 604800,
        AssignmentDurationInSeconds = 3600,
        Question = '''
        <QuestionForm xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd">
            <Overview>
                <Text>We are collecting data to create dense image captions as training data for LLMs. Please click the link below to complete the survey. After completing the survey, return to this page and enter the unique survey code you received at the end of the survey to receive credit.</Text>
            </Overview>

            <Overview>
                <Text>Please click the link below to complete the survey:</Text>
                <Text>https://data-labeler-ten.vercel.app/</Text>  <!-- Just use plain text URL -->
            </Overview>        
            <Question>
                <QuestionIdentifier>surveycode</QuestionIdentifier>
                <DisplayName>Survey Code</DisplayName>
                <IsRequired>true</IsRequired>
                <QuestionContent>
                    <Text>Please enter the confirmation code provided at the end of the survey:</Text>
                </QuestionContent>
                <AnswerSpecification>
                    <FreeTextAnswer/>
                </AnswerSpecification>
            </Question>
        </QuestionForm>
        '''
    )

    print(response['HIT']['HITId'])


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