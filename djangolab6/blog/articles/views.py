from .models import Article
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def archive(request):
    if request.user.is_authenticated:
        return render(request, 'archive.html', {"posts": Article.objects.all()})
    else:
        message = 'Для просмотра содержимого страницы необходимо войти в систему.'
        return render(request, 'archive.html', {'message': message})


def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404


def create_post(request):
    if request.user != 'AnonymousUser':
        if request.method == "POST":
            form = {
                'text': request.POST["text"],
                'title': request.POST["title"]
            }
            not_unique = Article.objects.filter(title=form['title'])
            if not_unique:
                form['errors'] = u'Ошибка: Статья с таким названием уже существует. Придумайте другое.'
                return render(request, 'form.html', {'form': form})
            if form["text"] and form["title"]:
                Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                return render(request, 'archive.html', {"posts": Article.objects.all()})
            else:
                form['errors'] = u"Ошибка: Не все поля заполнены."
                return render(request, 'form.html', {'form': form})
        else:
            return render(request, 'form.html', {})
    else:
        raise Http404


def registration(request):
    if request.method == 'POST':
        form = {
            'login': request.POST['login'],
            'email': request.POST['email'],
            'password': request.POST['password'],
        }
        check_login = User.objects.filter(username=form['login'])
        check_email = User.objects.filter(email=form['email'])
        if check_login or check_email:
            form['errors'] = 'Логин или e-mail с таким названием уже сущетсвуют.'
            return render(request, 'registration.html', {'form': form})
        if form['login'] and form['email'] and form['password']:
            User.objects.create_user(form['login'], form['email'], form['password'])
            return redirect('auth')
        else:
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'registration.html', {'form': form})
    else:
        return render(request, 'registration.html',)


def auth(request):
    if request.method == 'POST':
        form = {
            'login': request.POST['login'],
            'password': request.POST['password'],
        }
        check_login = User.objects.filter(username=form['login'])
        if check_login and form['login'] and form['password']:
            user = authenticate(username=form['login'], password=form['password'])
            if user:
                login(request, user)
                return redirect('articles')
            else:
                form['errors'] = u'Логин или пароль введены неверно. Попробуйте снова.'
                return render(request, 'login.html', {'form': form})
        else:
            form['errors'] = u'Пользователь с таким именем еще не зарегестрирован или вы ввели не все данные.'
            return render(request, 'login.html', {'form': form})
    else:
        return render(request, 'login.html')


def deauth(request):
    logout(request)
    message = 'Вы вышли из системы.'
    return render(request, 'registration.html', {"message": message})