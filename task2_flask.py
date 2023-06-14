from flask import Flask, request, jsonify

app = Flask(__name__)

# Dictionary to store registered users
users = {}

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    if username in users:
        return jsonify({'message': 'This user already exists. Please check'}), 400
    
    users[username] = password
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    if username not in users or users[username] != password:
        return jsonify({'message': 'Access denied. Please check the credentials'}), 401
    
    return jsonify({'message': 'Access granted'})

if __name__ == '__main__':
    app.run()
