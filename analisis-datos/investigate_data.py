import unicodecsv as csv
from datetime import datetime as dt
import numpy as np

#### Function for reading the file ##############
def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = csv.DictReader(f)
        return list(reader)
################################################


### Functions for fixing the data types #########
def parse_string(number):
    if number == "":
        return None
    else:
        return str(number)

def parse_int(number):
    if number == "":
        return None
    else:
        return int(number)

def parse_float(number):
    if number == "":
        return None
    else:
        return float(number)

def parse_date(date):
    if date == "":
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')

def parse_bool(boolean):
    if boolean == "True":
        boolean = True;
    else:
        boolean = False;
    return boolean
###############################################


############ Read the files ###################
enrollments = read_csv('enrollments.csv')
daily_engagement = read_csv('daily_engagement.csv')
project_submissions = read_csv('project_submissions.csv')

### For each of these three tables, find the number of rows in the table and
### the number of unique students in the table. To find the number of unique
### students, you might want to create a set of the account keys in each table.

#### Clean up the data #########################
for enrollment in enrollments:
    enrollment['account_key'] = parse_int(enrollment['account_key'])
    enrollment['join_date'] = parse_date(enrollment['join_date'])
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_int(enrollment['days_to_cancel'])
    enrollment['is_udacity'] = parse_bool(enrollment['is_udacity'])
    enrollment['is_canceled'] = parse_bool(enrollment['is_canceled'])

for daily in daily_engagement:
    daily['acct'] = parse_string(daily['acct'])
    daily['account_key'] = parse_int(daily['acct'])
    del daily['acct']
    daily['utc_date'] = parse_date(daily['utc_date'])
    daily['num_courses_visited'] = parse_float(daily['num_courses_visited'])
    daily['total_minutes_visited'] = parse_float(daily['total_minutes_visited'])
    daily['lessons_completed'] = parse_float(daily['lessons_completed'])
    daily['projects_completed'] = parse_float(daily['projects_completed'])

for project in project_submissions:
    project['creation_date'] = parse_date(project['creation_date'])
    project['completion_date'] = parse_date(project['completion_date'])
    project['account_key'] = parse_int(project['account_key'])
    project['lesson_key'] = parse_int(project['lesson_key'])


#print(enrollments[0]) #Check the result
#print(daily_engagement[0]) #Check the result
#print(project_submissions[0]) #Check the result
################################################

### Function for getting the unique values
### previously, I identify the keys and change the name of the daily_engagement's key
def unique_data(datalist):
    unique = []
    for data in datalist:
        if not data['account_key'] in unique:
            unique.append(data['account_key'])
    return unique

### Function for removing the test account ######
def remove_test_account(datalist):
    unique = []
    for data in datalist:
        if not data['account_key'] in test_account:
            unique.append(data['account_key'])
    return unique

#################################################


### Obtain the test account that we must not considerate in the analisys.
test_account = set() #Use the set object because it return the data without duplicated.
for enrollment in enrollments:
    if enrollment['is_udacity']:
        test_account.add(enrollment['account_key'])

### Analisys some errors
c = 0
engagement_unique_students = unique_data(daily_engagement)
for enrollment in enrollments:
    student = enrollment['account_key']
    if student not in engagement_unique_students and (enrollment['join_date'] != enrollment['cancel_date']):
        c += 1


enrollment_num_rows = len(enrollments)
engagement_num_rows = len(daily_engagement)
submission_num_rows = len(project_submissions)
enrollment_num_unique_students = len(unique_data(enrollments))
engagement_num_unique_students = len(unique_data(daily_engagement))
submission_num_unique_students = len(unique_data(project_submissions))
non_test_account_enrollment = remove_test_account(enrollments)
non_test_account_engagement = remove_test_account(daily_engagement)
non_test_account_submission = remove_test_account(project_submissions)

#print(len(non_test_account_engagement))
#print(len(non_test_account_enrollment))
#print(len(non_test_account_submission))

paid_students = {}
enrollment_students = []
enrollment_join_date = []

for enrollment in enrollments:
    student = enrollment['account_key']
    if student in non_test_account_enrollment and (enrollment['days_to_cancel'] == None or enrollment['days_to_cancel'] > 7):
        enrollment_students.append(student)
        enrollment_join_date.append(enrollment['join_date'])

paid_students = dict(zip(enrollment_students, enrollment_join_date))


total_minutes_visited_students = {}
enrollment_students = []
total_minutes_student = []

for student in paid_students.keys():
    total_minutes = 0
    for daily in daily_engagement:
        if student == daily['account_key']:
            total_minutes += daily['total_minutes_visited']

    enrollment_students.append(student)
    total_minutes_student.append(total_minutes)

total_minutes_visited_students = dict(zip(enrollment_students, total_minutes_student))
total_minutes = total_minutes_visited_students.values()

print("Mean: {}".format(np.mean(total_minutes_student)))
