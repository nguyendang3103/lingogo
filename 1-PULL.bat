@echo off
chcp 65001 >nul
title PULL - Lay ban moi nhat tu GitHub
cd /d "%~dp0"

echo ==============================================
echo   PULL: lay ban moi nhat tu GitHub ve
echo ==============================================
echo.

where git >nul 2>&1
if errorlevel 1 goto :LOI_GIT

echo Dang keo ban moi...
git pull --rebase --autostash
if errorlevel 1 goto :LOI

echo.
echo ==============================================
echo   XONG! Da co ban moi nhat.
echo ==============================================
echo.
pause
exit /b 0

:LOI_GIT
echo.
echo ==============================================
echo   LOI: May chua cai Git hoac chua tim thay Git.
echo   Hay CHUP MAN HINH nay roi gui cho AI nho xu ly.
echo ==============================================
echo.
pause
exit /b 1

:LOI
echo.
echo ==============================================
echo   LOI: Khong keo duoc ban moi (xem dong do o tren).
echo   Hay CHUP MAN HINH nay roi gui cho AI nho xu ly.
echo ==============================================
echo.
pause
exit /b 1
