import numpy as np
import pandas as pd
import database
from database.Classes import Connection

def launchETL(db):
    dataset = Connection.query_all(db, 'select e.id_etablissement, e.libelle, da.libelle_activite, ta.type_activite, e.code_postal, e.agrement from etablissement e inner join concerne co on e.id_etablissement=co.id_etablissement inner join domaine_activite da on co.id_activite=da.id_activite inner join cible ci on co.id_etablissement=ci.id_etablissement inner join type_activite ta on ci.id_type_activite=ta.id_type_activite;')
    
    df = pd.DataFrame(dataset)
    print(df.head())
