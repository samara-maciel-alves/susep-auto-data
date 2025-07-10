import requests
# import certifi # certifi não é mais necessário se você usar verify=False
import zipfile
import io
import os
import urllib3 # Importe urllib3 para desabilitar o aviso de segurança

# Desabilita o aviso de segurança que aparece ao usar verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://www2.susep.gov.br/redarq.asp?arq=BaseCompleta.zip"
ARQUIVOS_DESEJADOS = {"ses_seguros.csv", "ses_ramos.csv", "ses_cias.csv"}
PASTA_SAIDA = "data"

def baixar_e_extrair_csvs(url, arquivos_desejados, pasta_saida):
    print("🔄 Baixando arquivo da SUSEP...")
    try:
        # AQUI É A MUDANÇA: Use verify=False para pular a verificação SSL
        resposta = requests.get(url, verify=False)
        resposta.raise_for_status() # Garante que erros HTTP (4xx, 5xx) sejam tratados como exceções
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o arquivo: {e}")
        print("Certificado SSL não pôde ser verificado. A verificação foi ignorada (verify=False).")
        return # Sai da função se houver erro no download

    print("📦 Extraindo arquivos selecionados do ZIP...")
    try:
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
    except zipfile.BadZipFile:
        print("Erro: O arquivo baixado não é um arquivo ZIP válido. Pode ter ocorrido um problema no download.")
    except Exception as e:
        print(f"Erro durante a extração dos arquivos: {e}")

if __name__ == "__main__":
    baixar_e_extrair_csvs(URL, ARQUIVOS_DESEJADOS, PASTA_SAIDA)
