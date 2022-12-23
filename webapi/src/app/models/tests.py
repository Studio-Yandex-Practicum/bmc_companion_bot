from datetime import datetime

from db.pg import db


class Test(db.Model):
    tablename = "tests"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # created_by = db.Column(db.Integer, ForeignKey='user.id')
    updated_at = db.Column(db.DateTime, default=None)
    deleted_at = db.Column(db.DateTime, default=None)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            # created_by=test.created_by,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at
        )

    def from_dict(self, data):
        for field in ['name', ]:
            if field in data:
                setattr(self, field, data[field])
