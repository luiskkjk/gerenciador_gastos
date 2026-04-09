from flask import Flask, render_template, request, redirect, url_for
from db import db
from datetime import datetime
from models import Gastos



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dados.db"
db.init_app(app)

@app.route('/')
def home():
    gastos = db.session.query(Gastos).all()
    return render_template('home.html', gastos=gastos)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'GET':
        return render_template('adicionar.html')
    elif request.method =='POST':
        data_str=request.form.get('dataGasto')
       
        if not data_str:
            return "Data é obrigatória!"

        valor = request.form['valorGasto']
        data=datetime.strptime(data_str, "%Y-%m-%d").date()
        descricao = request.form['descGasto']
        categoria = request.form['catGasto']

        novo_gasto = Gastos(valor=valor, data=data, descricao=descricao, categoria=categoria)
        db.session.add(novo_gasto)
        db.session.commit()

        return redirect(url_for('home'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    gasto = db.session.query(Gastos).filter_by(id=id).first()
    if request.method == "GET":
        return render_template('editar.html', gasto=gasto)
    elif request.method == "POST":
        valor = request.form['valorGasto']
        data = request.form['dataGasto']
        descricao = request.form['descGasto']
        categoria = request.form['catGasto']

        gasto.valor = valor
        gasto.data = data
        gasto.descricao = descricao
        gasto.categoria = categoria
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/deletar/<int:id>')
def deletar(id):
    gasto = db.session.query(Gastos).filter_by(id=id).first()
    db.session.delete(gasto)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)