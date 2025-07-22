from django.db import models
from login.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid
from django.utils.translation import gettext_lazy as _
# 問題一覧

def hash_id(article_id):
    return hashlib.sha256(str(article_id).encode('utf-8')).hexdigest()

class Problems(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField(null=True)
    problem = models.TextField(verbose_name='問題',null=True)
    difficulty=models.IntegerField(null=True, default=1,validators=[MinValueValidator(0),MaxValueValidator(5)])
    target_time=models.IntegerField(verbose_name='目標回答時間',null=True,default=5)
    sample_explanation = models.TextField(verbose_name='サンプル説明',null=True)
    is_public = models.BooleanField(default=True)
    group_only = models.BooleanField(default=False)
    created_at = models.DateTimeField(_('created_at'), default=timezone.now)
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = hash_id(str(self.id ))
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'problems'

    def __str__(self) -> str:
        return str(f"{self.id}_{self.title}")

class Judge_group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    admins = models.ManyToManyField(User, blank=True,related_name='admin')
    problems = models.ManyToManyField(Problems,verbose_name='問題',blank=True, related_name='judge_groups')
    member = models.ManyToManyField(User, blank=True,related_name='member')
    introduction = models.CharField(max_length=1000, blank=True, null=True)
    starttime = models.DateTimeField(null=True,blank=True)
    endtime = models.DateTimeField(null=True,blank=True)
    is_public = models.BooleanField(default=True)
    finish = models.BooleanField(default=True)
    created_at = models.DateTimeField(_('created_at'), default=timezone.now)
    class Meta: 
        db_table = 'judge_group'
    """
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = hash_id(str(uuid.uuid4()))
        super().save(*args, **kwargs)
    """
    
def create_default_group(sender, **kwargs):
    fixed_uuid_str = "11111111-1111-1111-1111-111111111111"  # 任意のUUID文字列
    fixed_uuid = uuid.UUID(fixed_uuid_str)
    fixed_uuid_str2 = "22222222-2222-2222-2222-222222222222"  # 任意のUUID文字列
    fixed_uuid2 = uuid.UUID(fixed_uuid_str2)
    Judge_group.objects.get_or_create(name="difflist",id=fixed_uuid,is_public=False)
    Judge_group.objects.get_or_create(name="tutorial",id=fixed_uuid2,is_public=False)
# サンプルケース
class Sample_case(models.Model):
    case = models.TextField(null=True)
    answer = models.TextField(null=True)
    problem_id = models.ForeignKey(Problems, models.DO_NOTHING,default=1)
    class Meta:
        db_table = 'sample_case'
    
    def __str__(self) -> str:
        return str(self.problem_id)

# テストケース
class Case(models.Model):
    case = models.TextField(null=True)
    answer = models.TextField(null=True)
    problem_id = models.ForeignKey(Problems, models.DO_NOTHING,default=1)
    class Meta:
        db_table = 'test_case'
    
    def __str__(self) -> str:
        return str(self.problem_id)
    
# 提出結果
class Submission_results(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING,default=1)
    problem_id = models.ForeignKey(Problems, models.DO_NOTHING,default=1)
    group_id = models.ForeignKey(Judge_group, models.DO_NOTHING,default=0)
    language = models.CharField(max_length=20)  #提出言語
    code = models.TextField(null=True)  #コード
    status = models.CharField(max_length=10,blank=True,default="NG")    #ステータス
    score = models.IntegerField(blank=True, default=0)  # 点数
    created_at = models.DateTimeField(blank=True,default=timezone.now)
    class Meta:
        db_table = 'submission_results'
    
    def __str__(self) -> str:
        return str(f"{self.user_id}_{self.problem_id}")