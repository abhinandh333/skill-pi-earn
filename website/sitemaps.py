from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class StaticViewSitemap(Sitemap):
    protocol = 'https'

    def items(self):
         return [
            'home',
            'search_employees',
            'contact',
            'signup',
            'login',
        ]

    def location(self, item):
        return reverse(item)
