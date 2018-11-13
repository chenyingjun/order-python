from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from datetime import datetime

def user_veiw(request):
    return render(request, 'system/systemUser.html')

def user_page(request):
    page = request.POST.get('pageNum')
    pageSize = request.POST.get('pageSize')
    userList = User.objects.get_queryset().order_by('id')
    paginator = Paginator(userList, pageSize)
    try:
        userPage = paginator.page(page)
    except PageNotAnInteger:
        userPage = paginator.page(1)
    except EmptyPage:
        userPage = paginator.page(paginator.num_pages)

    list = []
    for user in userPage:
        isActive = '是' if user.is_active == True else '否'
        lastLogin = datetime.strftime(user.last_login, '%Y-%m-%d %H:%M:%S') if user.last_login is not None else ''
        dateJoined = datetime.strftime(user.date_joined, '%Y-%m-%d %H:%M:%S') if user.date_joined is not None else ''
        list.append({'id': user.id, 'username': user.username, 'email': user.email, 'lastLogin': lastLogin, 'dateJoined': dateJoined, 'isActive': isActive})
    resp = {'code': '200', 'data': {'total': userList.count(), 'numPages': paginator.num_pages, 'pageNum': userPage.number, 'pageSize': pageSize, 'size': list.__len__(), 'list': list}}
    return JsonResponse(resp)
