ECHO OFF
ECHO insert commit message ...
call git status
call git add .
set /p var=
call git commit -m "%var%"
call git push
PAUSE

