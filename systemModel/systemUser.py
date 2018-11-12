from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core import serializers
import json

def user_veiw(request):
    return render(request, 'system/systemUser.html')

def user_page(request):
    userList = User.objects.get_queryset().order_by('id')
    paginator = Paginator(userList, 2)
    page = request.POST.get('page')
    try:
        userPage = paginator.page(page)
    except PageNotAnInteger:
        userPage = paginator.page(1)
    except EmptyPage:
        userPage = paginator.page(paginator.num_pages)

    data = serializers.serialize("json", userPage)
    resp = {'code': '200', 'data': data}
    return HttpResponse(json.dumps(resp))
