from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for


from werkzeug.utils import secure_filename



app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = "./static/profile_pics"

SECRET_KEY = "SPARTA"

MONGODB_CONNECTION_STRING = "mongodb+srv://test_ikakomalasari:sparta@test.nrkvr1l.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGODB_CONNECTION_STRING)

db = client.dbsparta_plus_week4


@app.route("/", methods=['GET'])
def home():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])

        return render_template("index.html")
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="There was problem logging you in"))

        
@app.route("/login", methods=['GET'])
def login():
    msg = request.args.get("msg")
    return render_template("login.html", msg=msg)

    
@app.route("/user/<username>", methods=['GET'])
def user(username):
    # an endpoint for retrieving a user's profile information
    # and all of their posts
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        # if this is my own profile, True
        # if this is somebody else's profile, False

        status = username == payload["id"]  

        user_info = db.users.find_one(
            {"username": username}, 
            {"_id": False}
        )

        return render_template(
            "user.html",
             user_info=user_info, 
             status=status
        )

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route("/sign_in", methods=["POST"])
def sign_in():
    # an api endpoint for logging in
    return jsonify({"result": "success"})


@app.route("/sign_up/save", methods=["POST"])
def sign_up():
    # an api endpoint for signing up
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    password_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    # we should save the user to the database
    return jsonify({"result": "success"})


@app.route("/sign_up/check_dup", methods=["POST"])
def check_dup():
    # ID we should check whether or not the id is already taken
    return jsonify({"result": "success"})


@app.route("/update_profile", methods=["POST"])
def save_img():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        # WKita update profil user disini
        return jsonify({
            "result": "success", 
            "msg": "Your profile has been updated"}
        )
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/posting", methods=["POST"])
def posting():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        # Kita buat  post baru disini
        return jsonify({
            "result": "success", 
            "msg": "Posting successful!"}
        )
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/get_posts", methods=["GET"])
def get_posts():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"]
        )
        # Kita mengambil daftar lengkap post disini
        return jsonify({
            "result": "success", 
            "msg": "Successful fetched all posts"}
        )
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/update_like", methods=["POST"])
def update_like():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"]
        )
        # Kita mengganti hitungan like suatu post disini
        return jsonify({
            "result": "success", 
            "msg": "updated"}
        )
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route('/about', methods=["GET"] )
def about():
    return render_template("about.html")

@app.route('/secret', methods=["GET"] )
def secret():
    return render_template("secret.html")
    # token_receive = request.cookies.get("mytoken")
    # try:
    #     payload = jwt.decode(
    #         token_receive, 
    #         SECRET_KEY, 
    #         algorithms=["HS256"]
    #     )
    #     # Kita mengganti hitungan like suatu post disini
    #     return jsonify({
    #         "result": "success", 
    #         "msg": "updated"}
    #     )
    # except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
    #     return redirect(url_for("home"))


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)

