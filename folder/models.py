from django.db import models

# Create your models here.
class Folder(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='Product_id')
    user_id = models.ForeignKey("users", related_name="users", on_delete=models.CASCADE, db_column="user_id")
    name = models.CharField(null=True, max_length=255, verbose_name='폴더 이름')
    description = models.CharField(null=True, max_length=255, verbose_name='폴더 설명')
    created_at = models.DateTimeField(null = True, auto_now=True, verbose_name='추가된 날짜')
    updated_at = models.DateTimeField(null = True, auto_now=True, verbose_name='업뎃 된 날짜')
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name='삭제된 날짜')
    Is_deleted = models.BooleanField(blank = False, null = True, default= False, verbose_name='삭제된 상품인지 여부')

    class Meta:
        # abstract = True  # sqlite3 사용 시 어째선지 이게 있으면 마이그레이션이 안 됨.
        managed = True
        db_table = 'folders'
        app_label = 'folder'
        ordering = ['created_at', ]
        verbose_name_plural = '폴더'