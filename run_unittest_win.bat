@echo off
set CURRENT_DIR=%cd%

set PYTHONPATH=%CURRENT_DIR%\src;%CURRENT_DIR%\src\ssd;%CURRENT_DIR%\tests;%PYTHONPATH%

echo %PYTHONPATH%

rem run pytest
pytest
