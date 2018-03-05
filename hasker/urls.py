"""hasker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

from answers import views

import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.index, name='index'),
    url(r'^search/?$', views.search_result, name='search_result'),
    url(r'^tag/(?P<tag>[a-zA-Z0-9]+)/$', views.tag_result, name='tag_result'),
    url(r'^login/$', views.user_login, name="login"),
    url(r'^logout/$', views.user_logout, name="logout"),
    url(r'^ask/?$', views.ask_question, name="ask"),
    url(r'^tags.json$', views.list_tags_json, name="tags.json"),
    url(r'^question/(?P<question_id>\d+)/?$', views.view_question, name='view_question'),
    url(r'^question/(?P<question_id>\d+)/vote/(?P<action>[plus|minus]+)/?$', views.question_vote, name='question_vote'),
    url(r'^question/(?P<question_id>\d+)/vote/(?P<answer_id>\d+)/(?P<action>[plus|minus]+)/?$', views.answer_vote, name='answer_vote'),
    url(r'^answer/(?P<answer_id>\d+)/accept/?$', views.answer_accept, name='answer_accept'),
    url(r'^user/(?P<user_id>\d+)/?$', views.view_user, name='view_user'),
    url(r'^signup/?$', views.signup, name='signup'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns