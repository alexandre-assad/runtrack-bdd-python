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

cursor.execute("SELECT nom,capacite FROM salles ")
resultat = cursor.fetchall()
print(resultat)

cursor.close()
conn.close()
