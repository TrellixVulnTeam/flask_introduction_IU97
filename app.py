from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Task %>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'] #'content' is the id
        new_task = Todo(content=task_content)  # create db.obj
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/') # redirect to homepage
        except:
            return 'There was an issue when adding your task.'
    else:
        tasks = Todo.query.order_by(Todo.date_created.desc()).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/') # redirect to homepage
    except:
        return 'There was an problem when deleting the task.'

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content'] #'content' is the id
        try:
            db.session.commit()
            return redirect('/') # redirect to homepage
        except:
            return 'There was an issue when updating your task.'
    else:
        return render_template('update.html', task=task)
# This is the port and IP address of the server
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port=2345)