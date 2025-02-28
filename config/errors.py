from django.shortcuts import render

from django.views import View


class CustomPageNotFoundView(View):
    def get(self, request, exception=None):
        return render(request, '404.html', status=404)

custom_page_not_found_as_view = CustomPageNotFoundView.as_view()
