from django.contrib import admin
from assets import models
# Register your models here.
from assets import asset_handler


admin.site.site_header = 'Michael后台管理'
admin.site.site_title = 'Michael'


class AssetAdmin(admin.ModelAdmin):
    list_display = ['sn', 'asset_type', 'name', 'status', 'department_per', 'c_time', 'm_time']
    list_filter = ['asset_type', 'status', 'c_time']
    search_fields = ('sn', 'manage_ip')

    def save_model(self, request, obj, form, change):
        obj.approved_by = request.user
        obj.save()


class ServerAdmin(admin.ModelAdmin):
    list_display = ['ser_sub_asset_type', 'ser_os_type', 'ser_department_per', 'ser_phone', 'ser_mail']
    list_filter = ['ser_sub_asset_type', 'ser_os_type']
    search_fields = ('ser_department_per', )


class NewAssetAdmin(admin.ModelAdmin):
    list_display = ['aud_asset_type', 'aud_sn', 'aud_name', 'aud_department_per', 'c_time', 'm_time']
    list_filter = ['aud_asset_type', 'aud_status', 'c_time']
    search_fields = ('aud_sn', 'aud_manage_ip')

    actions = ['approve_selected_assets']

    def approve_selected_assets(self, request, queryset):
        # 获得被打钩的checkbox对应的资产
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        success_upline_number = 0
        for asset_id in selected:
            obj = asset_handler.ApproveAsset(request, asset_id)
            ret = obj.asset_upline()
            if ret:
                success_upline_number += 1
        # 顶部绿色提示信息
        self.message_user(request, "成功批准  %s  条新资产上线！" % success_upline_number)

    approve_selected_assets.short_description = '通过审核'

# class NewAssetAdmin(admin.ModelAdmin):
#     list_display = ['asset_type', 'sn', 'model', 'manufacturer', 'c_time', 'm_time']
#     list_filter = ['asset_type', 'manufacturer', 'c_time']
#     search_fields = ('sn',)
#
#     actions = ['approve_selected_assets']
#
#     def approve_selected_assets(self, request, queryset):
#         selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
#         success_upline_number = 0
#         for asset_id in selected:
#             obj = asset_handler.ApproveAsset(request, asset_id)
#             ret = obj.asset_upline()
#             if ret:
#                 success_upline_number += 1
#
#         self.message_user(request, "成功批准  %s  条新资产上线！" % success_upline_number)
#
#     approve_selected_assets.short_description = '批准新资产上线'


admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.Server, ServerAdmin)
admin.site.register(models.OtherDevice)
admin.site.register(models.SecurityDevice)
admin.site.register(models.NetworkDevice)
# admin.site.register(models.Software)
admin.site.register(models.BusinessUnit)
# admin.site.register(models.Contract)
admin.site.register(models.Tag)
admin.site.register(models.IDC)
admin.site.register(models.Services)
admin.site.register(models.Database)
admin.site.register(models.Middleware)
admin.site.register(models.Manufacturer)
# admin.site.register(models.CPU)
# admin.site.register(models.Disk)
# admin.site.register(models.NIC)
# admin.site.register(models.RAM)
admin.site.register(models.EventLog)
admin.site.register(models.NewAssetApprovalZone, NewAssetAdmin)
