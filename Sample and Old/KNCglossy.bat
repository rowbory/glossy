SET PATH = %PATH%;%LOCALAPPDATA%\Google\Chrome\Application\
"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" --allow-file-access-from-files "%CD%\KNCmodLexicon.xml"
IF ERRORLEVEL <> 0 THEN pause
pause
:: %LOCALAPPDATA%\Google\Chrome\Application\chrome.exe
