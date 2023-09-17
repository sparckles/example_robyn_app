import json
from datetime import datetime

from robyn import Robyn, jsonify
from sqlalchemy import Date

import crud

from .models import Crime, SessionLocal

app = Robyn(__file__)


from robyn.robyn import Request, Response
from sqlalchemy.orm import Session


@app.post("/crimes")
async def add_crime(request):
    with SessionLocal() as db:
        crime = json.loads(request.body)
        insertion = crud.create_crime(db, crime)

    if insertion is None:
        raise Exception("Crime not added")

    return {
        "description": "Crime added successfully",
        "status_code": 200,
    }


@app.get("/crimes")
async def get_crimes(request):
    with SessionLocal() as db:
        skip = request.queries.get("skip", 0)
        limit = request.queries.get("limit", 100)
        crimes = crud.get_crimes(db, skip=skip, limit=limit)

    return crimes


@app.get("/crimes/:crime_id", auth_required=True)
async def get_crime(request):
    crime_id = int(request.path_params.get("crime_id"))
    with SessionLocal() as db:
        crime = crud.get_crime(db, crime_id=crime_id)

    if crime is None:
        raise Exception("Crime not found")

    return crime


@app.put("/crimes/:crime_id")
async def update_crime(request):
    crime = json.loads(request.body)
    crime_id = int(request.path_params.get("crime_id"))
    with SessionLocal() as db:
        updated_crime = crud.update_crime(db, crime_id=crime_id, crime=crime)
    if updated_crime is None:
        raise Exception("Crime not found")

    return updated_crime


@app.delete("/crimes/{crime_id}")
async def delete_crime(request):
    crime_id = int(request.path_params.get("crime_id"))
    with SessionLocal() as db:
        success = crud.delete_crime(db, crime_id=crime_id)
    if not success:
        raise Exception("Crime not found")

    return {"message": "Crime deleted successfully"}


from robyn.authentication import AuthenticationHandler, BearerGetter, Identity


class BasicAuthHandler(AuthenticationHandler):
    def authenticate(self, request):
        token = self.token_getter.get_token(request)
        print(token)

        try:
            # payload = decode_access_token(f"{ token }")
            if token:
                return Identity(claims={"user": "su"})
        except:
            return None
        #    username = json.loads( request.body )["username"]
        #    if payload["sub"] == username:
        username = "superman"
        if username != "batman":
            return None

        return Identity(claims={"username": username})


#        except:
#            return None

app.configure_authentication(BasicAuthHandler(token_getter=BearerGetter()))


@app.get("/needs_authentication", auth_required=True)
def needs_authentication(request):
    return "You are authenticated!"


@app.get("/users/me", auth_required=True)
async def get_current_user(request):
    user = request.identity.claims["user"]
    return user


import pathlib

from robyn.templating import JinjaTemplate, TemplateInterface


@app.get("/template")
def template(request):
    current_file_path = pathlib.Path(__file__).parent.resolve()
    templating_folder = current_file_path / "templates"
    return JinjaTemplate(templating_folder).render_template(
        "index.html", request=request
    )


def view(request):
    def get():
        return "Hello World!"

    def post():
        return "Hello World! THis is a post method"


app.add_view("/view", view)


from robyn import SubRouter

frontend = SubRouter(__name__, prefix="/frontend")

import pathlib

from robyn.templating import JinjaTemplate, TemplateInterface


@frontend.get("/frontend")
def frontend_template(request):
    return "Hello World!"


app.include_router(frontend)


if __name__ == "__main__":
    app.start(port=8081)
