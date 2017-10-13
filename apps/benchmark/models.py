from django.db import models


class Benchmark(models.Model):
    app = models.CharField(max_length=255, blank=True, null=True)
    suite = models.CharField(max_length=255, blank=True, null=True)
    suite_description = models.CharField(max_length=255, blank=True, null=True)
    command_line_arguments = models.CharField(max_length=255, blank=True, null=True)
    db_type = models.CharField(max_length=255, blank=True, null=True)
    db_info = models.CharField(max_length=255, blank=True, null=True)
    db_stat_before_benchmark = models.CharField(max_length=255, blank=True, null=True)
    db_stat_after_benchmark = models.CharField(max_length=255, blank=True, null=True)
    computer_info = models.CharField(max_length=255, blank=True, null=True)
    django_version = models.CharField(max_length=255, blank=True, null=True)
    django_user = models.CharField(max_length=255, blank=True, null=True)
    last_handled_exception = models.CharField(max_length=255, blank=True, null=True)
    last_unhandled_exception = models.CharField(max_length=255, blank=True, null=True)
    records_in = models.PositiveIntegerField(blank=True, null=True)
    records_out = models.PositiveIntegerField(blank=True, null=True)
    begin_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    is_complete = models.NullBooleanField()
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return '{id} | {created_at} | {app} | {suite} | {db_type} | {django_version}'.format(
            id=self.id, created_at=self.created_at, app=self.app,
            suite=self.suite, db_type=self.db_type, django_version=self.django_version
        )

class BenchmarkStep(models.Model):
    benchmark = models.ForeignKey(Benchmark)
    number = models.PositiveIntegerField()
    description = models.CharField(max_length=255, blank=True, null=True)
    last_handled_exception = models.CharField(max_length=255, blank=True, null=True)
    last_unhandled_exception = models.CharField(max_length=255, blank=True, null=True)
    records_in = models.PositiveIntegerField(blank=True, null=True)
    records_out = models.PositiveIntegerField(blank=True, null=True)
    begin_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    is_complete = models.NullBooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return '{id} | Benchmark ID {bid} | Step {number} | {description}'.format(
            id=self.id, bid=self.benchmark.id,
            number=self.number, description=self.description
        )

class BenchmarkLog(models.Model):
    benchmark = models.ForeignKey(Benchmark)
    log = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return '{id} | Benchmark ID {bid} | Created at {created_at} | Updated at {updated_at}'.format(
            id=self.id, bid=self.benchmark.id,
            created_at=self.created_at, updated_at=self.updated_at
        )
