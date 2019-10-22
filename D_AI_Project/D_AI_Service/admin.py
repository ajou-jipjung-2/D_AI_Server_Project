from django.contrib import admin
from .models import NounLabel, AdjLabel

# class NounAdmin(admin.ModelAdmin):
#     list_display = ['id', 'noun', 'count', 'created_at' ]
# admin.site.register(NounLabel, NounAdmin)
admin.site.register(AdjLabel)
# Register your models here.

# @admin.register(NounLabel)
# class NounAdmin(admin.ModelAdmin):
#
# 	def delete(self, obj):
# 		return '<input type="button" value="Delete" onclick="location.href=\'%s/delete/\'" />'.format(obj.pk)
#
# 	delete.allow_tags = True
# 	delete.short_description = 'Delete object'
#
# 	list_display = ['id', 'noun', 'count','created_at','delete']
# 	list_display_links = ['id', 'noun']


class ResourceAdmin(admin.ModelAdmin):

	def delete(self, obj):
		return '<input type="button" value="Delete" onclick="location.href=\'%s/delete/\'" />'.format(obj.pk)

	delete.allow_tags = True
	delete.short_description = 'Delete object'

	list_display = ('id',  'noun', 'count', 'delete')

admin.site.register(NounLabel, ResourceAdmin)