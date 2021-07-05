#!/usr/bin/env python3

import sys
import os
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
config.set_up_django()

from django.contrib.auth.models import User
from judge.models import *
import random

#///////////////////////////////////////////////////////////////////////////////

def ReadFile(file_name, mode='r'):
    r=''
    with open(file_name, mode) as f:
        r=f.read()
    return r

#///////////////////////////////////////////////////////////////////////////////

def UserExists(user_name):
    return Profile.objects.filter(name=user_name).exists()

def GetUserModel(user):
    if isinstance(user, User):
        return user

    if isinstance(user, Profile):
        return user.user

    if isinstance(user, str):
        user_filter=User.objects.filter(username=user)
        return user_filter[0] if user_filter.exists() else None

    return None

def GetProfileModel(profile):
    if isinstance(profile, Profile):
        return profile

    if isinstance(profile, User):
        return profile.profile

    if isinstance(profile, str):
        user_filter=User.objects.filter(username=profile)
        return user_filter[0].profile if user_filter.exists() else None

    return None

def CreateProfile(
    student_id,
    password,
    name,
    course,
    github_account,
    github_repository):

    if User.objects.filter(username=student_id).exists():
        return '{}: {} has existed'.format(CreateUser.__name__, student_id)

    course_ = GetCourseModel(course)

    if course_ == None:
        return '{}: {} does not exist'.format(CreateUser.__name__, course)
    
    course = course_

    user = User.objects.create_user(
            username=student_id,
            email=student_id + '@ntu.edu.tw',
            password=password)
    
    user.save()
    
    profile = Profile.objects.create(
        user=user,
        name=name,        
        github_account=github_account,
        github_repository=github_repository)
    
    profile.courses.add(course)
    profile.save()
    print('ok')
    
    return ''

def DeleteUser(user):
    user = GetUserModel(user)

    if user != None:
        user.delete()

#///////////////////////////////////////////////////////////////////////////////

def GetCourseModel(course):
    if isinstance(course, Course):
        return course

    if isinstance(course, str):
        course_filter=Course.objects.filter(name=course)
        return course_filter[0] if course_filter.exists() else None

    return None

def CourseExists(course_name):
    return Course.objects.filter(name=course_name).exists()

def CreateCourse(course_name):
    course_filter = Course.objects.filter(name=course_name)

    if course_filter.exists():
        return course_filter[0]

    return Course.objects.create(name=course_name)

def AddUserToCourse(user, course):
    user=GetUserModel(user)

    if user == None:
        return '{}: user not found'.format(AddUserToCourse.__name__)

    course=GetCourseModel(course)

    if course == None:
        return '{}: course not found'.format(AddUserToCourse.__name__)

    user.courses.add(course)
    user.save()

    return ''

#///////////////////////////////////////////////////////////////////////////////

def ProblemExists(problem_name):
    return Problem.objects.filter(name=problem_name).exists()

def GetProblemModel(problem):
    if isinstance(problem, Problem):
        return problem
    
    if isinstance(problem, str):
        problem_filter=Problem.objects.filter(name=problem)
        return problem_filter[0] if problem_filter.exists() else None
    
    return None

def CreateProblem(
    name,
    staff_viewable_only,
    course,
    title,
    description,
    input_format,
    output_format,
    sample_input,
    sample_output,
    deadline_datetime,
    required_files):

    if ProblemExists(name):
        return '{}: {} has existed'.format(CreateProblem.__name__, name)

    course=GetCourseModel(course)

    if course == None:
        return '{}: course not found'.format(CreateProblem.__name__)

    problem = Problem.objects.create(
        name=name,
        staff_viewable_only=staff_viewable_only,
        course=course,
        title=title,
        description=description,
        input_format=input_format,
        output_format=output_format,
        sample_input=sample_input,
        sample_output=sample_output,
        deadline_datetime=deadline_datetime)
        
    for via in ['S', 'P']:
        for filename in required_files[via]:
            RequiredFile.objects.create(
                problem=problem,
                filename=filename,
                via='S')

    return ''

