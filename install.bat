@echo off
REM knowledge-wiki Skill Installer for Windows
REM Installs the skill to %USERPROFILE%\.hermes\skills\knowledge-management\knowledge-wiki\
REM and runs setup for path configuration.

setlocal enabledelayedexpansion

set SKILL_NAME=knowledge-wiki
set SKILL_CATEGORY=knowledge-management
set TARGET_DIR=%USERPROFILE%\.hermes\skills\%SKILL_CATEGORY%\%SKILL_NAME%
set SOURCE_DIR=%~dp0

echo ============================================================
echo   knowledge-wiki Skill Installer (Windows)
echo ============================================================
echo.

REM 1. Check for Hermes installation
echo [1/6] Checking for Hermes installation...
set HERMES_CONFIG=%USERPROFILE%\.hermes\config.yaml
if not exist "%HERMES_CONFIG%" (
    echo ❌ Hermes configuration not found at: %HERMES_CONFIG%
    echo    Please install Hermes first: https://hermes-agent.nousresearch.com
    echo.
    set /p CUSTOM_HERMES="   Hermes config path (or Enter to abort): "
    if "!CUSTOM_HERMES!"=="" (
        exit /b 1
    )
    set HERMES_CONFIG=!CUSTOM_HERMES!
    if not exist "%HERMES_CONFIG%" (
        echo    ❌ Not found: %HERMES_CONFIG%
        exit /b 1
    )
)
echo ✅ Hermes config found: %HERMES_CONFIG%

REM 2. Check Python
echo [2/6] Checking Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found in PATH. Please install Python 3.8+ and add to PATH.
    exit /b 1
)
for /f "tokens=2 delims= " %%i in ('python -c "import sys; print(sys.version_info.major, sys.version_info.minor)"') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found

REM 3. Copy skill files
echo [3/6] Installing skill to: %TARGET_DIR%
mkdir "%TARGET_DIR%" 2>nul
xcopy /E /I /Y "%SOURCE_DIR%*" "%TARGET_DIR%\" >nul
echo ✅ Skill files copied

REM 4. Install Python dependencies
echo [4/6] Installing Python dependencies...
if exist "%TARGET_DIR%\scripts\requirements.txt" (
    pip install -q -r "%TARGET_DIR%\scripts\requirements.txt" 2>nul || (
        echo ⚠️  Some optional dependencies may have failed (PDF/DOCX/XLSX conversion).
        echo    Core functionality (indexing, validation) will still work.
    )
    echo ✅ Dependencies installed
) else (
    echo ⚠️  requirements.txt not found, skipping
)

REM 5. Copy workspace template
echo [5/6] Setting up workspace...
cd /d "%TARGET_DIR%"
python scripts/setup.py --auto

REM 6. Final verification
echo [6/6] Verifying installation...
if exist "%USERPROFILE%\.config\knowledge-wiki\config.yaml" (
    echo ✅ Config created: %USERPROFILE%\.config\knowledge-wiki\config.yaml
) else (
    echo ⚠️  Config not found - run setup.py manually if needed
)

echo.
echo ============================================================
echo   ✅ Installation Complete!
echo ============================================================
echo.
echo Skill installed to: %TARGET_DIR%
echo.
echo Next steps:
echo   1. Restart Hermes or reload skills
echo   2. The skill will be available as 'knowledge-wiki'
echo   3. Config file: %USERPROFILE%\.config\knowledge-wiki\config.yaml
echo   4. Workspace created with AGENTS.md, instructions\, knowledge\, etc.
echo.
echo To verify installation:
echo   hermes skill list | findstr knowledge-wiki
echo.
pause