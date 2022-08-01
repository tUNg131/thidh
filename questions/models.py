from django.db import models
from accounts.models import User


TOAN = "t"
TIENG_ANH = "0"
TIENG_PHAP = "1"
TIENG_NGA = "2"
TIENG_TRUNG = "3"
TIENG_HAN = "4"
TIENG_NHAT = "5"
TIENG_DUC = "6"
VAT_LY = "l"
HOA_HOC = "h"
SINH_HOC = "s"
LICH_SU = "u"
DIA_LY = "d"
GIAO_DUC_CONG_DAN = "g"
SUBJECTS = [
    (TOAN, "Toán"),
    (TIENG_ANH, "Tiếng Anh"),
    (TIENG_PHAP, "Tiếng Pháp"),
    (TIENG_NGA, "Tiếng Nga"),
    (TIENG_TRUNG, "Tiếng Trung"),
    (TIENG_HAN, "Tiếng Hàn"),
    (TIENG_NHAT, "Tiếng Nhật"),
    (TIENG_DUC, "Tiếng Đức"),
    (VAT_LY, "Vật lý"),
    (HOA_HOC, "Hóa học"),
    (SINH_HOC, "Sinh học"),
    (LICH_SU, "Lịch sử"),
    (DIA_LY, "Địa lý"),
    (GIAO_DUC_CONG_DAN, "Giáo dục công dân"),
]


class Section(models.Model):
    class Meta:
        ordering = ["index"]

    name = models.CharField(max_length=100)
    instructions = models.TextField(verbose_name="Section Instructions")
    index = models.PositiveSmallIntegerField(verbose_name="Section Index")

    def __str__(self):
        return self.name


class Paper(models.Model):
    subject = models.CharField(max_length=1, choices=SUBJECTS)
    instructions = models.TextField(verbose_name="Paper Instructions")
    sections = models.ManyToManyField(Section, through="Question", related_name="papers")


class PastPaper(Paper):
    code = models.CharField(max_length=5)
    date = models.DateField(verbose_name="Exam Date", auto_now=True)

    def __str__(self):
        return f"{self.get_subject_display()} {self.code} {self.date.year}"


class QuestionType(models.Model):
    """Type of questions"""
    name = models.CharField(max_length=50)
    subject = models.CharField(max_length=1, choices=SUBJECTS)


class Question(models.Model):
    class Meta:
        ordering = ["index"]

    text = models.TextField(verbose_name="Question")
    index = models.PositiveSmallIntegerField(verbose_name="Question index")

    paper = models.ForeignKey(Paper, related_name="questions", on_delete=models.CASCADE)
    section = models.ForeignKey(Section, related_name="questions", on_delete=models.CASCADE)
    type = models.ForeignKey(QuestionType, related_name="questions", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, through="UserQuestion", related_name="questions")


class Choice(models.Model):
    class Meta:
        ordering = ["index"]

    text = models.CharField(max_length=50, verbose_name="Answer")
    is_correct = models.BooleanField(verbose_name="Is correct choice?")
    index = models.PositiveSmallIntegerField(verbose_name="Choice index")

    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)


class UserQuestion(models.Model):
    timestamp = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    last_attempt = models.ForeignKey(Choice, on_delete=models.CASCADE)
