from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from services.game import Game

router = APIRouter(
    prefix="",
    tags=["game"]
)

templates = Jinja2Templates(directory="templates")
game = Game()

@router.get("/", response_class=HTMLResponse)
async def get_members(request: Request):
    question = await game.get_question()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "question": question[0],
        "ans1": question[1],
        "ans2": question[2],
        "ans3": question[3],
        "ans4": question[4]
    })


@router.post("/answer1")
def choose_answer1(request: Request):
    pass


@router.post("/answer2")
def choose_answer2(request: Request):
    pass


@router.post("/answer3")
def choose_answer3(request: Request):
    pass


@router.post("/answer4")
def choose_answer4(request: Request):
    pass
