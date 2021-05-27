from flask import Flask, jsonify, request, make_response
import jwt 
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = "python+iot"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') # http://127.0.0.1:5000/route?token=4038953jfsodfjso
        print("TOKEN DENTRO DO DECORADOR {}".format(token))
        if not token:
            return jsonify({'message': 'Falta de Token'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            print("DATA {}".format(data))
        except:
            return jsonify({'message': 'Token esta invalido'})

        return f(*args, **kwargs)

    return decorated

@app.route('/naoProtegido')
def naoProtegido():
    return jsonify({'message': 'Em nenhum lugar vejo isso!!!'})

@app.route('/protegido')
@token_required
def protegido():
    return jsonify({'message': 'Isso somente eh validado pela pessoa com token valido'})
 
@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'estudosJWT':
        token = jwt.encode({'usuario': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)}, app.config['SECRET_KEY'], algorithm='HS256')
        print(token)
        return jsonify({'token': jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])}) 

    return make_response('Verifique o login!!!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

if __name__ == "__main__":
    app.run(debug=True)