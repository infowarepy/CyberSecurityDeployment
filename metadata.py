import pikepdf
import pandas as pd
import csv

def extract_pdf_paths(csv_file):
    data = pd.read_csv(csv_file)
    pdf_paths = data["path"].tolist()
    return pdf_paths

if __name__ == "__main__":
    csv_file = "pdf_log.csv"
    pdf_paths = extract_pdf_paths(csv_file)
    df=pd.read_csv('metadata.csv')
    columns=df.columns
    keys=[]
    for pdf_filename in pdf_paths:
        temp=pdf_filename.split('/')
        country=temp[0]
        name=temp[1]
        data=[country,name]
        try:
            pdf = pikepdf.Pdf.open(pdf_filename)
            docinfo = pdf.docinfo
            keys=list(docinfo.keys())
            for column in columns:
                if f'/{column}' in keys:
                    data.append(str(docinfo[f'/{column}']))
                else:
                    data.append('')
            with open("metadata.csv", "a",newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
        except:
            print(f'error in {pdf_filename}')
        