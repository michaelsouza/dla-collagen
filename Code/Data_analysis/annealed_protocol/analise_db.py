import json
from collections import defaultdict

def analisar_vizinhanca_db(caminho_arquivo_db):
    """
    Lê um arquivo .db, analisa as conexões entre os bastões (rods)
    e imprime um relatório de vizinhança.
    """
    # Usamos defaultdict(set) para agregar facilmente os vizinhos de cada bastão
    # sem duplicatas.
    mapa_vizinhos = defaultdict(set)
    bastoes_encontrados = set()

    print(f"--- Iniciando analise do arquivo: {caminho_arquivo_db} ---\n")

    try:
        with open(caminho_arquivo_db, 'r') as f:
            for i, linha in enumerate(f):
                # Ignora linhas em branco
                if not linha.strip():
                    continue

                try:
                    # Tenta carregar a linha como um objeto JSON
                    dados = json.loads(linha)

                    # Estamos interessados apenas em entradas de partículas,
                    # pois elas contêm a informação de vizinhança.
                    if 'pid' in dados and 'rid' in dados and 'neigh_rids' in dados:
                        rid_atual = dados['rid']
                        vizinhos = dados['neigh_rids']

                        # Adiciona o bastão atual ao conjunto de todos os bastões
                        bastoes_encontrados.add(rid_atual)

                        # Para o bastão atual, adiciona todos os seus vizinhos
                        # ao seu conjunto de vizinhos no nosso mapa.
                        mapa_vizinhos[rid_atual].update(vizinhos)
                        
                        # A vizinhança é mútua: se o bastão A é vizinho de B,
                        # então B também é vizinho de A.
                        for vizinho_rid in vizinhos:
                            mapa_vizinhos[vizinho_rid].add(rid_atual)

                except json.JSONDecodeError:
                    # Se uma linha não for um JSON válido (ex: linhas de 'rod' ou 'layer' sem neigh_rids),
                    # nós a ignoramos para este teste.
                    pass
                except KeyError:
                    # Se um JSON de partícula não tiver os campos esperados, ignoramos.
                    pass

    except FileNotFoundError:
        print(f"ERRO: Arquivo nao encontrado em '{caminho_arquivo_db}'")
        return

    # --- Geração do Relatório ---
    
    print("--- Resumo da Analise ---\n")
    
    total_bastoes = len(bastoes_encontrados)
    if total_bastoes == 0:
        print("Nenhum bastao com informacao de vizinhanca foi encontrado no arquivo.")
        return
        
    print(f"Total de bastoes (rods) unicos encontrados: {total_bastoes}\n")

    # Imprime a lista de vizinhos para cada bastão
    print("--- Mapa de Vizinhanca (Rod ID -> Vizinhos) ---\n")
    bastoes_isolados = 0
    # Ordena os IDs dos bastões para uma saída consistente
    for rid in sorted(list(bastoes_encontrados)):
        vizinhos = mapa_vizinhos.get(rid, set())
        if not vizinhos:
            bastoes_isolados += 1
        
        # Converte o conjunto de vizinhos em uma lista ordenada para melhor leitura
        vizinhos_ordenados = sorted(list(vizinhos))
        print(f"Rod ID: {rid:4d} | Vizinhos ({len(vizinhos_ordenados):2d}): {vizinhos_ordenados}")

    print("\n--- Analise Final ---\n")
    print(f"Bastoes com vizinhos: {total_bastoes - bastoes_isolados}")
    print(f"Bastoes isolados (sem vizinhos): {bastoes_isolados}")
    
    if bastoes_isolados > 0:
        print("\nAviso: Foram encontrados bastoes isolados. Isso pode indicar problemas na geometria ou na criacao de vizinhos.")
    else:
        print("\nSucesso: Todos os bastoes encontrados possuem pelo menos um vizinho.")


# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    # IMPORTANTE: Altere este nome de arquivo para o nome do seu arquivo .db
    NOME_ARQUIVO_DB = "ts_2_seed_130.db"
    
    analisar_vizinhanca_db(NOME_ARQUIVO_DB)