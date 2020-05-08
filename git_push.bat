ECHO OFF
ECHO insert commit message ...
set /p var=
ECHO ON
call git add .
call git commit -m "%var%"
call git push
PAUSE

