# Figma Flowchart Design Guide for Kolam Art Studio

## 🎨 Figma Design Structure

### Color Palette
```
Primary Blue: #3B82F6
Secondary Purple: #8B5CF6
Success Green: #10B981
Warning Orange: #F59E0B
Error Red: #EF4444
Neutral Gray: #6B7280
Background: #F9FAFB
```

### Typography
- **Headers**: Inter Bold, 16-20px
- **Body**: Inter Regular, 12-14px
- **Labels**: Inter Medium, 10-12px

## 📐 Component Specifications

### 1. Main User Box
```
Size: 300x60px
Background: Linear gradient (#3B82F6 to #8B5CF6)
Text: "🎨 USER - Opens Kolam Art Studio"
Text Color: White
Border Radius: 12px
```

### 2. Frontend Section
```
Size: 400x80px
Background: #E0F2FE (Light Blue)
Border: 2px solid #3B82F6
Text: "🌐 REACT FRONTEND (Port 3000)"
Subtitle: "Professional Header • Canvas Studio • Image Upload"
Border Radius: 8px
```

### 3. Action Boxes (3 boxes side by side)
```
Each Box: 120x80px
Background: White
Border: 1px solid #D1D5DB
Shadow: 0 1px 3px rgba(0,0,0,0.1)

Box 1: "📤 UPLOAD IMAGE"
Box 2: "🎨 DRAW PATTERN" 
Box 3: "📚 BROWSE TEMPLATES"
```

### 4. API Request Boxes
```
Size: 200x60px each
Background: #FEF3C7 (Light Yellow)
Border: 1px solid #F59E0B

Left: "🔍 ANALYSIS REQUEST"
Right: "🎭 GENERATION REQUEST"
```

### 5. Backend Main Box
```
Size: 500x100px
Background: #F3E8FF (Light Purple)
Border: 2px solid #8B5CF6
Text: "🔧 FLASK BACKEND (Port 5000)"
Subtitle: "Request Validation • CORS • Error Handling"
```

### 6. Processing Modules (3 boxes)
```
Each: 150x80px
Background: White
Border: 1px solid #8B5CF6

Module 1: "🔬 ANALYSIS MODULE"
Module 2: "🎭 GENERATION MODULE"
Module 3: "📊 ADVANCED PROCESSING"
```

### 7. Python Engine (Large Container)
```
Size: 600x200px
Background: #ECFDF5 (Light Green)
Border: 2px solid #10B981
Title: "🐍 PYTHON ANALYSIS ENGINE"

Inside 4 process boxes (120x60px each):
1. "IMAGE PREPROCESS" (Grayscale, Blur, Threshold)
2. "DOT DETECTION" (Hough Circle)
3. "LINE SKELETONIZE" (Morpho Thinning)
4. "GRAPH ANALYSIS" (NetworkX, Eulerian)

Below 3 analysis boxes (150x60px each):
1. "SYMMETRY ANALYSIS" (Bilateral, Radial, Rotation)
2. "CULTURAL CLASSIFICATION" (Tamil Nadu, Karnataka, etc.)
3. "QUALITY SCORE" (Metrics, Fallback)
```

### 8. Response Box
```
Size: 400x60px
Background: #F0FDF4 (Light Green)
Border: 1px solid #10B981
Text: "📤 JSON RESPONSE"
Subtitle: "Analysis Results • Pattern Data • Cultural Info"
```

### 9. Frontend Rendering
```
Size: 400x60px
Background: #EFF6FF (Light Blue)
Border: 1px solid #3B82F6
Text: "🎨 FRONTEND RENDERING"
Subtitle: "State Update • Toast Messages • Results Display"
```

### 10. Result Types (3 boxes)
```
Each: 120x80px

Success (Green): 
- Background: #ECFDF5
- Border: #10B981
- "✅ SUCCESS"

Timeout (Orange):
- Background: #FFFBEB
- Border: #F59E0B
- "⚠️ TIMEOUT"

Error (Red):
- Background: #FEF2F2
- Border: #EF4444
- "❌ ERROR"
```

### 11. Final Actions (2 boxes)
```
Each: 150x60px

Export:
- Background: #F0F9FF
- Border: #3B82F6
- "📥 EXPORT"

Retry:
- Background: #F9FAFB
- Border: #6B7280
- "🔄 RETRY"
```

## 🔗 Connector Arrows

### Arrow Style
- **Stroke**: 2px
- **Color**: #6B7280
- **Style**: Solid line with arrowhead
- **Corner Radius**: 4px for bends

### Flow Direction
1. User → Frontend (straight down)
2. Frontend → 3 Actions (split into 3)
3. Actions → Requests (merge into 2)
4. Requests → Backend (merge into 1)
5. Backend → Modules (split into 3)
6. Modules → Python Engine (merge into 1)
7. Python Engine → Response (straight down)
8. Response → Frontend Rendering (straight down)
9. Frontend Rendering → Results (split into 3)
10. Results → Final Actions (merge into 2)

## 📏 Layout Grid

### Figma Frame Setup
```
Frame Size: 1200x1600px
Background: #FFFFFF
Grid: 8px baseline grid
Margins: 40px all sides
```

### Vertical Spacing
- Between major sections: 40px
- Between related elements: 20px
- Between text lines: 8px

### Horizontal Spacing
- Between side-by-side elements: 20px
- Center alignment for single elements
- Even distribution for multiple elements

## 🎯 Step-by-Step Figma Instructions

### Step 1: Setup
1. Create new Figma file
2. Add frame (1200x1600px)
3. Set background to white
4. Enable 8px grid

### Step 2: Create Components
1. Start with User box at top
2. Add Frontend section below
3. Create 3 action boxes in row
4. Add request boxes
5. Create backend section
6. Add processing modules
7. Create large Python engine container
8. Add all sub-components inside

### Step 3: Add Connectors
1. Use line tool
2. Set 2px stroke
3. Add arrowheads
4. Connect all elements following flow

### Step 4: Typography
1. Add all text elements
2. Use Inter font family
3. Apply color scheme
4. Check contrast ratios

### Step 5: Final Polish
1. Align all elements
2. Check spacing consistency
3. Add subtle shadows
4. Test readability

## 💡 Pro Tips for Figma

1. **Use Components**: Create reusable components for boxes
2. **Auto Layout**: Use for consistent spacing
3. **Constraints**: Set up responsive behavior
4. **Variants**: Create different states if needed
5. **Styles**: Save colors and text styles
6. **Export**: Export as PNG (2x) for presentations

## 🚀 Final Export Settings

### For PPT Presentation
- Format: PNG
- Scale: 2x
- Background: Transparent or White
- Size: 1200x1600px (will scale down nicely)

### For PDF Documentation
- Format: PDF
- Quality: High
- Include: All layers

यह guide follow करके आप Figma में professional flowchart बना सकते हैं!

