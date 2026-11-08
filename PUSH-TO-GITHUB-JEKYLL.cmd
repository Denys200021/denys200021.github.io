@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

set "DEFAULT_REPO_URL=https://github.com/Legioniz/Legioniz.github.io.git"
set "REMOTE_NAME=portfolio-live"
set "REPO_URL=%DEFAULT_REPO_URL%"
set "REPO_INPUT="

echo.
echo  LEGIONIZ PORTFOLIO - GITHUB PAGES JEKYLL PUSH
echo  =============================================
echo.
echo This script pushes the CURRENT FOLDER to GitHub.
echo Destination: %DEFAULT_REPO_URL%
echo.

where git >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Git for Windows was not found.
  echo Install Git from https://git-scm.com/download/win, then run this script again.
  goto :failed
)

echo [CHECK] Verifying the Jekyll Pages deployment files...
if not exist "index.html" (
  echo [ERROR] index.html is missing. Extract the complete portfolio ZIP first.
  goto :failed
)
if not exist "package.json" (
  echo [ERROR] package.json is missing. Run this script from the portfolio root folder.
  goto :failed
)
if not exist ".github\workflows\deploy.yml" (
  echo [ERROR] .github\workflows\deploy.yml is missing.
  goto :failed
)
if not exist ".github\jekyll\_config.yml" (
  echo [ERROR] .github\jekyll\_config.yml is missing.
  goto :failed
)
if not exist "public\King-Art-Pacumberto-CV.pdf" (
  echo [ERROR] Public CV PDF is missing from public\.
  goto :failed
)
if not exist "public\King-Art-Pacumberto-Resume.pdf" (
  echo [ERROR] Original Resume PDF is missing from public\.
  goto :failed
)

echo [OK] Portfolio root and GitHub Pages Jekyll workflow found.
echo.

set /p "REPO_INPUT=Repository URL (press ENTER to use the default): "
if not "%REPO_INPUT%"=="" set "REPO_URL=%REPO_INPUT%"
if /I not "%REPO_URL:~-4%"==".git" (
  echo [ERROR] Use the HTTPS Git URL ending in .git.
  goto :failed
)

echo.
echo [TARGET] %REPO_URL%
echo [INFO] Remote name: %REMOTE_NAME%
echo.

if not exist ".git" (
  echo [INIT] Initializing Git in this folder...
  git init
  if errorlevel 1 goto :gitfailed
)

rem Keep a dedicated remote so an existing origin is never overwritten.
git remote get-url %REMOTE_NAME% >nul 2>nul
if errorlevel 1 (
  echo [REMOTE] Adding %REMOTE_NAME%...
  git remote add %REMOTE_NAME% "%REPO_URL%"
  if errorlevel 1 goto :gitfailed
) else (
  for /f "delims=" %%U in ('git remote get-url %REMOTE_NAME%') do set "CURRENT_REMOTE=%%U"
  if /I not "!CURRENT_REMOTE!"=="%REPO_URL%" (
    echo [ERROR] The existing %REMOTE_NAME% remote points somewhere else:
    echo         !CURRENT_REMOTE!
    echo To avoid redirecting or overwriting another project, this script stopped.
    echo Update that remote manually only after confirming the repository.
    goto :failed
  )
)

rem Do not allow common local environment files to be accidentally committed.
set "TRACKED_ENV="
for %%F in (.env .env.local .env.development .env.production .env.staging) do (
  git ls-files --error-unmatch "%%F" >nul 2>nul && set "TRACKED_ENV=1"
)
if defined TRACKED_ENV (
  echo [ERROR] A local environment file is already tracked by Git.
  echo         Remove it from tracking before pushing. Never publish secrets.
  goto :failed
)

rem The original resume PDF may contain a personal phone number.
echo [PRIVACY] The Full Portfolio includes the original Resume PDF.
echo           It may contain your phone number and will be publicly downloadable.
choice /c YN /n /m "Have you reviewed this and want to continue? [Y/N] "
if errorlevel 2 goto cancelled

rem Configure identity locally only when Git has no existing identity.
for /f "delims=" %%N in ('git config user.name 2^>nul') do set "GIT_USER_NAME=%%N"
for /f "delims=" %%E in ('git config user.email 2^>nul') do set "GIT_USER_EMAIL=%%E"
if not defined GIT_USER_NAME (
  set /p "GIT_USER_NAME=Enter the name to show on your Git commits: "
  if not defined GIT_USER_NAME goto :identityfailed
  git config user.name "!GIT_USER_NAME!"
  if errorlevel 1 goto :gitfailed
)
if not defined GIT_USER_EMAIL (
  set /p "GIT_USER_EMAIL=Enter the email to show on your Git commits: "
  if not defined GIT_USER_EMAIL goto :identityfailed
  git config user.email "!GIT_USER_EMAIL!"
  if errorlevel 1 goto :gitfailed
)

echo.
echo [BRANCH] Setting the deployment branch to main...
git branch -M main
if errorlevel 1 goto :gitfailed

echo [STAGE] Adding portfolio files (items in .gitignore remain excluded)...
git add -A
if errorlevel 1 goto :gitfailed

git diff --cached --check
if errorlevel 1 (
  echo [ERROR] Git found whitespace errors in the staged changes. Fix them before pushing.
  goto :failed
)

git diff --cached --quiet
if errorlevel 1 (
  echo [COMMIT] Creating the deployment commit...
  git commit -m "Deploy portfolio with GitHub Pages Jekyll"
  if errorlevel 1 goto :gitfailed
) else (
  echo [INFO] No new staged changes; keeping the existing commit.
)

git rev-parse --verify HEAD >nul 2>nul
if errorlevel 1 (
  echo [ERROR] No local commit exists. Nothing can be pushed.
  goto :failed
)

echo.
echo [PUSH] Pushing main to GitHub...
echo [SAFEGUARD] No force-push will be used. Existing remote history will not be overwritten.
git push -u %REMOTE_NAME% main
if errorlevel 1 (
  echo.
  echo [PUSH BLOCKED] GitHub rejected the push or authentication failed.
  echo If the repository was created with a README or license, it may already have history.
  echo Do NOT force-push. Reconcile the remote history first, or create an empty repository.
  goto :failed
)

echo.
echo [SUCCESS] Portfolio source pushed to GitHub.
echo.
echo NEXT: Open https://github.com/Legioniz/Legioniz.github.io/actions
echo Wait for the Jekyll Pages workflow to finish successfully.
echo In repository Settings ^> Pages, set Source to GitHub Actions.
echo.
echo Expected public URLs after successful deployment:
echo   https://legioniz.github.io/
echo   https://legioniz.github.io/?view=recruiter
echo.
pause
exit /b 0

:cancelled
echo.
echo [CANCELLED] No files were pushed. Review the privacy warning before retrying.
pause
exit /b 1

:identityfailed
echo [ERROR] Git commit name and email are required.
goto :failed

:gitfailed
echo.
echo [ERROR] A Git command failed. Read the message above and resolve it before retrying.
goto :failed

:failed
echo.
echo No force-push was performed. Your existing remote history was not overwritten.
pause
exit /b 1
