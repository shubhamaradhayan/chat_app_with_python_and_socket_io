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
        code = request.form.get("join_code", False)
        room_id = request.form.get("create_room_id")
        join = request.form.get("join",  False)
        create = request.form.get("create", False)

        if join is not False and code is "":
            return render_template("index.html", error="Please Enter Room Id to Join", name=name)
        if create is not False :
            rooms[room_id] = {'members':0, 'messages':[]}

        elif code not in rooms:
            return render_template("index.html", error="Please Enter a valid Room Id to Join", name=name)
        
        if code == "" and room_id != "" :
            session["room"] = room_id
        elif code != "" and room_id == "":
            session["room"] = code
        session["name"] = name
     

        print('rooms', rooms)

        return redirect(url_for('chat'))
    return render_template("index.html", session=session)



@app.route("/chat")
def chat():

    if not session:
        return redirect('/')
    return render_template("chat.html", name=session.get("name"), room_id=session.get("room"))




@app.route("/existRoom")
def existRoom():
    session.clear()
    return redirect('/')




@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")

    if not room or not name:
        return
    
    if room not in rooms:
        leave_room(room)
        return

    print(room, name )
    join_room(room)
    send({"name":name, "message":"has entered the room "}, to=room)
    rooms[room]["members"] +=1
    # print(f"{name} has entered the room")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0 :
            del rooms[room]

    send({"name":name, "message":"has left the room "}, to=room)
    # print(f"{name} has left the room")



@socketio.on("message")
def message(data):
    room = session.get("room")
    name = session.get("name")
    
    if room not in rooms:
        return


    send({"name":name, "message": data['data']}, to=room)
    rooms[room]["messages"].append({"name":name, "message": data['data']})
    print(f"Msg Data is {data}")




if __name__ == "__main__":
    socketio.run(app, debug=True)