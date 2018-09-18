import json
import requests
import datetime 
import math
from django.shortcuts import render, redirect
from django.db.models import F 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from nightstand_dashboard.models import Book, Reader, Chapter, ReaderChapter, ChapterComment, Group, GroupChapter
from nightstand_dashboard.forms import CommentForm, SearchForm, CreateGroupForm



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

@login_required()
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
        progress = math.floor((completed_count/chapter_count)*100)
        context["books"][book.id].append(progress)
    context['comments'] = sorted(comments, reverse=True, key= lambda k: k.datetime)[:15]
    context["reader"] = reader
    context["to_do"] = ReaderChapter.objects.filter(reader=reader, completed=False).order_by(F('duedate').asc(nulls_last=True))[:5]
    return render(request, "nightstand_dashboard/dashboard.html", context)

@login_required()
def add_book(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        param = {"q": form.data['search_term'].replace(" ", "+")}
        r = requests.get('https://nightstand-db.herokuapp.com/books', params=param)
        results = json.loads(r.text)
        return render(request, 'nightstand_dashboard/add_book.html', {"form": form, "books": results})
    else:
        form = SearchForm()
        return render(request, 'nightstand_dashboard/add_book.html', {"form": form })

@login_required()
def book_view(request, pk):
    reader = Reader.objects.get(user=request.user)
    book = Book.objects.get(pk=pk)
    chapters = Chapter.objects.filter(book=book)
    book_reader_groups = list()
    groups = Group.objects.filter(book=book)
    for group in groups:
        if reader in group.readers.all():
            book_reader_groups.append(group)
    if request.method == "GET":
        book_chapters = list()
        book_comments = list()
        for chapter in chapters:
            book_chapters.append(ReaderChapter.objects.get(chapter=chapter, reader=reader))
            book_comments += chapter.chaptercomment_set.all()
        comments = sorted(book_comments, reverse=True, key= lambda k: k.datetime)
        return render(request, 'nightstand_dashboard/book_view.html', {"book": book, "book_chapters": book_chapters, "comments": comments, "reader": reader, "groups": book_reader_groups})
    else:
        return HttpResponseForbidden()

@login_required()
def book_add(request, olid):
    reader = Reader.objects.get(user=request.user)
    if Book.objects.filter(OLID=olid).count():
        book = Book.objects.get(OLID=olid)
        book.readers.add(reader)
        for chapter in book.chapter_set.all():
            ReaderChapter.objects.create(chapter=chapter, reader=reader)
        return redirect(f"/books/{book.id}")
    else:
        r = requests.get(f'https://nightstand-db.herokuapp.com/books?olid={olid}')
        results = json.loads(r.text)
        book = results[0]
        chapters = book["chapters"]
        new_book = Book.objects.create(title=book["title"], OLID=book["olid"], author=book["author"], thumbnail=f"http://covers.openlibrary.org/b/olid/{book['olid']}-M.jpg", pages=book["pages"])
        new_book.readers.add(reader)
        for chapter in chapters:
           new_chapter = Chapter.objects.create(book=new_book, name=chapter["title"].replace("--", ""))
           ReaderChapter.objects.create(chapter=new_chapter, reader=reader)
        return redirect(f"/books/{new_book.id}")

@login_required()
def like(request, pk):
    comment = ChapterComment.objects.get(pk=pk)
    reader = Reader.objects.get(user=request.user)
    if reader in comment.likes.all():
        comment.likes.remove(reader)
    else:
        comment.likes.add(reader)
    return HttpResponse("OK")
    
@login_required()
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
            if request.GET.get("next") == "book":
                return redirect(f'/books/{chapter.book.id}')
            elif request.GET.get("next") == "group":
                return redirect(f'/groups/{request.GET.get("id")}')
    else:
        form = CommentForm()

    return render(request, f"nightstand_dashboard/add_comment.html", {"form": form, "chapter": chapter})

@login_required()
def complete_chapter(request, pk):
    ReaderChapter.objects.filter(pk=pk).update(completed=True)
    return HttpResponse("OK")

@login_required()
def duedate(request, pk):
    if request.GET.get("type") == "reader":
        chapter = ReaderChapter.objects.filter(pk=pk)
        if request.method == "POST":
            newdate = json.loads(request.body.decode("utf-8"))["newdate"]
            chapter.update(duedate=newdate)
        return HttpResponse("OK")
    elif request.GET.get("type") == "group":
        chapter = GroupChapter.objects.filter(pk=pk)
        if request.method == "POST":
            newdate = json.loads(request.body.decode("utf-8"))["newdate"]
            chapter.update(duedate=newdate)
        return HttpResponse("OK")

@login_required()
def groups_view(request, olid):
    no_groups_message = "There are no groups for this book, but you can start your own!"
    if Book.objects.filter(OLID=olid).count():
        book = Book.objects.get(OLID=olid)
        groups = Group.objects.filter(book=book)
        if len(groups):
            return render(request, "nightstand_dashboard/groups.html", {"groups": groups, "olid": olid})
        else:
            return render(request, "nightstand_dashboard/groups.html", {"message": no_groups_message, "olid": olid})
    else:
        return render(request, "nightstand_dashboard/groups.html", {"message": no_groups_message, "olid": olid})


@login_required()
def group_detail(request, pk):
    reader = Reader.objects.get(user=request.user)
    group = Group.objects.get(pk=pk)
    readers = group.readers.all()
    context = {"reader": reader, "group": group, "readers": dict()}
    comments = list()
    for chapter in group.book.chapter_set.all():
        comments_set = chapter.chaptercomment_set.all()
        comments += [comment for comment in comments_set if comment.reader in readers]
    context["comments"] = sorted(comments, reverse=True, key= lambda k: k.datetime)
    for reader in readers:
        chapters = list()
        for chapter in group.book.chapter_set.all():
            group_chapter = GroupChapter.objects.get(chapter=chapter)
            reader_chapter = ReaderChapter.objects.get(chapter=chapter, reader=reader)
            if reader_chapter.completed:
                chapters.append("-completed")
            elif group_chapter.duedate and group_chapter.duedate < datetime.date.today():
                chapters.append("-overdue")
            else:
                chapters.append("")
        context["readers"][str(reader)] = chapters
    return render(request, "nightstand_dashboard/group_detail.html", context)


@login_required()
def group_add(request, pk):
    reader = Reader.objects.get(user=request.user)
    group = Group.objects.get(pk=pk)
    group.readers.add(reader)
    if group.book not in reader.books.all():
        group.book.readers.add(reader)
        for chapter in group.book.chapter_set.all():
            duedate = GroupChapter.objects.get(chapter=chapter, group=group).duedate
            ReaderChapter.objects.create(chapter=chapter, reader=reader, duedate=duedate)
    return redirect(f"/groups/{pk}")

@login_required()
def create_group(request, olid):
    reader = Reader.objects.get(user=request.user)
    if request.method == "POST":
        book = Book.objects.get(OLID=olid)
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = Group.objects.create(name=form['group_name'].value(), book=book)
            group.readers.add(reader)
            for chapter in book.chapter_set.all():
                GroupChapter.objects.create(chapter=chapter, group=group)
            if reader not in book.readers.all():
                book.readers.add(reader)
                for chapter in book.chapter_set.all():
                    ReaderChapter.objects.create(reader=reader, chapter=chapter)
            return redirect(f"/groups/{group.id}")
    else:
        book = None
        if Book.objects.filter(OLID=olid).count():
            book = Book.objects.get(OLID=olid)
        else:
            r = requests.get(f'https://nightstand-db.herokuapp.com/books?olid={olid}')
            results = json.loads(r.text)
            book = results[0]
            chapters = book["chapters"]
            book = Book.objects.create(title=book["title"], OLID=book["olid"], author=book["author"], thumbnail=f"http://covers.openlibrary.org/b/olid/{book['olid']}-M.jpg", pages=book["pages"])
            for chapter in chapters:
                Chapter.objects.create(book=book, name=chapter["title"].replace("--", ""))   
        form = CreateGroupForm()
        return render(request, "nightstand_dashboard/create_group.html", {"form": form, "book": book})

@login_required()
def delete_user_book(request, pk):
    reader = Reader.objects.get(user=request.user)
    book = Book.objects.get(pk=pk)
    book.readers.remove(reader)
    for chapter in book.chapter_set.all():
        reader_chapter = ReaderChapter.objects.get(chapter=chapter, reader=reader)
        reader_chapter.delete()
    groups = Group.objects.filter(book=book)
    for group in groups:
        group.readers.remove(reader)
    return redirect("/dashboard/")

@login_required()
def leave_group(request, pk):
    reader = Reader.objects.get(user=request.user)
    group = Group.objects.get(pk=pk)
    group.readers.remove(reader)
    return redirect("/dashboard/")
            
               
    

    








