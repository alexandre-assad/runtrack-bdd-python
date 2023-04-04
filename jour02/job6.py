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

cursor.execute("SELECT capacite FROM salles ")
resultat = cursor.fetchall()
superficie = 0
for superficie_i in resultat:
    superficie += superficie_i[0]
    
print(f'La capacite de toutes les salles est de : {superficie} ')
cursor.close()
conn.close()
