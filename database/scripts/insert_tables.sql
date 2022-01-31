START TRANSACTION;
INSERT INTO TABLE public.utilisateur( id_user SERIAL, mail VARCHAR(255),nom VARCHAR(30),prenom VARCHAR(30),password VARCHAR(255), PRIMARY KEY(id_user));
INSERT INTO TABLE public.historique( id_hist SERIAL, id_user INT, created_at DATE, estimation TEXT, PRIMARY KEY(id_hist),FOREIGN KEY(id_user) REFERENCES utilisateur(id_user));
COMMIT;