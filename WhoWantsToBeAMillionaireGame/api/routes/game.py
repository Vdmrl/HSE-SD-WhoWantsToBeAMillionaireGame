from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, JSONResponse
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


@router.post("/{answer}")
def choose_answer( answer: str):
    print(f"{answer=}")
    game.give_answer(int(answer))

@router.get("/next")
async def get_question():
    question = await game.get_question()
    return JSONResponse({
        "question": question[0],
        "ans1": question[1],
        "ans2": question[2],
        "ans3": question[3],
        "ans4": question[4]
    })