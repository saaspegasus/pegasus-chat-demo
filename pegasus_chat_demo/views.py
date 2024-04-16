from django.template.response import TemplateResponse


def chat(request):
    return TemplateResponse(request, "chat_demo/single_chat.html")
