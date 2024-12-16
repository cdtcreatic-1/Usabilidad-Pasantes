from django.contrib import admin
from .models import *

class DesignQuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'test_id']
    filter_horizontal = ['heuristics']

class DesignTestAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields['code'].initial = str(uuid.uuid4())[:10]
        return form

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user_id = request.user
        super().save_model(request, obj, form, change)

class EvaluatorStandardResponseAdmin(admin.ModelAdmin):
    list_display = ['question', 'evaluator_access', 'is_complete']

admin.site.register(DesignQuestion, DesignQuestionAdmin)
admin.site.register(DesignTest, DesignTestAdmin)
admin.site.register(EvaluatorStandardResponse, EvaluatorStandardResponseAdmin)
admin.site.register(EvaluatorHeuristicResponse)
#///////////////////////////////////////////////////////////////////////////
admin.site.register([HeuristicCheckList, HeuristicOwner, HeuristicDescriptions, HeuristicEvaluations, PorcentajeCheckList, EvaluatorInfo, User])