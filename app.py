from main_update2 import *
from pdf_selector_update1 import *
from country_driver import scrap_country
from cybersecurity_news_scrapping.app import *
from flask import Flask, request, redirect, url_for, session, render_template, jsonify
import json
import pandas


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html',label=[])

@app.route('/scrapping',methods=['POST'])
def recurse():
    countries_input = request.form.get('countries')
    countries=[i.strip() for i in countries_input.split('\n')]
    print(countries)
    for country in countries:
        scrap_country(country_name=country)
        def scrapper():
            scrap_country(country_name=country)
            return render_template('index.html',label=f'{country} done')
        scrapper()
    return render_template('index.html',label=f'{country} done')
         

@app.route('/news',methods=['POST'])
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
