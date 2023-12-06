@echo off

set FILE_PATH=instance\db.sqlite3

if exist "%FILE_PATH%" (
    del "%FILE_PATH%"
    echo File removed successfully!
) else (
    echo File does not exist!
)
