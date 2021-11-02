from django.db import models 
from user.models import User
from folder.models import Folder
from brand.models import Brand, addedBrand, likedBrand

# Create your models here. 

class Product(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='Product_id')
    user_id = models.ForeignKey(User, null = True, blank = False, on_delete=models.CASCADE)
    folder_id = models.ForeignKey(Folder, null = True, blank = False, on_delete=models.CASCADE)
    brand_id = models.ForeignKey(Brand, null = True, blank = True, on_delete=models.CASCADE)
    added_brand_id = models.ForeignKey(addedBrand, null = True, blank = True, on_delete=models.CASCADE)

    name = models.CharField(null=True, max_length=255, verbose_name='상품 이름')
    price = models.CharField(null=True, max_length=255, verbose_name='상품 가격')
    image_url = models.CharField(null=True, max_length=255, verbose_name='상품 이미지 링크')
    site_url = models.CharField(null=True, max_length=255, verbose_name='상품 사이트 링크')
    
    created_at = models.DateTimeField(null = False, auto_now_add=True, verbose_name='생성된 날짜')
    updated_at = models.DateTimeField(null = True, auto_now=True, verbose_name='수정된 날짜')
    deleted_at = models.DateTimeField(null = True, verbose_name='삭제된 날짜')
    Is_deleted = models.BooleanField( null = False, default= False, verbose_name='삭제된 브랜드인지 여부')


    class Meta:
        # abstract = True  # sqlite3 사용 시 어째선지 이게 있으면 마이그레이션이 안 됨.
        managed = True
        db_table = 'products'
        app_label = 'product'
        ordering = ['created_at', ]
        verbose_name_plural = '상품'