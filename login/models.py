from django.db import models

# Create your models here.
class NGUOIDUNG(models.Model):
    TEN_DANG_NHAP = models.CharField(max_length=100)
    HO_TEN = models.CharField(max_length=100)
    EMAIL = models.EmailField(max_length=100)
    SO_DIEN_THOAI = models.CharField(max_length=20)
    QUYEN_CHOICES = [
        ('user', 'Người dùng'),
        ('driver', 'Tài xế'),
        ('seller', 'Người bán'),
    ]
    QUYEN = models.CharField(max_length=10, choices=QUYEN_CHOICES)

    def __str__(self):
        return self.TEN_DANG_NHAP