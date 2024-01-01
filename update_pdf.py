import os
import shutil
import requests
import pandas as pd
import PyPDF2

def get_file_size(file_path):
    try:
        size = os.path.getsize(file_path)
        return size
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

def download_file(url, save_path):
    try:
        response = requests.get(url)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded file from {url} and saved to {save_path}.")
    except Exception as e:
        print(f"An error occurred while downloading: {e}")

def update_file(original_file, new_file):
    try:
        shutil.copy2(new_file, original_file)
        print(f"Updated '{original_file}' with content from '{new_file}'.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def compare_content(org_file, new_file):
    pdf_content = lambda read_pdf: ''.join([page.extract_text().replace("\n", ' ').lower() for page in read_pdf.pages])
    org_pdf_content=pdf_content(PyPDF2.PdfReader(org_file))
    new_pdf_content=pdf_content(PyPDF2.PdfReader(new_file))
    if org_pdf_content==new_pdf_content:
        return True
    return False

# Read CSV file
if __name__ == "__main__":
    csv_file_path = "pdf_log.csv"
    df = pd.read_csv(csv_file_path)

    for index, row in df.iterrows():
        country = row['country']
        file_name = row['pdf_name']
        path = row['path']
        link = row['link']
        
        existing_file_path = path
        existing_file_size = get_file_size(existing_file_path)
        
        if existing_file_size is not None:
            download_file(link, "new_file_temp.pdf")
            new_file_path = "new_file_temp.pdf"
            new_file_size = get_file_size(new_file_path)
            
            if new_file_size is not None:
                if existing_file_size == new_file_size and compare_content(existing_file_path,new_file_path):
                    print(f"No change for {country}: Sizes and content are the same.")
                else:
                    update_file(existing_file_path, new_file_path)
            
            try:
                os.remove(new_file_path)
            except Exception as e:
                print(e)
        else:
            print(f"Could not compare file sizes for {country}.")
