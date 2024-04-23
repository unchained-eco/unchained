from unchained.urls import path

from .views import hello

urlpatterns = [path("/api", hello)]
