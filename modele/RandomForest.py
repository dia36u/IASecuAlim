from database.Classes import Connection
from imblearn import under_sampling, over_sampling
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split

db = Connection.connection_to_database()
requete_libelle = 'select e.id_etablissement, e.libelle, da.libelle_activite, ta.type_activite, e.code_postal, e.agrement, nh.niveau_hygiene from etablissement e inner join concerne co on e.id_etablissement=co.id_etablissement inner join domaine_activite da on co.id_activite=da.id_activite inner join cible ci on co.id_etablissement=ci.id_etablissement inner join type_activite ta on ci.id_type_activite=ta.id_type_activite inner join inspecte i on e.id_etablissement=i.id_etablissement inner join niveau_hygiene nh on nh.id_hygiene=i.id_hygiene;'
requete_id = 'select e.id_etablissement, da.id_activite, ta.id_type_activite, e.code_postal, e.agrement, nh.id_hygiene from etablissement e inner join concerne co on e.id_etablissement=co.id_etablissement inner join domaine_activite da on co.id_activite=da.id_activite inner join cible ci on co.id_etablissement=ci.id_etablissement inner join type_activite ta on ci.id_type_activite=ta.id_type_activite inner join inspecte i on e.id_etablissement=i.id_etablissement inner join niveau_hygiene nh on nh.id_hygiene=i.id_hygiene;'

dataset = Connection.query_all(db, requete_id)
df = pd.DataFrame(dataset, columns=['id_etablissement','id_activite', 'id_type_activite', 'code_postal','agrement','niveau_hygiene'])

df['code_postal'] = df['code_postal'].apply(lambda x: str(x)[:2])
df['code_postal'] = df['code_postal'].astype("int64")


class predict:
    cls = None
    X = df[["id_activite", "id_type_activite", "code_postal"]]
    y = df["niveau_hygiene"]
    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.3,random_state=1,stratify=df.niveau_hygiene)
    # y_train.shape
    seed = 5
    smote = SMOTE(sampling_strategy = 'auto', random_state = seed,k_neighbors = 7)
    X_train_smote, y_train_smote,  = smote.fit_resample(X_train, y_train)
    cls = RandomForestClassifier(n_estimators=60,random_state=2)
    cls.fit(X_train_smote,y_train_smote)


