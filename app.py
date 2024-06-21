from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
import re
from database import init_db, get_db_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuration de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'jvideo.ub@gmail.com'
app.config['MAIL_PASSWORD'] = 'NFlpb048!'
app.config['MAIL_DEFAULT_SENDER'] = 'jvideo.ub@gmail.com'

mail = Mail(app)

# Initialiser la base de données
init_db()

# Page d'accueil
@app.route('/')
def home():
    return render_template('home.html')

# Page de connexion
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE prenom = ? AND password = ?', (username, password)).fetchone()
    conn.close()

    if user:
        return redirect('/cours_ouest_du_chateau')
    else:
        flash('Votre identifiant ou votre mot de passe est incorrect. Cela peut-être dû à une candidature pas encore validée ou une faute de frappe. 😊', 'error')
        return redirect('/')

# Page d'inscription
@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        prenom = request.form['prenom']
        nom = request.form['nom']
        email = request.form['email']
        password = request.form['password']

        # Validation du mot de passe
        if not re.match(r'^(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{9,})', password):
            flash('Le mot de passe doit contenir au moins 9 caractères, un chiffre et un caractère spécial.', 'error')
            return redirect('/inscription')

        if prenom and nom and email and password:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (prenom, nom, email, password) VALUES (?, ?, ?, ?)', (prenom, nom, email, password))
            conn.commit()
            conn.close()

            msg = Message('Votre inscription à Poudlard', recipients=[email])
            msg.body = 'Votre candidature est officiellement envoyée, vous recevrez un mail pour savoir si elle est validée !'
            mail.send(msg)

            flash('Votre candidature est officiellement envoyée, vous recevrez un mail pour savoir si elle est validée !', 'success')
            return redirect('/')
        else:
            flash('Il manque des informations...', 'error')

    return render_template('inscription.html')

if __name__ == '__main__':
    app.run(debug=True)
