from flask_sqlalchemy import SQLAlchemy
from sqlmodel import SQLModel


DATABASE_URL = "sqlite:///:memory:"
db = SQLAlchemy(model_class=SQLModel)
