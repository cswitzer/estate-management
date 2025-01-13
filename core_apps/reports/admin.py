from django.contrib import admin

from core_apps.reports.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["id", "reported_user", "reported_by", "created_at"]
    search_fields = ["reported_user__username", "reported_by__username"]
    list_filter = ["created_at"]
    date_hierarchy = "created_at"
    readonly_fields = ["id", "created_at"]
    ordering = ["-created_at"]
