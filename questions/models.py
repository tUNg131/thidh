from django.db import models


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

    def __str__(self):
        return self.get_subject_display() + " " + str(self.date.year)


class Question(models.Model):
    json_data = models.JSONField(verbose_name="Question JSON")
    correct_answer = models.CharField(
        max_length=1,
        choices=get_choices(['A', 'B', 'C', 'D'])
    )
    paper = models.ForeignKey('Paper', on_delete=models.CASCADE)


def question_to_dict(question):
    """
    Return a dict containing the data in question instance suitable for passing as
    QuestionForm's keyword arguments.
    """
    return {
        'question_text': question.json_data['qst'],
        'choices': get_choices(question.json_data['ans'])
    }
