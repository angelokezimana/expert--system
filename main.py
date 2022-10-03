import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from expert_system import InreferenceEngine, Patient
from schemas import PatientForm


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def post_index(
    request: Request, form_data: PatientForm = Depends(PatientForm.as_form)
):
    engine = InreferenceEngine()
    engine.reset()
    engine.declare(
        Patient(
            age=form_data.age,
            glycemie=form_data.glycemie,
            shakiness=form_data.shakiness,
            hunger=form_data.hunger,
            sweating=form_data.sweating,
            headach=form_data.headach,
            diabetic_parents=form_data.diabetic_parents,
            pale=form_data.pale,
            urination=form_data.urination,
            thirst=form_data.thirst,
            blurred_vision=form_data.blurred_vision,
            dry_mouth=form_data.dry_mouth,
            smelling_breath=form_data.smelling_breath,
            shortness_of_breath=form_data.shortness_of_breath,
        )
    )
    engine.run()

    results: list
    is_sick: bool

    if not engine.results:
        results = ["The child is in good health"]
        is_sick = False
    else:
        results = engine.results
        is_sick = True

    return templates.TemplateResponse(
        "index.html", {"request": request, "is_sick": is_sick, "results": results}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
