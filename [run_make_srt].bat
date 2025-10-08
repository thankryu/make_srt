
@echo off
chcp 65001 > nul
echo ================================================
echo 🎬 Whisper 자막 생성 프로그램
echo ================================================
echo.

REM Python 경로 설정 (필요시 수정)
set PYTHON_PATH=python

REM Python 스크립트 경로
set SCRIPT_PATH=C:\Users\thank\Downloads\makeSrt_faster_whisper_xxl.py

REM 현재 BAT 파일이 있는 폴더를 작업 디렉토리로 전달
echo 📂 작업 폴더: %~dp0
echo 🐍 Python 스크립트: %SCRIPT_PATH%
echo.

REM Python 스크립트 실행 (현재 폴더를 인자로 전달)
REM %~dp0 끝의 백슬래시 제거
set WORK_DIR=%~dp0
if "%WORK_DIR:~-1%"=="\" set WORK_DIR=%WORK_DIR:~0,-1%
%PYTHON_PATH% "%SCRIPT_PATH%" "%WORK_DIR%"

echo.
echo ================================================
echo ✅ 작업이 완료되었습니다.
echo ================================================
pause