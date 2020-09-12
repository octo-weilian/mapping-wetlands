ECHO OFF
call git add .
ECHO insert commit message ...
set /p var=
call git commit -m "%var%"
call git push
PAUSE

