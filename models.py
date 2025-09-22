import datetime
import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal_text = db.Column(db.String(1000), nullable=False)
    plan_json = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "goal_text": self.goal_text,
            "plan": json.loads(self.plan_json),
            "created_at": self.created_at.isoformat()
        }
