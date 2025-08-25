@echo off
setlocal

REM ===== CONFIG =====
set "REPO_URL=https://github.com/Prasad9246-dev/PlayWright_POC.git"
set "BRANCH=Arun_Development"
set "TEST_FILE=tests\test_TEST-001.py"
set "REPO_DIR=%~1"
if "%REPO_DIR%"=="" set "REPO_DIR=%USERPROFILE%\PlayWright_POC"
REM ==================

echo Repo:   %REPO_URL%
echo Branch: %BRANCH%
echo Dir:    %REPO_DIR%
echo Test:   %TEST_FILE%
echo.

REM Ensure Git is available
where git >nul 2>&1 || (echo [ERROR] Git not found. Install: https://git-scm.com/download/win & pause & exit /b 1)

REM Clone or update branch
if not exist "%REPO_DIR%" (
  echo Cloning %BRANCH%...
  git clone --branch %BRANCH% --single-branch "%REPO_URL%" "%REPO_DIR%" || (pause & exit /b 1)
) else (
  echo Updating %BRANCH%...
  pushd "%REPO_DIR%"
  git remote set-url origin "%REPO_URL%" >nul 2>&1
  git fetch origin %BRANCH%
  git checkout %BRANCH% || (popd & pause & exit /b 1)
  git reset --hard origin/%BRANCH%
  popd
)

pushd "%REPO_DIR%"

REM Pick Python launcher already on the machine (no venv)
set "PYEXE="
where py >nul 2>&1 && set "PYEXE=py -3"
if "%PYEXE%"=="" ( where python >nul 2>&1 && set "PYEXE=python" )
if "%PYEXE%"=="" ( echo [ERROR] Python not found on PATH. & pause & exit /b 1 )

echo.
echo ===== Running ONLY %TEST_FILE% (live output; no log file) =====
echo Command: %PYEXE% -m pytest -s "%TEST_FILE%" -v
echo.
%PYEXE% -m pytest -s "%TEST_FILE%" -v

echo.
echo (Window will stay open for analysis.)
pause

popd
endlocal
