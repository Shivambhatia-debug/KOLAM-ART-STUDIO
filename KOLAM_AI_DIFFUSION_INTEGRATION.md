# 🎨 Kolam AI Diffusion Integration

## Overview

Successfully integrated **Stable Diffusion + ControlNet** into your existing Kolam Art production backend and React frontend. This adds AI-powered Kolam image generation capabilities to your production system.

## ✨ What's Been Added

### **Backend Integration (production_backend.py)**

1. **New Dependencies Added:**
   - `torch>=2.0.0` - PyTorch for AI models
   - `diffusers>=0.21.0` - Hugging Face diffusers library
   - `transformers>=4.30.0` - Transformers for model loading
   - `accelerate>=0.20.0` - Model acceleration
   - `opencv-python>=4.8.0` - Image preprocessing
   - `xformers>=0.0.20` - Memory efficient attention

2. **New API Endpoints:**
   - `GET /api/diffusion/health` - Check diffusion models health
   - `POST /api/diffusion/generate` - Generate 3 AI Kolam variants
   - `GET /api/diffusion/status` - Detailed models status

3. **AI Models Integrated:**
   - **Base Model**: runwayml/stable-diffusion-v1-5
   - **ControlNet**: lllyasviel/sd-controlnet-canny
   - **Scheduler**: UniPCMultistepScheduler
   - **Device**: Auto-detects CUDA/CPU

### **Frontend Integration**

1. **New React Component**: `KolamDiffusionGenerator.jsx`
   - Drag & drop file upload
   - Real-time progress indicators
   - Beautiful UI with styled-components
   - Error handling and validation

2. **New Page**: `KolamDiffusion.jsx`
   - Full-page diffusion generator
   - Integrated with existing routing

3. **Navigation Updated**: Added "AI Diffusion" link to header

## 🚀 Quick Start

### 1. Install AI Dependencies

```bash
# Run the setup script
python setup_diffusion.py
```

### 2. Start Your Production Backend

```bash
python production_backend.py
```

### 3. Start Your React Frontend

```bash
npm start
```

### 4. Access AI Diffusion

Navigate to: `http://localhost:3000/ai-diffusion`

## 🔧 API Endpoints

### `POST /api/diffusion/generate`

**Request:**
- `image`: Image file (JPG, PNG, GIF)
- Max size: 10MB

**Response:**
```json
{
  "success": true,
  "session_id": "abc12345",
  "original_image": {
    "size": [512, 512],
    "format": "PNG"
  },
  "generated_images": [
    {
      "variant": 1,
      "prompt": "Intricate symmetrical Kolam art...",
      "filename": "kolam_diffusion_1_abc12345_20231201_143022.png",
      "url": "/outputs/kolam_diffusion_1_abc12345_20231201_143022.png",
      "size": [512, 512],
      "type": "diffusion_generated"
    }
  ],
  "message": "Successfully generated 3 Kolam variants using AI diffusion",
  "generation_type": "stable_diffusion_controlnet"
}
```

### `GET /api/diffusion/health`

**Response:**
```json
{
  "diffusion_available": true,
  "models_loaded": true,
  "device": "cuda",
  "controlnet_loaded": true
}
```

### `GET /api/diffusion/status`

**Response:**
```json
{
  "diffusion_available": true,
  "models_loaded": true,
  "device": "cuda",
  "controlnet_loaded": true,
  "pipeline_loaded": true,
  "memory_efficient": true
}
```

## 🎨 Generated Variants

The AI generates 3 unique artistic variants:

1. **Traditional Style**: "Intricate symmetrical Kolam art, chalk powder style, traditional Indian design, white on dark background, detailed patterns, sacred geometry"

2. **Digital Art**: "Colorful digital Kolam design, mandala-like, vibrant colors, modern interpretation, artistic, beautiful, high quality"

3. **Minimalist**: "Minimal geometric Kolam pattern with curves, clean lines, simple design, elegant, contemporary, black and white"

## ⚡ Performance

### **With CUDA (GPU)**
- Generation time: 30-60 seconds
- Memory usage: 6-8GB VRAM
- Recommended: RTX 3060 or better

