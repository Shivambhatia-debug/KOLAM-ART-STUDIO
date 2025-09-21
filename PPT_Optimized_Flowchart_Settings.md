# PPT-Optimized Flowchart Settings for Eraser.io

## 📏 Perfect PPT Dimensions

### **Canvas Size Settings:**
```
Width: 1920px (16:9 ratio)
Height: 1080px 
OR
Width: 1600px (4:3 ratio)  
Height: 1200px

Recommended: 1920x1080 (modern widescreen)
```

### **Export Settings:**
```
Format: PNG or SVG
Resolution: 300 DPI (high quality)
Background: White or Transparent
```

## 🔤 Text Visibility Guidelines

### **Font Sizes for PPT:**
```
Main Titles: 24-32px
Subtitle/Labels: 18-24px  
Body Text: 16-20px
Small Details: 14-16px (minimum readable)
Annotations: 12-14px
```

### **Box Dimensions:**
```
Large Containers: 400-600px width, 120-180px height
Medium Boxes: 250-350px width, 80-120px height
Small Boxes: 180-250px width, 60-80px height
```

## 🎨 PPT-Specific Eraser.io Prompt Additions

### **Add these settings to your prompt:**

```
// PPT OPTIMIZATION SETTINGS
canvas_size: 1920x1080
font_requirements: {
  title_size: "28px",
  subtitle_size: "20px", 
  body_size: "16px",
  minimum_readable: "14px"
}

box_sizing: {
  large_containers: "500x150px",
  medium_boxes: "300x100px", 
  small_boxes: "200x70px"
}

text_visibility: {
  high_contrast: true,
  dark_text_on_light_background: true,
  minimum_font_weight: "medium",
  avoid_thin_fonts: true
}

spacing_requirements: {
  minimum_gap_between_boxes: "40px",
  arrow_thickness: "3-4px",
  border_thickness: "2-3px"
}

// COLOR SCHEME FOR PPT VISIBILITY
colors: {
  primary: "#2563EB" (strong blue),
  secondary: "#7C3AED" (strong purple),
  success: "#059669" (strong green),
  warning: "#D97706" (strong orange), 
  error: "#DC2626" (strong red),
  neutral: "#374151" (dark gray for text)
}

ppt_readability: {
  avoid_light_colors: true,
  ensure_contrast_ratio: "minimum 4.5:1",
  use_bold_text: "for all labels",
  white_background_preferred: true
}
```

## 📐 Modified Technical Flowchart Prompt (PPT-Ready)

