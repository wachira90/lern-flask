#!python
from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/', methods=['GET', 'POST'])
def home_get():
    if (request.method == 'GET') :
        data = "This GET hello world"
        return jsonify({'data': data})

    if (request.method == 'POST'):
        req = request.get_json()
        n1 = req['name1']
        data = "This POST hello world " + n1
        return jsonify({'data': data})

# Hash a Password
@app.route('/hash', methods=['GET'])
def hash():
    hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
    return jsonify({'data': hashed_password})

# Hash a Password
@app.route('/verify', methods=['GET'])
def verify():
    hashed_password = 'dddddddfffffffff'
    is_valid = bcrypt.check_password_hash(hashed_password, 'password')
    if(is_valid):
        data = "data valid ok"
        return jsonify({'data': data})
    else:
        data = "data invalid error"
        return jsonify({'data': data})

@app.route('/home/<int:num>', methods=['GET'])
def disp(num):
    return jsonify({'data': num**2})
	# return redirect("/helloworld")

@app.route('/test', methods=['POST'])
def test():
    request_data = request.get_json()
    language = request_data['language']
    framework = request_data['framework']
    python_version = request_data['version_info']['python']
    example = request_data['examples'][0]
    boolean_test = request_data['boolean_test']
    return '''
		The language value is: {}
		The framework value is: {}
		The Python version is: {}
		The item at index 0 in the example list is: {}
		The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)

@app.route('/gggg', methods=['GET'])
def gggg():
    response = jsonify({'message':'unauthorized'})
    return response, 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
'''
https://www.geeksforgeeks.org/password-hashing-with-bcrypt-in-flask/
pip install flask-bcrypt
'''
