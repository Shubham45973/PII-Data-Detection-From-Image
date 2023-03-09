import json
import boto3

def textdetection(bucket,key):
    textract_client=boto3.client('textract')
    response=textract_client.detect_document_text(
        Document={
        'S3Object': {
            'Bucket': bucket,
            'Name': key
        }
    }
    )
    detected_text=''
    for item in response['Blocks']:
        if (item['BlockType']=='LINE'):
            detected_text=detected_text + ""+item['Text']
    print(detected_text)
    text_analysis(detected_text)
    
def text_analysis(detected_text):
    comprehend_client=boto3.client('comprehend')
    
    comprehend_res=comprehend_client.contains_pii_entities(
        Text=detected_text,
        LanguageCode='en'

    )
    dict_len=len(comprehend_res['Labels'])
    dict={}
    for i in range(0,dict_len):
        print(comprehend_res['Labels'][i])
        if(comprehend_res['Labels'][i]['Score']>=0.9):
            dict[comprehend_res['Labels'][i]['Name']]=comprehend_res['Labels'][i]['Score']
        
    print(dict)    
    print(len(comprehend_res['Labels']))
    
    
    

    
def lambda_handler(event, context):
    try:
        size = event['Records'][0]['s3']['object']['size'] 
    except KeyError:
        pass

    bucket = event['Records'][0]['s3']['bucket']['name'] 
    key = event['Records'][0]['s3']['object']['key']
   
    textdetection(bucket,key)