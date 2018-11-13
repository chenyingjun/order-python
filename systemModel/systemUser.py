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
    usernameParam = request.POST.get('username')
    isActiveParam = request.POST.get('isActive')
    startTimeParam = request.POST.get('startTime')
    endTimeParam = request.POST.get('endTime')
    userList = User.objects.get_queryset()
    if usernameParam is not None:
        userList = userList.get(username__contains=usernameParam)
    if isActiveParam is not None:
        userList = userList.get(is_active__contains=isActiveParam)
    if startTimeParam is not None:
        startTime = datetime.strptime(startTimeParam + ' 00:00:00', '%Y%m%d %H:%M:%S')
        userList = userList.filter(last_login__gte=startTime)
    if endTimeParam is not None:
        endTime = datetime.strptime(endTimeParam + ' 23:59:59', '%Y%m%d %H:%M:%S')
        userList = userList.filter(last_login__lte=endTime)
    userList = userList.order_by('-id')
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
