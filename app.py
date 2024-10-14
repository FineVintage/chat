from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
CORS(app)
socketio = SocketIO(app)

users = []

@app.route('/')
def home():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if username and username not in users:
            users.append(username)
            return redirect(url_for('chat', username=username))
        return 'Username already taken!', 400
    return render_template('register.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@socketio.on('connect')
def handle_connect():
    emit('user_list', users, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    # Remove the user from the list if they disconnect
    username = request.sid  # Using session ID to identify users (custom logic needed)
    if username in users:
        users.remove(username)
    emit('user_list', users, broadcast=True)

@socketio.on('message')
def handle_message(data):
    emit('message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
