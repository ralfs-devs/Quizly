from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from quiz_management_app.models import Quiz
from quiz_management_app.api.serializers import QuizSerializer
from quiz_management_app.services import QuizGenerationService


class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Quiz.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        video_url = request.data.get("url")
        if not video_url:
            return Response(
                {"error": "A YouTube URL is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quiz = QuizGenerationService.generate_quiz_from_video(
                user=request.user,
                video_url=video_url
            )
            serializer = self.get_serializer(quiz)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
