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
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        number = request.form['number']
        print(name)
        # print(role)
        # print(number)
        new_task = Contact(name=name, role=role, number=number)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return 'There was an issue adding your contact'

    else:
        tasks = Contact.query.order_by(Contact.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Contact.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that contact'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Contact.query.get_or_404(id)

    if request.method == 'POST':
        task.name = request.form['name']
        task.role = request.form['role']
        task.number = request.form['number']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your contact'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
