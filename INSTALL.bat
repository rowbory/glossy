@echo off
REM Install prerequisites
ECHO If we see lxml on the line belw then we already have LXML installed.
python3 -m pip list | findstr lxml
IF %errorlevel% == 0 (
	ECHO We are ready to go. LXML is already installed.
) ELSE (
	ECHO I have to install LXML from the internet. Just a moment...
	python3 -m pip install lxml
	IF %errorlevel% ==0 (
		ECHO I have installed LXML. Thanks for waiting. We are now ready to run glossy.
	) ELSE (
		ECHO Sorry I couldn't install lxml. Please run this install batch file again or install lxml manually.
		timeout /t -1
		EXIT
	)
)
timeout /t 5
python3 glossy9.py
timeout /t -1
