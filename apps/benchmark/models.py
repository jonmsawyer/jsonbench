import platform, re

import django
from django.utils import timezone
from django.db import models

import psutil


app_re = re.compile('func=(.*?),')

class BenchmarkSuite(models.Model):
    suite_name = models.CharField(max_length=255, blank=True, null=True)
    suite_docstring = models.CharField(max_length=1000, blank=True, null=True)
    command_line_arguments = models.CharField(max_length=255, blank=True, null=True)
    app_to_benchmark = models.CharField(max_length=255, blank=True, null=True)
    db_type = models.CharField(max_length=255, blank=True, null=True)
    db_info = models.CharField(max_length=255, blank=True, null=True)
    db_stat_before_suite = models.CharField(max_length=255, blank=True, null=True)
    db_stat_after_suite = models.CharField(max_length=255, blank=True, null=True)
    cpu_info = models.CharField(max_length=255, blank=True, null=True)
    python_info = models.CharField(max_length=255, blank=True, null=True)
    django_info = models.CharField(max_length=255, blank=True, null=True)
    django_user = models.CharField(max_length=255, blank=True, null=True)
    last_handled_exception = models.CharField(max_length=255, blank=True, null=True)
    last_unhandled_exception = models.CharField(max_length=255, blank=True, null=True)
    records_in = models.PositiveIntegerField(blank=True, null=True)
    records_out = models.PositiveIntegerField(blank=True, null=True)
    begin_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    is_complete = models.NullBooleanField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return '{id} | {created_at} | {app} | {suite} | {duration}'.format(
            id=self.id, created_at=self.created_at, app=self.app_to_benchmark,
            suite=self.suite_name, duration=self.duration
        )
    
    @staticmethod
    def NewWebBenchmarkSuite(request, name):
        try:
            matches = app_re.search(str(request.resolver_match))
            app = matches.groups()[0]
        except Exception as e:
            app = str(request.resolver_match)
        bs = BenchmarkSuite(
            suite_name='web.{}.request.{} {}'.format(name, request.method, request.get_full_path()),
            app_to_benchmark=app,
            cpu_info=str(platform.uname()),
            python_info=str(platform.python_build()),
            django_info=django.get_version(),
            django_user=str(request.user)
        )
        bs.save()
        return bs
    
    def start(self):
        self.is_complete = None
        self.end_time = None
        self.begin_time = timezone.now()
        self.is_complete = None
        self.save()
    
    def stop(self):
        try:
            self.current_step.stop()
        except:
            pass
        self.is_complete = True
        self.end_time = timezone.now()
        self.duration = self.end_time - self.begin_time
        self.is_complete = True
        self.save()
    
    def next_step(self, request, name):
        try:
            current_step = self.current_step
            current_step.stop()
            next_step = current_step.step_number + 1
        except:
            current_step = None
            next_step = 1
        try:
            matches = app_re.search(str(request.resolver_match))
            app = matches.groups()[0]
        except Exception as e:
            app = str(request.resolver_match)
        bs = BenchmarkStep(
            benchmark=self,
            step_number=next_step,
            description='{} | {}'.format(name, app)
        )
        bs.save()
        bs.start()
        self.current_step = bs
    
    def log(self, log):
        BenchmarkLog(benchmark=self, log=log).save()

class BenchmarkStep(models.Model):
    benchmark = models.ForeignKey(BenchmarkSuite)
    step_number = models.PositiveIntegerField()
    description = models.CharField(max_length=255, blank=True, null=True)
    ram_info_before_step = models.CharField(max_length=255, blank=True, null=True)
    ram_info_after_step = models.CharField(max_length=255, blank=True, null=True)
    last_handled_exception = models.CharField(max_length=255, blank=True, null=True)
    last_unhandled_exception = models.CharField(max_length=255, blank=True, null=True)
    records_in = models.PositiveIntegerField(blank=True, null=True)
    records_out = models.PositiveIntegerField(blank=True, null=True)
    begin_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    is_complete = models.NullBooleanField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        # TODO: Fix references
        return '{id} | Benchmark ID {bid} | Step {number} | {description}'.format(
            id=self.id, bid=self.benchmark.id,
            number=self.step_number, description=self.description
        )
    
    def start(self):
        self.begin_time = timezone.now()
        self.end_time = None
        self.duration = None
        self.is_complete = None
        self.ram_info_before_step = str(psutil.virtual_memory())
        self.save()
    
    def stop(self):
        self.end_time = timezone.now()
        self.duration = self.end_time - self.begin_time
        self.is_complete = True
        self.ram_info_after_step = str(psutil.virtual_memory())
        self.save()

class BenchmarkLog(models.Model):
    benchmark = models.ForeignKey(BenchmarkSuite)
    log = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return '{id} | Benchmark ID {bid} | Created at {created_at} | Updated at {updated_at}'.format(
            id=self.id, bid=self.benchmark.id,
            created_at=self.created_at, updated_at=self.updated_at
        )
