import json
from country_driver import scrap_country
import boto3
from cybersecurity_news_scrapping import *
from tempfile import NamedTemporaryFile


def lambda_handler(event, context):
    # TODO implement
    scrapping_result=update_policy_data(event['country'])
    
    return {
        'statusCode': 200,
        'message': scrapping_result
    }


def update_policy_data(country):
    log_data=scrap_country(country_name=country)
    try:
        from dotenv import load_dotenv
        import os

        load_dotenv()
        S3_BUCKET_NAME=os.getenv('S3_BUCKET_NAME')
        REGION=os.getenv('REGION')
        ACCESS_KEY_ID=os.getenv('ACCESS_KEY_ID')
        SECRET_ACCESS_KEY=os.getenv('SECRET_ACCESS_KEY')

        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
        objects=[a['Key'] for a in s3.list_objects(Bucket='infowarepython').get('Contents', [])]
        country_log_file=f'CyberSecurityPolicies/{country}/{country}_log.csv'

        if country_log_file not in objects:
            csv_data='country_name,date,start_time,end_time,total_runtime,links,pdf_count,update\n'
        else:
            response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=country_log_file)
            csv_data = response['Body'].read().decode('utf-8')
        
        csv_data+=log_data
        csv_data=csv_data.encode('utf-8')
        s3.put_object(Bucket=S3_BUCKET_NAME, Key=country_log_file, Body=csv_data)

        return f'Successfully scrapped and updtaed log for {country}.'
    
    except Exception as e:
        return f'error occured.'
    

def update_news_data(country):
    log_news_data(country)
