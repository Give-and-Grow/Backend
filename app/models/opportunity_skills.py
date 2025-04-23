# Backend/app/models/opportunity_skills.py
opportunity_skills = db.Table(
    "opportunity_skills",
    db.Column(
        "opportunity_id",
        db.Integer,
        db.ForeignKey("opportunity.id"),
        primary_key=True,
    ),
    db.Column(
        "skill_id", db.Integer, db.ForeignKey("skill.id"), primary_key=True
    ),
)
