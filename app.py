from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=False)
    number = db.Column(db.String(200), nullable=False)
    cell = db.Column(db.String(200), nullable=False)
    landline = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        number = request.form['number']
        cell = request.form['cell']
        landline = request.form['landline']
        # print(name)
        # print(role)
        # print(number)
        new_contact = Contact(name=name, role=role, number=number, cell=cell, landline=landline)

        try:
            db.session.add(new_contact)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return 'There was an issue adding your contact'

    else:
        contacts = Contact.query.order_by(Contact.date_created).all()
        return render_template('index.html', contacts=contacts)


@app.route('/delete/<int:id>')
def delete(id):
    contact_to_delete = Contact.query.get_or_404(id)

    try:
        db.session.delete(contact_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that contact'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    contact = Contact.query.get_or_404(id)

    if request.method == 'POST':
        contact.name = request.form['name']
        contact.role = request.form['role']
        contact.number = request.form['number']
        contact.cell = request.form['cell']
        contact.landline = request.form['landline']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your contact'

    else:
        return render_template('update.html', contact=contact)


if __name__ == "__main__":
    app.run(debug=True)
