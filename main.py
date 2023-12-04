from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from databases import Database
from aiosqlite import connect



app = FastAPI()
database = Database("sqlite:///./users.db")
metadata = MetaData()



users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("age", Integer),
)


templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup():
    await database.connect()
    engine = create_engine(str(database.url))
    metadata.create_all(engine)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(request: Request, name: str = Form(...), age: int = Form(...)):
    query = users.insert().values(name=name, age=age)
    await database.execute(query)
    return  "Your data saved successfully !!"

