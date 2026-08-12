from flask import Flask, render_template, request
from main import run_repo_health

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    report = ""

    if request.method == "POST":
        repo_url = request.form["repo_url"]

        try:
            report = run_repo_health(repo_url)
        except Exception as e:
            report = str(e)

    return render_template("index.html", report=report)


if __name__ == "__main__":
    app.run(debug=True)