# Aqui estão definidas as classes de modelo para a aplicação, que funcionam como a estrutura para os dados.
# Cada classe representa uma tabela no banco de dados, e os atributos da classe correspondem às colunas da tabela.

from flask_sqlalchemy import SQLAlchemy
from db import db

class Gastos(db.Model):
    __tablename__ = 'gastos'

    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False)
    descricao = db.Column(db.String(50))
    categoria = db.Column(db.String(20), nullable=False, unique=False)

    def __repr__(self):
        return f"<Gastos {self.id}>"