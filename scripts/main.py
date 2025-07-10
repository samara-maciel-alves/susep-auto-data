import os
import zipfile
import requests
import pandas as pd
from io import BytesIO

# URL do ZIP da SUSEP
URL = "https://www2.susep.gov.br/redarq.asp?arq=BaseCompleta.zip"

# Cria pasta de destino
os.makedirs("data", exist_ok=True)

def download_and_extract_zip(url):
    print("🔄 Baixando arquivo da SUSEP...")
    response = requests.get(url)
    zipfile_obj = zipfile.ZipFile(BytesIO(response.content))
    return zipfile_obj

def process_excel_files(zipfile_obj):
    for filename in zipfile_obj.namelist():
        if filename.endswith(".xls") or filename.endswith(".xlsx"):
            print(f"📄 Lendo: {filename}")
            with zipfile_obj.open(filename) as file:
                try:
                    df = pd.read_excel(file)
                    name = filename.split("/")[-1].replace(".xls", ".csv").replace(".xlsx", ".csv")
                    output_path = os.path.join("data", name)
                    df.to_csv(output_path, index=False, encoding="utf-8-sig")
                    print(f"✅ Convertido para CSV: {output_path}")
                except Exception as e:
                    print(f"⚠️ Erro ao processar {filename}: {e}")

if __name__ == "__main__":
    zipfile_obj = download_and_extract_zip(URL)
    process_excel_files(zipfile_obj)
