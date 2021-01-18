from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/sam/Desktop/TODO FLASK/todo.db"
db = SQLAlchemy(app)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos = todos)

@app.route("/isCompleted/<string:id>")
def completeTodo(id): #todo tamamlama.
    todo = Todo.query.filter_by(id = id).first()
    todo.isCompleted = not todo.isCompleted #todo tamamlanmamışsa tamamlar, tamamlanmışsa tamamlanmadıya çevirir.
    db.session.commit() #database güncellenir.
    return redirect(url_for("index")) #index döndürülür.

@app.route("/delete/<string:id>")
def deleteTodo(id): #todo silme.
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo) #seçilen todo database'den silinir.
    db.session.commit() #database güncellenir.
    return redirect(url_for("index")) #index döndürülür.

@app.route("/add", methods = ["POST"])
def addTodo(): #todo ekleme.
    title = request.form.get("title")
    newTodo = Todo(title = title, isCompleted = False)
    db.session.add(newTodo) #yeni todo database'e eklenir.
    db.session.commit() #database güncellenir.
    return redirect(url_for("index")) #index döndürülür.

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80))
    isCompleted = db.Column(db.Boolean)

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)
