from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['home', 'about', 'contact', 'search']  # Add your named URL patterns here

    def location(self, item):
        return reverse(item)
