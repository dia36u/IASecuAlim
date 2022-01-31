import pandas as pd
from Classes import Connection


types = pd.DataFrame(Connection.query_all(Connection.connection_to_database(),'select * from type_activite;'), columns=['id','type'])
#print(types)
#etablissements = pd.DataFrame(Connection.query_all(conn,'select id_etablissement, siret from etablissement;'))
csv=pd.read_csv('database/data/cible.csv', sep=";")
#print(csv.head())

for index in csv.index:
    for index_type in types.index:
        if types['type'][index_type] == csv['ods_type_activite'][index]:
            csv['ods_type_activite'][index] = types['id'][index_type]
print(csv.head())

    