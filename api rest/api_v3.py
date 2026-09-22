from flask import Flask, jsonify, request
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
@app.route('/v3/etudiants/', methods=['GET'])
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
@app.route('/v3/etudiants/<int:id>', methods=['GET'])
def getEtudiant(id):
    req = f"SELECT * FROM etudiant WHERE idetudiant = {id}"
    print(req)

    try:
        cursor.execute(req)
        row = cursor.fetchone()

        etudiant = {
            "identifiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
        }

        return jsonify(etudiant), 200

    except TypeError:
        return jsonify({"erreur": "id invalide"}), 404

@app.route ('/v3/etudiants/',methods=['POST'])
def addEtudiant():
    nom = request.json['nom']
    prenom = request.json['prenom']
    email = request.json['email']
    telephone = request.json['telephone']
    req = f"INSERT INTO etudiant (nom,penom,email,telephone) \
        VALUES ('{nom}','{prenom}','{email}','{telephone}',)"
    cursor.execute(req)
    db.commit()
    #return req 
    return jsonify ({'message':'Ajout OK'}), 201

@app.route('/v3/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    nom = request.json['nom']
    prenom = request.json['prenom']
    email = request.json['email']
    telephone = request.json['telephone']
    req = f"UPDATE etudiant\
        SET nom='{nom}' , prenom='{prenom}', email='{email}', telephone='{telephone}'\
        WHERE idEtudiant={id}"
    cursor.execute(req)
    db.commit()
    return jsonify({'message':'modification OK'})

@app.route('/v3/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    req = f"DELETE FROM etudiant WHERE idEtudiant={id}"
    cursor.execute(req)
    db.commit()
    #return req
    return jsonify({'message':'Suppression OK'}), 200

#if _name_ == '_main_':
    #app.run(host= '0.0.0.0', debug=True)



#if __name__ == "__main__":
    #app.run(debug=True)

@app.route('/v3/login',methods=['get'])
def login():
    username = "user1"
    password = "123456"

    req = f"SELECT * FROM user WHERE login = '{username}'AND password = '{password}'"
    cursor.execute(req)
    data = cursor.fetchone()
    if data: 
        return jsonify("acces autorisé",200)
    else:
        return jsonify("accces refuse",401)



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)