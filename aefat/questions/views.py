from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404,\
    render_to_response

from aefat.activities.models import Activity
from aefat.decorators import ajax_required
from aefat.questions.forms import QuestionForm, AnswerForm
from aefat.questions.models import Question, Answer
from endless_pagination.decorators import page_template
from django.template.context import RequestContext

# @login_required
# def _questions(request, questions, active):
#     paginator = Paginator(questions, 10)
#     page = request.GET.get('page')
#     try:
#         questions = paginator.page(page)
#     except PageNotAnInteger:
#         questions = paginator.page(1)
#     except EmptyPage:
#         questions = paginator.page(paginator.num_pages)
#     return render(request, 'questions/questions.html', {'questions': questions, 'active': active})

@login_required
def _questions(request, questions, active, template='questions/questions.html', extra_context=None):
    context = {
               'questions': questions, 
               'active': active
               }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))


@login_required
@page_template('questions/questions_page.html')
def questions(request, template='questions/questions.html', extra_context=None):
    context = {
               'questions': Question.get_unanswered(), 
               'active': 'unanswered'
               }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))

@login_required
@page_template('questions/questions_page.html')
def answered(request, template='questions/questions.html', extra_context=None):
    context = {
               'questions': Question.get_answered(), 
               'active': 'answered'
               }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))

@login_required
@page_template('questions/questions_page.html')
def unanswered(request, template='questions/questions.html', extra_context=None):
    context = {
               'questions': Question.get_unanswered(), 
               'active': 'unanswered'
               }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))

@login_required
@page_template('questions/questions_page.html')
def all(request, template='questions/questions.html', extra_context=None):
    context = {
               'questions': Question.objects.all(), 
               'active': 'all'
               }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))

@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
           question = Question()
           question.user = request.user
           question.title = form.cleaned_data.get('title')
           question.description = form.cleaned_data.get('description')
           question.save()
           tags = form.cleaned_data.get('tags')
           question.create_tags(tags)
           return redirect('/questions/')
        else:
            return render(request, 'questions/ask.html', {'form': form})        
    else:
        form = QuestionForm()
    return render(request, 'questions/ask.html', {'form': form})

@login_required
def question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    form = AnswerForm(initial={'question': question})
    return render(request, 'questions/question.html', {'question': question, 'form': form})

@login_required
def answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            user = request.user
            answer = Answer()
            answer.user = request.user
            answer.question = form.cleaned_data.get('question')
            answer.description = form.cleaned_data.get('description')
            answer.save()
            user.profile.notify_answered(answer.question)
            return redirect(u'/questions/{0}/'.format(answer.question.pk))
        else:
            question = form.cleaned_data.get('question')
            return render(request, 'questions/question.html', {'question': question, 'form': form})
    else:
        return redirect('/questions/')

@login_required
@ajax_required
def accept(request):
    answer_id = request.POST['answer']
    answer = Answer.objects.get(pk=answer_id)
    user = request.user
    try:
        user.profile.unotify_accepted(answer.question.get_accepted_answer())  # answer.accept cleans previous accepted answer
    except Exception, e:
        pass
    if answer.question.user == user:
        answer.accept()
        user.profile.notify_accepted(answer)
        return HttpResponse()
    else:
        return HttpResponseForbidden()

@login_required
@ajax_required
def vote(request):
    answer_id = request.POST['answer']
    answer = Answer.objects.get(pk=answer_id)
    vote = request.POST['vote']
    user = request.user
    activity = Activity.objects.filter(Q(activity_type=Activity.UP_VOTE) | Q(activity_type=Activity.DOWN_VOTE), user=user, answer=answer_id)
    if activity:
        activity.delete()
    if vote in [Activity.UP_VOTE, Activity.DOWN_VOTE]:
        activity = Activity(activity_type=vote, user=user, answer=answer_id)
        activity.save()
    return HttpResponse(answer.calculate_votes())

@login_required
@ajax_required
def favorite(request):
    question_id = request.POST['question']
    question = Question.objects.get(pk=question_id)
    user = request.user
    activity = Activity.objects.filter(activity_type=Activity.FAVORITE, user=user, question=question_id)
    if activity:
        activity.delete()
        user.profile.unotify_favorited(question)
    else:
        activity = Activity(activity_type=Activity.FAVORITE, user=user, question=question_id)
        activity.save()
        user.profile.notify_favorited(question)
    return HttpResponse(question.calculate_favorites())
