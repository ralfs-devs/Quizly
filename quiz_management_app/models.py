from django.db import models
from django.conf import settings


class Quiz(models.Model):
    """Represents a quiz owned by a specific user.

    Attributes:
        owner (ForeignKey): The user who created the quiz.
        title (CharField): The title of the quiz.
        description (TextField): A brief description of the quiz.
        video_url (URLField): The source URL of the YouTube video.
        created_at (DateTimeField): Timestamp when the quiz was created.
        updated_at (DateTimeField): Timestamp when the quiz was last updated.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quizzes'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns the string representation of the quiz."""
        return f"{self.title} (Owner: {self.owner.username})"


class Question(models.Model):
    """Represents a question within a specific quiz.

    Attributes:
        quiz (ForeignKey): The quiz this question belongs to.
        question_title (CharField): The title or text of the question.
        question_options (JSONField): A list of 4 answer options.
        answer (CharField): The correct answer string.
        created_at (DateTimeField): Timestamp when the question was created.
        updated_at (DateTimeField): Timestamp when the question was last updated.
    """
    quiz = models.ForeignKey(
        Quiz,
        related_name='questions',
        on_delete=models.CASCADE
    )
    question_title = models.CharField(max_length=500)
    question_options = models.JSONField(default=list)
    answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns the string representation of the question."""
        return self.question_title
