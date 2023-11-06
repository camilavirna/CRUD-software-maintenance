from . import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(20))

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "nome": self.nome,
            "telefone": self.telefone,
        }
