import mysql.connector
import hashlib

class Database:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    # --- Authentification ---
    def login(self, request):
        auth = request.authorization
        if auth is None:
            return 401

        username = auth.username
        password = auth.password

        try:
            connector = self.connect()
        except mysql.connector.Error:
            return 500

        cursor = connector.cursor()
        try:
            cursor.execute(
                f"SELECT * FROM user WHERE login = '{username}' AND password = '{password}'"
            )
            data = cursor.fetchone()
            if data:
                return 200
            else:
                return 401
        except mysql.connector.Error:
            return 500
        finally:
            connector.close()

    # --- Lire tous les étudiants ---
    def readAll(self):
        try:
            connector = self.connect()
        except mysql.connector.Error:
            return 500

        cursor = connector.cursor()
        try:
            cursor.execute("SELECT * FROM etudiant")
            return cursor.fetchall()
        except mysql.connector.Error:
            return 400
        finally:
            connector.close()

    # --- Lire un seul étudiant ---
    def readOne(self, id):
        try:
            connector = self.connect()
        except mysql.connector.Error:
            return 500

        cursor = connector.cursor()
        try:
            cursor.execute(f"SELECT * FROM etudiant WHERE idEtudiant = {id}")
            data = cursor.fetchone()
            if data:
                return data
            else:
                return 404
        except mysql.connector.Error:
            return 400
        finally:
            connector.close()

    # --- Ajouter un étudiant ---
    def create(self, nom, prenom, email, telephone):
        try:
            connector = self.connect()
        except mysql.connector.Error:
            return 500

        cursor = connector.cursor()
        try:
            req = f"""INSERT INTO etudiant (nom, prenom, email, telephone)
                      VALUES ('{nom}', '{prenom}', '{email}', '{telephone}')"""
            cursor.execute(req)
            connector.commit()
            return 201
        except mysql.connector.Error:
            return 400
        finally:
            connector.close()

    # --- Modifier un étudiant ---
    def update(self, id, nom, prenom, email, telephone):
        try:
            connector = self.connect()
        except mysql.connector.Error:
            return 500

        cursor = connector.cursor()
        try:
            req = f"""UPDATE etudiant
                      SET nom = '{nom}', prenom = '{prenom}',
                          email = '{email}', telephone = '{telephone}'
                      WHERE idetudiant = {id}"""
            cursor.execute(req)
            if cursor.rowcount == 0:
                return 404
            connector.commit()
            return 200
        except mysql.connector.Error:
            return 400
        finally:
            connector.close()

    # --- Supprimer un étudiant ---
    def delete(self, id):
        try:
            connector = self.connect()
        except mysql.connector.Error:
            return 500

        cursor = connector.cursor()
        try:
            req = f"DELETE FROM etudiant WHERE idetudiant = {id}"
            cursor.execute(req)
            if cursor.rowcount == 0:
                return 404
            connector.commit()
            return 200
        except mysql.connector.Error:
            return 400
        finally:
            connector.close()