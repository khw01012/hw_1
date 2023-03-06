from django.shortcuts import render
import googletrans
# Create your views here.
def index(request):
    bf = request.GET.get("bf", "")
    fr = request.GET.get("fr", "")
    to = request.GET.get("to", "")
    context = {
        "ndict" : googletrans.LANGUAGES,
        "fr" : fr,
        "to" : to,
    }
    if bf:
        trans = googletrans.Translator()
        after = trans.translate(bf, src=fr, dest=to)        
        context.update({
            "bf" : bf,
            "af" : after.text,
        })

    return render(request, "trans/index.html", context)