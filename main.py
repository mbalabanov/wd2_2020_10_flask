from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        username = request.form.get("username")
        print(username)
        return render_template("hello_world.html")
    elif request.method == "GET":
        return render_template("hello_world.html")


@app.route('/about', methods=["GET"])
def about():
    return render_template("about.html")


@app.route('/faq', methods=["GET"])
def faq():
    return render_template("faq.html")


if __name__ == '__main__':
    app.run(host='localhost', port=7890)
