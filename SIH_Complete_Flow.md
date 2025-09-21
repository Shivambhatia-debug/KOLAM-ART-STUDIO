# SIH 2025 - Kolam Art Studio Complete System Flow

```
                                    ┌─────────────────────────────────────────────────────────────┐
                                    │                     🎨 USER                                 │
                                    │              Opens Kolam Art Studio                          │
                                    └─────────────────┬───────────────────────────────────────────┘
                                                      │
                                                      ▼
                                    ┌─────────────────────────────────────────────────────────────┐
                                    │              🌐 REACT FRONTEND (Port 3000)                  │
                                    │  • Professional Header • Canvas Studio • Image Upload       │
                                    │  • Pattern Gallery • Color Tools • Export Options           │
                                    └─────────────────┬───────────────────────────────────────────┘
                                                      │
                        ┌─────────────────────────────┼─────────────────────────────┐
                        ▼                             ▼                             ▼
                ┌───────────────┐           ┌───────────────┐           ┌───────────────┐
                │ 📤 UPLOAD     │           │ 🎨 DRAW       │           │ 📚 BROWSE     │
                │    IMAGE      │           │  PATTERN      │           │ TEMPLATES     │
                │               │           │               │           │               │
                │ • Drag & Drop │           │ • Canvas      │           │ • Regional    │
                │ • File Select │           │ • Tools       │           │ • Festival    │
                │ • Validation  │           │ • Symmetry    │           │ • Traditional │
                └───────┬───────┘           └───────┬───────┘           └───────┬───────┘
                        │                           │                           │
                        └─────────────────┬─────────────────┬─────────────────┘
                                          ▼                 ▼
                        ┌─────────────────────────┐ ┌─────────────────────────┐
                        │    🔍 ANALYSIS         │ │   🎭 GENERATION        │
                        │      REQUEST           │ │      REQUEST           │
                        └─────────┬───────────────┘ └─────────┬───────────────┘
                                  │                           │
                                  ▼                           ▼
                        ┌─────────────────────────┐ ┌─────────────────────────┐
                        │ POST /api/analyze       │ │ POST /api/generate-*   │
                        │ POST /api/advanced-     │ │ • Cultural patterns    │
                        │      analysis           │ │ • Festival themes      │
                        │ • mode: standard/deep   │ │ • Template-based       │
                        │ • timeout: 10s/22s      │ │ • Custom parameters    │
                        └─────────┬───────────────┘ └─────────┬───────────────┘
                                  │                           │
                                  └─────────────────┬─────────────────┘
                                                    ▼
                                    ┌─────────────────────────────────────────────────────────────┐
                                    │             🔧 FLASK BACKEND (Port 5000)                    │
                                    │   • Request Validation • CORS • Error Handling              │
                                    └─────────────────┬───────────────────────────────────────────┘
                                                      │
                        ┌─────────────────────────────┼─────────────────────────────┐
                        ▼                             ▼                             ▼
                ┌───────────────┐           ┌───────────────┐           ┌───────────────┐
                │ 🔬 ANALYSIS   │           │ 🎭 GENERATION │           │ 📊 ADVANCED   │
                │   MODULE      │           │    MODULE     │           │   PROCESSING  │
                │               │           │               │           │               │
                │ • Symmetry    │           │ • Grid Create │           │ • OpenCV      │
                │ • Complexity  │           │ • Cultural    │           │ • NetworkX    │
                │ • Cultural    │           │ • Festival    │           │ • Hough       │
                │   Region      │           │ • Colors      │           │ • Skeleton    │
                └───────┬───────┘           └───────┬───────┘           └───────┬───────┘
                        │                           │                           │
                        └─────────────────┬─────────────────┬─────────────────┘
                                          ▼                 ▼
                ┌─────────────────────────────────────────────────────────────────────┐
                │                    🐍 PYTHON ANALYSIS ENGINE                        │
                │                                                                     │
                │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
                │  │   IMAGE     │  │    DOT      │  │    LINE     │  │   GRAPH     │ │
                │  │ PREPROCESS  │─▶│ DETECTION   │─▶│SKELETONIZE  │─▶│  ANALYSIS   │ │
                │  │             │  │             │  │             │  │             │ │
                │  │ • Grayscale │  │ • Hough     │  │ • Morpho    │  │ • NetworkX  │ │
                │  │ • Blur      │  │   Circle    │  │   Thinning  │  │ • Eulerian  │ │
                │  │ • Threshold │  │ • Validate  │  │ • Edge      │  │   Path      │ │
                │  │ • Resize    │  │   Circles   │  │   Extract   │  │ • Validate  │ │
                │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │
                │                                    │                                │
                │  ┌─────────────┐  ┌─────────────┐  ▼              ┌─────────────┐  │
                │  │  SYMMETRY   │  │  CULTURAL   │                 │  QUALITY    │  │
                │  │  ANALYSIS   │  │CLASSIFICA  │                 │   SCORE     │  │
                │  │             │  │    TION     │                 │             │  │
                │  │ • Bilateral │  │ • Tamil Nadu│                 │ • Metrics   │  │
                │  │ • Radial    │  │ • Karnataka │                 │ • Fallback  │  │
                │  │ • Rotation  │  │ • Kerala    │                 │ • Timeout   │  │
                │  │ • Scores    │  │ • Andhra    │                 │   Handling  │  │
                │  └─────────────┘  └─────────────┘                 └─────────────┘  │
                └─────────────────────────────────┬───────────────────────────────────┘
                                                  ▼
                                    ┌─────────────────────────────────────────────────────────────┐
                                    │                   📤 JSON RESPONSE                          │
                                    │  • Analysis Results • Pattern Data • Cultural Info          │
                                    │  • Processing Steps • Error Messages • Success Status       │
                                    └─────────────────┬───────────────────────────────────────────┘
                                                      │
                                                      ▼
                                    ┌─────────────────────────────────────────────────────────────┐
                                    │              🎨 FRONTEND RENDERING                          │
                                    │  • State Update • Toast Messages • Results Display          │
                                    │  • Canvas Drawing • Pattern Visualization • Export          │
                                    └─────────────────┬───────────────────────────────────────────┘
                                                      │
                        ┌─────────────────────────────┼─────────────────────────────┐
                        ▼                             ▼                             ▼
                ┌───────────────┐           ┌───────────────┐           ┌───────────────┐
                │ ✅ SUCCESS    │           │ ⚠️ TIMEOUT    │           │ ❌ ERROR      │
                │               │           │               │           │               │
                │ • Show        │           │ • Show retry  │           │ • Show error  │
                │   Results     │           │   suggestion  │           │   message     │
                │ • Display     │           │ • Fallback    │           │ • Fallback    │
                │   Cultural    │           │   analysis    │           │   options     │
                │   Info        │           │ • User guide  │           │ • Help tips   │
                └───────┬───────┘           └───────┬───────┘           └───────┬───────┘
                        │                           │                           │
                        └─────────────────┬─────────────────┬─────────────────┘
                                          ▼                 ▼
                                ┌─────────────────┐ ┌─────────────────┐
                                │  📥 EXPORT      │ │  🔄 RETRY       │
                                │                 │ │                 │
                                │ • PNG Image     │ │ • New Analysis  │
                                │ • SVG Vector    │ │ • Different     │
                                │ • JSON Data     │ │   Parameters    │
                                │ • Cultural      │ │ • Help Guide    │
                                │   Metadata      │ │                 │
                                └─────────────────┘ └─────────────────┘
```

## Key Features Shown:

1. **Complete User Journey** - Upload → Analysis → Results → Export
2. **Frontend-Backend Communication** - API calls और responses
3. **Advanced Processing Pipeline** - OpenCV → NetworkX → Analysis
4. **Error Handling** - Timeout, fallback, retry mechanisms
5. **Cultural Integration** - Regional classification और festival themes
6. **Export Options** - Multiple formats और metadata

यह single comprehensive flowchart है जो पूरे system को एक diagram में दिखाता है!

