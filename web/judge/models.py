from django.db import models
from django.core.validators import validate_slug

from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=32, default='')
    
    def __str__(self):
        return '[#{}][profile size={}]'.format(self.name, self.profiles.count())

class Problem(models.Model):
    # this is convenient when you are now constructing a problem and don't want
    # users to see it for the time being
    staff_viewable_only = models.BooleanField(default=False)

    name = models.CharField(primary_key=True, blank=False, max_length=32)
    title = models.CharField(max_length=32)

    course = models.ForeignKey(Course, related_name='problems',
        blank=True, null=True, on_delete=models.SET_NULL)

    description = models.TextField()

    input_format = models.TextField()
    output_format = models.TextField()
    
    sample_input = models.TextField()
    sample_output = models.TextField()

    deadline_datetime = models.DateTimeField()

    language = models.CharField(max_length=2,
                                choices=[('CP', 'C++'),
                                         ('PY', 'Python'),
                                         ('JA', 'Java')],
                                default='JA')

    def __str__(self):
        return self.brief()
    
    def brief(self):
        return '[#{}][Course={}] {}'.format(
            self.name,
            self.course.name,
            self.title
        )
    
    def detail(self):
        r = ''
        r += 'staff_viewable_only: ' + str(self.staff_viewable_only) + '\n'
        r += 'course: ' + self.group + '\n'
        r += 'name: ' + self.name + '\n'
        r += 'title: ' + self.title + '\n'
        r += 'deadline_datetime: ' + str(self.deadline_datetime) + '\n'
        r += 'language: ' + self.language + '\n'
        return r

    class Meta:
        ordering = ['pk']


class RequiredFile(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    filename = models.CharField(max_length=32)
    via = models.CharField(max_length=1,
                           choices=[('S', 'Submitted'),
                                    ('P', 'Provided')])

    def __str__(self):
        return '[#{}][Problem={{{}}}] {} ({})'.format(
            self.pk,
            str(self.problem),
            self.filename,
            self.get_via_display()
        )

    class Meta:
        ordering = ['problem__pk', 'via', 'filename']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, 
        related_name='profile', primary_key=True)
    
    courses = models.ManyToManyField(Course, related_name='profiles', blank=True)

    name = models.CharField(max_length=32)

    github_account = models.CharField(max_length=32,
                                      blank=True,
                                      validators=[validate_slug])
    github_repository = models.CharField(max_length=32,
                                         blank=True,
                                         validators=[validate_slug])

    solved_problems = models.ManyToManyField(Problem,
                                             related_name='solved_profiles',
                                             blank=True)

    def __str__(self):
        return '[#{}][User={}][Courses={}] {}'.format(
            self.pk,
            self.user,
            ', '.join([i.name for i in self.courses.all()])
                if self.courses.exists() else None,
            self.name
        )
    
    class Meta:
        ordering = ['user__username']


class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    status = models.CharField(max_length=2,
                              choices=[('FE', 'Format Error'),
                                       ('SU', 'Submitting'),
                                       ('SE', 'Submission Error'),
                                       ('CO', 'Compiling'),
                                       ('CE', 'Compilation Error'),
                                       ('JU', 'Judging'),
                                       ('AC', 'Accepted'),
                                       ('WA', 'Wrong Answer'),
                                       ('RE', 'Runtime Error')],
                              default='SU')
    submission_datetime = models.DateTimeField()

    # detailed_messages = models.TextField(blank=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return '[#{}][Problem={{{}}}][Profile={{{}}}]'.format(
            self.pk,
            str(self.problem),
            str(self.profile)
        )
    
    def has_message(self):
        return bool(self.message)
    
    def get_message_header(self):        
        if self.status == 'WA':
            return 'The following mismatches occurred during comparison:'
        
        if self.status == 'RE':
            return 'The following errors occurred during execution:'
        
        return self.get_status_display() + ':'
    
    def get_message(self):
        return self.message

    class Meta:
        ordering = ['-pk']
