from django.core.management.base import BaseCommand
from pastpapers.models import PastPaper

json_data = {
    "instructions": "4 questions, 2 sections, 2-2",
    "sections": [
        {
            "instructions": "Choose the correct answer!",
            "questions": [
                {
                    "text": "1+1=?",
                    "options": ["1", "2", "3", "4"]
                },
                {
                    "text": "2+2=?",
                    "options": ["1", "2", "3", "4"]
                },
            ]
        },
        {
            "instructions": "Instructions are the same!",
            "questions": [
                {
                    "text": "1+3=?",
                    "options": ["1", "2", "3", "4"]
                },
                {
                    "text": "4+2=?",
                    "options": ["1", "5", "3", "6"]
                },
            ]
        },
    ]
}

correct_options = ["1", "3", "3", "3"]


class Command(BaseCommand):
    help = "Create a simple paper"

    def handle(self, *args, **options):
        PastPaper.objects.create(
            json_data=json_data,
            correct_options=correct_options
        )
