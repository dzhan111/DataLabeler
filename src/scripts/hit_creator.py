import argparse
import datetime
import boto3
import time
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import os

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