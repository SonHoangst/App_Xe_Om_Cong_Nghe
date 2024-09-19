from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class QUANAN(models.Model):
    nguoi_dung = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    tenquan = models.CharField(max_length=100, default="Chưa xác định tên quán ăn!")
    vitriquan = models.CharField(max_length=150, null=True)
    lat = models.FloatField(default=0)
    var = models.FloatField(default=0)
    TEN_tinhtrangquan_CHOICES = (
        ('tinhtrang1', 'Mở cửa'),
        ('tinhtrang2', 'Đóng cửa'),
    )
    tinhtrangquan = models.CharField(max_length=255, choices=TEN_tinhtrangquan_CHOICES, default='tinhtrang2')
    def __str__(self):
        return f"{self.tenquan}"

class DOAN(models.Model):
    nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quanan = models.ForeignKey(QUANAN, on_delete=models.CASCADE)
    tendoan = models.CharField(max_length=100, default="Chưa xác định tên đồ ăn!")
    giamua = models.IntegerField(default=0)
    TEN_tinhtrangdoan_CHOICES = (
        ('tinhtrang1', 'Còn hàng'),
        ('tinhtrang2', 'Hết hàng'),
    )
    tinhtrangdoan = models.CharField(max_length=255, choices=TEN_tinhtrangdoan_CHOICES, default='tinhtrang1')
    def __str__(self):
        return f"{self.tendoan}"
    
class DONHANGDICHUYEN(models.Model):
    nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ten_dang_nhap_tai_xe = models.CharField(max_length=100, null=True)
    vitritaixe = models.CharField(max_length=150, null=True)
    diem_don = models.CharField(max_length=150, null=True)
    diem_den = models.CharField(max_length=150, null=True)
    vitritaixe_lat=models.FloatField(default=0)
    vitritaixe_var=models.FloatField(default=0)
    diem_don_lat=models.FloatField(default=0)
    diem_don_var=models.FloatField(default=0)
    diem_den_lat=models.FloatField(default=0)
    diem_den_var=models.FloatField(default=0)
    giaTien = models.IntegerField(default=0)
    hoaHong = models.FloatField(default=0)
    status = (
        ('tinhtrang1', 'Chờ xác nhận'),
        ('tinhtrang2', 'Đã xác nhận'),
        ('tinhtrang3', 'Đã hủy'),
        ('tinhtrang4', 'Đang di chuyển'),
        ('tinhtrang5', 'Đã hoàn thành'),
    )
    tinhtrang = models.CharField(max_length=255, choices=status, default='tinhtrang1')
    
    def save(self, *args, **kwargs):
        self.hoaHong = float(self.giaTien) * 0.7
        super(DONHANGDICHUYEN, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nguoi_dung.username}"
    

class GIOHANG(models.Model):
    nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    doan= models.ForeignKey(DOAN, on_delete=models.CASCADE)
    diem_giao = models.CharField(max_length=150, null=True)
    diem_giao_lat=models.FloatField(default=0)
    diem_giao_var=models.FloatField(default=0)
    ten_dang_nhap_tai_xe = models.CharField(max_length=100, null=True)
    vitritaixe_lat=models.FloatField(default=0)
    vitritaixe_var=models.FloatField(default=0)
    vitritaixe = models.CharField(max_length=150, null=True)
    soluong = models.IntegerField(default=1)
    status = (
        ('tinhtrang1', 'Thêm vào giỏ hàng'),
        ('tinhtrang2', 'Đặt hàng'),
        ('tinhtrang3', 'Đã hủy'),
        ('tinhtrang4', 'Quán ăn xác nhận'),
        ('tinhtrang5', 'Tài xế xác nhận'),
        ('tinhtrang6', 'Quán ăn đang chuẩn bị'),
        ('tinhtrang7', 'Tài xế đang trên đường giao'),
        ('tinhtrang8', 'Đã hoàn thành'),
    )
    tinhtrang = models.CharField(max_length=255, choices=status, default='tinhtrang1')
    ngayMua = models.DateTimeField(default=datetime.now())
    tienship = models.IntegerField(default=0)
    tongTien = models.IntegerField(default=0)
    thanhTien = models.IntegerField(default=0)
    hoaHong = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.tongTien = self.soluong * self.doan.giamua
        self.thanhTien = self.soluong * self.doan.giamua + self.tienship
        self.hoaHong = float(self.tienship) * 0.7
        super(GIOHANG, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nguoi_dung.username} - {self.doan.tendoan} - {self.soluong}"
    