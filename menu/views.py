from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from login.models import NGUOIDUNG
from django.contrib.auth import logout
from .models import DOAN, QUANAN, DONHANGDICHUYEN, GIOHANG
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
# Create your views here. 
@login_required(login_url='') 
def showMenu(request):
    current_user = request.user
    nguoidung = NGUOIDUNG.objects.filter(TEN_DANG_NHAP=current_user.username).first()
    user_role = nguoidung.QUYEN
    context = {
            'username': nguoidung.TEN_DANG_NHAP,
            'fullname': nguoidung.HO_TEN,
            'email': nguoidung.EMAIL,
            'phonenumber': nguoidung.SO_DIEN_THOAI,
            'user_role': user_role
        }

    return render(request, "menu/menu.html", context)
    
class sellerFood(LoginRequiredMixin, View):
    login_url = '/login/'

    def get_context_data(self, request):
        current_user = request.user
        nguoidung = NGUOIDUNG.objects.filter(TEN_DANG_NHAP=current_user.username).first()
        user_role = nguoidung.QUYEN
        nguoi_dung = request.user
        doan_list = DOAN.objects.filter(nguoi_dung=nguoi_dung)
        quanan = QUANAN.objects.filter(nguoi_dung=nguoi_dung).first()
        quanan_id = quanan.id
        quanan_lat = quanan.lat
        quanan_var = quanan.var
        tenquan = quanan.tenquan
        tinhtrangquan = quanan.tinhtrangquan
        danhsachdonhang = GIOHANG.objects.filter( doan__quanan__id = quanan_id ).filter(
                Q(tinhtrang='tinhtrang2') | Q(tinhtrang='tinhtrang4') | Q(tinhtrang='tinhtrang5') | Q(tinhtrang='tinhtrang6') | Q(tinhtrang='tinhtrang7') | Q(tinhtrang='tinhtrang8')
            )
        danhsachdonhangdangthuchien = GIOHANG.objects.filter( doan__quanan__id = quanan_id ).filter(
                Q(tinhtrang='tinhtrang2') | Q(tinhtrang='tinhtrang4') | Q(tinhtrang='tinhtrang5') | Q(tinhtrang='tinhtrang6')
            )
        
        context = {
            'username': nguoidung.TEN_DANG_NHAP,
            'fullname': nguoidung.HO_TEN,
            'email': nguoidung.EMAIL,
            'phonenumber': nguoidung.SO_DIEN_THOAI,
            'user_role': user_role,
            "doan_list": doan_list,
            "tenquan": tenquan,
            "tinhtrangquan": tinhtrangquan,
            "quanan_id": quanan_id,
            "quanan_lat": quanan_lat,
            "quanan_var": quanan_var,
            'danhsachdonhang':danhsachdonhang,
            'danhsachdonhangdangthuchien': danhsachdonhangdangthuchien
        }
        return context

    def get(self, request):
        context = self.get_context_data(request)
        return render(request, "menu/sellerfood.html", context)
    
    def post(self, request):
        if request.method == 'POST':
            if 'action' in request.POST:
                action = request.POST.get('action')
                if action == 'addfood':
                    tendoan = request.POST.get('tendoan')
                    giamua = request.POST.get('giamua')
                    tinhtrangdoan = request.POST.get('tinhtrangdoan')
                    current_user = request.user
                    quanan = QUANAN.objects.filter(nguoi_dung=current_user).first()
                    doan = DOAN(nguoi_dung=current_user, quanan=quanan, tendoan=tendoan, giamua=giamua, tinhtrangdoan=tinhtrangdoan)
                    doan.save()
                    message_addfood = "Thêm đồ ăn thành công"
                    context = self.get_context_data(request)
                    context['message_addfood'] = message_addfood
                    return render(request, 'menu/sellerfood.html', context)
                
                elif action == 'quanan':
                    quanan_id = request.POST.get('quanan_id')
                    quanan = QUANAN.objects.get(id=quanan_id)
                    tenquan = request.POST.get('tenquan')
                    tinhtrangquanan = request.POST.get('tinhtrangquanan')
                    quanan.tenquan = tenquan
                    quanan.tinhtrangquan = tinhtrangquanan
                    quanan.save()
                    message_quanan = "Sửa thông tin thành công"
                    context = self.get_context_data(request)
                    context['message_quanan'] = message_quanan
                    return render(request, 'menu/sellerfood.html', context)
                    
                elif action == 'suafood':
                    doan_id = request.POST.get('doan_id')
                    doan = DOAN.objects.get(id=doan_id)
                    tendoan = request.POST.get('tendoan')
                    giamua = request.POST.get('giamua')
                    tinhtrangdoan = request.POST.get('tinhtrangdoan')
                    doan.tendoan = tendoan
                    doan.giamua = giamua
                    doan.tinhtrangdoan = tinhtrangdoan
                    doan.save()
                    context = self.get_context_data(request)
                    return render(request, 'menu/sellerfood.html', context)
                
                elif action == 'setAddress':
                    diachifull = request.POST.get('pickup_location')
                    diachi = request.POST.get('pickup_location_hide')
                    pickup = diachi.split(',')
                    quanan_id = request.POST.get('quanan_id')
                    quanan = QUANAN.objects.get(id=quanan_id)
                    quanan.lat = float(pickup[0])
                    quanan.var = float(pickup[1])
                    quanan.vitriquan = diachifull
                    quanan.save()
                    message_suaDiaChi = "Sửa địa chỉ thành công"
                    context = self.get_context_data(request)
                    context['message_suaDiaChi'] = message_suaDiaChi
                    return render(request, 'menu/sellerfood.html', context)
                
                elif action == 'deletefood':
                    doan_id = request.POST.get('doan_id')
                    try:
                        doan = DOAN.objects.get(id=doan_id)
                        doan.delete()
                        return JsonResponse({'success': True})
                    except DOAN.DoesNotExist:
                        return JsonResponse({'success': False, 'error': 'Đồ ăn không tồn tại'})
                elif action == 'xacNhanDonHang':
                    giohangid = request.POST.get('giohangid')
                    giohang = GIOHANG.objects.filter(id=giohangid).first()
                    if giohang.tinhtrang == 'tinhtrang2':
                        giohang.tinhtrang = 'tinhtrang4'
                        giohang.save()
                    context = self.get_context_data(request)
                    context['messageXacNhan'] = "Xác nhận món ăn thành công!"
                    return render(request, 'menu/sellerfood.html', context) 
                elif action == 'xacNhanChuanBi':
                    giohangid = request.POST.get('giohangid')
                    giohang = GIOHANG.objects.filter(id=giohangid).first()
                    if giohang.tinhtrang == 'tinhtrang5':
                        giohang.tinhtrang = 'tinhtrang6'
                        giohang.save()
                    context = self.get_context_data(request)
                    context['messageXacNhan'] = "Xác nhận chuẩn bị món ăn thành công! Hãy chuẩn bị món ăn"
                    return render(request, 'menu/sellerfood.html', context) 
        
        return render(request, 'menu/sellerfood.html')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
