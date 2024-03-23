from flask import Flask, render_template, request,session, redirect,sessions, url_for
from flask_socketio import SocketIO, join_room, send, leave_room
from string import ascii_uppercase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

rooms = {}
print("rooms", rooms)
@app.route("/", methods=["POST","GET"])
def index():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code", False)
        room_id = request.form.get("room_id")
        join = request.form.get("join",  False)
        create = request.form.get("create", False)

        if join is not False and code is "":
            return render_template("index.html", error="Please Enter Room Id to Join", name=name)
        if create is not False :
            rooms[room_id] = {'members':0, 'messages':[]}

        elif code not in rooms:
            return render_template("index.html", error="Please Enter a valid Room Id to Join", name=name)

        session["name"] = name
        session["room"] = room_id       

        print('rooms', rooms)

        return redirect(url_for('chat'))
    return render_template("index.html", session=session)



@app.route("/chat")
def chat():
    if not session:
        return redirect('/')
    return render_template("chat.html", name=session["name"], room_id=session["room"])




@app.route("/existRoom")
def existRoom():
    session.clear()
    return redirect('/')




if __name__ == "__main__":
    socketio.run(app, debug=True)