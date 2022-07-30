import random

from django.core.management.base import BaseCommand
from questions.models import Question, Section, Paper


def get_question(paper, section):
    x, y = random.sample(range(10), k=2)  # from 0 to 9
    question_text = f"{x}+{y}=?"

    choices = [x, 2 * y, x - y, y]
    correct_answer = random.randint(1, 4)
    choices[correct_answer - 1] = x + y

    json_data = {
        "qnt": question_text,
        "chs": choices
    }

    kwargs = {
        "json_data": json_data,
        "correct_answer": correct_answer,
        "paper": paper,
        "section": section,
    }
    return Question(**kwargs)


class Command(BaseCommand):
    help = "Create simple papers"
    structure = [5, 5, 5, 5]

    def handle(self, *args, **options):
        self.create_paper()

    def create_paper(self):
        paper_kwargs = {
            "code": "Random Paper",
            "subject": "Rn",
            "type": "m"
        }
        p = Paper(**paper_kwargs)
        p.save()

        for i, questions_per_section in enumerate(self.structure):
            section_kwargs = {
                "name": f"section-{i}-random-paper",
                "instruction_text": "Choose the correct answer",
            }
            s = Section(**section_kwargs)
            s.save()

            for _ in range(questions_per_section):
                q = get_question(p, s)
                q.save()
