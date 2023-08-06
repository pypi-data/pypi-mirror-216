from .settings import settings

TORTOISE_ORM = {
    "connections": {"default": settings.DB_URL},
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
