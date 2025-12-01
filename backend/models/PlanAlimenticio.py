from extensions.db import db

class PlanAlimenticio(db.Model):
    __tablename__ = "plan_alimenticio"

    id = db.Column(db.Integer, primary_key=True)
    objetivo = db.Column(db.String(100))
    mascota_id = db.Column(db.Integer, db.ForeignKey("mascota.id"), nullable=False)

