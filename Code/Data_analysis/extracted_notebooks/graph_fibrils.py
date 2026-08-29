import matplotlib.pyplot as plt
import json
from collections import defaultdict
import numpy as np
from collections import Counter

# Caminho para o arquivo JSON
file_path = '/home/robert/Datas/Cores_fibrils/ts_2_seed_160.db'

# Processando o arquivo para mapear cada 'rid' aos seus vizinhos
neighbors_map = defaultdict(set)

try:
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line.strip())
            if 'rid' in data:
                rid = data['rid']
                neigh_rids = data.get('neigh_rids', [])
                for neigh_rid in neigh_rids:
                    neighbors_map[rid].add(neigh_rid)

except Exception as e:
    print(f"Erro ao processar o arquivo: {e}")

# Convertendo os conjuntos em listas para serem serializáveis em JSON
neighbors_map_serializable = {rid: list(neighbors) for rid, neighbors in neighbors_map.items()}

# Salvando o mapeamento em um arquivo JSON
output_file_path = 'saida_vizinhos.json'
try:
    with open(output_file_path, 'w') as outfile:
        json.dump(neighbors_map_serializable, outfile, indent=4)
    print(f"Dados salvos com sucesso em {output_file_path}")
except Exception as e:
    print(f"Erro ao salvar o arquivo: {e}")

# Primeiro, calculamos quantos vizinhos cada 'rid' tem
neighbors_count = {rid: len(neighbors) for rid, neighbors in neighbors_map.items()}

# Em seguida, calculamos a distribuição desses números de vizinhos
distribution = Counter(neighbors_count.values())

distribution

