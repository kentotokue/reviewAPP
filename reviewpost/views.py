from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate,login,logout
from .models import ReviewModel
from django.views.generic import CreateView

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


# Create your views here.

#サインアップの処理
def signupview(request):
    #print(request.POST.get('username_data'))
    if request.method == 'POST':
        username_data = request.POST['username_data']
        password_data = request.POST['password_data']
        try:
            user = User.objects.create_user(username_data,'',password_data)
        except IntegrityError:
            return render(request,'signup.html',{'error':'このユーザーは既に登録されています。'})
        print('POST method')
    else:
        return render(request, 'signup.html',{})
    return render(request, 'signup.html',{})

#ログインの処理
def loginview(request):
    if request.method == 'POST':
        username_data =request.POST['username_data']
        password_data =request.POST['password_data']
        user = authenticate(request,username = username_data,password = password_data)
        
        if user is not None:
            login(request,user)
            return redirect('list')
        else:
            return redirect('login')
    return render(request,'login.html')

#リストの表示
@login_required
def listview(request):
    object_list = ReviewModel.objects.all()
    return render(request,'list.html',{'object_list':object_list})

#詳細の表示
@login_required
def detailview(request,pk):
    object = ReviewModel.objects.get(pk = pk)
    return render(request,'detail.html',{'object':object})

#レビュー作成
class CreateClass(CreateView):
    template_name = 'create.html'
    model = ReviewModel 
    fields = ('title','content','author','images','evaluation')
    success_url = reverse_lazy('list')

#ログアウトの処理
def logoutview(request):
    logout(request)
    return redirect('login')

#「参考になった」ボタンの処理
def evaluationview(request,pk):
    post = ReviewModel.objects.get(pk=pk)
    author_name = request.user.get_username() + str(request.user.id)
    if author_name in post.useful_review_record:
        return redirect('list')
    else:
        post.useful_review = post.useful_review + 1
        post.useful_review_record = post.useful_review_record + author_name
        post.save()
        return redirect('list')