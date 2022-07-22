from django.db import models


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
    MCQ_CHOICES = [
        (1, 'A'),
        (2, 'B'),
        (3, 'C'),
        (4, 'D'),
    ]

    question_json = models.JSONField(verbose_name="Question JSON")
    correct_answer = models.CharField(
        max_length=1,
        choices=MCQ_CHOICES
    )
    paper = models.ForeignKey('Paper', on_delete=models.CASCADE)

