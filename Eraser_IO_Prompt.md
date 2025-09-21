# Eraser.io Prompts for Kolam Art Studio Flowchart

## 🎯 Eraser.io Complete Prompt (Recommended)

```
Create a system architecture diagram for "Kolam Art Studio" - a web application for analyzing traditional Indian Kolam patterns using the following specifications:

// User Layer
User [icon: user, color: blue] --> Frontend

// Frontend Layer  
Frontend [
  label: "React Frontend\n(Port 3000)",
  technology: "React.js",
  features: [
    "Professional Header",
    "Canvas Studio", 
    "Image Upload",
    "Pattern Gallery",
    "Export Options"
  ],
  color: lightblue
]

// User Actions
Frontend --> UploadImage [label: "📤 Upload Image\n• Drag & Drop\n• File Select\n• Validation"]
Frontend --> DrawPattern [label: "🎨 Draw Pattern\n• Canvas Tools\n• Symmetry Guides"]  
Frontend --> BrowseTemplates [label: "📚 Browse Templates\n• Regional Patterns\n• Festival Themes"]

// Request Processing
UploadImage --> AnalysisRequest [label: "🔍 Analysis Request"]
DrawPattern --> AnalysisRequest
UploadImage --> GenerationRequest [label: "🎭 Generation Request"] 
BrowseTemplates --> GenerationRequest

// API Endpoints
AnalysisRequest --> AnalyzeAPI [
  label: "POST /api/analyze\nPOST /api/advanced-analysis",
  details: "mode: standard/deep\ntimeout: 10s/22s",
  color: orange
]

GenerationRequest --> GenerateAPI [
  label: "POST /api/generate-*",
  details: "• Cultural patterns\n• Festival themes\n• Template-based",
  color: orange
]

// Backend Layer
AnalyzeAPI --> Backend
GenerateAPI --> Backend

Backend [
  label: "Flask Backend\n(Port 5000)",
  technology: "Python Flask",
  features: [
    "Request Validation",
    "CORS Handling", 
    "Error Management"
  ],
  color: purple
]

// Backend Modules
Backend --> AnalysisModule [
  label: "🔬 Analysis Module",
  features: ["Symmetry", "Complexity", "Cultural Region"]
]

Backend --> GenerationModule [
  label: "🎭 Generation Module", 
  features: ["Grid Creation", "Cultural Styling", "Color Schemes"]
]

Backend --> AdvancedProcessing [
  label: "📊 Advanced Processing",
  technologies: ["OpenCV", "NetworkX", "Hough Transform"]
]

// Python Analysis Engine
AnalysisModule --> PythonEngine
GenerationModule --> PythonEngine  
AdvancedProcessing --> PythonEngine

PythonEngine [
  label: "🐍 Python Analysis Engine",
  color: green,
  pipeline: [
    "Image Preprocessing → Dot Detection → Line Skeletonization → Graph Analysis",
    "Symmetry Analysis + Cultural Classification + Quality Scoring"
  ]
]

// Processing Steps (Internal Pipeline)
PythonEngine contains {
  ImagePreprocess [label: "Image Preprocess\n• Grayscale\n• Blur\n• Threshold"]
  DotDetection [label: "Dot Detection\n• Hough Circles\n• Validation"]  
  LineSkeletonize [label: "Line Skeletonize\n• Morphological\n• Edge Extract"]
  GraphAnalysis [label: "Graph Analysis\n• NetworkX\n• Eulerian Path"]
  
  ImagePreprocess --> DotDetection --> LineSkeletonize --> GraphAnalysis
  
  SymmetryAnalysis [label: "Symmetry Analysis\n• Bilateral\n• Radial\n• Rotational"]
  CulturalClassification [label: "Cultural Classification\n• Tamil Nadu\n• Karnataka\n• Kerala\n• Andhra Pradesh"]
  QualityScore [label: "Quality Score\n• Metrics\n• Fallback\n• Timeout Handling"]
}

// Response Flow
PythonEngine --> JSONResponse [
  label: "📤 JSON Response",
  content: [
    "Analysis Results",
    "Pattern Data", 
    "Cultural Info",
    "Processing Steps",
    "Status Messages"
  ],
  color: lightgreen
]

// Frontend Rendering
JSONResponse --> FrontendRender [
  label: "🎨 Frontend Rendering",
  features: [
    "State Updates",
    "Toast Messages", 
    "Results Display",
    "Canvas Drawing",
    "Visualization"
  ]
]

// Result Types
FrontendRender --> Success [
  label: "✅ Success",
  actions: ["Show Results", "Display Cultural Info"],
  color: green
]

FrontendRender --> Timeout [
  label: "⚠️ Timeout", 
  actions: ["Retry Suggestion", "Fallback Analysis"],
  color: yellow
]

FrontendRender --> Error [
  label: "❌ Error",
  actions: ["Error Message", "Help Tips"],
  color: red
]

// Final Actions
Success --> Export [label: "📥 Export\n• PNG\n• SVG\n• JSON\n• Metadata"]
Timeout --> Retry [label: "🔄 Retry\n• New Analysis\n• Different Params"]
Error --> Retry

// Styling
style User fill:#e1f5fe
style Frontend fill:#bbdefb  
style Backend fill:#d1c4e9
style PythonEngine fill:#c8e6c9
style JSONResponse fill:#dcedc8
```

