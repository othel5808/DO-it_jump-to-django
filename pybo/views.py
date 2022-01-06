from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse
from django.utils import timezone

from pybo.models import Question, Answer
from .forms import QuestionForm, AnswerForm


def index(request):
    """
  pybo 목록 출력
  """
    page = request.GET.get('page', '1') # 페이지

    question_list = Question.objects.order_by('-create_date')

    #페이징 처리
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
  pybo 내용 출력
  """
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
  answer 내용 입력
  """
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.create_date = timezone.now()
            answer.author = request.user
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    # todo 나중에 `render()`와 `redirect()`의 차이점에 대해 확인 할 것
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request):
    """
    question 생성
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.author = request.user
            question.save()
            return redirect('pybo:index')

    # method == 'GET'
    else:
        form = QuestionForm()
    context = {'form': form}
    # return render(request, 'pybo/question_form.html', {'form': form})
    return render(request, 'pybo/question_form.html', context)

def question_modify(request, question_id):
    """
    pybo 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form= QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
  """
  pybo 질문 삭제
  """

  question = get_object_or_404()(Question, pk=question_id)
  if request.user != question.author:
    messages.error(request, '삭제 권한이 없습니다.')
    return redirect('pybo:detail', question_id=question.id)
  question.delete()
  return redirect('pybo:index')