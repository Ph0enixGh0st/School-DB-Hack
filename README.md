# School DB Hack
The script allows to change marks, сhastisements, and commendations in the school database.

## How to install
Download and unpack ZIP file from GIT Hub repository: https://github.com/Ph0enixGh0st/School-DB-Hack.git

# Prerequisites
Python3 should be already installed and you should have access to school database in place.
The scripts.py file should be copied into the same folder with 'manage.py'.

## How to run
```bash
python scripts.py -n "{Schoolkid full name in Russian}" -s "{Subject name in Russian}"
```
Only one name and one subject at a time.
All words in Full Name and Subject are to be capitalized.

## def fix_marks(child)
The function takes schoolkid's name as an argument and turns all grades lower than '4' (i.e. 2 and 3) into '5' for this student.

## def remove_chastisements(child):
The function takes schoolkid's name as an argument and deletes all chastisements from the database.

## def create_commendation(child, subject):
The function takes schoolkid's name and subject to create appraisal for the subject's last lesson taken by the student.

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
