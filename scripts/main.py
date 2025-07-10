
pip install certifi requests

import requests
import certifi
import zipfile
import io
import os

URL = "https://www2.susep.gov.br/redarq.asp?arq=BaseCompleta.zip"
ARQUIVOS_DESEJADOS = {"ses_seguros.csv", "ses_ramos.csv", "ses_cias.csv"}
PASTA_SAIDA = "data"

def baixar_e_extrair_csvs(url, arquivos_desejados, pasta_saida):
    print("🔄 Baixando arquivo da SUSEP...")
    resposta = requests.get(url, verify=certifi.where())
    resposta.raise_for_status()

    print("📦 Extraindo arquivos selecionados do ZIP...")
    with zipfile.ZipFile(io.BytesIO(resposta.content)) as zip_file:
        # Cria pasta de saída se não existir
        os.makedirs(pasta_saida, exist_ok=True)
        
        for nome_arquivo in zip_file.namelist():
            # Verifica se o arquivo está na lista desejada e tem extensão .csv
            if nome_arquivo in arquivos_desejados and nome_arquivo.endswith('.csv'):
                print(f"Extraindo {nome_arquivo}...")
                with zip_file.open(nome_arquivo) as arquivo_zip:
                    conteudo = arquivo_zip.read()
                    caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)
                    with open(caminho_arquivo, 'wb') as f:
                        f.write(conteudo)
    print("✅ Extração concluída.")

if __name__ == "__main__":
    baixar_e_extrair_csvs(URL, ARQUIVOS_DESEJADOS, PASTA_SAIDA)
