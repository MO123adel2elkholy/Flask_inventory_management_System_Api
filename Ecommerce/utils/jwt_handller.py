from flask_jwt_extended import JWTManager

jwt = JWTManager()
print("DEBUG: jwt object id in jwt_handller:", id(jwt))
