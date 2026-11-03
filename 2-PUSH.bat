@echo off
chcp 65001 >nul
title PUSH - Luu Lingogo len GitHub
cd /d "%~dp0"

echo ==============================================
echo   PUSH: luu app Lingogo va day len GitHub
echo ==============================================
echo.

where git >nul 2>&1
if errorlevel 1 goto :LOI_GIT

for /f "delims=" %%i in ('powershell -NoProfile -Command "Get-Date -Format 'dd/MM/yyyy HH:mm'"') do set NGAYGIO=%%i

echo [1/4] Gom cac thay doi...
git add -A
if errorlevel 1 goto :LOI

echo [2/4] Commit (%NGAYGIO%)...
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "Cap nhat Lingogo %NGAYGIO%"
    if errorlevel 1 goto :LOI
) else (
    echo      Khong co thay doi moi, bo qua commit.
)

echo [3/4] Keo ban moi tu GitHub ve truoc...
git pull --rebase
if errorlevel 1 goto :LOI_PULL

echo [4/4] Day len GitHub...
git push
if errorlevel 1 goto :LOI

echo.
echo ==============================================
echo   XONG! Da luu va day len an toan.
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

:LOI_PULL
echo.
echo ==============================================
echo   LOI khi keo ban moi ve (co the bi trung noi dung).
echo   Dang huy buoc gop de khong mat du lieu...
git rebase --abort >nul 2>&1
echo   Hay CHUP MAN HINH nay roi gui cho AI nho xu ly.
echo ==============================================
echo.
pause
exit /b 1

:LOI
echo.
echo ==============================================
echo   LOI: Co buoc bi that bai (xem dong do o tren).
echo   Hay CHUP MAN HINH nay roi gui cho AI nho xu ly.
echo ==============================================
echo.
pause
exit /b 1
