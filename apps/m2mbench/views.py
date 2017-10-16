from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User

from apps.m2mbench.models import Board, Thread, Post

boards_per_page = settings.JSONBENCH_BOARDS_PER_PAGE
threads_per_page = settings.JSONBENCH_THREADS_PER_PAGE
posts_per_page = settings.JSONBENCH_POSTS_PER_PAGE

def index(request):
    cd = {'boards': None, 'prof': None}
    p = Paginator(Board.objects.all(), boards_per_page)
    try:
        boards = p.page(request.GET.get('ipage'))
    except PageNotAnInteger:
        boards = p.page(1)
    except EmptyPage:
        boards = p.page(p.num_pages)
    cd['boards'] = boards
    cd['prof'] = 'prof' if 'prof' in request.GET else ''
    return render(request, 'm2mbench/index.html', cd)

def view_board(request, board_id=None):
    cd = {'board_id': board_id, 'threads': None, 'prof': None}
    board = Board.objects.get(pk=board_id)
    p = Paginator(board.thread_set.all(), threads_per_page)
    try:
        threads = p.page(request.GET.get('bpage'))
    except PageNotAnInteger:
        threads = p.page(1)
    except EmptyPage:
        threads = p.page(p.num_pages)
    cd['board'] = board
    cd['threads'] = threads
    cd['prof'] = 'prof' if 'prof' in request.GET else ''
    cd['ipage'] = request.GET.get('ipage', '')
    return render(request, 'm2mbench/view_board.html', cd)

def view_thread(request, board_id=None, thread_id=None):
    cd = {'board_id': board_id, 'thread_id': thread_id, 'posts': None, 'prof': None}
    board = Board.objects.get(pk=board_id)
    thread = Thread.objects.get(pk=thread_id)
    p = Paginator(thread.post_set.all(), posts_per_page)
    try:
        posts = p.page(request.GET.get('tpage'))
    except PageNotAnInteger:
        posts = p.page(1)
    except EmptyPage:
        posts = p.page(p.num_pages)
    cd['board'] = board
    cd['thread'] = thread
    cd['posts'] = posts
    cd['prof'] = 'prof' if 'prof' in request.GET else ''
    cd['ipage'] = request.GET.get('ipage', '')
    cd['bpage'] = request.GET.get('bpage', '')
    cd['posts_per_page'] = posts_per_page
    return render(request, 'm2mbench/view_thread.html', cd)

def view_post(request, board_id=None, thread_id=None, post_id=None):
    cd = {'board_id': board_id, 'thread_id': thread_id, 'post_id': post_id, 'posts': None, 'prof': None}
    bs = request.benchmarksuite
    board = Board.objects.get(pk=board_id)
    thread = Thread.objects.get(pk=thread_id)
    post = Post.objects.get(pk=post_id)
    p = Paginator(thread.post_set.all(), 1)
    try:
        posts = p.page(request.GET.get('ppage'))
    except PageNotAnInteger:
        posts = p.page(1)
    except EmptyPage:
        posts = p.page(p.num_pages)
    cd['board'] = board
    cd['thread'] = thread
    cd['posts'] = posts
    cd['post'] = post
    cd['prof'] = 'prof' if 'prof' in request.GET else ''
    cd['ipage'] = request.GET.get('ipage', '')
    cd['bpage'] = request.GET.get('bpage', '')
    cd['tpage'] = request.GET.get('tpage', '')
    cd['ppage'] = request.GET.get('ppage', '')
    if posts.has_previous():
        prev_posts = p.page(posts.previous_page_number())
        for prev_post in prev_posts:
            cd['prev_post'] = prev_post # shoud only loop once
            cd['prev_post_tpage'] = int((prev_posts.number - 1)/posts_per_page) + 1
    else:
        cd['prev_post'] = None
        cd['prev_post_tpage'] = posts.number
    if posts.has_next():
        next_posts = p.page(posts.next_page_number())
        for next_post in next_posts:
            cd['next_post'] = next_post # should only loop once
            cd['next_post_tpage'] = int((next_posts.number - 1)/posts_per_page) + 1
    else:
        cd['next_post'] = None
        cd['next_post_tpage'] = posts.number
    if request.GET.get('mark_read'):
        bs.next_step(request, 'm2mbench: before read_post') if bs else None
        cd['post_has_been_read'] = read_post(thread, post, request.user)
        bs.next_step(request, 'm2mbench: after read_post') if bs else None
    if request.GET.get('mark_unread'):
        bs.next_step(request, 'm2mbench: before unread_post') if bs else None
        cd['post_has_been_unread'] = unread_post(thread, post, request.user)
        bs.next_step(request, 'm2mbench: after unread_post') if bs else None
    bs.next_step(request, 'm2mbench: before is_post_read') if bs else None
    cd['post_is_read'] = is_post_read(thread, post, request.user)
    bs.next_step(request, 'm2mbench: after read_post') if bs else None
    return render(request, 'm2mbench/view_post.html', cd)

def is_post_read(thread, post, user):
    if post.readers.filter(pk=user.id):
        return True
    else:
        return False

def read_post(thread, post, user):
    try:
        readers = post.readers.filter(pk=user.id)
        if not readers:
            post.readers.add(user)
        return True
    except:
        return False

def unread_post(thread, post, user):
    try:
        readers = post.readers.filter(pk=user.id)
        if readers:
            post.readers.remove(user)
        return True
    except:
        return False
