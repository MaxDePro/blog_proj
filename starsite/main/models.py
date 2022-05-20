from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Post(models.Model):

    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    body = models.TextField(max_length=800, blank=True, db_index=True)
    data_pub = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_pub']

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('tags_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tags_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tags_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
