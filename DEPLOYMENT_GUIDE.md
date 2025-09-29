# 🚀 Kolam Art System - Deployment Guide

## Overview
This guide will help you deploy your Kolam Art system with:
- **Backend**: Flask API on Render
- **Frontend**: React app on Vercel

## 📋 Prerequisites
- GitHub repository with your code
- Render account (free tier available)
- Vercel account (free tier available)
- Git installed locally

---

## 🔧 Backend Deployment (Render)

### Step 1: Prepare Backend for Render
✅ **Already Done**: The following files have been created/updated:
- `backend/Procfile` - Tells Render how to run your app
- `backend/requirements.txt` - Updated with gunicorn for production
- `backend/app.py` - Updated with production configuration

### Step 2: Deploy to Render

1. **Go to Render Dashboard**
   - Visit [render.com](https://render.com)
   - Sign up/Login with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure Service**
   ```
   Name: kolam-art-backend
   Environment: Python 3
   Region: Choose closest to your users
   Branch: main (or your default branch)
   Root Directory: backend
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
   ```

4. **Set Environment Variables**
   ```
   FLASK_ENV=production
   FRONTEND_URL=https://kolam-art-frontend.vercel.app
   PORT=5000
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Note your backend URL (e.g., `https://kolam-art-backend.onrender.com`)

---

## 🎨 Frontend Deployment (Vercel)

### Step 1: Prepare Frontend for Vercel
✅ **Already Done**: The following files have been created/updated:
- `vercel.json` - Vercel configuration
- `package.json` - Updated with vercel-build script
- `src/config/api.js` - API configuration for different environments

### Step 2: Deploy to Vercel

1. **Go to Vercel Dashboard**
   - Visit [vercel.com](https://vercel.com)
   - Sign up/Login with GitHub

2. **Import Project**
   - Click "New Project"
   - Import your GitHub repository
   - Select your repository

3. **Configure Project**
   ```
   Project Name: kolam-art-frontend
   Framework Preset: Create React App
   Root Directory: ./ (root)
   Build Command: npm run build
   Output Directory: build
   ```

4. **Set Environment Variables**
   ```
   REACT_APP_API_URL=https://kolam-art-backend.onrender.com
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment (2-5 minutes)
   - Note your frontend URL (e.g., `https://kolam-art-frontend.vercel.app`)

---

## 🔄 Update Backend CORS (After Frontend Deployment)

After getting your Vercel URL, update the backend CORS:

1. **Go to Render Dashboard**
   - Find your backend service
   - Go to "Environment" tab

2. **Update Environment Variable**
   ```
   FRONTEND_URL=https://your-actual-vercel-url.vercel.app
   ```

3. **Redeploy**
   - Click "Manual Deploy" → "Deploy latest commit"

---

## 🧪 Testing Your Deployment

### Test Backend
```bash
curl https://your-backend-url.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "modules_loaded": {...}
}
```

### Test Frontend
1. Visit your Vercel URL
2. Try uploading an image for analysis
3. Test pattern generation
4. Check if API calls work

---

## 🔧 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure `FRONTEND_URL` in backend matches your Vercel URL
   - Check that CORS origins include your domain

2. **Build Failures**
   - Check build logs in Render/Vercel dashboard
   - Ensure all dependencies are in requirements.txt/package.json

3. **API Not Responding**
   - Check Render service logs
   - Verify environment variables are set correctly

4. **Frontend Can't Connect to Backend**
   - Verify `REACT_APP_API_URL` is set correctly
   - Check network tab in browser dev tools

### Performance Optimization

1. **Render Free Tier Limitations**
   - Services sleep after 15 minutes of inactivity
   - First request after sleep takes ~30 seconds
   - Consider upgrading to paid plan for production

2. **Vercel Free Tier**
   - 100GB bandwidth per month
   - Unlimited static deployments
   - Perfect for frontend hosting

---

## 📊 Monitoring

### Render Monitoring
- Check service logs in Render dashboard
- Monitor uptime and performance
- Set up alerts for downtime

### Vercel Monitoring
- View deployment logs
- Monitor build performance
- Check analytics for usage

---

## 🔄 Continuous Deployment

Both platforms support automatic deployments:
- **Render**: Deploys on every push to main branch
- **Vercel**: Deploys on every push to any branch (with preview URLs)

### Workflow
1. Make changes locally
2. Push to GitHub
3. Render automatically deploys backend
4. Vercel automatically deploys frontend
5. Test your changes

---

## 💰 Cost Estimation

### Free Tier Limits
- **Render**: 750 hours/month (enough for small projects)
- **Vercel**: Unlimited static sites, 100GB bandwidth

### Paid Plans (if needed)
- **Render**: $7/month for always-on service
- **Vercel**: $20/month for Pro features

---

## 🎯 Next Steps

1. **Custom Domain** (Optional)
   - Add custom domain in Vercel settings
   - Update CORS in backend accordingly

2. **SSL Certificates**
   - Automatically handled by both platforms
   - HTTPS enabled by default

3. **Database** (Future)
   - Add PostgreSQL on Render if needed
   - Use environment variables for connection

4. **CDN** (Future)
   - Vercel provides global CDN automatically
   - Consider CloudFlare for additional optimization

---

## 📞 Support

If you encounter issues:
1. Check the logs in Render/Vercel dashboards
2. Review this guide for common solutions
3. Check GitHub issues for similar problems
4. Contact platform support if needed

---

**🎉 Congratulations!** Your Kolam Art system should now be live and accessible worldwide!
