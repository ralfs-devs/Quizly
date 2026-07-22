import json
import os
import whisper
from google import genai
from google.genai import types
import yt_dlp

from core import settings
from quiz_management_app.models import Quiz, Question
from quiz_management_app.utils import _normalize_video_url


class QuizGenerationService:
    """Service class handling the business logic for quiz generation."""

    @staticmethod
    def generate_quiz_from_video(user, video_url):
        """Downloads audio, transcribes with whisper, and generates questions."""
        video_url = _normalize_video_url(video_url)
        audio_path = QuizGenerationService._download_audio(video_url)
        try:
            transcript = QuizGenerationService._transcribe_audio(audio_path)
            quiz_data = QuizGenerationService._generate_questions_from_transcript(
                transcript)

            quiz = Quiz.objects.create(
                owner=user,
                title=quiz_data["title"],
                description=quiz_data["description"],
                video_url=video_url
            )

            for q_data in quiz_data["questions"]:
                Question.objects.create(
                    quiz=quiz,
                    question_title=q_data["question_title"],
                    question_options=q_data["question_options"],
                    answer=q_data["answer"]
                )

            return quiz
        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)

    @staticmethod
    def _download_audio(video_url):
        """Downloads audio track from YouTube video using yt-dlp."""
        output_template = os.path.join("/tmp", "temp_audio.%(ext)s")
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "quiet": True,
            "noplaylist": True,
            "js_runtimes": {"node": {}},
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            return base + ".mp3"

    @staticmethod
    def _transcribe_audio(audio_path):
        """Transcribes local audio file using local Whisper model."""
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, fp16=False)
        return result["text"]

    @staticmethod
    def _generate_questions_from_transcript(transcript):
        """Generates quiz structure from transcript text using the API."""
        client = genai.Client()
        prompt = f"""
        Based on the following transcript, generate a quiz in valid JSON format.
        The quiz must follow this exact structure:
        {{
          "title": "Create a concise quiz title based on the topic of the transcript.",
          "description": "Summarize the transcript in no more than 150 characters. Do not include any quiz questions or answers.",
          "questions": [
            {{
              "question_title": "The question goes here.",
              "question_options": ["Option A", "Option B", "Option C", "Option D"],
              "answer": "The correct answer from the above options"
            }},
            ...
            (exactly 10 questions)
          ]
        }}
        Requirements:
        - Each question must have exactly 4 distinct answer options.
        - Only one correct answer is allowed per question, and it must be present in 'question_options'.
        - The output must be valid JSON and parsable as-is (e.g., using Python's json.loads).
        - Do not include explanations, comments, or any text outside the JSON.
        - The language of Questions and Answers should be the same as in the Transscript

        Transcript:
        {transcript}
        """

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "title": {"type": "STRING"},
                        "description": {"type": "STRING"},
                        "questions": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "question_title": {"type": "STRING"},
                                    "question_options": {
                                        "type": "ARRAY",
                                        "items": {"type": "STRING"}
                                    },
                                    "answer": {"type": "STRING"}
                                },
                                "required": ["question_title", "question_options", "answer"]
                            }
                        }
                    },
                    "required": ["title", "description", "questions"]
                },
            ),
        )

        return json.loads(response.text)
