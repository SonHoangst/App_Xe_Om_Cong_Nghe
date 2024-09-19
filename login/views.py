from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User
from .models import NGUOIDUNG
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from menu.models import QUANAN

# Create your views here.
class LoginAndRegister(View):
    def get(self, request):
        return render(request, "login/login.html")

    def post(self, request):
        if request.method == 'POST':
            if 'action' in request.POST:
                action = request.POST.get('action')
                if action == 'login':
                    username = request.POST.get('username')
                    password = request.POST.get('password')
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        menu_url = reverse('menu:showMenu')
                        return redirect(menu_url)
                    else:
                        error_message = "Tên đăng nhập hoặc mật khẩu không hợp lệ"
                        return render(request, 'login/login.html', {'error_message': error_message})
                elif action == 'register':
                    username = request.POST.get('username')
                    password = request.POST.get('password')
                    email = request.POST.get('email')
                    fullname = request.POST.get('fullname')
                    phonenumber = request.POST.get('phonenumber')
                    role = request.POST.get('role')
                    
                    if User.objects.filter(username=username).exists():
                        error_message = "Tên đăng nhập đã tồn tại"
                        return render(request, 'login/login.html', {'error_message': error_message})
                    else:
                        user = User.objects.create_user(username, email, password)
                        user.save()
                        nguoidung = NGUOIDUNG(TEN_DANG_NHAP=username, HO_TEN=fullname, EMAIL=email, SO_DIEN_THOAI=phonenumber, QUYEN=role)
                        nguoidung.save()

                        if role == 'seller':
                            quanan = QUANAN(nguoi_dung=user, tenquan="Chưa xác định tên quán ăn!", lat=0, var=0, tinhtrangquan='tinhtrang2')
                            quanan.save()
                        error_message = "Đăng ký thành công. Vui lòng đăng nhập"
                        return render(request, 'login/login.html', {'error_message': error_message})
        return render(request, 'login/login.html')
    
@login_required(login_url='') 
def dangxuat(request):
    logout(request)
    return redirect("login:LoginAndRegister")