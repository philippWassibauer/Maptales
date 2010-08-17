from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from blog.models import Post
from tagging.models import Tag, TaggedItem
from photos.models import Image
from bookmarks.models import BookmarkInstance

from wiki.models import Article as WikiArticle

def tags(request, tag, template_name='tags/index.html'):
    tag = get_object_or_404(Tag, name=tag)
    
    alltags = TaggedItem.objects.get_by_model(Post, tag).filter(status=2)
    
    phototags = TaggedItem.objects.get_by_model(Image, tag)

    return render_to_response(template_name, {
        'tag': tag,
        'alltags': alltags,
        'phototags': phototags,
        'bookmarktags': bookmarktags,
        'project_tags': project_tags,
        'project_topic_tags': project_topic_tags,
        'project_task_tags': project_task_tags,
        'wiki_article_tags': wiki_article_tags,
    }, context_instance=RequestContext(request))
