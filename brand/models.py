from django.db import models

# Create your models here. 

class Brand(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='브랜드 id')
    name = models.CharField(null=False, max_length=255, verbose_name='브랜드 이름')
    en_name = models.CharField(null=False, max_length=255, verbose_name='브랜드 영어 이름')
    site_url = models.CharField(null=True, max_length=255, verbose_name='브랜드 url')
    logo_url = models.CharField(null=True, max_length=255, verbose_name='로고 url')
    total_click_count = models.BigIntegerField(null=False, default = 0, verbose_name='브랜드를 클릭한 횟수')
    like_count = models.BigIntegerField(null=False, default = 0, verbose_name='브랜드를 좋아요한 횟수')

    created_at = models.DateTimeField(null = False, auto_now_add=True, verbose_name='생성된 날짜')
    updated_at = models.DateTimeField(null = True, auto_now=True, verbose_name='수정된 날짜')
    deleted_at = models.DateTimeField(null = True, verbose_name='삭제된 날짜')
    Is_deleted = models.BooleanField( null = True, default= False, verbose_name='삭제된 브랜드인지 여부')
    class Meta:
        # abstract = True  # sqlite3 사용 시 어째선지 이게 있으면 마이그레이션이 안 됨.
        managed = True
        db_table = 'brands'
        app_label = 'brand'
        ordering = ['created_at', ]
        verbose_name_plural = '브랜드'


class addedBrand(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='브랜드 id')
    user_id = models.ForeignKey("users", related_name="users", on_delete=models.CASCADE, db_column="user_id")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성된 날짜')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정된 날짜')
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name='삭제된 날짜')
    name = models.CharField(null=False, max_length=255, verbose_name='브랜드 이름')
    en_name = models.CharField(null=False, max_length=255, verbose_name='브랜드 영어 이름')
    site_url = models.CharField(null=True, max_length=255, verbose_name='브랜드 url')
    logo_url = models.CharField(null=True, max_length=255, verbose_name='로고 url')

    class Meta:
        # abstract = True  # sqlite3 사용 시 어째선지 이게 있으면 마이그레이션이 안 됨.
        managed = True
        db_table = 'added_brands'
        app_label = 'brand'
        ordering = ['created_at', ]
        verbose_name_plural = '유저가 추가한 브랜드'

class likedBrand(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='브랜드 id')
    user_id = models.ForeignKey("users", related_name="users", on_delete=models.CASCADE, db_column="user_id")
    brand_id = models.ForeignKey("brands", related_name="brands", on_delete=models.CASCADE, db_column="brand_id")
    added_brand_id = models.ForeignKey("added_brands", related_name="added_brands", on_delete=models.CASCADE, db_column="added_brand_id")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성된 날짜')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정된 날짜')
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name='삭제된 날짜')

    class Meta:
        # abstract = True  # sqlite3 사용 시 어째선지 이게 있으면 마이그레이션이 안 됨.
        managed = True
        db_table = 'liked_brands'
        app_label = 'brand'
        ordering = ['created_at', ]
        verbose_name_plural = '유저가 담은 브랜드'