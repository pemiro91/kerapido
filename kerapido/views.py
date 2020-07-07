from django.shortcuts import render
from kerapido.models import Fotos


# Create your views here.

def upload_images(request):
    if request.POST:
        for file in request.FILES.getlist('images'):
            instance = Fotos(
                title="Pacho",
                file=file
            )
            instance.save()
    context = {}
    return render(request, "base.html", context)
