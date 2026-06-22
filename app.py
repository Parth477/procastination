from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# ---------- LOGIN ----------
@app.route("/")
def login():
    return render_template("login.html")


# ---------- SIGNUP ----------
@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        f = open("users.txt","a")
        f.write(username + "," + password + "\n")
        f.close()

        return redirect("/")

    return render_template("signup.html")


# ---------- LOGIN CHECK ----------
@app.route("/dashboard", methods=["POST"])
def dashboard():

    username = request.form["username"]
    password = request.form["password"]

    try:
        f = open("users.txt","r")
        users = f.readlines()
        f.close()
    except:
        users = []

    for user in users:
        u,p = user.strip().split(",")

        if u == username and p == password:
            return redirect("/dashboardview/"+username)

    return "<h1>Login Failed</h1>"


# ---------- DASHBOARD VIEW ----------
@app.route("/dashboardview/<username>")
def dashboardview(username):

    try:
        f = open("tasks.txt", "r")
        lines = f.readlines()
        f.close()
    except:
        lines = []

    tasks = []

    for line in lines:
        parts = line.strip().split(":")

        if parts[0] == username:
            if len(parts) == 3:
                tasks.append({"task": parts[1], "done": True})
            else:
                tasks.append({"task": parts[1], "done": False})

    total = len(tasks)
    done = len([t for t in tasks if t["done"]])

    score = 0
    if total != 0:
        score = int((done / total) * 100)

    return render_template(
        "dashboard.html",
        user=username,
        tasks=tasks,
        score=score
    )

  


# ---------- ADD TASK ----------
@app.route("/addtask", methods=["POST"])
def addtask():

    task = request.form["task"]
    username = request.form["username"]

    f = open("tasks.txt","a")
    f.write(username + ":" + task + "\n")
    f.close()

    return redirect("/dashboardview/"+username)


# ---------- COMPLETE TASK ----------
@app.route("/complete", methods=["POST"])
def complete():

    task = request.form["task"]
    username = request.form["username"]

    f = open("tasks.txt","r")
    lines = f.readlines()
    f.close()

    f = open("tasks.txt","w")

    for line in lines:
        if line.strip() == username + ":" + task:
            f.write(username + ":" + task + ":done\n")
        else:
            f.write(line)

    f.close()

    return redirect("/dashboardview/"+username)

@app.route("/delete", methods=["POST"])
def delete():

    task = request.form["task"]
    username = request.form["username"]

    f = open("tasks.txt","r")
    lines = f.readlines()
    f.close()

    f = open("tasks.txt","w")

    for line in lines:
        if line.strip().startswith(username + ":" + task):
            continue
        else:
            f.write(line)

    f.close()

    return redirect("/dashboardview/"+username)

app.run(debug=True)