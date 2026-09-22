from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="ciel2027"
)

cursor = db.cursor()


@app.route('/')
def home():
    return 'Page d\'accueil'


# Récupérer tous les étudiants
@app.route('/v1/etudiants/', methods=['GET'])
def getEtudiants():
    etudiants = []

    request = "SELECT * FROM etudiant"
    cursor.execute(request)

    result = cursor.fetchall()

    for row in result:
        etudiant = {
            "identifiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
        }

        etudiants.append(etudiant)

    return jsonify(etudiants), 201


# Récupérer un étudiant avec son identifiant
@app.route('/v1/etudiants/<int:id>', methods=['GET'])
def getEtudiant(id):
    request = f"SELECT * FROM etudiant WHERE idetudiant = {id}"
    print(request)

    cursor.execute(request)
    row = cursor.fetchone()

    if row is None:
        return jsonify({"message": "Étudiant introuvable"}), 404

    etudiant = {
        "idetudiant": row[0],
        "nom": row[1],
        "prenom": row[2],
        "email": row[3],
        "telephone": row[4]
    }

    return jsonify(etudiant), 200

@app.route ('/v1/etudiants/',methods=['POST'])
def addEtudiant():
    nom = request.json['nom']
    prenom = request.json['prenom']
    email = request.json['email']
    telephone = request.json['telephone']
    req = f"INSERT INTO etudiant (nom,penom,email,telephone) \
        VALUES ('{nom}','{prenom}','{email}','{telephone}',)"
    cursor.execute(req)
    mydb.commit()
    #return req 
    return jsonify ({'message':'Ajout OK'}), 201

@app.route('/v1/etudiants/,<int:id>', methods=['PUT'])
def updateEtudiant(id):
    nom = request.json['nom']
    prenom = request.json['prenom']
    email = request.json['telephone']
    req = f"UPDATE etudiant\
        SET nom='{nom}' , prenom='{prenom}', email='{email}', telephone='{telephone}\
        WHERE idEtudiant={id}"
    cursor.execute(req)
    mydb.commit()
    return jsonify({'message':'modification OK'})

@app.route('/v1/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    req = f"DELETE FROM etudiant WHERE idEtudiant={id}"
    cursor.execute(req)
    mydb.commit()
    #return req
    return jsonify({'message':'Suppression OK'}), 200

#if _name_ == '_main_':
    #app.run(host= '0.0.0.0', debug=True)



if __name__ == "__main__":
    app.run(debug=True)