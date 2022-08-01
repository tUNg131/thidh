import random

from django.core.management.base import BaseCommand
from questions.models import Choice, Question, Section, Paper, QuestionType


def create_question(**kwargs):
    question_template = "{}+{}=?"
    x, y = random.sample(range(10), k=2)
    shift = random.randint(0, 3)
    kwargs.update({"text": question_template.format(x, y)})

    q = Question.objects.create(**kwargs)

    choice_index = i_ls = list(range(4))
    random.shuffle(choice_index)
    for c_i, i in zip(choice_index, i_ls):
        text = x + y + i - shift
        is_correct = (i == shift)
        index = c_i

        c = Choice.objects.create(
            text=text,
            is_correct=is_correct,
            index=index,
            question=q
        )


def create_paper():
    p1 = Paper.objects.create(
        subject="0", instruction="Choose the correct answer")

    p2 = Paper.objects.create(
        subject="0", instruction="Choose the correct answer")

    s1 = Section.objects.create(
        name="Random section 1",
        instruction="Choose the correct answer",
        index=1
    )

    s2 = Section.objects.create(
        name="Random section 2",
        instruction="Choose the correct answer",
        index=2
    )

    qt = QuestionType.objects.create(name="Random question", subject="0")

    for p in [p1, p2]:
        i = 1
        for s in [s1, s2]:
            for _ in range(10):
                create_question(
                    index=i,
                    paper=p,
                    section=s,
                    type=qt
                )
                i += 1


class Command(BaseCommand):
    help = "Create simple papers"

    def handle(self, *args, **options):
        create_paper()

