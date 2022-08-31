from django.core.management.base import BaseCommand
from thidh.pastpapers.models import PastPaper

template_name = ""
questions = [
    [
        "Congratulations!",
        "I'm sorry",
        "Good job!",
        "I'm glad you like it"
    ],
    [
        "That's not a good choice",
        "I don't agree with you",
        "I quite agree with you",
        "You should think of it again"
    ]
]
correct_options = ["0", "0", "0", "0"]


class Command(BaseCommand):
    help = "Create a simple paper"

    def handle(self, *args, **options):
        PastPaper.objects.create(
            template_name=template_name,
            questions=questions,
            correct_options=correct_options
        )