class userMove(LoginRequiredMixin, View):
    login_url = '/login/'
    def get_context_data(self, request):
        current_user = request.user
        nguoidung = NGUOIDUNG.objects.filter(TEN_DANG_NHAP=current_user.username).first()
        user_role = nguoidung.QUYEN
        nguoi_dung = request.user
        donhangdichuyen_list = DONHANGDICHUYEN.objects.filter(nguoi_dung=nguoi_dung)
        donhanghientai = DONHANGDICHUYEN.objects.filter(
            nguoi_dung=nguoi_dung
            ).filter(
                Q(tinhtrang='tinhtrang1') | Q(tinhtrang='tinhtrang2') | Q(tinhtrang='tinhtrang4')
            )
        context = {
                'username': nguoidung.TEN_DANG_NHAP,
                'fullname': nguoidung.HO_TEN,
                'email': nguoidung.EMAIL,
                'phonenumber': nguoidung.SO_DIEN_THOAI,
                'user_role': user_role, 
                'donhangdichuyen_list': donhangdichuyen_list,
                'donhanghientai': donhanghientai
        }
        return context
    
    def get(self, request):
        context = self.get_context_data(request)
        return render(request, "menu/usermove.html", context)
    
    def post(self, request):
        if request.method == 'POST':
            if 'action' in request.POST:
                action = request.POST.get('action')
                if action == 'datXe':
                    current_user = request.user
                    donhangcuaban = DONHANGDICHUYEN.objects.filter(nguoi_dung=current_user)
                    for donhang in donhangcuaban:
                        if donhang.tinhtrang == 'tinhtrang1' or donhang.tinhtrang == 'tinhtrang2' or donhang.tinhtrang == 'tinhtrang4':
                            context = self.get_context_data(request)
                            return render(request, "menu/usermove.html", context)
                    diemDon = request.POST.get('pickup_location')
                    diemDen = request.POST.get('destination_location')
                    diachiDon = request.POST.get('pickup_location_hide')
                    pickupDon = diachiDon.split(',')
                    diachiDen = request.POST.get('destination_location_hide')
                    pickupDen = diachiDen.split(',')
                    giaTien = request.POST.get('giaTien')
                    donhangdichuyen = DONHANGDICHUYEN(nguoi_dung=current_user, diem_don_lat= float(pickupDon[0]),diem_don_var= float(pickupDon[1]),diem_den_lat= float(pickupDen[0]),diem_den_var= float(pickupDen[1]),giaTien=giaTien, diem_don=diemDon, diem_den=diemDen)
                    donhangdichuyen.save()
                    message_datXe = "Đặt xe thành công"
                    context = self.get_context_data(request)
                    context['message_datXe'] = message_datXe
                    return redirect('menu:usermove')
                elif action == 'huyDon':
                    id = request.POST.get('idDonHang')
                    donhang = DONHANGDICHUYEN.objects.get(id=id)
                    if donhang.tinhtrang == "tinhtrang1":
                        id = request.POST.get('idDonHang')
                        donhang = DONHANGDICHUYEN.objects.get(id=id)
                        donhang.tinhtrang = "tinhtrang3"
                        donhang.save()
                        message_huyDon= "Huỷ đơn thành công"
                        context = self.get_context_data(request)
                        context['message_huyDon'] = message_huyDon
                        return render(request, 'menu/menu.html', context)    
                    else:
                        message_huyDon= "Đơn hàng đang được xử lý. Không thể hủy đơn"
                        context = self.get_context_data(request)
                        context['message_huyDon'] = message_huyDon
                        return redirect('menu:usermove')
        return render(request, 'menu/usermove.html')
    
