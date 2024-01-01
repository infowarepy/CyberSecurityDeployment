from main_update2 import *
from pdf_selector_update1 import *
from country_driver import scrap_country
from cybersecurity_news_scrapping.app import *
import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
S3_BUCKET_NAME=os.getenv('S3_BUCKET_NAME')
REGION=os.getenv('REGION')
ACCESS_KEY_ID=os.getenv('ACCESS_KEY_ID')
SECRET_ACCESS_KEY=os.getenv('SECRET_ACCESS_KEY')

s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
objects=[a['Key'] for a in s3.list_objects(Bucket='infowarepython').get('Contents', [])]


def scrapper():
    df = pd.read_csv('test_country.csv')
    countries=df["Country_Name"]
    log_file='CyberSecurityPolicies/log_details.csv'
    csv_data=''
    if log_file not in objects:
        csv_data=f'country_name,date,start_time,end_time,total_runtime,links,pdf_count,update\n'
    response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=log_file)
    csv_data = response['Body'].read().decode('utf-8')
    for country in countries:
        data=scrap_country(country_name=country)
        csv_data += data
        csv_data=csv_data.encode('utf-8')
        s3.put_object(Bucket=S3_BUCKET_NAME, Key=log_file, Body=csv_data)
        

    return render_template('index.html',label=f'{country} done')
         


def news():
    countries_input = request.form.get('countries')
    countries=[i.strip() for i in countries_input.split('\n')]
    json_data=log_data(cnt)
    return jsonify(json_data)
    
# @app.route('/upload', methods=['POST'])
# def upload():
#     countries_input = request.form.get('countries')
    
#     # Split the entered countries
#     countries = [country.strip() for country in countries_input.split(',')]

#     # If a file is uploaded, extract countries from the CSV file
#     uploaded_file = request.files['file']
#     if uploaded_file:
#         # Save the file to a temporary location
#         csv_path = '/tmp/uploaded_countries.csv'
#         uploaded_file.save(csv_path)

#         # Read countries from the CSV file
#         with open(csv_path, 'r') as csv_file:
#             reader = csv.reader(csv_file)
#             for row in reader:
#                 countries.extend(row)

if __name__ == '__main__':
    app.run(debug=True)
