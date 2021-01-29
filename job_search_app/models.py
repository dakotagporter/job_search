from flask_sqlalchemy import SQLAlchemy

# Instantiate SQL Alchemy database
DB = SQLAlchemy()


class Job(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String(100), nullable=False)
    comp = DB.Column(DB.String(100), nullable=True)
    loc = DB.Column(DB.String(100), nullable=False)
    salary = DB.Column(DB.String(100), nullable=True)
    desc = DB.Column(DB.String(1000), nullable=False)
