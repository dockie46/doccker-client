import uvicorn
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from middlewares.loggingMiddleware import LoggingMiddleware
from dependencies import get_docker_client, get_prediction_manager
from routers import containers, images


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(containers.router)
app.include_router(images.router)

app.add_middleware(LoggingMiddleware)


@app.get("/")
def render_root(request: Request):
    """
    Root endpoint that returns a simple greeting message.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/pages/images")
def render_images(request: Request, docker_client=Depends(get_docker_client)):
    """
    Root endpoint that returns a list of images.
    """
    return templates.TemplateResponse("images.html", {
        "request": request,
        "images": docker_client.list_images(),
        "docker_ready": docker_client.is_docker_online()
    })


@app.get("/pages/containers")
def render_containers(request: Request, docker_client=Depends(get_docker_client)):
    """
    Root endpoint that returns a list of containers.
    """
    return templates.TemplateResponse("containers.html", {
        "request": request,
        "containers": docker_client.list_containers(),
        "docker_ready": docker_client.is_docker_online()
    })


@app.get("/pages/predictions", response_class=HTMLResponse)
def render_prediction(request: Request, client=Depends(get_prediction_manager)):
    """
    Render the prediction page. If prediction fails, show error on the page.
    """
    try:
        result = client.predict_memory_usage()
        return templates.TemplateResponse("prediction.html", {
            "request": request,
            "result": result,      # Pydantic object
            "error": None          # No error
        })
    except Exception as e:
        return templates.TemplateResponse("prediction.html", {
            "request": request,
            "result": None,
            "error": str(e)        # Pass error message to template
        })


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
