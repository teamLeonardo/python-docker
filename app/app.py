from flask import Flask, request ,jsonify
from flask_jwt_extended import JWTManager , create_access_token, jwt_required , get_jwt_identity

app = Flask(__name__)
# crear lista de usuarios del servidor
listUser = [
	{ "id": "1", "username": "leonardo" ,"password" : "123" }
]

# Configura la extensión Flask-JWT-Extended
app.config["JWT_SECRET_KEY"] = "token-seguro" # ¡Cambia las palabras "super-secret" por otra cosa!
jwt = JWTManager(app)


@app.route('/')
def hello():
	return "Hello World! asdasdasd"


# Crea una ruta para autenticar a los usuarios y devolver el token JWT.
# La función create_access_token() se utiliza para generar el JWT.
@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    # Filtrar usuarios por nombre de usuario y contraseña
    resultados = list(filter(lambda x: x["username"] == username and x["password"] == password, listUser))
    
    if len(resultados) > 0:
        user_id = resultados[0]["id"]  # Accede al primer usuario encontrado
        access_token = create_access_token(identity=user_id)
        return jsonify({"token": access_token, "user_id": user_id})
    else:
        return jsonify({"message": "Usuario o contraseña incorrectos"}), 401

   

# Protege una ruta con jwt_required, bloquea las peticiones
# sin un JWT válido presente.
@app.route('/user', methods=["GET"])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    
    user = list(filter(lambda x: x["id"] == current_user_id, listUser))
    
    if len(user) > 0:
        user_id = user[0]["id"]  # Accede al primer usuario encontrado
        return jsonify({"id": user_id, "username": user[0]['username']}), 200
    else:
        return jsonify({"message": "no se encontro usuario"}), 401


   

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
