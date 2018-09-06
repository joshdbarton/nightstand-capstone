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
    reader = Reader.objects.get(user=request.user)
    books = reader.books.all()
    context = {"books": dict()}
    for book in books:
        context['books'][book.id] = [book.title, book.thumbnail]
        progress = 0
        chapters = Chapter.objects.filter(book=book)
        book_chapters = list()
        chapter_count = 0
        completed_count = 0
        for chapter in chapters:
            if ReaderChapter.objects.get(reader=reader, chapter=chapter).completed:
                completed_count += 1
            chapter_count += 1
        progress = completed_count/chapter_count
        context["books"][book.id].append(progress)
    return render(request, "nightstand_dashboard/dashboard.html", context)


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
        for chapter in chapters:
            book_chapters.append(ReaderChapter.objects.get(chapter=chapter, reader=reader))
            book_comments += chapter.chaptercomment_set.all()
        return render(request, 'nightstand_dashboard/book_view.html', {"book": book, "book_chapters": book_chapters, "book_comments": book_comments})
    else:
        return HttpResponseForbidden()

def book_add(request, pk):
    reader = Reader.objects.get(user=request.user)
    book = Book.objects.get(pk=pk)
    book.readers.add(reader)
    for chapter in book.chapter_set.all():
        ReaderChapter.objects.create(chapter=chapter, reader=reader)
    return redirect(f"/books/{pk}")



