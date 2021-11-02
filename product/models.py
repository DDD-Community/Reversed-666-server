from django.db import models 

# Create your models here. 

class Product(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='Product_id')
    user_id = models.ForeignKey("users", null = False, related_name="users", on_delete=models.CASCADE, db_column="user_id")
    folder_id = models.ForeignKey("folders", null = False, related_name="folders", on_delete=models.CASCADE, db_column="folder_id")
    brand_id = models.ForeignKey("brands", null = True, related_name="brands", on_delete=models.CASCADE, db_column="brand_id")
    added_brand_id = models.ForeignKey("added_brands", null = True, related_name="added_brands", on_delete=models.CASCADE, db_column="added_brand_id")

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