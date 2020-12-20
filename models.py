import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from flask_migrate import Migrate
from config import database_setup


database_name = database_setup["database_name_production"]
database_port = database_setup["port"]
database_path = os.environ.get(
    "DATABASE_URL", "postgresql://{}/{}".format(database_port, database_name)
)
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Inhabitant(db.Model):
    __tablename__ = "Inhabitant"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    flat_number = Column(Integer, nullable=False)
    inquiries = db.relationship("Inquiry", backref="inhabitant", lazy=True)

    def __init__(self, email, flat_number, name):
        self.name = name
        self.email = email
        self.flat_number = flat_number

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "email": self.email,
            "flat_number": self.flat_number,
            "name": self.name,
        }

    def __repr__(self):
        return f"{self.name}:{self.email}"


class Inquiry(db.Model):
    __tablename__ = "Inquiry"

    id = Column(Integer, primary_key=True)
    items = Column(String, nullable=False)
    status = Column(String, nullable=True)
    tag = Column(String, nullable=True)
    inquirer_id = Column(
        Integer, db.ForeignKey("Inhabitant.id"), nullable=False
    )

    def __init__(self, inquirer_id, items, status, tag):
        self.inquirer_id = inquirer_id
        self.items = items
        self.status = status
        self.tag = tag

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "inquirer_id": self.inquirer_id,
            "items": self.items,
            "status": self.status,
            "tag": self.tag,
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"Inquiry: {self.id}"
