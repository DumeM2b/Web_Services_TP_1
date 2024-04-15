from flask import Flask, render_template, request, jsonify
from sqlalchemy import TextClause, create_engine, text
import random
from faker import Faker
from random import randint
import requests

# Chaîne de connexion à la base de données PostgreSQL
db_string = "postgresql://root:root@localhost:5432/postgres"

# Créer une instance de moteur SQLAlchemy
engine = create_engine(db_string)

# Chemin du fichier SQL
sql_file_path = "table_creation.sql"

# Créer une application Flask
app = Flask(__name__)

# Fonction pour exécuter une requête SQL sans résultat
def run_sql(query: TextClause):
    """Exécute une requête SQL sans résultat.

    Args:
        query (TextClause): Objet de requête SQLAlchemy.
    """
    with engine.connect() as connection:
        trans = connection.begin()
        connection.execute(query)
        trans.commit()

# Fonction pour exécuter une requête SQL avec des résultats
def run_sql_with_results(query: TextClause):
    """Exécute une requête SQL avec des résultats.

    Args:
        query (TextClause): Objet de requête SQLAlchemy.

    Returns:
        ResultProxy: Résultat de la requête.
    """
    with engine.connect() as connection:
        trans = connection.begin()
        result = connection.execute(query)
        trans.commit()
        return result

# Créer une instance de Faker
fake = Faker()

# Fonction pour peupler la table users avec des données fictives
def populate_table():
    """Peuple la table users avec des données fictives."""
    for _ in range(100):  # Insérer 100 utilisateurs
        firstname = fake.first_name()
        lastname = fake.last_name()
        age = random.randrange(18, 90)
        email = fake.email()
        job = fake.job().replace("'", "")
        insert_statement = text(f"""
            INSERT INTO users (firstname, lastname, age, email, job)
            VALUES ('{firstname}', '{lastname}', '{age}', '{email}', '{job}')
            RETURNING id
        """)
        # Récupérer l'id de l'utilisateur inséré
        user_id = run_sql_with_results(insert_statement).scalar()
        print(user_id)

        # Insérer des applications pour cet utilisateur
        for _ in range(random.randint(1, 5)):
            appname = fake.company()
            username = fake.user_name()
            lastconnection = fake.date_time_between(start_date='-30d', end_date='now')
            insert_application_statement = text(f"""
                INSERT INTO applications (appname, username, lastconnection, user_id)
                VALUES ('{appname}', '{username}', '{lastconnection}', '{user_id}')
            """)
            run_sql(insert_application_statement)

# Fonction pour lire le contenu d'un fichier SQL
def read_sql_file(file_path):
    """Lit le contenu d'un fichier SQL.

    Args:
        file_path (str): Chemin du fichier SQL.

    Returns:
        str: Contenu du fichier SQL.
    """
    with open(file_path, 'r') as file:
        return file.read()

# Route pour récupérer les utilisateurs
@app.route('/user', methods=['GET'])
def get_users():
    """Route pour récupérer les utilisateurs depuis la base de données."""
    if request.method == 'GET':
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM users"))
            users_list = []
            for row in result:
                user_data = {
                    'id': row.id,
                    'firstname': row.firstname,
                    'lastname': row.lastname,
                    'age': row.age,
                    'email': row.email,
                    'job': row.job
                }
                users_list.append(user_data)
        return jsonify(users_list)

# Route pour la page d'accueil
@app.route('/home')
def home():
    """Route pour la page d'accueil."""
    # Récupérer les données des utilisateurs depuis l'API Flask
    response = requests.get('http://localhost:5000/user')

    users = response.json()

    return render_template('home.html', users=users)

# Point d'entrée de l'application Flask
if __name__ == '__main__':
    with app.app_context():
        # Lire le contenu du fichier SQL
        sql_query = read_sql_file(sql_file_path)
        # Exécuter la requête SQL
        run_sql(text(sql_query))
        # Appel à la fonction pour peupler la table
        populate_table()
    app.run(debug=True)