```
title: "Kolam Art Studio - Technical Architecture"
subtitle: "SIH 2025 Problem Statement 25107 Solution"

// PPT OPTIMIZATION
canvas: 1920x1080
export: "PNG, 300 DPI, white background"
font_scheme: "Bold text, high contrast, minimum 16px"
spacing: "Generous spacing for readability"

// LARGE TOP SECTION
user: 🎨 USER [
  label: "Opens Kolam Art Studio",
  size: "500x120px",
  font: "24px bold",
  color: "#2563EB",
  contrast: "high"
]

user --> frontend

// PROMINENT FRONTEND SECTION  
frontend: 🌐 REACT FRONTEND (Port 3000) [
  label: "Professional UI • Canvas Studio • Image Upload\nPattern Gallery • Export Tools",
  size: "600x140px", 
  font: "20px bold",
  color: "#3B82F6",
  background: "#EFF6FF"
]

// CLEAR ACTION BOXES (Side by side)
frontend --> upload_box [size: "280x100px", font: "18px"]
frontend --> draw_box [size: "280x100px", font: "18px"] 
frontend --> browse_box [size: "280x100px", font: "18px"]

upload_box: 📤 UPLOAD [
  label: "Image Upload\n• Drag & Drop\n• Validation",
  color: "#059669"
]

draw_box: 🎨 DRAW [
  label: "Canvas Studio\n• Real-time Tools\n• Symmetry Guides", 
  color: "#7C3AED"
]

browse_box: 📚 BROWSE [
  label: "Pattern Gallery\n• Regional Styles\n• Festival Themes",
  color: "#D97706"
]

// PROMINENT API SECTION
upload_box --> api_section
draw_box --> api_section
browse_box --> api_section

api_section: 🔗 API GATEWAY [
  label: "REST API Endpoints\nPOST /api/analyze • /api/advanced-analysis • /api/generate",
  size: "700x120px",
  font: "18px bold",
  color: "#DC2626"
]

// LARGE BACKEND SECTION
api_section --> backend

backend: 🔧 FLASK BACKEND (Port 5000) [
  label: "Python Microservices • Auto-scaling • Error Recovery",
  size: "600x120px",
  font: "20px bold", 
  color: "#7C3AED",
  background: "#F3E8FF"
]

// HIGHLIGHTED PROCESSING ENGINE
backend --> processing_engine

processing_engine: 🐍 PYTHON AI ENGINE [
  label: "OpenCV + NetworkX + Custom Algorithms\n5-Step Advanced Processing Pipeline",
  size: "700x160px",
  font: "20px bold",
  color: "#059669", 
  background: "#ECFDF5",
  border: "4px solid #059669"
]

// CLEAR PIPELINE STEPS (Horizontal flow)
processing_engine contains {
  step1: "1. IMAGE PREPROCESS" [size: "150x80px", font: "14px bold"]
  step2: "2. DOT DETECTION" [size: "150x80px", font: "14px bold"] 
  step3: "3. LINE SKELETON" [size: "150x80px", font: "14px bold"]
  step4: "4. GRAPH ANALYSIS" [size: "150x80px", font: "14px bold"]
  
  step1 --> step2 --> step3 --> step4
}

// PROMINENT RESULTS SECTION
processing_engine --> results_section

results_section: 📊 ANALYSIS RESULTS [
  label: "92% Accuracy • Cultural Classification • Mathematical Validation",
  size: "600x100px",
  font: "18px bold",
  color: "#2563EB"
]

// CLEAR OUTCOME BOXES
results_section --> success_outcome [size: "250x80px"]
results_section --> timeout_outcome [size: "250x80px"]
results_section --> error_outcome [size: "250x80px"]

success_outcome: ✅ SUCCESS [
  label: "Pattern Analysis\n& Export Options",
  color: "#059669",
  font: "16px bold"
]

timeout_outcome: ⚠️ TIMEOUT [
  label: "Fallback Analysis\n& Retry Options", 
  color: "#D97706",
  font: "16px bold"
]

error_outcome: ❌ ERROR [
  label: "Error Recovery\n& Help Guide",
  color: "#DC2626", 
  font: "16px bold"
]

// STYLING FOR PPT READABILITY
style user fill:#EFF6FF,stroke:#2563EB,stroke-width:3px,font-size:24px
style frontend fill:#EFF6FF,stroke:#3B82F6,stroke-width:3px,font-size:20px
style backend fill:#F3E8FF,stroke:#7C3AED,stroke-width:3px,font-size:20px
style processing_engine fill:#ECFDF5,stroke:#059669,stroke-width:4px,font-size:20px
style results_section fill:#FEF3C7,stroke:#D97706,stroke-width:3px,font-size:18px

// PPT ANNOTATIONS (Large, readable)
annotation performance: "⚡ 92% Accuracy, Sub-second Processing"
annotation innovation: "🚀 World's First Kolam-specific AI System"  
annotation scalability: "🌍 Enterprise-ready, Cloud-native Architecture"
```

## 🎯 PPT Presentation Tips:

### **1. Single Slide Strategy:**
- **Full-screen flowchart** (占満整个slide)
- **No additional text** on slide
- **Explain verbally** while pointing

### **2. Multi-slide Strategy:**
- **Overview slide**: Complete small flowchart
- **Detail slides**: Zoomed sections with larger text
- **Progressive disclosure**: Show one section at a time

### **3. Export Settings:**
```
Eraser.io → Export → PNG
Resolution: 300 DPI
Size: 1920x1080
Background: White
```

### **4. PowerPoint Import:**
```
Insert → Pictures → From File
Resize: Fit to slide width
Position: Center alignment
```

### **5. Presentation Tips:**
- **Use laser pointer** to highlight sections
- **Explain flow** step by step
- **Emphasize key metrics** (92% accuracy, etc.)
- **Highlight innovations** (first-of-its-kind)

यह settings के साथ आपका flowchart perfectly readable होगा PPT में! 🎯

