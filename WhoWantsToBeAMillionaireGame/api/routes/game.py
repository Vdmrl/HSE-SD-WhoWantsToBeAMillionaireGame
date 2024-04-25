from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from services import game

router = APIRouter(
    prefix="",
    tags=["game"]
)

templates = Jinja2Templates(directory="templates")
current_game = game.Game()


@router.get("/", response_class=HTMLResponse)
async def registration(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.get("/{name}/", response_class=HTMLResponse)
async def get_members(request: Request, name: str):
    quest = await current_game.get_question()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": name,
        "question": quest[0],
        "ans1": quest[1],
        "ans2": quest[2],
        "ans3": quest[3],
        "ans4": quest[4],
        "awards": list(reversed(game.win_amounts)),
        "award": game.win_amounts[current_game.round],
        "records": await game.Game.get_records(10)
    })


@router.post("/{name}/{answer}")
async def choose_answer(request: Request, name: str, answer: str):
    await current_game.give_answer(name, int(answer))
    quest = await current_game.get_question()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": name,
        "question": quest[0],
        "ans1": quest[1],
        "ans2": quest[2],
        "ans3": quest[3],
        "ans4": quest[4],
        "awards": list(reversed(game.win_amounts)),
        "award": game.win_amounts[current_game.round],
        "records": await game.Game.get_records(10)
    })


@router.get("/favicon.ico")
async def get_favicon():
    pass
