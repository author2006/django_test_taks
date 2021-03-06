from django.db import models


# Create your models here.
class GroupManager(models.Manager):
    def get_queryset(self):
        return super(GroupManager, self).get_queryset().select_related('group_monitor').prefetch_related('student_set')


class Student(models.Model):
    full_name = models.CharField(max_length=75)
    photo = models.ImageField(upload_to='students')
    birthdate = models.DateField()
    studentid_cart = models.CharField(max_length=25, blank=True)
    group = models.ForeignKey(to='Group')

    def __unicode__(self):
        return self.full_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.studentid_cart:
            try:
                student_id = self.id or (Student.objects.latest('id').id + 1)
            except Student.DoesNotExist:
                student_id = 1

            self.studentid_cart = u'{}-{}'.format(self.group.group_name, student_id)

        super(Student, self).save(force_insert, force_update, using, update_fields)


class Group(models.Model):
    group_name = models.CharField(max_length=25)
    group_monitor = models.ForeignKey(to=Student, related_name='+', blank=True, null=True, default=None)

    objects = GroupManager()

    def __unicode__(self):
        return self.group_name

    def get_group_monitor(self):
        return self.group_monitor.full_name if self.group_monitor else 'Group monitor not assigned.'

    get_group_monitor.short_description = 'Group monitor'

    def _students_count(self):
        return self.student_set.count()

    students_count = property(_students_count)
