# Aqui estão os testes para a aplicação de gerenciamento de gastos. Esses testes verificam se as funcionalidades de adicionar, editar e deletar gastos estão funcionando corretamente.

import os
import sys
from datetime import date

import pytest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from app import app, db
from models import Gastos


@pytest.fixture
def client(tmp_path):
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{tmp_path / 'test.db'}"

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client


def test_adicionar_gasto(client):
    response = client.post(
        "/adicionar",
        data={
            "valorGasto": "45.00",
            "dataGasto": "2026-04-11",
            "descGasto": "Uber",
            "categoriaSelecionada": "",
            "novaCategoria": "Transporte",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Uber" in response.data
    assert b"Transporte" in response.data
    assert b"R$45.0" in response.data


def test_editar_gasto(client):
    with app.app_context():
        gasto = Gastos(
            valor=50.0, data=date(2026, 4, 10), descricao="Almoco", categoria="Comida"
        )
        db.session.add(gasto)
        db.session.commit()
        gasto_id = gasto.id

    response = client.post(
        f"/editar/{gasto_id}",
        data={
            "valorGasto": "55.00",
            "dataGasto": "2026-04-12",
            "descGasto": "Almoco atualizado",
            "categoriaSelecionada": "Comida",
            "novaCategoria": "",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Almoco atualizado" in response.data
    assert b"R$55.0" in response.data
    assert b"2026/04/12" in response.data


def test_deletar_gasto(client):
    with app.app_context():
        gasto = Gastos(
            valor=30.0,
            data=date(2026, 4, 10),
            descricao="Cafe",
            categoria="Alimentacao",
        )
        db.session.add(gasto)
        db.session.commit()
        gasto_id = gasto.id

    response = client.get(f"/deletar/{gasto_id}", follow_redirects=True)

    assert response.status_code == 200
    assert b"Cafe" not in response.data
    assert b"Alimentacao" not in response.data
