import mysql.connector
import json

with open ("config.json","r+") as fichier:
    data = json.load(fichier)
    mdp = data["mdp"]
    
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=mdp,
    database="Zoo",
    auth_plugin='mysql_native_password'
)
cursor = conn.cursor()

TABLE = {}
TABLE["cage"] = (
    "CREATE TABLE `cage` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `capacite` int NOT NULL,"
    "  `superficie` int NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB"
)
TABLE['animal'] = (
    "CREATE TABLE `animal` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `nom` varchar(255) NOT NULL,"
    "  `race` varchar(255) NOT NULL,"
    "  `naissance` varchar(255) NOT NULL,"
    "  `pays` varchar(255) NOT NULL,"
    "  `id_cage` int NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB"
)

for table_name in TABLE:
    new_table = TABLE[table_name]
    try:
        cursor.execute(new_table)
    except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
    else:
        print("k")
        

add_animal = ("INSERT INTO animal "
              "( nom, race, naissance, pays, id_cage) "
              "VALUES ( %s, %s, %s, %s, %s)")
add_cage = ("INSERT INTO cage "
            "(id,capacite,superficie) "
            "VALUES (%s, %s, %s)")

donnees_animal = [("Tigrou","Tigre du Bingal","12/15/2019","Bingal",1),("Caramel","Cheval","11/06/2008","France",2),("Winnie","Grizzlie","08/10/2015","Canada",3),("Bourriquet","Ane","02/25/2010","Allemagne",2)]
donnees_cage = [(1,5,50),(2,10,300),(3,2,40),(4,1,20)]
for i in donnees_animal:
    cursor.execute(add_animal, i)
for i in donnees_cage:
    cursor.execute(add_cage, i)


cursor.execute("SELECT * FROM animal")
resultat = cursor.fetchall()
print(resultat)

while True:
    action = input("""
Monsieur le directeur, que voulez vous faire ?
(1) Gestion des animaux
(2) Liste des animaux    
(3) Superficie des cages  
(4) Quitter
""")
    if action == "1":
        action_gestion = input("""
Monsieur le directeur, que voulez vous faire ?
(1) Ajouter un animal d'une cage
(2) Modifier un animal d'une cage
(3) Supprimer l'animal d'une cage
""")
        cage = int(input("Veuillez dire l'id de la cage"))
        if action_gestion == "1":
            nom = input("\nNom : ")
            race = input("\nRace : ")
            naissance = input("\nNaissance (mm/dd/yyyy): ")
            pays = input("\nPays : ")
            cursor.execute(add_animal, (nom,race,naissance,pays,cage))
        elif action_gestion == "2":
            id = int(input("\ID : "))
            newCage = int(input("\Cage : "))
            cursor.execute(f"UPDATE animal SET id_cage = {newCage} WHERE animal.id = {id}")
        elif action_gestion == "3":
            id = int(input("\ID : "))
            cursor.execute(f"DELETE FROM animal WHERE animal.id = {id}")
    elif action == "2":
        cursor.execute("SELECT cage.id,animal.nom,animal.race,animal.naissance,animal.pays,animal.id FROM cage INNER JOIN animal ON animal.id_cage = cage.id WHERE animal.id_cage != 0 ORDER BY cage.id ")
        resultat = cursor.fetchall()
        print("\n")
        for i in resultat:
            print(i)

        
    elif action == "3":
        cursor.execute("SELECT superficie FROM cage ")
        resultat = cursor.fetchall()
        superficie = 0
        for superficie_i in resultat:
            superficie += superficie_i[0]
        print(f'La superficie de toutes les cages est de : {superficie} ')
        
    elif action == '4':
        break
    else:
        print("\n Oups veuillez faire un choix")
cursor.close()
conn.close()