## 🔧 Eraser.io Simplified Prompt (If Above Doesn't Work)

```
diagram: kolam-art-studio

// Main Flow
user: User
frontend: React Frontend (Port 3000)
backend: Flask Backend (Port 5000) 
engine: Python Analysis Engine

user -> frontend
frontend -> backend: API Requests
backend -> engine: Processing
engine -> backend: Results
backend -> frontend: JSON Response

// Frontend Actions
upload: Upload Image
draw: Draw Pattern  
browse: Browse Templates

frontend -> upload
frontend -> draw
frontend -> browse

// API Endpoints
analyze: /api/analyze
advanced: /api/advanced-analysis
generate: /api/generate

upload -> analyze
draw -> analyze
browse -> generate

analyze -> backend
advanced -> backend
generate -> backend

// Backend Processing
analysis: Analysis Module
generation: Generation Module
processing: Advanced Processing

backend -> analysis
backend -> generation  
backend -> processing

analysis -> engine
generation -> engine
processing -> engine

// Python Pipeline
preprocess: Image Preprocessing
detection: Dot Detection (Hough)
skeleton: Line Skeletonization  
graph: Graph Analysis (NetworkX)
symmetry: Symmetry Analysis
cultural: Cultural Classification

engine -> preprocess
preprocess -> detection
detection -> skeleton
skeleton -> graph
graph -> symmetry
graph -> cultural

// Results
success: Success Results
timeout: Timeout Handling
error: Error Handling
export: Export Options
retry: Retry Options

backend -> success
backend -> timeout
backend -> error

success -> export
timeout -> retry
error -> retry

// Styling
user [color: blue]
frontend [color: lightblue] 
backend [color: purple]
engine [color: green]
success [color: green]
timeout [color: orange]
error [color: red]
```

## 📋 Eraser.io Usage Instructions:

### Step 1: Access Eraser.io
1. Go to **eraser.io**
2. **Sign up** या login करें
3. **"New Diagram"** click करें

### Step 2: Choose Template
1. **"Architecture Diagram"** select करें
2. या **"Blank Canvas"** से start करें

### Step 3: Input Prompt
1. **AI Assistant** या **Text mode** open करें
2. **Paste** complete prompt
3. **Generate** click करें

### Step 4: Refine
1. **Auto-generated** diagram review करें
2. **Manual adjustments** करें
3. **Colors और layout** customize करें
4. **Export** PNG/SVG for presentation

## 💡 Pro Tips for Eraser.io:

### 1. **Use Simplified Syntax**
- Eraser.io prefers **simple node -> node** connections
- **Avoid complex nested structures** in first attempt

### 2. **Incremental Building**
- Start with **basic flow** (simplified prompt)
- **Add details** step by step
- **Test each section** before adding more

### 3. **Alternative Approach**
```
// Start Simple
User -> Frontend -> Backend -> Engine -> Results

// Then Add Details
Frontend contains [Upload, Draw, Browse]
Backend contains [Analysis, Generation, Processing]
Engine contains [Preprocess, Detect, Analyze]
```

### 4. **Export Options**
- **PNG**: For presentations
- **SVG**: For scalable graphics
- **Link sharing**: For collaboration

यह Eraser.io में आपका exact flowchart बना देगा! 🚀

