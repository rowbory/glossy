@echo off
SET glossy_ver=1.5.2
SET pt_registry_key=HKLM\Software\ScrChecks\1.0

if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
:64bit
SET pt_registry_key=HKLM\Software\Wow6432Node\ScrChecks\1.0
)


IF NOT EXIST "glossy.py" (
	@echo "Please reinstall glossy. I can't find the glossy.py file."
	PAUSE
	rem EXIT
)
for /f "tokens=2,*" %%a in ('reg query %pt_registry_key%\Program_Files_Directory_Ptw7') do SET py_exe="%%bpython24\python.exe"
IF NOT EXIST %py_exe% (
	echo I can't find the 'Paratext 7' folder
	pause
	exit
)

REM echo Checking 'My Paratext Projects' location...


FOR /F "tokens=2,*" %%a IN ('reg query %pt_registry_key%\Settings_Directory') DO @SET mpp=%%b
IF EXIST %mpp% (
	REM echo Paratext Project directory is %mpp%
)

IF NOT EXIST "%mpp%" (
	echo I can't find the 'My Paratext Projects' folder. Please report this to David Rowbory.
	pause
	exit
)

@ECHO Glossy version %glossy_ver% finding lexicons from "%mpp%" using Python engine %py_exe%
@echo ----------------------------------------

explorer display_glossies.html

IF EXIST %py_exe% (
	REM note that we needed the \ because otherwise we end with what looks to python like an escaped quote \"
	%py_exe% glossy.py "%mpp%\"
)
IF NOT ERRORLEVEL 0 (
@echo
@echo
@echo There was a problem with the glossy Python script. Please report this to David Rowbory.
PAUSE
)

IF ERRORLEVEL 0 (
@echo
@echo OK, we're finished now.
PAUSE
)

