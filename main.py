from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Base de datos SQLite en un archivo
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "telefono": self.telefono}

# Crear la base de datos y las tablas si no existen
with app.app_context():
    if not os.path.exists('users.db'):
        db.create_all()
        print("Base de datos creada.")

# Endpoint para obtener un usuario por ID
@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

# Endpoint para crear un usuario
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], telefono=data['telefono'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status": "Usuario creado", "user": new_user.to_dict()}), 201

# Endpoint para actualizar un usuario
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.get_json()
    user.name = data.get('name', user.name)  # Actualiza el nombre si se proporciona
    user.telefono = data.get('telefono', user.telefono)  # Actualiza el teléfono si se proporciona
    db.session.commit()
    
    return jsonify({"status": "Usuario actualizado", "user": user.to_dict()}), 200

# Endpoint para eliminar un usuario
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"status": "Usuario eliminado"}), 200

if __name__ == '__main__':
    app.run(debug=True)
