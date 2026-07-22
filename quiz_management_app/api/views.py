from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from quiz_management_app.models import Quiz
from quiz_management_app.api.serializers import QuizSerializer
from quiz_management_app.services import QuizGenerationService


class QuizViewSet(viewsets.ModelViewSet):
    """ViewSet for managing quiz operations including creation, updates, and deletion."""

    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Returns the queryset of quizzes owned by the current authenticated user."""
        return Quiz.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """Creates a new quiz from a provided video URL."""
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

    def update(self, request, *args, **kwargs):
        """Updates an existing quiz instance."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Performs a partial update on an existing quiz instance."""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Deletes an existing quiz instance."""
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
