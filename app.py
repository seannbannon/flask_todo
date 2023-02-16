from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# function to return a string every time we create a new element
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
# connects to the 'content' id in the index.html
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
# commit task to database
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
# looks at all the database contents in the order it was created and display them all
            tasks = Todo.query.order_by(Todo.date_created).all()
            return 'There was an issue adding your task.'
        

    else:
        return render_template('index.html', tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)
