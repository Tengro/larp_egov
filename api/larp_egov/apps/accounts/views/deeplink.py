from django.views.generic import TemplateView


class DeeplinkView(TemplateView):
    template_name = "deeplink.html"
