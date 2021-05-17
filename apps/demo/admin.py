from django.contrib import admin

from demo.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_sn', 'trade_no', 'pay_status']


admin.site.site_title = "关关雎鸠管理后台"
admin.site.site_header = "关关雎鸠管理后台"
