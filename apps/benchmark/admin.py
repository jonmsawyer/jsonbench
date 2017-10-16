from django.contrib import admin

from apps.benchmark.models import BenchmarkSuite, BenchmarkStep, BenchmarkLog

class StepInline(admin.StackedInline):
    model = BenchmarkStep

class LogInline(admin.StackedInline):
    model = BenchmarkLog
    max_num = 1

class BenchmarkSuiteAdmin(admin.ModelAdmin):
    inlines = [
        StepInline,
        LogInline
    ]

admin.site.register(BenchmarkSuite, BenchmarkSuiteAdmin)
admin.site.register(BenchmarkStep)
admin.site.register(BenchmarkLog)
