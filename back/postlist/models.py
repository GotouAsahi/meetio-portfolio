import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.timezone import now
from login.models import User
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

@deconstructible
class FileExtensionValidator:
    def __init__(self, allowed_extensions):
        self.allowed_extensions = allowed_extensions

    def __call__(self, value):
        file_extension = value.name.split('.')[-1].lower()
        if file_extension not in self.allowed_extensions:
            raise ValidationError(f"許可されている拡張子は {', '.join(self.allowed_extensions)} です。")

def file_size(value):
    limit = 1000000000
    if value.size>limit:
        raise ValidationError('File too large. Size should not exceed 1GB.')

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'category'
class Ganre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return '{} {} '.format(self.name, self.id)
    
    class Meta:
        db_table = 'ganre'

class Tag(models.Model):
    name = models.CharField('タグ', primary_key=True, unique=True, max_length=20)

    def __str__(self):
        return self.name

def create_default_group(sender, **kwargs):
    names = ['テクノロジー', 'ビジネス', 'クリエイティブ', 'サウンド', 'ビデオ', 'デザイン', 'AI/機械学習', 'IoT', 'ソフトウェア開発',
            'ネットワーク/セキュリティ', 'データサイエンス/データ分析', 'クラウドコンピューティング', 'ゲーム開発', 'ビジネス戦略/コンサルティング',
            'マーケティング/広告', 'プロジェクト管理', 'データ分析/ビジネスインテリジェンス', '事業開発/新規事業', '販売/営業', '写真',
            'マルチメディア制作', 'イラスト', 'アート作品', '音楽制作', '声優', 'ナレーション', 'ビデオ/映像制作', 'アニメーション制作',
            '映画/ドラマ制作', '俳優', 'パフォーマンス', '製品デザイン', 'インテリアデザイン', 'グラフィックデザイン', 'イベントデザイン',
            'デジタルデザイン', 'ウェブデザイン', 'キャラクターデザイン']
    
    for x,y in enumerate(names):
        Category.objects.get_or_create(name=y) if x < 6 else Ganre.objects.get_or_create(name=y)
        
import uuid
def hash_id(article_id):
    return hashlib.sha256(str(article_id).encode('utf-8')).hexdigest()

class Portfolio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, models.DO_NOTHING,default=1)
    category_id = models.ForeignKey(Category, models.DO_NOTHING,default=1)
    ganre_id = models.ForeignKey(Ganre, models.DO_NOTHING,default=1)
    title = models.CharField(max_length=100, db_index=True)
    # title_image = models.ImageField(upload_to="thumbnail",blank=True, null=True)
    title_image = models.CharField(max_length=100, blank=True, null=True)
    movie = models.FileField(upload_to="movie/", validators=[FileExtensionValidator(allowed_extensions=['MOV','MPEG4','mp4','mp3','mpeg' ]),file_size],blank=True, null=True)
    sentence = models.TextField(db_index=True)
    like_count = models.ManyToManyField(User,blank=True, related_name='like')
    created_date = models.DateTimeField(default=now)
    update_date = models.DateTimeField(default=now)
    view_count = models.PositiveBigIntegerField(default=0, db_index=True)
    is_public = models.BooleanField(default=True)
    tag = models.ManyToManyField(Tag, verbose_name='タグ', blank=True)
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = hash_id(str(uuid.uuid4()))
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        #adminで見にくいと思いますが、いいね機能で必要なので　str(self.id)　は変更しないでください
        return self.title
    
    class Meta:
        db_table = 'portfolio'

class Portfolio_Draft(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING,default=1)
    category_id = models.ForeignKey(Category, models.DO_NOTHING,default=1)
    ganre_id = models.ForeignKey(Ganre, models.DO_NOTHING,default=1)
    title = models.CharField(max_length=100, db_index=True)
    title_image = models.CharField(max_length=100, blank=True, null=True)
    movie = models.FileField(upload_to="movie/", validators=[FileExtensionValidator(allowed_extensions=['MOV','MPEG4','mp4','mp3','mpeg' ]),file_size],blank=True, null=True)
    sentence = models.TextField(db_index=True)
    #like_count = models.ManyToManyField(User,blank=True, related_name='like')
    created_date = models.DateTimeField(default=now)
    #update_date = models.DateTimeField(default=now)
    #view_count = models.PositiveBigIntegerField(default=0, db_index=True)
    #is_public = models.BooleanField(default=True)
    tag = models.ManyToManyField(Tag, verbose_name='タグ', blank=True)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        db_table = 'portfolio_Draft'


#五島町
class TitleImage(models.Model):

    image = models.ImageField(upload_to="thumbnail",verbose_name="画像",blank=True,null=True)

    class Meta:
        db_table = "title_image"
        
class Image(models.Model):

    image = models.ImageField(upload_to="sentence_image",verbose_name="画像",blank=True,null=True)

    class Meta:
        db_table = "image"


class Reply(models.Model):
    """コメントに紐づく返信"""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField('コメント')
    created_at = models.DateTimeField('作成日', default=now)
    is_public = models.BooleanField('公開設定', default=True)
   
    def __str__(self):
        return self.text[:20]

class Comment(models.Model):
    """記事に紐づくコメント"""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField('コメント')
    target = models.ForeignKey(Portfolio, on_delete=models.CASCADE, verbose_name='対象記事')
    reply = models.ManyToManyField(Reply,symmetrical=False,blank=True, related_name='reply')
    created_at = models.DateTimeField('作成日', default=now)
    is_public = models.BooleanField('公開設定', default=True)

    def __str__(self):
        return self.text[:20]

