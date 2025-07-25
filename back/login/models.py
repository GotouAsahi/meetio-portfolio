from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone
from school.models import School
from django.conf import settings
import uuid


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Users must have an username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
    
def hash_id(article_id):
    return hashlib.sha256(str(article_id).encode('utf-8')).hexdigest()

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(_('氏名'), max_length=50, blank=False,unique=False)
    nickname = models.CharField(_('ニックネーム'), max_length=50, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True,null=True)
    Profession = models.CharField(_('職業'), max_length=10, blank=False,default="その他")

    icon = models.CharField(max_length=100,blank=True, null=True, default=getattr(settings, 'DEFAULT_ICON_URL'))
    banner = models.CharField(max_length=100, blank=True, null=True, default=getattr(settings, 'DEFAULT_BANNER_URL'))
    introduction = models.CharField(max_length=200, blank=True, null=True)
    
    github = models.CharField(max_length=100,blank=True, null=True)
    twitter = models.CharField(max_length=100,blank=True, null=True)
    instagram = models.CharField(max_length=100,blank=True, null=True)
    facebook = models.CharField(max_length=100,blank=True, null=True)
    pixiv = models.CharField(max_length=100,blank=True, null=True)
    scout_receive = models.BooleanField(default=False)

    followers= models.ManyToManyField('self',symmetrical=False,blank=True, related_name='follower')
    follows= models.ManyToManyField('self',symmetrical=False,blank=True, related_name='follow')
    
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    gender = models.IntegerField(_('性別'), blank=False, null=False,default=3)
    school = models.ForeignKey(School, on_delete=models.CASCADE,blank=True, null=True)
    rank = models.CharField(max_length=1,default="F")
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    
    
    objects = UserManager()

    #EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = hash_id(str(uuid.uuid4()))
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return str(self.username)
    
class Icon(models.Model):

    image = models.ImageField(upload_to="icon",verbose_name="画像",blank=True,null=True)

    class Meta:
        db_table = "icon"
        
class Banner(models.Model):

    image = models.ImageField(upload_to="banner",verbose_name="画像",blank=True,null=True)

    class Meta:
        db_table = "banner"