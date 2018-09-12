import json
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse, HttpResponseForbidden
from nightstand_dashboard.models import Book, Reader, Chapter, ReaderChapter, ChapterComment
from nightstand_dashboard.forms import CommentForm, SearchForm



def index(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return redirect('/login')

def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            new_user = authenticate(username=f.cleaned_data["username"], password=f.cleaned_data["password1"])
            login(request, new_user)
            return redirect('/add_book')

    else:
        logout(request)
        f = UserCreationForm()

    return render(request, 'nightstand_dashboard/registration.html', {'form': f})

def dashboard(request):
    reader = Reader.objects.get(user=request.user)
    books = reader.books.all()
    context = {"books": dict()}
    comments = list()
    for book in books:
        context['books'][book.id] = [book.title, book.thumbnail]
        progress = 0
        chapters = Chapter.objects.filter(book=book)
        chapter_count = 0
        completed_count = 0
        for chapter in chapters:
            chapter_comments = chapter.chaptercomment_set.all()
            if chapter_comments.count() > 0:
                comments.extend(chapter_comments)
            if ReaderChapter.objects.get(reader=reader, chapter=chapter).completed:
                completed_count += 1
            chapter_count += 1
        progress = completed_count/chapter_count
        context["books"][book.id].append(progress)
    context['comments'] = sorted(comments, reverse=True, key= lambda k: k.datetime)[:15]
    context["reader"] = reader
    context["to_do"] = ReaderChapter.objects.filter(reader=reader, completed=False).order_by('duedate')[:5]
    return render(request, "nightstand_dashboard/dashboard.html", context)


def add_book(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        books = list()
        param = {"q": form.data['search_term'].replace(" ", "+")}
        r = requests.get('http://localhost:3000/books', params=param)
        results = json.loads(r.text)
        return render(request, 'nightstand_dashboard/add_book.html', {"form": form, "books": results})
    else:
        form = SearchForm()
        return render(request, 'nightstand_dashboard/add_book.html', {"form": form })

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
        comments = sorted(book_comments, reverse=True, key= lambda k: k.datetime)
        return render(request, 'nightstand_dashboard/book_view.html', {"book": book, "book_chapters": book_chapters, "comments": comments, "reader": reader})
    else:
        return HttpResponseForbidden()

def book_add(request, olid):
    reader = Reader.objects.get(user=request.user)
    book = Book.objects.filter(OLID=olid)
    if len(book):
        book = Book.objects.get(OLID=olid)
        book.readers.add(reader)
        for chapter in book.chapter_set.all():
            ReaderChapter.objects.create(chapter=chapter, reader=reader)
        return redirect(f"/books/{book.id}")
    else:
        r = requests.get(f'http://localhost:3000/books?olid={olid}')
        results = json.loads(r.text)
        book = results[0]
        chapters = book["chapters"]
        new_book = Book.objects.create(title=book["title"], OLID=book["olid"], author=book["author"], thumbnail=f"http://covers.openlibrary.org/b/olid/{book['olid']}-S.jpg", pages=book["pages"])
        new_book.readers.add(reader)
        for chapter in chapters:
           new_chapter = Chapter.objects.create(book=new_book, name=chapter["title"].replace("--", ""))
           new_chapter.readers.add(reader)
        return redirect(f"/books/{new_book.id}")


def like(request, pk):
    comment = ChapterComment.objects.get(pk=pk)
    reader = Reader.objects.get(user=request.user)
    if reader in comment.likes.all():
        comment.likes.remove(reader)
    else:
        comment.likes.add(reader)
    return HttpResponse("OK")
    

def comment_view(request, pk):
    reader = Reader.objects.get(user=request.user)
    chapter = Chapter.objects.get(pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.reader = reader
            new_comment.chapter = chapter
            new_comment.save()
            return redirect(f'/books/{chapter.book.id}')
    else:
        form = CommentForm()

    return render(request, f"nightstand_dashboard/add_comment.html", {"form": form, "chapter": chapter})

def complete_chapter(request, pk):
    ReaderChapter.objects.filter(pk=pk).update(completed=True)
    return HttpResponse("OK")

def duedate(request, pk):
    chapter = ReaderChapter.objects.filter(pk=pk)
    if request.method == "POST":
        newdate = json.loads(request.body.decode("utf-8"))["newdate"]
        chapter.update(duedate=newdate)
    return HttpResponse("OK")








