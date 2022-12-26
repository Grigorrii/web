import uvicorn
from setting_web import app
from routers.users.manager_routers import router as RouterUsers
from routers.documents.manager_routers import router as RouterDocument
from routers.workspace.manager_routers import router as RouterWorkSpace


app.include_router(RouterUsers)
app.include_router(RouterDocument)
app.include_router(RouterWorkSpace)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
