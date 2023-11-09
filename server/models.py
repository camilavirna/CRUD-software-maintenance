from . import db


class User(db.Model):
    __tablename__ = "USER"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(20))

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "nome": self.nome,
            "telefone": self.telefone,
        }
