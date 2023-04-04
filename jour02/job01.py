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

cursor.execute("SELECT * FROM Etudiants ")
resultat = cursor.fetchall()

for ligne in resultat:
    print(ligne)
    
cursor.close()
conn.close()
