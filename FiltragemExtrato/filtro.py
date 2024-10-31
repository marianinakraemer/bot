import os

# Função para remover a coluna de taxas em cada extrato
def remover_coluna_taxa(caminho_arquivo):
    try:
        linhas_sem_taxa = []

        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            cabecalho = arquivo.readline().strip().split('\t')
            if "TAXA" in cabecalho:
                indice_taxa = cabecalho.index("TAXA")
                linhas_sem_taxa.append('\t'.join(col for i, col in enumerate(cabecalho) if i != indice_taxa))

                for linha in arquivo:
                    colunas = linha.strip().split('\t')
                    if len(colunas) > indice_taxa:
                        linha_sem_taxa = '\t'.join(col for i, col in enumerate(colunas) if i != indice_taxa)
                        linhas_sem_taxa.append(linha_sem_taxa)

                return linhas_sem_taxa
            else:
                print(f"   - Coluna 'TAXA' não encontrada em {caminho_arquivo}.")
                return None

    except Exception as e:
        print(f"Erro ao processar {caminho_arquivo}: {e}")
        return None

# Função principal para processar todos os extratos na pasta
def processar_extratos(caminho_extratos):
    arquivos_filtrados = []
    for arquivo_extrato in os.listdir(caminho_extratos):
        caminho_extrato = os.path.join(caminho_extratos, arquivo_extrato)
        if os.path.isfile(caminho_extrato) and arquivo_extrato.endswith('.txt'):
            print(f"Processando extrato: {arquivo_extrato}")
            linhas_sem_taxa = remover_coluna_taxa(caminho_extrato)
            if linhas_sem_taxa:
                arquivo_sem_taxas = caminho_extrato.replace('.txt', '_sem_coluna_taxa.txt')
                with open(arquivo_sem_taxas, 'w', encoding='utf-8') as f_sem_taxa:
                    f_sem_taxa.write("\n".join(linhas_sem_taxa) + "\n")
                print(f"Extrato sem coluna de taxas salvo em: {arquivo_sem_taxas}")
                arquivos_filtrados.append(arquivo_sem_taxas)
            else:
                print("Nenhuma linha foi salva.")
    return arquivos_filtrados
