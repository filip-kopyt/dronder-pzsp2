import logging
from dataclasses import dataclass
from http import HTTPStatus
from typing import Annotated, Self

import pydantic_core
from flask import Blueprint, Response, jsonify, request
from pydantic import (
    BaseModel,
    EmailStr,
    StringConstraints,
    ValidationError,
    model_validator,
)
from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, SQLModel, select

from db import db

bp = Blueprint("auth", __name__, url_prefix="/auth")


class RegisterForm(BaseModel):
    first_name: Annotated[str, StringConstraints(strip_whitespace=True)]
    last_name: Annotated[str, StringConstraints(strip_whitespace=True)]
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=9)]
    re_password: Annotated[str, StringConstraints(min_length=9)]

    @model_validator(mode="after")
    def validate_same_password(self) -> Self:
        if self.password != self.re_password:
            error = pydantic_core.InitErrorDetails(
                type=pydantic_core.PydanticCustomError(
                    "value_error",
                    "Passwords do not match",
                    {"reason": "Passwords do not match"},
                ),
                loc=("re_password",),
                input=self,
                ctx={"reason": "Passwords do not match"},
            )
            raise ValidationError.from_exception_data(
                self.__class__.__name__, [error])
        return self


class LoginForm(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=9)]


@dataclass
class User(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)


@bp.route("/register", methods=["POST"])
def register_user():
    form: RegisterForm
    try:
        form = RegisterForm(**(request.json or {}))  # pyright: ignore[reportUnknownArgumentType]  # noqa: E501
    except ValidationError as e:
        logging.info(f"Bad register_user request form\n{e}")
        return Response(
            e.json(include_input=False),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

    try:
        user = User.model_validate(form)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
    except IntegrityError as e:
        return jsonify(
            {
                "error": "IntegrityError",
                "message": str(e.orig),
            }
        ), HTTPStatus.BAD_REQUEST
    return jsonify(user.model_dump()), HTTPStatus.CREATED


# NOTE: Development only
# FIX: Remove or authenticate
@bp.route("/list", methods=["GET"])
def list_users():
    users = db.session.execute(select(User).order_by(User.email)).scalars()
    return jsonify(users.all())


@bp.route("/login", methods=["POST"])
def login_user():
    form: LoginForm
    try:
        form = LoginForm(**(request.json or {}))  # pyright: ignore[reportUnknownArgumentType]  # noqa: E501
    except ValidationError as e:
        logging.info(f"Bad register_user request form\n{e}")
        return Response(
            e.json(include_input=False),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

    user = db.session.scalars(
        select(User).filter_by(email=form.email)).one_or_none()

    if user is None:
        return "User doen't exists", HTTPStatus.NOT_FOUND

    if user.password != form.password:
        return "Invalid password", HTTPStatus.BAD_REQUEST

    # TODO: Authentication with JWT
    return f"User {form.email} logged in", HTTPStatus.OK
