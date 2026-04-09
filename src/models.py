from flask_sqlalchemy import SQLAlchemy
from db import db

class Gastos(db.Model):
    __tablename__ = 'gastos'

    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False)
    descricao = db.Column(db.String(50))
    categoria = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return f"<{self.nome}>"