import os
import json
import boto3


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    obj = s3.get_object(Bucket=bucket, Key=key)
    file_text = obj['Body'].read()
    file_dict = json.loads(file_text)
    input_text = file_dict['results']['transcripts'][0]['transcript']
    print(input_text)
    
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=input_text,
        SourceLanguageCode='en',
        TargetLanguageCode='ja'
        )
    
    output_text = response.get('TranslatedText')
    print(output_text)
    output_file_name = os.path.splitext(os.path.basename(key))[0] + '_ja.txt'
    s3.put_object(Body=output_text, Bucket=bucket, Key=output_file_name)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'output_text': output_text
        })
    }
