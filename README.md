# GLO-2005 - Projet
## Nom et IDUL

    Alissa Audet | ALAUD52

## Seter MySql
Pour seter son mot de passe à "root", faite cette commande dans le terminal MySql de root

    ALTER USER 'root'@'localhost' IDENTIFIED BY 'root'; FLUSH PRIVILEGES;

## Ajouter/installer requirement
Seter fichier requirement selon l'environnement:

      pip freeze > requirements.txt
Installer requirement : 

    pip install -r requirements.txt

## Exécuter l'application

    python code\app.py

### Que fait app.py : 
1. init_database.py : réinitialise la BD
2. load_all_data.py : charger des données factices
3. Lancer le serveur Flas

        http://127.0.0.1:5000

## Structure du projet
### Couches
1. templates :	Contient les fichiers HTML qui définissent l'apparence des pages.
2. static : Contient les fichiers js pour gérer les appels API.
3. routes : Définit les endpoints (séparé par table).
4. models : Contient les fichiers pour interagir avec la base de données (séparé par table).
5. database : Gère la base de données et contient les scripts d'initialisation.



