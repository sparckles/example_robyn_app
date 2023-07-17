
from datetime import datetime
from robyn import Robyn, jsonify
from sqlalchemy import Date
from .models import SessionLocal, Crime
from .crud import get_crimes, create_crime, get_crime
import json

app = Robyn(__file__)

@app.get("/", const=True)
def index():
    return "Hello World!"

@app.get("/crimes")
async def crimes():
    with SessionLocal() as db:
        crimes = get_crimes(db)

    print(crimes)
    return jsonify({
        "crimes": [str(i) for i in crimes ]
    })
    # return crimes

@app.get("/crimes/:crime_id")
async def crime(request):
    crime_id = int(request.path_params.get("crime_id"))

    with SessionLocal() as db:
        crime_ = get_crime(db, crime_id=crime_id)

    return crime_

@app.post("/crimes")
async def post_crimes(request):
    crime = json.loads(request.body)
    crime["date"] = datetime.strptime(crime["date"], "%d/%m/%y").date()
    crime_to_insert = Crime(**crime)

    with SessionLocal() as db:
        crime_ = create_crime(db, crime_to_insert)

    return crime_


if __name__ == "__main__":
    app.start(port=8081)

            