class driverMove(LoginRequiredMixin, View):
    login_url = '/login/'
    def get_context_data(self, request):
        current_user = request.user
        nguoidung = NGUOIDUNG.objects.filter(TEN_DANG_NHAP=current_user.username).first()
        user_role = nguoidung.QUYEN
        donhangcothenhan = DONHANGDICHUYEN.objects.filter(tinhtrang='tinhtrang1', ten_dang_nhap_tai_xe__isnull=True)
        donhangcuaban = DONHANGDICHUYEN.objects.filter( ten_dang_nhap_tai_xe=current_user.username)
        donhangdangnhan = DONHANGDICHUYEN.objects.filter(
            ten_dang_nhap_tai_xe=current_user.username,
            ).filter(
                Q(tinhtrang='tinhtrang2') | Q(tinhtrang='tinhtrang4')
            )
        context = {
                'username': nguoidung.TEN_DANG_NHAP,
                'fullname': nguoidung.HO_TEN,
                'email': nguoidung.EMAIL,
                'phonenumber': nguoidung.SO_DIEN_THOAI,
                'user_role': user_role, 
                'donhangcothenhans': donhangcothenhan,
                'donhangcuaban': donhangcuaban,
                'donhangdangnhan': donhangdangnhan
        }
        return context
    
    def get(self, request):
        context = self.get_context_data(request)
        return render(request, "menu/drivermove.html", context)
    
    def post(self, request):
        if request.method == 'POST':
            if 'action' in request.POST:
                action = request.POST.get('action')
                if action == 'nhandon':
                    tentaixe = request.POST.get('username')
                    id = request.POST.get('idDonHang')
                    vitritaixe = request.POST.get('diachitaixe')
                    vitritaixehide = request.POST.get('diachitaixehide')
                    vitritaixemang = vitritaixehide.split(',')
                    vitri_lat = float(vitritaixemang[0])
                    vitri_var = float(vitritaixemang[1])
                    donhang = DONHANGDICHUYEN.objects.get(id=id)
                    if donhang.tinhtrang != "tinhtrang1":
                        message_nhanDon= "Đơn hàng này đã được xử lý."
                        context = self.get_context_data(request)
                        context['message_nhanDon'] = message_nhanDon
                        return redirect('menu:drivermove')
                    else:
                        donhang.ten_dang_nhap_tai_xe=tentaixe
                        donhang.tinhtrang = "tinhtrang2"
                        donhang.vitritaixe = vitritaixe
                        donhang.vitritaixe_lat=vitri_lat
                        donhang.vitritaixe_var=vitri_var
                        donhang.save()
                        message_nhanDon= "Nhận đơn thành công"
                        context = self.get_context_data(request)
                        context['message_nhanDon'] = message_nhanDon
                        return redirect('menu:drivermove')
                elif action == 'chuyenTrangThaiDonHang':
                    id = request.POST.get('idDonHang')
                    donhang = DONHANGDICHUYEN.objects.get(id=id)
                    if donhang.tinhtrang == "tinhtrang2":
                        donhang.tinhtrang = "tinhtrang4"
                        donhang.save()
                        message_chuyenTrangThai= "Đã xác nhận tới điểm đón"
                        context = self.get_context_data(request)
                        context['message_chuyenTrangThai'] = message_chuyenTrangThai
                        return redirect('menu:drivermove')
                    else:
                        donhang.tinhtrang = "tinhtrang5"
                        donhang.save()
                        message_chuyenTrangThai= "Đã xác nhận hoàn thành đơn hàng"
                        context = self.get_context_data(request)
                        context['message_chuyenTrangThai'] = message_chuyenTrangThai
                        return redirect('menu:drivermove')
        return render(request, 'menu/drivermove.html')
    
