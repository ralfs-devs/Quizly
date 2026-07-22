from rest_framework import serializers
from quiz_management_app.models import Quiz, Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id",
            "question_title",
            "question_options",
            "answer",
            "created_at",
            "updated_at",
        ]


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    url = serializers.URLField(
        source="video_url", write_only=True, required=False)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "video_url",
            "url",
            "questions",
        ]
        read_only_fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "video_url",
            "questions",
        ]
        extra_kwargs = {"video_url": {"required": False}}

    def validate(self, attrs):
        if self.context["request"].method == "POST":
            url = attrs.get("video_url") or self.initial_data.get("url")
            if not url:
                raise serializers.ValidationError(
                    {"url": "This field is required."})
            attrs["video_url"] = url
        return attrs
