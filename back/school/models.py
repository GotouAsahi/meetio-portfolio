from django.db import models
from django.utils.translation import gettext_lazy as _


class School(models.Model):
    classification = models.CharField(_('学校区分'),blank=True,max_length=10,null=True)
    name = models.CharField(_('学校名'),blank=True,max_length=40,null=True)
    faculty = models.CharField(_('学部'),blank=True,max_length=30,null=True)
    department = models.CharField(_('学科'),blank=True,max_length=30,null=True)
    grade = models.IntegerField(_('学年'), blank=True,null=True)
    graduation_year = models.CharField(_('卒業年度'),blank=True,max_length=5,null=True)

    def __str__(self) -> str:
        return str(self.name)