class userFood(LoginRequiredMixin, View):
    login_url = '/login/'

    def get_context_data(self, request):
        current_user = request.user
        nguoidung = NGUOIDUNG.objects.filter(TEN_DANG_NHAP=current_user.username).first()
        user_role = nguoidung.QUYEN
        nguoi_dung = request.user
        doan_list = DOAN.objects.all()
        quanan_list = QUANAN.objects.filter(tinhtrangquan = 'tinhtrang1')
        giohangcuaban = GIOHANG.objects.filter( nguoi_dung=current_user, tinhtrang='tinhtrang1' ).order_by('doan__quanan__id')
        giohangdangxuly = GIOHANG.objects.filter( nguoi_dung=current_user ).filter(
                Q(tinhtrang='tinhtrang2') | Q(tinhtrang='tinhtrang4') | Q(tinhtrang='tinhtrang5') | Q(tinhtrang='tinhtrang6')  | Q(tinhtrang='tinhtrang7') 
            )
        listDonHang  = GIOHANG.objects.filter( nguoi_dung=current_user ).filter(
                Q(tinhtrang='tinhtrang2') | Q(tinhtrang='tinhtrang3') |Q(tinhtrang='tinhtrang4') | Q(tinhtrang='tinhtrang5') | Q(tinhtrang='tinhtrang6')  | Q(tinhtrang='tinhtrang7')| Q(tinhtrang='tinhtrang8') 
            )
        context = {
            'username': nguoidung.TEN_DANG_NHAP,
            'fullname': nguoidung.HO_TEN,
            'email': nguoidung.EMAIL,
            'phonenumber': nguoidung.SO_DIEN_THOAI,
            'user_role': user_role,
            'doan_list': doan_list,
            'quanan_list':quanan_list, 
            # 'giohangcuaban':giohangcuaban,
            'giohangdangxuly':giohangdangxuly,
            'listDonHang':listDonHang,

        }
        return context
    
    def get(self, request):
        context = self.get_context_data(request)
        return render(request, "menu/userfood.html", context)
    
    def post(self, request):
        if request.method == 'POST':
            if 'action' in request.POST:
                action = request.POST.get('action')
                if action == 'getDanhSachMonAn':
                    quananid = request.POST.get('quananid')
                    quanan= QUANAN.objects.filter(id=quananid).first()
                    listdoan = DOAN.objects.filter(quanan = quanan).filter( Q(tinhtrangdoan='tinhtrang1') |  Q(tinhtrangdoan='Còn hàng') )
                    giohangcuaban = GIOHANG.objects.filter( nguoi_dung=request.user, tinhtrang='tinhtrang1',doan__quanan__id = quananid )
       
                    context = self.get_context_data(request)
                    context['listDoAn'] = listdoan
                    context['giohangcuaban'] = giohangcuaban  
                    context['quananlat'] = quanan.lat
                    context['quananvar'] = quanan.var
                    return render(request, 'menu/userfood.html', context)
                elif action == 'themGioHang':
                    nguoidung = request.user
                    idMonAn = request.POST.get('idMonAn')
                    doan = DOAN.objects.get(pk=idMonAn)
                    checkGioHang = GIOHANG.objects.filter(nguoi_dung=nguoidung, doan=doan, tinhtrang='tinhtrang1').first()
                    if checkGioHang:
                        checkGioHang.soluong = checkGioHang.soluong + 1
                        checkGioHang.save()
                    else:
                        giohang = GIOHANG(nguoi_dung = nguoidung, doan=doan)
                        giohang.save()
                    quanan= QUANAN.objects.filter(id=doan.quanan.id).first()
                    listdoan = DOAN.objects.filter(quanan = quanan)
                    context = self.get_context_data(request)
                    context['listDoAn'] = listdoan
                    return render(request, 'menu/userfood.html', context) 
                elif action == 'datMonAn':
                    # current_user = request.user
                    giohangid = request.POST.get('giohangid')
                    giohang = GIOHANG.objects.filter(id=giohangid).first()
                    diem_giao =  giohangid = request.POST.get('pickup_location')
                    diachiGiao = request.POST.get('pickup_location_hide')
                    giaTien = request.POST.get('giaTien')
                    pickupGiao = diachiGiao.split(',')
                    if giohang.tinhtrang == 'tinhtrang1':
                        giohang.tinhtrang = 'tinhtrang2'
                        giohang.diem_giao = diem_giao
                        giohang.diem_giao_lat = float(pickupGiao[0])
                        giohang.diem_giao_var = float(pickupGiao[1])
                        giohang.tienship = float(giaTien)
                        giohang.save()
                    context = self.get_context_data(request)
                    context['messageDatMonAn'] = "Đặt món ăn thành công! Chờ quán ăn xác nhận."
                    return render(request, 'menu/userfood.html', context) 
                elif action == 'deletefood':
                            giohangid = request.POST.get('giohang_id')
                            try:
                                giohang = GIOHANG.objects.get(id=giohangid)
                                giohang.delete()
                                return JsonResponse({'success': True})
                            except DOAN.DoesNotExist:
                                return JsonResponse({'success': False, 'error': 'Sản phẩm không tồn tại'})
                                
        return render(request, 'menu/userfood.html')
    
