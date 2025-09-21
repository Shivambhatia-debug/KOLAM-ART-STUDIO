# FigJam AI Prompt for Kolam Art Studio Flowchart

## 🎯 Complete Prompt (Copy-Paste Ready)

```
Create a comprehensive system architecture flowchart for "Kolam Art Studio" - a web application for analyzing traditional Indian Kolam patterns. Structure the flow vertically from top to bottom with these exact components:

**TOP LEVEL:**
- User box: "🎨 USER - Opens Kolam Art Studio"

**FRONTEND LAYER:**
- Large box: "🌐 REACT FRONTEND (Port 3000)" with subtitle "Professional Header • Canvas Studio • Image Upload • Pattern Gallery • Color Tools • Export Options"

**USER ACTIONS (3 boxes side by side):**
- Left: "📤 UPLOAD IMAGE" (Drag & Drop, File Select, Validation)
- Center: "🎨 DRAW PATTERN" (Canvas, Tools, Symmetry)
- Right: "📚 BROWSE TEMPLATES" (Regional, Festival, Traditional)

**REQUEST TYPES (2 boxes):**
- Left: "🔍 ANALYSIS REQUEST"
- Right: "🎭 GENERATION REQUEST"

**API ENDPOINTS (2 boxes):**
- Left: "POST /api/analyze, POST /api/advanced-analysis" with details "mode: standard/deep, timeout: 10s/22s"
- Right: "POST /api/generate-*" with details "Cultural patterns, Festival themes, Template-based, Custom parameters"

**BACKEND LAYER:**
- Large box: "🔧 FLASK BACKEND (Port 5000)" with subtitle "Request Validation • CORS • Error Handling"

**BACKEND MODULES (3 boxes):**
- Left: "🔬 ANALYSIS MODULE" (Symmetry, Complexity, Cultural Region)
- Center: "🎭 GENERATION MODULE" (Grid Create, Cultural, Festival, Colors)
- Right: "📊 ADVANCED PROCESSING" (OpenCV, NetworkX, Hough, Skeleton)

**PYTHON ENGINE (Large container with internal pipeline):**
- Main container: "🐍 PYTHON ANALYSIS ENGINE"
- Internal flow (4 connected boxes): "IMAGE PREPROCESS" → "DOT DETECTION" → "LINE SKELETONIZE" → "GRAPH ANALYSIS"
- Below main flow (3 boxes): "SYMMETRY ANALYSIS", "CULTURAL CLASSIFICATION", "QUALITY SCORE"
- Include technical details for each step

**RESPONSE LAYER:**
- Box: "📤 JSON RESPONSE" with subtitle "Analysis Results • Pattern Data • Cultural Info • Processing Steps • Error Messages • Success Status"

**FRONTEND RENDERING:**
- Box: "🎨 FRONTEND RENDERING" with subtitle "State Update • Toast Messages • Results Display • Canvas Drawing • Pattern Visualization • Export"

**RESULT TYPES (3 boxes):**
- Left: "✅ SUCCESS" (Show Results, Display Cultural Info)
- Center: "⚠️ TIMEOUT" (Show retry suggestion, Fallback analysis, User guide)
- Right: "❌ ERROR" (Show error message, Fallback options, Help tips)

**FINAL ACTIONS (2 boxes):**
- Left: "📥 EXPORT" (PNG Image, SVG Vector, JSON Data, Cultural Metadata)
- Right: "🔄 RETRY" (New Analysis, Different Parameters, Help Guide)

**DESIGN REQUIREMENTS:**
- Use professional blue/purple gradient color scheme
- Add clear directional arrows showing data flow
- Group related components with subtle backgrounds
- Include emojis as shown for visual appeal
- Make boxes properly sized and well-spaced
- Add technical details in smaller text under main labels
- Show branching and merging of data flows clearly
- Use consistent styling throughout

**CONNECTIONS:**
- User flows down to Frontend
- Frontend splits into 3 user actions
- Actions merge into 2 request types
- Requests flow to respective API endpoints
- APIs merge into Backend
- Backend splits into 3 modules
- Modules merge into Python Engine
- Engine processes through internal pipeline
- Results flow through Response → Frontend Rendering
- Rendering splits into 3 result types
- Results merge into 2 final actions

Create this as a clear, professional flowchart suitable for a technical presentation.
```

## 🎨 Alternative Shorter Prompt (If Above is Too Long)

```
Design a system flowchart for "Kolam Art Studio" web app showing:

FLOW: User → React Frontend (3000) → Upload/Draw/Browse → Analysis/Generation APIs → Flask Backend (5000) → Python Engine (OpenCV+NetworkX pipeline) → JSON Response → Frontend Rendering → Success/Timeout/Error → Export/Retry

TECHNICAL DETAILS:
- Frontend: React with canvas, image upload, pattern gallery
- Backend: Flask with /api/analyze, /api/advanced-analysis, /api/generate endpoints
- Engine: Image preprocessing → Dot detection → Line skeletonization → Graph analysis → Symmetry/Cultural classification
- Results: Success (show results), Timeout (retry), Error (fallback)

STYLE: Professional blue/purple colors, clear arrows, grouped components, emojis for sections, vertical top-to-bottom flow.
```

## 💡 Usage Tips:

1. **Copy करें** पहला complete prompt
2. **FigJam में paste** करें AI feature में
3. **अगर result अच्छा नहीं** तो second shorter prompt try करें
4. **Manual refinement** करें specific details के लिए
5. **Colors और spacing** adjust करें

यह prompt आपके exact flowchart को recreate करेगा! 🚀

