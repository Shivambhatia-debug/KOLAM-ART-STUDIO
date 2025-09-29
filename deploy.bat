@echo off
REM Kolam Art System Deployment Script for Windows
REM This script helps prepare and deploy your Kolam Art system

echo 🎨 Kolam Art System Deployment Helper
echo =====================================

REM Check if git is available
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed. Please install Git first.
    pause
    exit /b 1
)

echo ✅ Git is available

REM Check if we're in a git repository
git rev-parse --git-dir >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Not in a git repository. Please initialize git first.
    echo    git init
    echo    git remote add origin https://github.com/yourusername/yourrepo.git
    pause
    exit /b 1
)

echo ✅ Git repository detected

REM Check for uncommitted changes
git diff-index --quiet HEAD --
if %errorlevel% neq 0 (
    echo ⚠️  You have uncommitted changes. Please commit them first:
    echo    git add .
    echo    git commit -m "Prepare for deployment"
    pause
    exit /b 1
)

echo ✅ No uncommitted changes

REM Check if remote origin exists
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ No remote origin found. Please add your GitHub repository:
    echo    git remote add origin https://github.com/yourusername/yourrepo.git
    pause
    exit /b 1
)

echo ✅ Remote origin configured

REM Push to GitHub
echo 📤 Pushing to GitHub...
git push origin main

if %errorlevel% equ 0 (
    echo ✅ Successfully pushed to GitHub
) else (
    echo ❌ Failed to push to GitHub
    pause
    exit /b 1
)

echo.
echo 🚀 Deployment Preparation Complete!
echo ==================================
echo.
echo Next steps:
echo 1. Go to https://render.com and deploy your backend
echo 2. Go to https://vercel.com and deploy your frontend
echo 3. Follow the detailed guide in DEPLOYMENT_GUIDE.md
echo.
echo Backend URL will be: https://kolam-art-backend.onrender.com
echo Frontend URL will be: https://kolam-art-frontend.vercel.app
echo.
echo Good luck with your deployment! 🎉
pause
