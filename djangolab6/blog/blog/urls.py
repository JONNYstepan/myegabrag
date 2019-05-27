from django.contrib import admin
from django.urls import path
from articles import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.archive, name='articles'),
    path('', views.registration, name='registration'),
    url(r'^article/(?P<article_id>\d+)$', views.get_article, name='get_article'),
    url(r'create_new_post/$', views.create_post, name="create_new_post"),
    path('registration/', views.registration, name='registration'),
    path('login/', views.auth, name='auth'),
    path('logout', views.deauth, name='deauth')
]
