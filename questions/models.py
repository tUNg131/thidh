from django.db import models
from auth.models import User


def get_choices(options):
    return [(str(i), option) for (i, option) in enumerate(options)]


class Paper(models.Model):
    SUBJECTS = [
        ('En', 'Tieng Anh'),
    ]

    code = models.CharField(verbose_name="Paper Code", max_length=10)
    subject = models.CharField(
        max_length=2,
        choices=SUBJECTS
    )
    date = models.DateField(verbose_name="Paper Date")
    is_past_paper = models.BooleanField()

    def __str__(self):
        return self.get_subject_display() + " " + str(self.date.year)


class Section(models.Model):
    instruction_text = models.CharField(verbose_name="Section instruction")
    paper = models.ForeignKey('Paper', related_name="sections", on_delete=models.CASCADE)
    

class Question(models.Model):
    json_data = models.JSONField(verbose_name="Question JSON")
    correct_answer = models.CharField(
        max_length=1,
        choices=get_choices(['A', 'B', 'C', 'D'])
    )
    section = models.ForeignKey('Section', related_name="questions", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, through='UserQuestion', related_name="questions")


def question_to_dict(question):
    """
    Return a dict containing the data in question instance suitable for passing as
    QuestionForm's keyword arguments.
    """
    return {
        'question_text': question.json_data['qnt'],
        'choices': get_choices(question.json_data['chs'])
    }

def paper_to_dict(paper):
    """
    Return a dict containing the data in paper instance suitable for passing as
    PaperForm's keyword arguments.
    """
    sections = []
    for s in paper.sections:
        section = {}
        section['section_instruction'] = s['instr']


class UserQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    last_attempt = models.CharField(max_length=1, choices=get_choices(['A', 'B', 'C', 'D']))