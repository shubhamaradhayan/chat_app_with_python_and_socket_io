from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
    # return "<p>Hello, World!</p>"


@app.route("/chat")
def chat():
    return render_template("chat.html")
    # return "<p>Hello, World!</p>"



if __name__ == "__main__":
    app.run(debug=True)