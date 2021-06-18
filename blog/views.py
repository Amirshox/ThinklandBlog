from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q

from .models import Article
from .forms import CommentForm, NewUserForm


def article_list(request):
    search = request.GET.get('search')

    if request.user.is_authenticated:
        if search:
            articles = Article.objects.filter(Q(title__icontains=search) & Q(content__icontains=search))
        else:
            articles = Article.objects.all()
    else:
        if search:
            articles = Article.objects.filter(
                Q(type='free') & Q(title__icontains=search) & Q(content__icontains=search))
        else:
            articles = Article.objects.filter(type='free')

    return render(request, 'blog/article_list.html', {'articles': articles})


def article_detail(request, slug):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, slug=slug)

        comments = article.comments.all()

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment_form = comment_form.save(commit=False)
                comment_form.author = request.user
                comment_form.publish = timezone.now()
                comment_form.article = article
                comment_form.save()
                return HttpResponseRedirect(f'/articles/{article.slug}/')
        else:
            comment_form = CommentForm()

        context = {
            'article': article,
            'comment_form': comment_form,
            'comments': comments
        }
        return render(request, 'blog/article_detail.html', context)


def category_list(request, slug):
    if request.user.is_authenticated:
        articles = Article.objects.filter(category__slug=slug)
    else:
        articles = Article.objects.filter(type='Free', category__slug=slug)
    return render(request, 'blog/article_list.html', {'articles': articles})


def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("article_list")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm
    return render(request, "register.html", context={"form": form})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("article_list")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "login.html", context={"form": form})


def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("article_list")
