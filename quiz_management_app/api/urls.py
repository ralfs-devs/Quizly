"""URL Routing for the quiz_management_app."""

from rest_framework.routers import DefaultRouter
from quiz_management_app.api.views import QuizViewSet

router = DefaultRouter()
router.register(r"quizzes", QuizViewSet, basename="quiz")

urlpatterns = router.urls
