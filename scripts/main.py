import os
import zipfile
import requests
from io import BytesIO

URL = "https://www2.susep.gov.br/redarq.asp?arq=BaseCompleta.zip"

os.makedirs("data", exist_ok=True)

arquivos_desejados = ["ses_seguros.xls", "ses_ramos.xls", "ses_cias.xls",
                     "ses_seguros.xlsx", "ses_ramos.xlsx", "ses_cias.xlsx"]

def download_and_extract_selected_files(url):
    print("🔄 Baixando arquivo da SUSEP...")
    response = requests.get(url, verify=False)
    zipfile_obj = zipfile.ZipFile(BytesIO(response.content))
    for filename in zipfile_obj.namelist():
        base_name = filename.split("/")[-1].lower()
        if base_name in arquivos_desejados:
            print(f"📄 Extraindo {filename} ...")
            zipfile_obj.extract(filename, "data")
            # Se quiser, pode mover/renomear para ficar só o arquivo, sem pastas internas:
            import shutil
            shutil.move(f"data/{filename}", f"data/{base_name}")
    print("✅ Extração concluída.")

if __name__ == "__main__":
    download_and_extract_selected_files(URL)
