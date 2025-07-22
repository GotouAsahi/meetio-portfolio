from django.contrib import admin
from.models import Category, Portfolio,Tag,Comment,Reply,Ganre,Portfolio_Draft,TitleImage,Image
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("title", "id","created_date")
    list_filter = ("created_date",)
admin.site.register(Category)
admin.site.register(Ganre)
admin.site.register(Portfolio,PortfolioAdmin)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Portfolio_Draft)
admin.site.register(TitleImage)
admin.site.register(Image)