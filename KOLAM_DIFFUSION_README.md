# 🎨 Kolam Diffusion Generator

AI-powered Kolam image generation using Stable Diffusion + ControlNet. Upload a Kolam image and get 3 unique artistic variants.

## ✨ Features

- **AI-Powered Generation**: Uses Stable Diffusion v1.5 + ControlNet Canny
- **3 Unique Variants**: Each with different artistic styles
- **Real-time Processing**: Generate variants in 1-3 minutes
- **Download Support**: Save generated images locally
- **Responsive UI**: Clean, modern interface with TailwindCSS
- **CUDA Support**: Automatic GPU acceleration when available

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Run the setup script
python setup_kolam_diffusion.py
```

Or install manually:

```bash
# Install Python requirements
pip install -r diffusion_requirements.txt
```

### 2. Start the API Server

**Windows:**
```bash
start_kolam_diffusion.bat
```

**Linux/Mac:**
```bash
./start_kolam_diffusion.sh
```

**Manual:**
```bash
python kolam_diffusion_api.py
```

### 3. Open the Frontend

Open `kolam_diffusion_test.html` in your web browser.

## 📋 Requirements

### System Requirements
- **Python 3.8+**
- **8GB+ RAM** (16GB recommended)
- **CUDA-compatible GPU** (optional, but recommended for speed)
- **10GB+ free disk space** (for model downloads)

### Python Dependencies
- Flask 2.3.3
- PyTorch 2.0+
- Diffusers 0.21+
- Transformers 4.30+
- OpenCV 4.8+
- Pillow 10.0+

## 🔧 API Endpoints

### `POST /generate`
Generate 3 Kolam variants from uploaded image.

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
      "filename": "kolam_variant_1_abc12345_20231201_143022.png",
      "url": "/outputs/kolam_variant_1_abc12345_20231201_143022.png",
      "size": [512, 512]
    }
  ]
}
```

### `GET /health`
Check API health and model status.

### `GET /models/status`
Check if models are loaded and device info.

## 🎨 Generated Variants

1. **Traditional Style**: "Intricate symmetrical Kolam art, chalk powder style"
2. **Digital Art**: "Colorful digital Kolam design, mandala-like"
3. **Minimalist**: "Minimal geometric Kolam pattern with curves"

## 🖥️ Frontend Features

- **File Upload**: Drag & drop or click to select
- **File Validation**: Type and size checking
- **Loading States**: Progress indicators and spinners
- **Error Handling**: User-friendly error messages
- **Image Display**: High-quality preview with download buttons
- **Responsive Design**: Works on desktop and mobile

## ⚡ Performance Tips

### For GPU Users (CUDA)
- Generation time: 30-60 seconds
- Memory usage: 6-8GB VRAM
- Recommended: RTX 3060 or better

### For CPU Users
- Generation time: 3-5 minutes
- Memory usage: 8-12GB RAM
- Recommended: 16GB+ RAM

## 🔧 Troubleshooting

### Common Issues

**1. "Models not loaded" error**
```bash
# Check if models are downloading
# First run may take 10-15 minutes to download models
```

**2. CUDA out of memory**
```bash
# Reduce image size or use CPU
# Set environment variable:
export CUDA_VISIBLE_DEVICES=""
```

**3. Slow generation**
```bash
# Check if CUDA is available:
python -c "import torch; print(torch.cuda.is_available())"
```

**4. Import errors**
```bash
# Reinstall requirements:
pip install -r diffusion_requirements.txt --force-reinstall
```

### Memory Optimization

For systems with limited RAM:

1. **Use CPU only:**
```python
# In kolam_diffusion_api.py, change:
device = "cpu"  # Force CPU usage
```

2. **Reduce image size:**
```python
# The API automatically resizes images > 1024px
# Upload smaller images for faster processing
```

3. **Enable memory efficient attention:**
```python
# Already enabled in the code:
pipe.enable_attention_slicing()
```

## 📁 File Structure

```
kolam_diffusion/
├── kolam_diffusion_api.py      # Flask API server
├── KolamDiffusionGenerator.jsx # React component
├── kolam_diffusion_test.html   # Test frontend
├── diffusion_requirements.txt   # Python dependencies
├── setup_kolam_diffusion.py    # Setup script
├── start_kolam_diffusion.sh    # Linux/Mac startup
├── start_kolam_diffusion.bat   # Windows startup
├── outputs/                     # Generated images
└── README.md                   # This file
```

## 🎯 Usage Examples

### Basic Usage
1. Start the API server
2. Open `kolam_diffusion_test.html`
3. Upload a Kolam image
4. Wait for generation (1-3 minutes)
5. Download the 3 variants

### API Integration
```javascript
// Upload image via JavaScript
const formData = new FormData();
formData.append('image', file);

const response = await fetch('http://localhost:5000/generate', {
    method: 'POST',
    body: formData
});

const result = await response.json();
console.log(result.generated_images);
```

## 🔒 Security Notes

- API runs on localhost only
- No authentication required (local use)
- Generated images stored locally
- No external API calls

## 📊 Model Information

- **Base Model**: runwayml/stable-diffusion-v1-5
- **ControlNet**: lllyasviel/sd-controlnet-canny
- **Scheduler**: UniPCMultistepScheduler
- **Inference Steps**: 20
- **Guidance Scale**: 7.5
- **ControlNet Scale**: 1.0

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and research purposes. Please respect the licenses of the underlying models:

- Stable Diffusion: CreativeML Open RAIL-M
- ControlNet: Apache 2.0
- Diffusers: Apache 2.0

## 🆘 Support

If you encounter issues:

1. Check the console logs
2. Verify all dependencies are installed
3. Ensure sufficient memory/disk space
4. Try the troubleshooting section above

## 🎉 Enjoy!

Generate beautiful Kolam variants with AI! Share your creations and explore the intersection of traditional art and modern technology.












