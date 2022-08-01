from django.db import models
from accounts.models import User


def get_choices(options):
    options = ["---"] + options
    return [(str(i), option) for (i, option) in enumerate(options)]


DEFAULT_CHOICES = get_choices(["A", "B", "C", "D"])


class PaperManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("questions", "questions__section")


class Paper(models.Model):
    SUBJECTS = [
        ("r", "Random"),
        ("0", "Tieng Anh"),
    ]

    PAST_PAPER = "p"
    MOCK_PAPER = "m"
    QUESTION_COLLECTIONS = "c"
    PAPER_TYPES = [
        (PAST_PAPER, "Past paper"),
        (MOCK_PAPER, "Mock paper"),
        (QUESTION_COLLECTIONS, "Question collections"),
    ]

    code = models.CharField(max_length=5)
    subject = models.CharField(max_length=1, choices=SUBJECTS)
    date = models.DateField(verbose_name="Paper Date", auto_now=True)
    type = models.CharField(max_length=1, choices=PAPER_TYPES)

    objects = PaperManager()

    def __str__(self):
        subject = self.get_subject_display()
        type = self.get_type_display()
        year = self.date.year
        if self.type == Paper.PAST_PAPER:
            code = self.code
            return f"({type}) {subject} {year} ({code})"
        else:
            return f"({type}) {subject} {year}"


class Section(models.Model):
    name = models.CharField(max_length=100, verbose_name="Section name", unique=True)
    instruction_text = models.TextField(verbose_name="Section instruction")
    papers = models.ManyToManyField(Paper, through="Question", related_name="sections")

    def __str__(self):
        return self.name


class Question1(models.Model):
    json_data = models.JSONField(verbose_name="Question JSON")
    correct_answer = models.CharField(max_length=1, choices=DEFAULT_CHOICES)

    paper = models.ForeignKey(Paper, related_name="questions", on_delete=models.CASCADE)
    section = models.ForeignKey(Section, related_name="questions", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, through="UserQuestion", related_name="questions")

    def __str__(self):
        return f"Question {self.id}"


class Question(models.Model):
    text = models.TextField(verbose_name="Question")

    paper = models.ForeignKey(Paper, related_name="questions", on_delete=models.CASCADE)
    section = models.ForeignKey(Section, related_name="questions", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, through="UserQuestion", related_name="questions")


class Choice(models.Model):
    text = models.CharField(verbose_name="Answer")
    is_correct = models.BooleanField(verbose_name="Is correct choice?")

    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)


class UserQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    last_attempt = models.CharField(max_length=1, choices=DEFAULT_CHOICES)