class driverFood(LoginRequiredMixin, View):
    login_url = '/login/'

    def get_context_data(self, request):
        current_user = request.user
        nguoidung = NGUOIDUNG.objects.filter(TEN_DANG_NHAP=current_user.username).first()
        user_role = nguoidung.QUYEN
        donhangcothenhan = GIOHANG.objects.filter(tinhtrang='tinhtrang4', ten_dang_nhap_tai_xe__isnull=True)
        
        context = {
            'username': nguoidung.TEN_DANG_NHAP,
            'fullname': nguoidung.HO_TEN,
            'email': nguoidung.EMAIL,
            'phonenumber': nguoidung.SO_DIEN_THOAI,
            'user_role': user_role,
            'donhangcothenhan':donhangcothenhan
        }
        return context
    
    def get(self, request):
        context = self.get_context_data(request)
        return render(request, "menu/driverfood.html", context)
    
    def post(self, request):
        if request.method == 'POST':
            if 'action' in request.POST:
                action = request.POST.get('action')
                if action == 'deletefood':
                            giohangid = request.POST.get('giohang_id')
                            try:
                                giohang = GIOHANG.objects.get(id=giohangid)
                                giohang.delete()
                                return JsonResponse({'success': True})
                            except DOAN.DoesNotExist:
                                return JsonResponse({'success': False, 'error': 'Sản phẩm không tồn tại'})