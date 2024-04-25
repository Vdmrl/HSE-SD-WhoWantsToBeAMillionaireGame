from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, JSONResponse
from services import game

router = APIRouter(
    prefix="",
    tags=["game"]
)

templates = Jinja2Templates(directory="templates")
current_game = game.Game()

@router.get("/", response_class=HTMLResponse)
async def get_members(request: Request):
    question = await current_game.get_question()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "question": question[0],
        "ans1": question[1],
        "ans2": question[2],
        "ans3": question[3],
        "ans4": question[4],
        "awards": list(reversed(game.win_amounts)),
        "award": game.win_amounts[current_game.round]
    })


@router.post("/{answer}")
async def choose_answer(request: Request, answer: str):
    print(f"{answer=}")
    current_game.give_answer(int(answer))
    question = await current_game.get_question()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "question": question[0],
        "ans1": question[1],
        "ans2": question[2],
        "ans3": question[3],
        "ans4": question[4],
        "awards": list(reversed(game.win_amounts)),
        "award": game.win_amounts[current_game.round]
    })

@router.get("/favicon.ico")
async def get_favicon():
    pass