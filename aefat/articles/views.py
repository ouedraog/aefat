from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

import markdown

from aefat.articles.forms import ArticleForm
from aefat.articles.models import Article, Tag, ArticleComment
from aefat.decorators import ajax_required
from django.template.context import RequestContext
from endless_pagination.decorators import page_template

@page_template('articles/articles_page.html')
@login_required
def articles(request, template='articles/articles.html', extra_context=None):
    context = {
        'articles': Article.objects.all(),
        'popular_tags': Tag.get_popular_tags()
        
    }
    
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))
    

def _articles(request, articles):
    paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    popular_tags = Tag.get_popular_tags()
    return render(request, 'articles/articles.html', {'articles': articles, 'popular_tags': popular_tags})

# @login_required
# def articles(request):
#     all_articles = Article.get_published()
#     return _articles(request, all_articles)

@login_required
def article(request, slug):
    article = get_object_or_404(Article, slug=slug, status=Article.PUBLISHED)
    return render(request, 'articles/article.html', {'article': article})

@login_required
def tag(request, tag_name):
    tags = Tag.objects.filter(tag=tag_name)
    articles = []
    for tag in tags:
        if tag.article.status == Article.PUBLISHED:
            articles.append(tag.article)
    return _articles(request, articles)

@login_required
def write(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = Article()
            article.create_user = request.user
            article.title = form.cleaned_data.get('title')
            article.content = form.cleaned_data.get('content')
            status = form.cleaned_data.get('status')
            if status in [Article.PUBLISHED, Article.DRAFT]:
                article.status = form.cleaned_data.get('status')
            article.save()
            tags = form.cleaned_data.get('tags')
            article.create_tags(tags)
            return redirect('/articles/')
    else:
        form = ArticleForm()
    return render(request, 'articles/write.html', {'form': form})

@login_required
def drafts(request):
    drafts = Article.objects.filter(create_user=request.user, status=Article.DRAFT)
    return render(request, 'articles/drafts.html', {'drafts': drafts})

@login_required
def edit(request, id):
    tags = ''
    if id:
        article = get_object_or_404(Article, pk=id)
        for tag in article.get_tags():
            tags = u'{0} {1}'.format(tags, tag.tag)
        tags = tags.strip()
    else:
        article = Article(create_user=request.user)

    if request.POST:
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('/articles/')
    else:
        form = ArticleForm(instance=article, initial={'tags': tags})
    return render(request, 'articles/edit.html', {'form': form})


@login_required
@ajax_required
def preview(request):
    try:
        if request.method == 'POST':
            content = request.POST.get('content')
            html = 'Nothing to display :('
            if len(content.strip()) > 0:
                html = markdown.markdown(content, safe_mode='escape')
            return HttpResponse(html)
        else:
            return HttpResponseBadRequest()
    except Exception, e:
        return HttpResponseBadRequest()

@login_required
@ajax_required
def comment(request):
    try:
        if request.method == 'POST':
            article_id = request.POST.get('article')
            article = Article.objects.get(pk=article_id)
            comment = request.POST.get('comment')
            comment = comment.strip()
            if len(comment) > 0:
                article_comment = ArticleComment(user=request.user, article=article, comment=comment)
                article_comment.save()
            html = u''
            for comment in article.get_comments():
                html = u'{0}{1}'.format(html, render_to_string('articles/partial_article_comment.html', {'comment': comment}))
            return HttpResponse(html)
        else:
            return HttpResponseBadRequest()
    except Exception, e:
        return HttpResponseBadRequest()
