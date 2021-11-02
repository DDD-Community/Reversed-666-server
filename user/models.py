from django.db import models

# Create your models here.
class User(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='사용자 id')
    apple_id = models.CharField(null=False, max_length=255, verbose_name='애플 아이디')
    kakao_id = models.CharField(null=False, max_length=255, verbose_name='카카오 아이디')
    email = models.CharField(null=False, max_length=255, verbose_name='사용자 이메일')
    password = models.CharField(null=False, max_length=255, verbose_name='사용자 비밀번호')
    nickname = models.CharField(null=False, max_length=255, verbose_name='사용자 별명')
    profile_image = models.CharField(null=True, max_length=255, verbose_name='프로필 이미지 url')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성된 날짜')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정된 날짜')
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name='삭제된 날짜')
    Is_deleted = models.BooleanField(blank = False, null = True, default= False, verbose_name='삭제된 유저인지 여부')
    role = models.CharField(null=True, max_length=255, verbose_name='사용자 역할')

    class Meta:
        # abstract = True  # sqlite3 사용 시 어째선지 이게 있으면 마이그레이션이 안 됨.
        managed = True
        db_table = 'users'
        app_label = 'user'
        ordering = ['created_at', ]
        verbose_name_plural = '사용자'