from django.db import models
from user.models import User

# Create your models here.
class Folder(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='Product_id')
    user = models.ForeignKey(User, null = True, blank = False, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=255, verbose_name='폴더 이름')
    description = models.CharField(null=True, blank = True, max_length=255, verbose_name='폴더 설명')

    created_at = models.DateTimeField(null = False, auto_now_add=True, verbose_name='생성된 날짜')
    updated_at = models.DateTimeField(null = True, auto_now=True, verbose_name='수정된 날짜')
    deleted_at = models.DateTimeField(null = True, verbose_name='삭제된 날짜')
    Is_deleted = models.BooleanField( null = False, default= False, verbose_name='삭제된 브랜드인지 여부')

    class Meta:
        # abstract = True  # sqlite3 사용 시 어째선지 이게 있으면 마이그레이션이 안 됨.
        managed = True
        db_table = 'folders'
        app_label = 'folder'
        ordering = ['created_at', ]
        verbose_name_plural = '폴더'