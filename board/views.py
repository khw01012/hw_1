from django.shortcuts import render, redirect
from .models import Board
from django.core.paginator import Paginator
# Create your views here.

def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(request.user)
    return redirect("board:detail", bpk)

def unlikey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    return redirect("board:detail", bpk)

def index(request):
    pg = request.GET.get("page", 1)
    cate = request.GET.get("cate", "")
    kw = request.GET.get("kw", "")

    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            try:
                from acc.models import User
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none()

        elif cate == "con":
            b = Board.objects.filter(content__contains=kw)
    else:
        b = Board.objects.all()

    b = b.order_by("-pubdate")
    pag = Paginator(b, 3)
    obj = pag.get_page(pg)
    context = {
        "bset" : obj,
        "kw" : kw,
        "cate" : cate
    }
    return render(request, "board/index.html", context)


def update(request, bpk):
    b = Board.objects.get(id=bpk)

    if request.user != b.writer:
        return redirect("board:index")
        
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        b.subject, b.content = s,c
        b.save()
        return redirect("board:detail", bpk)
    context = {
        "b" :b
    }
    return render(request, "board/update.html", context)

def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        Board(subject=s, writer=request.user, content=c).save()
        return redirect("board:index")
    return render(request, "board/create.html")

def delete(request, bpk):
    b = Board.objects.get(id=bpk)
    if request.user == b.writer:
        b.delete()
    else:
        pass # 메세지 (불법적인 접근)
    return redirect("board:index")

def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    context = {
        "b" : b
    }
    return render(request, "board/detail.html", context)

