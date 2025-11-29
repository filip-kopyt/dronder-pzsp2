import os
from flask_sqlalchemy import SQLAlchemy
from sqlmodel import SQLModel

DATABASE_URL = f"postgresql+psycopg2://{os.environ['DB_USER']}:{
    os.environ['DB_PASSWORD']}@database/{os.environ['DB_NAME']}"
db = SQLAlchemy(model_class=SQLModel, engine_options={"echo": True})
