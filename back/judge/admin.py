from django.contrib import admin
from.models import Problems, Submission_results, Case, Judge_group, Sample_case

class ProblemsAdmin(admin.ModelAdmin):
    list_display = ("title", "id","created_at")
    list_filter = ("created_at",)
    
class Judge_groupAdmin(admin.ModelAdmin):
    list_display = ("name", "id","created_at")
    list_filter = ("created_at",)
    
admin.site.register(Problems,ProblemsAdmin)
admin.site.register(Submission_results)
admin.site.register(Case)
admin.site.register(Judge_group,Judge_groupAdmin)
admin.site.register(Sample_case)

# Register your models here.
