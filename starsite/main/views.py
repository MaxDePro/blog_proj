from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *

from .utils import *

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import View
from django.db.models import Q

def hello(request):
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))

    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_next():
        next_page = '?page={}'.format(page.next_page_number())
    else:
        next_page = ''

    if page.has_previous():
        prev_page = '?page={}'.format(page.previous_page_number())
    else:
        prev_page = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_page': next_page,
        'prev_page': prev_page,
    }

    return render(request, 'main/main_page.html', context=context)


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model = Post
    model_form = PostForm
    template = 'main/post_create.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'main/post_update.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'main/post_delete.html'
    url_reverse = 'post_list_url'
    raise_exception = True


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'main/post_detail.html'


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'main/tags_list.html', context={'tags': tags})


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'main/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'main/tag_update.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'main/tag_delete.html'
    url_reverse = 'tags_list_url'
    raise_exception = True


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'main/tag_detail.html'
