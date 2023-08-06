from django.contrib import admin

# 引入用户平台
from .models import *


class RolePermissionAdmin(admin.ModelAdmin):
    fields = (
        "id", "type", "role", "api", "menu", "filter_filed_list", "remove_filed_list", "default_value_dict",
        "allow_values_dict", "output_filter_filed_list", "output_remove_filed_list", "created_time",
    )
    list_display = (
        "id", "type", "role", "api", "menu", "filter_filed_list", "remove_filed_list", "default_value_dict",
        "allow_values_dict", "output_filter_filed_list", "output_remove_filed_list", "created_time",
    )
    readonly_fields = ['id', "created_time"]
    list_per_page = 20


class GroupAdmin(admin.ModelAdmin):
    fields = ('id', 'group', 'group_name', 'parent_group_id', 'description')
    list_display = ('id', 'group', 'group_name', 'parent_group_id', 'description')
    readonly_fields = ['id']
    list_per_page = 20


class RoleAdmin(admin.ModelAdmin):
    fields = ('id', 'role', 'role_name', 'parent_role_id', 'user_group', 'description')
    list_display = ('id', 'role', 'role_name', 'parent_role_id', 'description')
    readonly_fields = ['id']
    list_per_page = 20


class UserToGroupAdmin(admin.ModelAdmin):
    fields = ('id', 'user_id', 'user_group')
    list_display = ('id', 'user_id', 'user_group')
    readonly_fields = ['id']
    list_per_page = 20


class UserToRoleAdmin(admin.ModelAdmin):
    fields = ('id', 'user_id', 'role')
    list_display = ('id', 'user_id', 'role')
    readonly_fields = ['id']
    list_per_page = 20


admin.site.register(RolePermission, RolePermissionAdmin)
admin.site.register(RoleUserGroup, GroupAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(UserToGroup, UserToGroupAdmin)
admin.site.register(UserToRole, UserToRoleAdmin)