def CreateProblemFromDir(problem_dir):
    if not os.path.isdir(problem_dir):
        return '{}: \'{}\' is not a valid directory'.format(
            CreateProblemFromDir.__nmae__, problem_dir)

    staff_viewable_only=ReadFile(os.path.join(
        problem_dir, 'staff_viewable_only'))

    if staff_viewable_only == 'True':
        staff_viewable_only=True
    elif staff_viewable_only == 'False':
        staff_viewable_only=False
    else:
        return '{}: staff_viewable_only is neither \'True\' nor \'False\''.format(
            CreateProblemFromDir.__name__)

    name=ReadFile(os.path.join(problem_dir, 'name'))
    course=ReadFile(os.path.join(problem_dir, 'course'))
    title=ReadFile(os.path.join(problem_dir, 'title'))
    description=ReadFile(os.path.join(problem_dir, 'description'))
    input_format=ReadFile(os.path.join(problem_dir, 'input_format'))
    output_format=ReadFile(os.path.join(problem_dir, 'output_format'))
    sample_input=ReadFile(os.path.join(problem_dir, 'sameple_input'))
    sample_output=ReadFile(os.path.join(problem_dir, 'sample_output'))
    deadline_datetime=ReadFile(os.path.join(problem_dir, 'deadline_datetime'))
    
    s=ReadFile(os.path.join(problem_dir, 'required_files')).split('\n')
    required_files={
        'S': [] if s[0] == '' else s[0].split(','),
        'P': [] if s[1] == '' else s[1].split(',') }
    
    CreateProblem(
        name,
        staff_viewable_only=staff_viewable_only,
        course=course,
        title=title,
        description=description,
        input_format=input_format,
        output_format=output_format,
        sample_input=sample_input,
        sample_output=sample_output,
        deadline_datetime=deadline_datetime,
        required_files=required_files)

    return ''

def SetProblem(
    name,
    staff_viewable_only,
    course,
    title,
    description,
    input_format,
    output_format,
    sample_input,
    sample_output,
    deadline_datetime,
    required_files):

    problem_filter=Problem.objects.filter(name=name)

    if not problem_filter.exists():
        return CreateProblem(
            name=name,
            staff_viewable_only=staff_viewable_only,
            course=course,
            title=title,
            description=description,
            input_format=input_format,
            output_format=output_format,
            sample_input=sample_input,
            sample_output=sample_output,
            deadline_datetime=deadline_datetime,
            required_files=required_files)
        
    problem=problem_filter[0]
    
    problem.name=name
    problem.staff_viewable_only=staff_viewable_only
    problem.title=title
    problem.description=description
    problem.input_format=input_format
    problem.output_format=output_format
    problem.sample_input=sample_input
    problem.deadline_datetime=deadline_datetime

    problem.save()

    for via in ['S', 'P']:
        for filename in required_files[via]:
            f=RequiredFile(
                problem=problem,
                filename=filename,
                via='S')
            
            f.save()
    

#///////////////////////////////////////////////////////////////////////////////

def ShowUserStats(user, problems=None):
    user=GetUserModel(user)

    if user == None:
        return '{}: user not found'.format(CreateProblem.__name__)

    profile=user.profile
    
    print('name             : ', profile.name, sep='')
    print('username         : ', user.username, sep='')
    print('password         : ', user.password, sep='')
    print('github_account   : ', profile.github_account, sep='')
    print('github_repository: ', profile.github_repository, sep='')
    print('solved_problems  : ')

    if problems == None:
        problems=Problem.objects.filter(course__in=user.profile.courses.all())

    solved_problems=profile.solved_problems.all()

    for problem in problems:
        problem_str=str(problem)
        print('\t{}:{}{}'.format(
            problem_str,
            ' ' * (max(40 - len(problem_str), 5)),
            '  Solved' if problem in solved_problems else 'Unsolved'
        ))
    
    return ''

def ShowProblemStatus():
    for problem in Problem.objects.all():
        print(problem)

def ShowCourseStatus(course=None):
    '''
    course = GetCourseModel(course)

    for user in course.profiles.all():
        print(user.profile)
    
    for problem in course.problems.all():
        print(problem)
    '''

    for courses in Course.objects.all():
        print(courses)


#///////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////

def main():
    return

if __name__ == '__main__':
    main()