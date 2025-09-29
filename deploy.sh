#!/bin/bash

# Kolam Art System Deployment Script
# This script helps prepare and deploy your Kolam Art system

echo "🎨 Kolam Art System Deployment Helper"
echo "====================================="

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a git repository. Please initialize git first."
    exit 1
fi

echo "✅ Git repository detected"

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  You have uncommitted changes. Please commit them first:"
    echo "   git add ."
    echo "   git commit -m 'Prepare for deployment'"
    exit 1
fi

echo "✅ No uncommitted changes"

# Check if remote origin exists
if ! git remote get-url origin &> /dev/null; then
    echo "❌ No remote origin found. Please add your GitHub repository:"
    echo "   git remote add origin https://github.com/yourusername/yourrepo.git"
    exit 1
fi

echo "✅ Remote origin configured"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub"
else
    echo "❌ Failed to push to GitHub"
    exit 1
fi

echo ""
echo "🚀 Deployment Preparation Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Go to https://render.com and deploy your backend"
echo "2. Go to https://vercel.com and deploy your frontend"
echo "3. Follow the detailed guide in DEPLOYMENT_GUIDE.md"
echo ""
echo "Backend URL will be: https://kolam-art-backend.onrender.com"
echo "Frontend URL will be: https://kolam-art-frontend.vercel.app"
echo ""
echo "Good luck with your deployment! 🎉"
