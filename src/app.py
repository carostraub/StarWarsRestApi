"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from models import db, Personaje
from models import db, Planeta
from models import db, Favorito
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    resultado = [user.serialize() for user in users]
    return jsonify(resultado), 200

@app.route('/personajes', methods=['GET'])
def obtener_personajes():

    personajes = Personaje.query.all() 
    personajes_serializable = list(map(lambda pe: pe.to_dict(), personajes))
    return jsonify(personajes_serializable), 200

def agregar_personaje():

    datos = request.get_json() 

    if not 'name' in datos or not datos['name']:
        return jsonify({ "msg": "Field name is required"}), 400
    if not 'specie' in datos or not datos['specie']:
        return jsonify({ "msg": "Field specie is required"}), 400
    if not 'height' in datos or not datos['height']:
        return jsonify({ "msg": "Field height is required"}), 400
    if not 'birth_year' in datos or not datos['birth_year']:
        return jsonify({ "msg": "Field birth year is required"}), 400
    if not 'gender' in datos or not datos['gender']:
        return jsonify({ "msg": "Field gender is required"}), 400

    personaje = Personaje()
    personaje.name = datos['name']
    personaje.specie = datos['specie']
    personaje.height = datos['height']
    personaje.birth_year = datos['birth_year']
    personaje.gender = datos['gender']
    personaje.save()

   

    return jsonify({ "status": "success", "message": "Personaje Agregado"}), 201


@app.route('/personajes/<int:personaje_id>', methods=['GET'])
def persona_especifico(persona_id):
    persona = Personaje.query.get(persona_id)
    personaje_serializable = list(map(lambda persojaesp: persojaesp.to_dict(), persona))
    return jsonify(personaje_serializable), 200

@app.route('/planetas', methods=['GET'])
def obtener_planetas():

    planetas = Planeta.query.all() 
    planetas_serializable = list(map(lambda pl: pl.to_dict(), planetas))
    return jsonify(planetas_serializable), 200

def agregar_planetas():

    datos = request.get_json() 

    if not 'name' in datos or not datos['name']:
        return jsonify({ "msg": "Field name is required"}), 400
    if not 'climate' in datos or not datos['climate']:
        return jsonify({ "msg": "Field climate is required"}), 400
    if not 'population' in datos or not datos['population']:
        return jsonify({ "msg": "Field population is required"}), 400
    if not 'terreno' in datos or not datos['terreno']:
        return jsonify({ "msg": "Field terreno is required"}), 400

    planeta = Planeta()
    planeta.name = datos['name']
    planeta.climate = datos['climate']
    planeta.population = datos['population']
    planeta.terreno = datos['terreno']
    planeta.save()

   

    return jsonify({ "status": "success", "message": "Planeta Agregado"}), 201

@app.route('/planetas/<int:planeta_id>', methods=['GET'])
def planeta_especifico(planeta_id):
    planet = Planeta.query.get(planeta_id)
    planeta_serializable = list(map(lambda planetesp: planetesp.to_dict(), planet))
    return jsonify(planeta_serializable), 200


@app.route('/users/favoritos', methods=['GET'])
def obtener_favoritos():

    favoritos = Favorito.query.all() 
    favoritos_serializable = list(map(lambda f: f.to_dict(), favoritos))
    return jsonify(favoritos_serializable), 200

@app.route('/favoritos/planetas/<int:planeta_id>', methods=['POST'])
def agregar_favoritospl():

    username = request.json.get("username") 
    user = User.query.get(username)
    planeta = Planeta.query.get(id)

    favorito = Favorito(username=user.username, planeta_id=id)
    db.session.add(favorito)
    db.session.commit()

    return jsonify({"msg":f"Planeta: {planeta.name} se agrego a tus favoritos"})


@app.route('/favoritos/personajes/<int:personaje_id>', methods=['POST'])
def agregar_favoritospe():

    username = request.json.get("username") 
    user = User.query.get(username)
    personaje = Personaje.query.get(id)

    favorito = Favorito(username=user.username, personaje_id=id)
    db.session.add(favorito)
    db.session.commit()
    
    return jsonify({"msg":f"Personaje: {personaje.name} se agrego a tus favoritos"})
   

@app.route('/favoritos/planetas/<int:planeta_id>', methods=['DELETE'])
def eliminar_favoritospl():

    username = request.json.get("username") 
    user = User.query.get(username)
    planeta = Planeta.query.get(id)

    favorito = Favorito.query.filter_by(username=user.username, planeta_id=id)
    db.session.delete(favorito)
    db.session.commit()

    return jsonify({"msg":f"Planeta: {planeta.name} se elimino a tus favoritos"})


@app.route('/favoritos/personajes/<int:personaje_id>', methods=['DELETE'])
def eliminar_favoritospe():

    username = request.json.get("username") 
    user = User.query.get(username)
    personaje = Personaje.query.get(id)

    favorito = Favorito.query.filter_by(username=user.username, personaje_id=id)
    db.session.delete(favorito)
    db.session.commit()

    return jsonify({"msg":f"Personaje: {personaje.name} se elimino a tus favoritos"})




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
