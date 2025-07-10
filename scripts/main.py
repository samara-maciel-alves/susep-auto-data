import requests
import zipfile
import io
import os
import urllib3

# Desabilita o aviso de segurança que aparece ao usar verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://www2.susep.gov.br/redarq.asp?arq=BaseCompleta.zip"
ARQUIVOS_DESEJADOS = {"ses_seguros.csv", "ses_ramos.csv", "ses_cias.csv"}
PASTA_SAIDA = "data"

def baixar_e_extrair_csvs(url, arquivos_desejados, pasta_saida):
    print("🔄 Baixando arquivo da SUSEP...")
    try:
        resposta = requests.get(url, verify=False)
        resposta.raise_for_status() # Garante que erros HTTP (4xx, 5xx) sejam tratados como exceções
        
        # --- DEBUG: Verifica o status do download e tamanho do conteúdo ---
        print(f"Status HTTP do download: {resposta.status_code}")
        print(f"Tamanho do conteúdo baixado: {len(resposta.content)} bytes")
        if len(resposta.content) == 0:
            print("AVISO: O conteúdo baixado está vazio. O arquivo ZIP pode não ter sido transferido.")
            return

    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o arquivo: {e}")
        print("Certificado SSL não pôde ser verificado. A verificação foi ignorada (verify=False).")
        return # Sai da função se houver erro no download

    print("📦 Extraindo arquivos selecionados do ZIP...")
    try:
        with zipfile.ZipFile(io.BytesIO(resposta.content)) as zip_file:
            # --- DEBUG: Lista todos os arquivos dentro do ZIP ---
            nomes_no_zip = zip_file.namelist()
            print(f"Arquivos encontrados no ZIP: {nomes_no_zip}")

            # Cria pasta de saída se não existir
            os.makedirs(pasta_saida, exist_ok=True)
            
            arquivos_extraidos_count = 0
            for nome_arquivo in nomes_no_zip:
                # Verifica se o arquivo está na lista desejada e tem extensão .csv
                if nome_arquivo in arquivos_desejados and nome_arquivo.endswith('.csv'):
                    print(f"Condição de extração atendida para: {nome_arquivo}")
                    try:
                        with zip_file.open(nome_arquivo) as arquivo_zip:
                            conteudo = arquivo_zip.read()
                            if not conteudo:
                                print(f"AVISO: Arquivo '{nome_arquivo}' dentro do ZIP está vazio.")
                                continue # Pula para o próximo arquivo se estiver vazio

                            caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)
                            with open(caminho_arquivo, 'wb') as f:
                                f.write(conteudo)
                            print(f"✅ Extraído: {nome_arquivo} para {caminho_arquivo} ({len(conteudo)} bytes)")
                            arquivos_extraidos_count += 1
                    except KeyError:
                        print(f"Erro: '{nome_arquivo}' não encontrado no ZIP (apesar de namelist()). Pulando.")
                    except Exception as inner_e:
                        print(f"Erro ao extrair '{nome_arquivo}': {inner_e}")
                else:
                    # --- DEBUG: Mostra arquivos que não foram selecionados ---
                    print(f"Ignorando arquivo (não na lista desejada ou não é CSV): {nome_arquivo}")

            if arquivos_extraidos_count == 0:
                print("❌ Nenhum arquivo CSV desejado foi encontrado ou extraído do ZIP.")
            else:
                print(f"✅ Extração concluída. Total de arquivos extraídos: {arquivos_extraidos_count}")

    except zipfile.BadZipFile:
        print("Erro: O arquivo baixado não é um arquivo ZIP válido. Pode ter ocorrido um problema no download ou o conteúdo não é um ZIP.")
    except Exception as e:
        print(f"Erro inesperado durante a extração dos arquivos: {e}")

if __name__ == "__main__":
    baixar_e_extrair_csvs(URL, ARQUIVOS_DESEJADOS, PASTA_SAIDA)
