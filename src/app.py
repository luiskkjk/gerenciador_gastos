# Este arquivo define as rotas e a lógica principal da aplicação Flask.
# Ele importa as classes de modelo do arquivo models.py para interagir com o banco de dados e renderizar as páginas HTML.

from flask import Flask, render_template, request, redirect, url_for

try:
    from src.db import db
    from src.models import Gastos
except ImportError:
    from db import db
    from models import Gastos
from datetime import datetime
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dados.db"
db.init_app(app)


def get_categorias():
    categorias = db.session.query(Gastos.categoria).distinct().all()
    return [categoria for (categoria,) in categorias if categoria]


@app.route("/")
def home():
    gastos = db.session.query(Gastos).all()
    total_gasto = sum(gasto.valor or 0 for gasto in gastos)

    # Apresentação de dados da API do Banco Central para mostrar a SELIC, CDI, IPCA e Dólar na página inicial.

    # SELIC
    resposta_selic = requests.get(
        "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1?formato=json"
    )
    dados_selic = resposta_selic.json()
    selic = dados_selic[0]["valor"]
    data_selic = dados_selic[0]["data"]

    # CDI
    resposta_cdi = requests.get(
        "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4389/dados/ultimos/1?formato=json"
    )
    dados_cdi = resposta_cdi.json()
    cdi = dados_cdi[0]["valor"]
    data_cdi = dados_cdi[0]["data"]

    # IPCA
    resposta_ipca = requests.get(
        "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json"
    )
    dados_ipca = resposta_ipca.json()
    ipca = dados_ipca[0]["valor"]
    data_ipca = dados_ipca[0]["data"]

    # Dólar
    resposta_dolar = requests.get(
        "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados/ultimos/1?formato=json"
    )
    dados_dolar = resposta_dolar.json()
    dolar = dados_dolar[0]["valor"]
    data_dolar = dados_dolar[0]["data"]

    return render_template(
        "home.html",
        gastos=gastos,
        total_gasto=total_gasto,
        selic=selic,
        data_selic=data_selic,
        cdi=cdi,
        data_cdi=data_cdi,
        ipca=ipca,
        data_ipca=data_ipca,
        dolar=dolar,
        data_dolar=data_dolar,
    )


@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if request.method == "GET":
        categorias = get_categorias()
        return render_template("adicionar.html", categorias=categorias)
    elif request.method == "POST":
        data_str = request.form.get(
            "dataGasto"
        )  # Recebe a data como string no formato 'YYYY-MM-DD'
        if not data_str:
            return "Data é obrigatória!"

        valor = request.form["valorGasto"]
        data = datetime.strptime(data_str, "%Y-%m-%d").date()
        descricao = request.form["descGasto"]

        categoria_selecionada = request.form.get("categoriaSelecionada", "")
        nova_categoria = request.form.get("novaCategoria", "").strip()
        if nova_categoria:
            categoria = nova_categoria
        else:
            categoria = categoria_selecionada

        if not categoria:
            return "Categoria é obrigatória!"

        novo_gasto = Gastos(
            valor=valor, data=data, descricao=descricao, categoria=categoria
        )
        db.session.add(novo_gasto)
        db.session.commit()

        return redirect(url_for("home"))


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    gasto = db.session.query(Gastos).filter_by(id=id).first()
    categorias = get_categorias()
    if request.method == "GET":
        return render_template("editar.html", gasto=gasto, categorias=categorias)
    elif request.method == "POST":
        valor = request.form["valorGasto"]
        data_str = request.form["dataGasto"]
        descricao = request.form["descGasto"]

        categoria_selecionada = request.form.get("categoriaSelecionada", "")
        nova_categoria = request.form.get("novaCategoria", "").strip()
        if nova_categoria:
            categoria = nova_categoria
        else:
            categoria = categoria_selecionada

        data_objeto = datetime.strptime(data_str, "%Y-%m-%d").date()

        gasto.valor = valor
        gasto.data = data_objeto
        gasto.descricao = descricao
        gasto.categoria = categoria
        db.session.commit()
        return redirect(url_for("home"))


@app.route("/deletar_categoria", methods=["POST"])
def deletar_categoria():
    categoria = request.form.get("categoriaParaApagar", "").strip()
    gasto_id = request.form.get("editarId")
    if categoria:
        gastos = db.session.query(Gastos).filter_by(categoria=categoria).all()
        for gasto in gastos:
            gasto.categoria = ""
        db.session.commit()
    if gasto_id and gasto_id.isdigit():
        return redirect(url_for("editar", id=int(gasto_id)))
    return redirect(url_for("home"))


@app.route("/deletar/<int:id>")
def deletar(id):
    gasto = db.session.query(Gastos).filter_by(id=id).first()
    db.session.delete(gasto)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
