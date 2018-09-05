from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseForbidden
from nightstand_dashboard.models import Book, Reader, Chapter, ReaderChapter



def index(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return redirect('/accounts/login')

def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('/add_book')

    else:
        logout(request)
        f = UserCreationForm()

    return render(request, 'nightstand_dashboard/registration.html', {'form': f})

def dashboard(request):
    return HttpResponse("<html><body>It's your dashboard!</body></html>")


def add_book(request):
    books = Book.objects.all()
    return render(request, 'nightstand_dashboard/add_book.html', {'books': books })

def book_view(request, pk):
    reader = Reader.objects.get(user=request.user)
    book = Book.objects.get(pk=pk)
    chapters = Chapter.objects.filter(book=book)

    if request.method == "GET":
        book_chapters = list()
        book_comments = list()
        reader_chapters = ReaderChapter.objects.all()
        for chapter in chapters:
            book_chapters.append(ReaderChapter.objects.get(chapter=chapter))
            book_comments = chapter.chaptercomment_set.all()
        return render(request, 'nightstand_dashboard/book_view.html', {"book": book, "book_chapters": book_chapters, "book_comments": book_comments})
    else:
        return HttpResponseForbidden()

def book_add(request, pk):
    pass



