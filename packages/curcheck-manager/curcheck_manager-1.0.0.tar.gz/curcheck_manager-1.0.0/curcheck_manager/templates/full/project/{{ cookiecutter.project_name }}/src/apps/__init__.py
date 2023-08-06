""" Сборка всех приложений проекта """

from .main.views import router as main_router

routers = [main_router]
models = ["src.apps.main.models"]
