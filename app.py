import json
from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, Plan
from planner import generate_plan

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plans.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/history")
def history():
    plans = Plan.query.order_by(Plan.created_at.desc()).all()
    return render_template("history.html", plans=plans)


@app.route("/plan/<int:plan_id>")
def view_plan(plan_id):
    p = Plan.query.get_or_404(plan_id)
    return render_template("plan_view.html", plan=p.to_dict())


@app.route("/api/plan", methods=["POST"])
def api_plan():
    try:
        goal = request.json.get("goal")
        if not goal:
            return jsonify({"error": "No goal provided"}), 400
        plan = generate_plan(goal)
        p = Plan(goal_text=goal, plan_json=json.dumps(plan))
        db.session.add(p)
        db.session.commit()
        return jsonify({"id": p.id, "plan": plan})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/clear_history", methods=["POST"])
def clear_history():
    """Clear all plans from history."""
    try:
        with app.app_context():
            db.session.query(Plan).delete()  # safer for SQLite
            db.session.commit()
        return redirect(url_for("history"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5050)
