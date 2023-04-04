import mysql.connector
import json

with open ("config.json","r+") as fichier:
    data = json.load(fichier)
    mdp = data["mdp"]
    
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=mdp,
    database="LaPlateforme",
    auth_plugin='mysql_native_password'
)
cursor = conn.cursor()
TABLE = {}
TABLE['employees'] = (
    "CREATE TABLE `employees` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `nom` varchar(255) NOT NULL,"
    "  `prenom` varchar(14) NOT NULL,"
    "  `salaire` float NOT NULL,"
    "  `id_service` int NOT NULL,"
    "CONSTRAINT `employees_ibfk_1` FOREIGN KEY (`id`)"
    " REFERENCES `services` (`id_service`) ON DELETE CASCADE,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")
TABLE["services"] = (
    "CREATE TABLE `services` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `nom` varchar(255) NOT NULL,"
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
        
add_employee = ("INSERT INTO employees "
               "(id, nom, prenom, salaire, id_service) "
               "VALUES (%s, %s, %s, %s, %s)")
add_service = ("INSERT INTO services "
               "(id, nom) "
               "VALUES (%s, %s)")

donnees_employee = [(1,"Garden", "John", 2800, 1),(2,"Garden", "Simon", 3800, 2),(3,"Roux", "Robert", 3200, 1),(4,"Dufont", "Sylvie", 4100, 3),(5,"Surris", "Isabelle", 2900, 2)]
donnees_services = [(1,"Developpement Web"),(2,"Compta"),(3,"Cybersecurite")]
for i in donnees_employee:
    cursor.execute(add_employee, i)
for i in donnees_services:
    cursor.execute(add_service, i)


# cursor.execute("SELECT employees.nom,employees.prenom,services.nom FROM employees INNER JOIN services ON employees.id_service =services.id")
# resultat = cursor.fetchall()
# print(resultat)

class Crud:
    
    def __init__(self,cursor):
        self.cursor = cursor
        

    def insert(self,newValue):
        self.cursor.execute(add_employee, newValue)
        
    def read(self):
        self.cursor.execute("SELECT employees.nom,employees.prenom,employees.salaire,services.nom FROM employees INNER JOIN services ON employees.id_service =services.id")

        resultat = self.cursor.fetchall()
        print(resultat)
    
    def delete_id(self,id):
        self.cursor.execute(f"DELETE FROM employees WHERE id = {id}")
        
    def update(self,categorie,newValue,id):
        self.cursor.execute(f"UPDATE employees SET employees.{categorie} = {newValue} WHERE id = {id}")

LaPlateforme = Crud(cursor)
LaPlateforme.read()
LaPlateforme.delete_id(2)
LaPlateforme.read()
LaPlateforme.insert((7,"Pigpig","Xavier",5470.0,3))
LaPlateforme.read()
LaPlateforme.update("nom","'Pigamo'",7)
LaPlateforme.update("salaire",6000.0,7)
LaPlateforme.read()
cursor.close()
conn.close()

