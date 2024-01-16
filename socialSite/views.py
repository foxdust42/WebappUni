from http.client import HTTPResponse

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import status
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer

from socialSite.forms import NewPostForm, NewCommentForm, XMLDownloadForm
from socialSite.models import Post, Comment
from .serializers import *


# Create your views here.

def home(request):
    return render(request, 'socialSite/home.html')


def posts(request):
    posts_list = Post.objects.all().order_by('-date_posted')
    show_mod = False
    if request.user.is_authenticated and (
            request.user.groups.filter(name='Moderator').exists() or request.user.is_superuser):
        show_mod = True
    return render(request, 'socialSite/posts.html', {'posts': posts_list, 'show_mod': show_mod})


def post(request, pk):
    show_mod = False
    if request.user.is_authenticated and (
            request.user.groups.filter(name='Moderator').exists() or request.user.is_superuser):
        show_mod = True
    if request.method == 'GET':
        this_post = get_object_or_404(Post, id=pk)
        comments = Comment.objects.filter(post=this_post)
        form = NewCommentForm()
        return render(request, 'socialSite/post.html',
                      {'post': this_post, 'comments': comments, 'form': form, 'show_mod': show_mod}, )
    if request.method == 'POST':
        this_post = get_object_or_404(Post, id=pk)
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to comment on this post")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        form = NewCommentForm(request.POST)
        if form.is_valid():
            new_comment = Comment(post=this_post)
            new_comment.content = form.cleaned_data['content']
            new_comment.user = request.user
            new_comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "Failed to post comment")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def make_post(request):
    if not request.user.is_active:
        messages.error(request, 'Please verify your email before making a post')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == 'GET':
        form = NewPostForm()
        return render(request, 'socialSite/new_post.html', {'form': form})

    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            new_post = Post(title=title, content=content, user_id=request.user.id)
            new_post.save()
            return redirect('post', pk=new_post.id)
        else:
            messages.error(request, 'Your post had errors.')
            return render(request, 'socialSite/new_post.html', {'form': form})


@login_required()
def edit_post(request, pk):
    e_post = get_object_or_404(Post, id=pk)
    if not request.user.id == e_post.user_id:
        messages.error(request, 'You may only edit your own posts.')
        return redirect('post', pk=e_post.id)
    if request.method == 'GET':
        form = NewPostForm(initial={'title': e_post.title, 'content': e_post.content})
        return render(request, 'socialSite/edit_post.html', {'form': form})
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            e_post.title = title
            e_post.content = content
            e_post.is_edited = True
            e_post.save()
            messages.success(request, 'Post edited successfully')
            return redirect('post', pk=e_post.id)


@login_required()
def delete_post(request, pk):
    if request.method == 'GET':
        kill_post = Post.objects.get(id=pk)
        if request.user.id == kill_post.user_id or request.user.groups.filter(
                name='Moderator').exists() or request.user.is_superuser:
            kill_post.delete()
            messages.success(request, 'Post deleted successfully')
            return redirect('posts')
        else:
            messages.error(request, 'You do not have permission to delete this post.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def posts_api(request):
    if request.method == 'GET':
        posts_list = Post.objects.all().order_by('-date_posted')
        serializer = PostSerializer(posts_list, many=True)
        resp_format = request.GET.get('format', 'json')
        if resp_format == 'json':
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        if resp_format == 'xml':
            renderer = XMLRenderer()
            return HttpResponse(XMLRenderer.render(renderer, data=serializer.data), content_type='application/xml')


def post_api(request, pk):
    if request.method == 'GET':
        this_post = get_object_or_404(Post, id=pk)
        comments = Comment.objects.filter(post=this_post)
        resp_format = request.GET.get('format', 'json')
        serializer = CommentSerializer(comments, many=True)
        if resp_format == 'json':
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        if resp_format == 'xml':
            renderer = XMLRenderer()
            return HttpResponse(XMLRenderer.render(renderer, data=serializer.data), content_type='application/xml')


@login_required()
def xml_interface(request):
    if not (request.user.is_authenticated and (
            request.user.groups.filter(name='Moderator').exists() or request.user.is_superuser)):
        return HttpResponseForbidden()
    if request.method == 'GET':
        form = XMLDownloadForm()
        return render(request, 'socialSite/XML_Interface.html', {'form': form})
