from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    active = db.Column(db.Boolean())

    favs = db.relationship("Favorito", backref='user')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            
        }
    
class Personaje(db.Model):
    __tablename__ ='personajes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    specie = db.Column(db.String(200), nullable=False)
    height = db.Column(db.String, nullable=False)
    birth_year = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)

    favorite = db.relationship("Favorito", backref='personajes')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "specie": self.specie,
            "height": self.height,
            "birth_year": self.birth_year,
            "gender": self.gender
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Planeta(db.Model):
    __tablename__ ='planetas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(200), nullable=False)
    population = db.Column(db.String, nullable=False)
    terreno = db.Column(db.String, nullable=False)

    favoritos = db.relationship("Favorito", backref='planetas')
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "terreno": self.terreno
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Favorito(db.Model):
    __tablename__ ='favoritos'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    favs_personajes = db.Column(db.Integer, db.ForeignKey('personajes.id'), primary_key=True)
    favs_planetas = db.Column(db.Integer, db.ForeignKey('planetas.id'), primary_key=True)

    def to_dict(self):
        return {
            "id": self.id,
            "favs_personajes": self.favs_personajes,
            "favs_planetas": self.favs_planetas,
            
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    


