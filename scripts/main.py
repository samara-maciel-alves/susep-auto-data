import os
import zipfile
import requests
import certifi
from io import BytesIO

URL = "https://www2.susep.gov.br/redarq.asp?arq=BaseCompleta.zip"

os.makedirs("data", exist_ok=True)

arquivos_desejados = ["ses_seguros.csv", "ses_ramos.csv", "ses_cias.csv"]

def download_and_extract_selected_csv(url):
    print("🔄 Baixando arquivo da SUSEP...")
    
    response = requests.get(url, verify=certifi.where())

    zipfile_obj = zipfile.ZipFile(BytesIO(response.content))
    
    print("Arquivos no ZIP:")
    print(zipfile_obj.namelist())
    
    for filename in zipfile_obj.namelist():
        base_name = filename.split("/")[-1].lower()
        if base_name in arquivos_desejados:
            print(f"📄 Extraindo {filename} ...")
            zipfile_obj.extract(filename, "data")
    print("✅ Extração concluída.")

if __name__ == "__main__":
    download_and_extract_selected_csv(URL)
