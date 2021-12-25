from django.db import models


# Create your models here.
class Question(models.Model):
    subject = models.CharField(
        help_text="질문의 제목",
        max_length=200,
    )
    content = models.TextField(
        help_text="질문의 내용",
    )
    create_date = models.DateTimeField(
        help_text="질문 작성 일시"
    )

    def __str__(self):
        return self.subject


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    content = models.TextField(
        help_text="답변 내용",
    )
    create_date = models.DateTimeField(
        help_text="답변 일시"
    )
