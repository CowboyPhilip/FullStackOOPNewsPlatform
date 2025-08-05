from app.server import App
from app.routes.main import routes
app_instance = App(routes)


app = app_instance.app

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)