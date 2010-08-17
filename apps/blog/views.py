from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.db import IntegrityError
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import date_based
from django.conf import settings

from blog.models import Post,PostImage
from blog.forms import BlogForm, BlogImageForm
import datetime

try:
    from notification import models as notification
except ImportError:
    notification = None

try:
    from friends.models import Friendship
    friends = True
except ImportError:
    friends = False

def main_blog(request, template_name="blog/main_blog.html"):
    blogposts = Post.objects.filter(status=2).select_related(depth=1) \
              .order_by("-publish") \
              .filter(author__is_staff=True)

    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(30) 
    featured_post = Post.objects.filter(publish__range=(start_date, end_date)).order_by('-views')
    if featured_post.count() > 0:
        featured_post = featured_post[0]
    else:
        featured_post = None

    search_terms = request.GET.get('search', '')
    if search_terms:
        blogposts = blogposts.filter(Q(title__icontains=search_terms)|Q(body__icontains=search_terms))

    return render_to_response(template_name, {
        "search_terms": search_terms,
        "featured_post": featured_post,
        "blogposts": blogposts,
    }, context_instance=RequestContext(request))

def blogs(request, username=None, template_name="blog/blogs.html"):
    blogs = Post.objects.filter(status=2).select_related(depth=1).order_by("-publish")
    if username is not None:
        user = get_object_or_404(User, username=username.lower())
        blogs = blogs.filter(author=user)
    return render_to_response(template_name, {
        "blogs": blogs,
    }, context_instance=RequestContext(request))

def post(request, username, slug, template_name="blog/post.html"):
    post = Post.objects.filter(slug=slug)
    if not post:
        raise Http404

    # check if post is only a draft
    if post[0].status == 1 and post[0].author != request.user:
        raise Http404
    
    post = post[0]
    post.views += 1

    post.save()

    try:
        next = post.get_next_by_publish()
    except:
        next = False

    try:
        previous = post.get_previous_by_publish()
    except:
        previous = False

    return render_to_response(template_name, {
        "post": post,
        "next": next,
        "previous": previous,
    }, context_instance=RequestContext(request))

@login_required
def your_posts(request, template_name="blog/your_posts.html"):
    return render_to_response(template_name, {
        "blogs": Post.objects.filter(author=request.user),
    }, context_instance=RequestContext(request))


@login_required
def destroy(request, id):
    post = Post.objects.get(pk=id)
    user = request.user
    title = post.title
    if post.author != request.user:
            request.user.message_set.create(message="You can't delete posts that aren't yours")
            return HttpResponseRedirect(reverse("blog_list_yours"))

    if request.method == "POST" and request.POST["action"] == "delete":
        post.delete()
        request.user.message_set.create(message=_("Successfully deleted post '%s'") % title)
        return HttpResponseRedirect(reverse("main_blog"))
    else:
        return HttpResponseRedirect(reverse("main_blog"))

    return render_to_response(context_instance=RequestContext(request))


@login_required
def new(request, form_class=BlogForm, template_name="blog/new.html"):
    if request.method == "POST":
        blog_form = form_class(request.user, request.POST, request.FILES)
        
        if blog_form.is_valid():
            blog = blog_form.save(request)
            return HttpResponseRedirect(blog.get_absolute_url())
    else:
        blog_form = form_class()

    return render_to_response(template_name, {
        "blog_form": blog_form
    }, context_instance=RequestContext(request))


@login_required
def edit(request, id, form_class=BlogForm, template_name="blog/edit.html"):
    post = get_object_or_404(Post, id=id)

    if request.method == "POST":
        if post.author != request.user:
            request.user.message_set.create(message="You can't edit posts that aren't yours")
            return HttpResponseRedirect(blog.get_absolute_url())
        blog_form = form_class(request.user, request.POST, request.FILES, instance=post)
    
        if blog_form.is_valid():
            old_title = post.title
            blog = blog_form.save(commit=False)
            if old_title != blog.title:
                from django.template.defaultfilters import slugify
                blog.slug = slugify(blog.title)
                from misc.utils import make_unique 
                blog.slug = make_unique(blog, lambda x: Post.objects.filter(slug__exact=x.slug).exclude(id=x.id).count() == 0)

            blog.save()
            request.user.message_set.create(message=_("Successfully updated post '%s'") % blog.title)
            #if notification:
                #if blog.status == 2: # published
                    #if friends: # @@@ might be worth having a shortcut for sending to all friends
                        #notification.send((x['friend'] for x in Friendship.objects.friends_for_user(blog.author)), "blog_friend_post", {"post": blog})
            
            return HttpResponseRedirect(blog.get_absolute_url())
    else:
        blog_form = form_class(instance=post)

    return render_to_response(template_name, {
        "blog_form": blog_form,
        "post": post,
    }, context_instance=RequestContext(request))


def post_selector_list(request, username, template_name="blog/post_selector_list.html"):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author__username=username).order_by("-publish")
    dynamic_div = 'dynamic_blogpost_list_div'
    ref_url = reverse('post_selector_list',args=(username,))
    return render_to_response(template_name, {
        "viewed_user": user,
        "posts": posts,
        "ref_url": ref_url,
        "dynamic_div": dynamic_div,
        "callback_function": request.GET.get("callback"),
    }, context_instance=RequestContext(request))