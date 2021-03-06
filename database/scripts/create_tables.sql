START TRANSACTION;
CREATE TABLE public.etablissement( id_etablissement SERIAL, siret VARCHAR(20) NOT NULL, adresse VARCHAR(255),code_postal VARCHAR(10),commune VARCHAR(255),coordonnees_gps VARCHAR(50),agrement VARCHAR(255),libelle VARCHAR(255), PRIMARY KEY(id_etablissement));
CREATE TABLE public.niveau_hygiene( id_hygiene SERIAL, niveau_hygiene VARCHAR(50),PRIMARY KEY(id_hygiene));
CREATE TABLE public.domaine_activite( id_activite SERIAL, libelle_activite VARCHAR(255), PRIMARY KEY(id_activite));
CREATE TABLE public.type_activite( id_type_activite SERIAL, type_activite VARCHAR(255),PRIMARY KEY(id_type_activite));
CREATE TABLE public.inspecte( id_etablissement INT, id_hygiene INT, numero_inspection VARCHAR(50),date_inspection VARCHAR(50),PRIMARY KEY(id_etablissement, id_hygiene, numero_inspection),UNIQUE(numero_inspection),FOREIGN KEY(id_etablissement) REFERENCES etablissement(id_etablissement),FOREIGN KEY(id_hygiene) REFERENCES niveau_hygiene(id_hygiene));
CREATE TABLE public.concerne( id_etablissement INT, id_activite INT, PRIMARY KEY(id_etablissement, id_activite),FOREIGN KEY(id_etablissement) REFERENCES etablissement(id_etablissement),FOREIGN KEY(id_activite) REFERENCES domaine_activite(id_activite));
CREATE TABLE public.cible( id_etablissement INT, id_type_activite INT, PRIMARY KEY(id_etablissement, id_type_activite),FOREIGN KEY(id_etablissement) REFERENCES etablissement(id_etablissement),FOREIGN KEY(id_type_activite) REFERENCES Type_activite(id_type_activite));
COMMIT;