### **CPU Only**
- Generation time: 3-5 minutes
- Memory usage: 8-12GB RAM
- Recommended: 16GB+ RAM

## 🔧 Technical Details

### **Image Processing Pipeline**
1. **Upload**: User uploads Kolam image
2. **Preprocessing**: Canny edge detection for ControlNet
3. **Generation**: 3 variants with different prompts
4. **Postprocessing**: Auto-resize to 1024x1024 max
5. **Storage**: Save to `/outputs/` directory
6. **Response**: Return URLs and metadata

### **Model Configuration**
- **Inference Steps**: 20
- **Guidance Scale**: 7.5
- **ControlNet Scale**: 1.0
- **Seed**: Fixed (42) for reproducibility
- **Memory Optimization**: Attention slicing enabled

## 🛠️ Troubleshooting

### **Common Issues**

1. **"Diffusion libraries not available"**
   ```bash
   pip install torch diffusers transformers accelerate opencv-python xformers
   ```

2. **"Models not loaded"**
   - First run takes 5-10 minutes to download models
   - Check backend logs for download progress
   - Ensure sufficient disk space (10GB+)

3. **CUDA out of memory**
   - System automatically falls back to CPU
   - Reduce image size before upload
   - Close other GPU-intensive applications

4. **Slow generation**
   - Check if CUDA is available: `python -c "import torch; print(torch.cuda.is_available())"`
   - Consider upgrading GPU or adding more RAM

### **Testing Integration**

```bash
# Test the integration
python test_diffusion_integration.py
```

## 📁 File Structure

```
KOLAM ART/
├── production_backend.py              # Updated with diffusion endpoints
├── src/
│   ├── components/
│   │   └── KolamDiffusionGenerator.jsx # New AI component
│   ├── pages/
│   │   └── KolamDiffusion.jsx         # New AI page
│   └── App.js                         # Updated with new route
├── backend/
│   └── requirements.txt               # Updated with AI dependencies
├── setup_diffusion.py                 # AI setup script
├── test_diffusion_integration.py      # Integration test
└── outputs/                           # Generated images directory
```

## 🎯 Usage Examples

### **Frontend Usage**
```jsx
// Navigate to AI Diffusion page
// URL: http://localhost:3000/ai-diffusion

// Upload a Kolam image
// Wait for AI generation (1-3 minutes)
// Download the 3 variants
```

### **API Usage**
```javascript
// Upload image via JavaScript
const formData = new FormData();
formData.append('image', file);

const response = await fetch('/api/diffusion/generate', {
    method: 'POST',
    body: formData
});

const result = await response.json();
console.log(result.generated_images);
```

## 🔒 Security & Performance

- **Rate Limiting**: 5 requests per minute for diffusion endpoints
- **File Validation**: Type and size checking
- **Memory Management**: Automatic attention slicing
- **Error Handling**: Comprehensive error responses
- **Logging**: Detailed generation logs

## 🎉 Features

✅ **AI-Powered Generation** - Stable Diffusion + ControlNet  
✅ **3 Unique Variants** - Different artistic styles  
✅ **Real-time Processing** - 1-3 minutes generation  
✅ **CUDA Acceleration** - Automatic GPU detection  
✅ **Memory Efficient** - Optimized for different hardware  
✅ **Error Handling** - Graceful fallbacks  
✅ **File Management** - Automatic saving and serving  
✅ **Cross-Platform** - Works on Windows, Linux, Mac  
✅ **Production Ready** - Integrated with existing system  

## 🚀 Next Steps

1. **Start the backend**: `python production_backend.py`
2. **Start the frontend**: `npm start`
3. **Navigate to**: `http://localhost:3000/ai-diffusion`
4. **Upload a Kolam image** and generate AI variants!

## 📞 Support

If you encounter issues:
1. Check the backend logs for detailed error messages
2. Run the integration test: `python test_diffusion_integration.py`
3. Ensure all dependencies are installed: `python setup_diffusion.py`
4. Verify sufficient memory and disk space

---

**🎨 Enjoy generating beautiful AI-powered Kolam variants!**