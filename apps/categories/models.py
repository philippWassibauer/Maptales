from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.utils.translation import ugettext_lazy as _

from treebeard.mp_tree import MP_Node

#
# Managers
#

class CategoryManager(models.Manager):
    """ custom manager for categories """

    def update_categories(self, obj, categories):
        """ updates the categories for the given object """
        ctype = ContentType.objects.get_for_model(obj)
        current_categorized_items = CategorizedItem.objects.filter(content_type=ctype, object_id=obj.id)
        
        # delete CategorizedItems not present in categories
        current_categorized_items.exclude(category__in=categories).delete()
        
        # Find what categories to add
        # FIXME: is there any optimized query for this?
        categories_to_add = self.exclude(items__in=current_categorized_items).filter(id__in=[c.id for c in categories])
        
        # create categorized items  for this
        for c in categories_to_add:
            CategorizedItem.objects.create(category=c, object=obj)

    def get_for_model(self, model):
        ctype = ContentType.objects.get_for_model(model)
        return self.filter(items__content_type=ctype).distinct()

    def get_for_object(self, obj):
        ctype = ContentType.objects.get_for_object(obj)
        return self.filter(items__content_type=ctype,
            object_id=obj.pk).distinct()
    
    def usage_for_queryset(self, queryset, counts=False, min_count=None):
        """
        Obtain a list of tags associated with instances of a model
        contained in the given queryset.

        If ``counts`` is True, a ``count`` attribute will be added to
        each tag, indicating how many times it has been used against
        the Model class in question.

        If ``min_count`` is given, only tags which have a ``count``
        greater than or equal to ``min_count`` will be returned.
        Passing a value for ``min_count`` implies ``counts=True``.
        """
        extra_joins = ' '.join(queryset.query.get_from_clause()[0][1:])
        where, params = queryset.query.where.as_sql()
        if where:
            extra_criteria = 'AND %s' % where
        else:
            extra_criteria = ''
        return None #self._get_usage(queryset.model, counts, min_count, extra_joins, extra_criteria, params)




#
# models
#

class Category(MP_Node):
    """ A category for items """
    name = models.CharField(_("name"), max_length=50, unique=True,
        help_text=_("Name of the Category"))
    slug = models.SlugField(_("slug"), unique=True,
        help_text=_("Slug, normally used in URLs"))
    description = models.TextField(_("description"), blank=True, help_text=_("Description of this category"))
    objects = CategoryManager()
    node_order_by = ('name',)

    class Meta:
        ordering =  ['name']
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


    def __unicode__(self):
        return self.name





class CategorizedItemManager(models.Manager):
    """
    FIXME There's currently no way to get the ``GROUP BY`` and ``HAVING``
          SQL clauses required by many of this manager's methods into
          Django's ORM.

          For now, we manually execute a query to retrieve the PKs of
          objects we're interested in, then use the ORM's ``__in``
          lookup to return a ``QuerySet``.

          Now that the queryset-refactor branch is in the trunk, this can be
          tidied up significantly.
    """
    def get_by_model(self, queryset_or_model, tags):
        """
        Create a ``QuerySet`` containing instances of the specified
        model associated with a given tag or list of tags.
        """
        tags = get_tag_list(tags)
        tag_count = len(tags)
        if tag_count == 0:
            # No existing tags were given
            queryset, model = get_queryset_and_model(queryset_or_model)
            return model._default_manager.none()
        elif tag_count == 1:
            # Optimisation for single tag - fall through to the simpler
            # query below.
            tag = tags[0]
        else:
            return self.get_intersection_by_model(queryset_or_model, tags)

        queryset, model = get_queryset_and_model(queryset_or_model)
        content_type = ContentType.objects.get_for_model(model)
        opts = self.model._meta
        tagged_item_table = qn(opts.db_table)
        return queryset.extra(
            tables=[opts.db_table],
            where=[
                '%s.content_type_id = %%s' % tagged_item_table,
                '%s.tag_id = %%s' % tagged_item_table,
                '%s.%s = %s.object_id' % (qn(model._meta.db_table),
                                          qn(model._meta.pk.column),
                                          tagged_item_table)
            ],
            params=[content_type.pk, tag.pk],
        )


class CategorizedItem(models.Model):
    category = models.ForeignKey(Category, verbose_name=_("category"), related_name="items")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey('content_type', 'object_id')
    objects = CategorizedItemManager()
    
    class Meta:
        unique_together = (('category', 'content_type', 'object_id'),)
        verbose_name = _("Categorized item")
        verbose_name_plural = _("Categorized items")

    def __unicode__(self):
        return u'%s [%s]' % (self.object, self.category)
