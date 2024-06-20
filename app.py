from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Placeholder for database interaction
# You should replace this with actual database code
# Note: For security, use a more secure method to store and validate passwords
users = [{'username': 'testuser', 'password': 'testpassword'}]

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Login page
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = next((user for user in users if user['username'] == username and user['password'] == password), None)

    if user:
        # Redirect to the new page if login is successful
        return redirect('/cours_ouest_du_chateau')
    else:
        flash('Votre identifiant ou votre mot de passe est incorrect. Cela peut-être dû à une candidature pas encore validée ou une faute de frappe. 😊', 'error')
        return redirect('/')

# Registration page
@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        prenom = request.form['prenom']
        nom = request.form['nom']
        password = request.form['password']
        email = request.form['email']

        if prenom and nom and password:
            # Placeholder for sending email
            # You should replace this with actual email sending code
            flash('Votre candidature est officiellement envoyée, vous recevrez un mail pour savoir si elle est validée !', 'success')
            # Replace 'jvideo.ub@gmail.com' with the actual email address
            # Send email here

            return redirect('/')
        else:
            flash('Il manque des informations...', 'error')

    return render_template('inscription.html')

if __name__ == '__main__':
    app.run(debug=True)
