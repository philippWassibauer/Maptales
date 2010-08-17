#import datetime
#from haystack import indexes
#from haystack.sites import site
#from blog.models import Post
#
#from haystack.sites import site#
#
#class PostIndex(indexes.SearchIndex):
#    text = indexes.CharField(document=True, use_template=True)
#    title = indexes.CharField(model_attr='title')
#    creator = indexes.CharField(model_attr='author')
#    created_at = indexes.DateTimeField(model_attr='created_at')
#    updated_at = indexes.DateTimeField(model_attr='updated_at')
#    publish_at = indexes.DateTimeField(model_attr='publish')
#    tags = indexes.CharField(model_attr='tags')
#
#    def get_query_set(self):
#        return Post.objects.filter(status=2, publish__lte=datetime.datetime.now())
#
#
#site.register(Post, PostIndex)
#
#
