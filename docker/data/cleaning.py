import pandas as pd

# prendre tous les fichiers json du dossier data et les fusionner en un seul

# data_full = pd.DataFrame()
# for i in range(1,13):
#     data = pd.read_json(f'data/data_{i}.json')
#     data_full = pd.concat([data_full,data], ignore_index=True)

data_full = pd.read_json('data/data_full.json')

# supprimer les doublons
data_full = data_full.drop_duplicates(subset=['id_tmdb'], keep='first')
# supprimer les lignes avec "id_imdb" = "N/A"
data_full = data_full[data_full['id_imdb'] != 'N/A']

# sauvegarder le fichier
data_full.to_json('data/data_full.json', orient='records', indent=4)