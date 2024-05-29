INSTALLED_APPS = ["unchainedproject.app"]
MIDDLEWARE = ["unchainedproject.middlewares.m1.CustomMiddleware1"]
DEBUG: bool = True
ROOT_URLCONF: str = "unchainedproject.routes"
PROJECT_NAME: str = "unchainedproject"
