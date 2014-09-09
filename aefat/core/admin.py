from aefat.feeds.models import Feed
from aefat.auth.models import Profile
from aefat.articles.models import Article
from aefat.articles.models import ArticleComment
from django.contrib import admin

admin.site.register(Feed)
admin.site.register(Profile)
admin.site.register(Article)
admin.site.register(ArticleComment)