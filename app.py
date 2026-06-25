from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = "voting_system_secret"

# Initialize counters in session
def get_counters():
    if "eligible" not in session:
        session["eligible"] = 0
    if "not_eligible" not in session:
        session["not_eligible"] = 0
    return session["eligible"], session["not_eligible"]

@app.route("/")
def index():
    get_counters()  # initialize if not set
    return render_template("index.html")

@app.route("/apply", methods=["POST"])
def apply():
    data = request.get_json()
    cnic = data.get("cnic", "").strip().lower()
    age_str = data.get("age", "")

    # OPTION 1 logic — mirrors original Python code exactly
    if cnic == "yes":
        try:
            age = int(age_str)
        except ValueError:
            return jsonify({"status": "error", "message": "Please enter a valid age."})

        if age >= 18:
            session["eligible"] = session.get("eligible", 0) + 1
            session.modified = True
            return jsonify({
                "status": "eligible",
                "message": "You are eligible for the vote ✔",
                "eligible": session["eligible"],
                "not_eligible": session["not_eligible"]
            })
        else:
            session["not_eligible"] = session.get("not_eligible", 0) + 1
            session.modified = True
            return jsonify({
                "status": "not_eligible",
                "message": "You are not eligible for the vote ✘",
                "eligible": session["eligible"],
                "not_eligible": session["not_eligible"]
            })
    else:
        return jsonify({"status": "no_cnic", "message": "First make your CNIC."})

@app.route("/stats")
def stats():
    eligible, not_eligible = get_counters()
    return jsonify({
        "eligible": eligible,
        "not_eligible": not_eligible,
        "total": eligible + not_eligible
    })

@app.route("/reset", methods=["POST"])
def reset():
    session["eligible"] = 0
    session["not_eligible"] = 0
    session.modified = True
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    app.run(debug=True)