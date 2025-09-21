# Kolam Art Studio - Technical Implementation Details

## System Architecture

### Overall Architecture
```
┌───────────────────┐     ┌───────────────────┐     ┌───────────────────┐
│  React Frontend   │◄────►│   Flask Backend   │◄────►│  Analysis Engine  │
│                   │     │                   │     │                   │
│  - User Interface │     │  - API Endpoints  │     │  - Core Algorithms │
│  - Canvas Drawing │     │  - Data Handling  │     │  - Math Libraries  │
│  - Visualization  │     │  - Authentication │     │  - ML Models       │
└───────────────────┘     └───────────────────┘     └───────────────────┘
```

### Frontend Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     React Components                        │
├─────────────┬─────────────┬─────────────┬─────────────┬─────┘
│             │             │             │             │
▼             ▼             ▼             ▼             ▼
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  Pages  │   │   UI    │   │ Canvas  │   │  API    │   │ State   │
│         │   │Components│   │ Drawing │   │Services │   │Management│
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
```

### Backend Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                      Flask API Server                       │
├─────────────┬─────────────┬─────────────┬─────────────┬─────┘
│             │             │             │             │
▼             ▼             ▼             ▼             ▼
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│ Analysis │   │Generation│   │ Cultural │   │  Image  │   │  Error  │
│Endpoints │   │Endpoints │   │ Analysis │   │Processing│   │ Handling│
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
```

## Core Algorithms

### 1. Image Processing Pipeline

```python
def process_image(image_data):
    # Convert to numpy array
    img_array = np.array(image_data)
    
    # Grayscale conversion
    if len(img_array.shape) > 2 and img_array.shape[2] > 1:
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    else:
        gray = img_array
    
    # Noise reduction
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Adaptive thresholding
    binary = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # Perspective correction (optional)
    if perspective_correction:
        binary = correct_perspective(binary)
    
    return binary
```

### 2. Dot Detection with Hough Circle Transform

```python
def detect_dots(binary_image):
    # Apply Hough Circle Transform
    circles = cv2.HoughCircles(
        binary_image, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
        param1=50, param2=30, minRadius=1, maxRadius=20
    )
    
    dots = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            dots.append({
                'center': center,
                'radius': radius
            })
    
    return dots
```

### 3. Line Skeletonization

```python
def skeletonize_pattern(binary_image):
    # Apply skeletonization
    skeleton = skimage.morphology.skeletonize(binary_image > 0)
    
    # Convert to uint8 for OpenCV processing
    skeleton_img = np.uint8(skeleton * 255)
    
    return skeleton_img
```

### 4. Graph Construction from Skeleton

```python
def construct_graph(skeleton_img, dots):
    # Create empty graph
    G = nx.Graph()
    
    # Add dots as nodes
    for i, dot in enumerate(dots):
        G.add_node(i, pos=dot['center'], is_dot=True)
    
    # Find branch points in skeleton
    branch_points = find_branch_points(skeleton_img)
    
    # Add branch points as nodes
    for i, point in enumerate(branch_points):
        node_id = i + len(dots)
        G.add_node(node_id, pos=point, is_dot=False)
    
    # Connect nodes based on skeleton paths
    connect_nodes_by_paths(G, skeleton_img)
    
    return G
```

### 5. Symmetry Detection

```python
def detect_symmetry(points):
    # Center the points
    center = np.mean(points, axis=0)
    centered_points = points - center
    
    # Check for bilateral symmetry
    bilateral_score = check_bilateral_symmetry(centered_points)
    
    # Check for rotational symmetry
    rotational_data = check_rotational_symmetry(centered_points)
    
    # Check for radial symmetry
    radial_score = check_radial_symmetry(centered_points)
    
    # Determine primary symmetry type
    symmetry_type = determine_primary_symmetry(
        bilateral_score, rotational_data, radial_score
    )
    
    return {
        'type': symmetry_type,
        'bilateral': bilateral_score,
        'rotational': rotational_data,
        'radial': radial_score
    }
```

### 6. Fractal Analysis

```python
def calculate_fractal_dimension(binary_image):
    # Box counting method
    # Initialize variables
    scales = np.logspace(0.01, 1, num=20, base=2)
    counts = []
    
    # Count boxes at different scales
    for scale in scales:
        box_size = max(1, int(scale * min(binary_image.shape)))
        if box_size < min(binary_image.shape):
            count = count_boxes(binary_image, box_size)
            counts.append(count)
    
    # Calculate fractal dimension as slope
    coeffs = np.polyfit(np.log(scales), np.log(counts), 1)
    fractal_dimension = -coeffs[0]  # Negative because of inverse relationship
    
    return fractal_dimension
```

### 7. Eulerian Path Validation

```python
def check_eulerian_properties(graph):
    # Check if graph is connected
    if not nx.is_connected(graph):
        return {
            'is_eulerian': False,
            'is_semi_eulerian': False,
            'connected_components': nx.number_connected_components(graph),
            'euler_path_exists': False
        }
    
    # Count nodes with odd degree
    odd_degree_nodes = [node for node, degree in graph.degree() if degree % 2 == 1]
    odd_count = len(odd_degree_nodes)
    
    # Determine Eulerian properties
    is_eulerian = (odd_count == 0)  # Eulerian circuit exists
    is_semi_eulerian = (odd_count == 2)  # Eulerian path exists
    
    return {
        'is_eulerian': is_eulerian,
        'is_semi_eulerian': is_semi_eulerian,
        'odd_degree_nodes': odd_degree_nodes,
        'connected_components': 1,
        'euler_path_exists': is_eulerian or is_semi_eulerian
    }
```

### 8. Cultural Classification

```python
def classify_cultural_region(pattern_features):
    # Extract relevant features
    symmetry = pattern_features['symmetry']
    complexity = pattern_features['complexity']
    dot_pattern = pattern_features['dot_pattern']
    line_style = pattern_features['line_style']
    
    # Calculate regional scores
    scores = {
        'tamil_nadu': calculate_tamil_nadu_score(symmetry, complexity, dot_pattern, line_style),
        'karnataka': calculate_karnataka_score(symmetry, complexity, dot_pattern, line_style),
        'kerala': calculate_kerala_score(symmetry, complexity, dot_pattern, line_style),
        'andhra_pradesh': calculate_andhra_score(symmetry, complexity, dot_pattern, line_style),
        'telangana': calculate_telangana_score(symmetry, complexity, dot_pattern, line_style)
    }
    
    # Find region with highest score
    region = max(scores, key=scores.get)
    confidence = scores[region]
    
    return {
        'region': region,
        'confidence': confidence,
        'all_scores': scores
    }
```

### 9. Pattern Generation

```python
def generate_pattern(grid_size, symmetry_type, region=None, festival=None):
    # Create dot grid
    dots = create_dot_grid(grid_size)
    
    # Apply symmetry constraints
    symmetry_constraints = apply_symmetry_constraints(dots, symmetry_type)
    
    # Generate paths based on constraints
    paths = generate_paths(dots, symmetry_constraints)
    
    # Apply regional style (if specified)
    if region:
        paths = apply_regional_style(paths, region)
    
    # Apply festival theme (if specified)
    if festival:
        colors = apply_festival_theme(paths, festival)
    else:
        colors = generate_default_colors(paths)
    
    return {
        'dots': dots,
        'paths': paths,
        'colors': colors,
        'symmetry_type': symmetry_type,
        'region': region,
        'festival': festival
    }
```

## API Endpoints

### 1. `/api/analyze` - Pattern Analysis

**Request:**
```json
{
  "image": "base64_encoded_image_data",
  "type": "image_upload"
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "symmetry_type": "bilateral",
    "complexity": "medium",
    "cultural_region": "tamil_nadu",
    "confidence": 0.85,
    "dot_count": 16,
    "line_count": 24,
    "fractal_dimension": 0.6,
    "recommendations": [
      "Traditional Tamil Nadu style Kolam with bilateral symmetry",
      "Medium complexity suitable for everyday practice"
    ]
  }
}
```

### 2. `/api/advanced-analysis` - Advanced Analysis

**Request:**
```json
{
  "image": "base64_encoded_image_data",
  "mode": "deep"
}
```

**Response:**
```json
{
  "success": true,
  "advanced_analysis": {
    "image_processing": {
      "dots_detected": 16,
      "skeleton_generated": true,
      "graph_constructed": true
    },
    "geometric_properties": {
      "dot_count": 16,
      "graph_nodes": 24,
      "graph_edges": 32,
      "connected_components": 1
    },
    "eulerian_analysis": {
      "is_eulerian": true,
      "is_semi_eulerian": false,
      "euler_path_exists": true,
      "recommendations": ["Perfect! This Kolam has an Eulerian circuit"]
    },
    "symmetry_analysis": {
      "bilateral": {
        "score": 0.92,
        "type": "bilateral (vertical)",
        "details": "Vertical axis with 92.0% accuracy"
      },
      "rotational": {
        "score": 0.85,
        "type": "4-fold rotational",
        "details": "4-fold with 85.0% accuracy"
      }
    },
    "cultural_classification": {
      "region": "tamil_nadu",
      "confidence": 0.85
    },
    "quality_score": 0.88,
    "texture_features": {
      "entropy": 4.2,
      "contrast": 0.6,
      "homogeneity": 0.7
    },
    "skeleton_metrics": {
      "branch_points": 12,
      "end_points": 16,
      "avg_branch_length": 24.5
    },
    "fractal_estimate": 1.28
  }
}
```

### 3. `/api/generate-cultural` - Cultural Pattern Generation

**Request:**
```json
{
  "region": "tamil_nadu",
  "grid_size": 5,
  "use_colors": true
}
```

**Response:**
```json
{
  "success": true,
  "pattern": {
    "dots": [[50, 50], [100, 50], [150, 50], ...],
    "paths": [
      [[50, 50], [100, 50], [150, 100], ...],
      [[200, 200], [250, 250], [300, 250], ...]
    ],
    "colors": ["#DC143C", "#FF8C00", "#FFD700", ...],
    "region": "tamil_nadu",
    "cultural_info": {
      "traditional_name": "Sikku Kolam",
      "symbolism": "Represents prosperity and good fortune",
      "occasion": "Daily morning ritual"
    },
    "mathematical_properties": {
      "symmetry_type": "bilateral",
      "dot_count": 25,
      "path_count": 4
    }
  }
}
```

## Database Schema

### Pattern Template Schema
```json
{
  "id": "string",
  "name": "string",
  "type": "string",
  "region": "string",
  "complexity": "string",
  "symmetry_type": "string",
  "grid_size": [5, 5],
  "dots": [[x1, y1], [x2, y2], ...],
  "paths": [[[x1, y1], [x2, y2], ...], ...],
  "colors": ["#color1", "#color2", ...],
  "cultural_info": {
    "traditional_name": "string",
    "symbolism": "string",
    "occasion": "string"
  },
  "mathematical_properties": {
    "symmetry_type": "string",
    "fractal_dimension": 0.0,
    "euler_path": true
  }
}
```

### Analysis Result Schema
```json
{
  "id": "string",
  "timestamp": "datetime",
  "image_hash": "string",
  "analysis": {
    "symmetry_type": "string",
    "complexity": "string",
    "cultural_region": "string",
    "confidence": 0.0,
    "dot_count": 0,
    "line_count": 0,
    "fractal_dimension": 0.0
  },
  "advanced_analysis": {
    "eulerian_analysis": {
      "is_eulerian": true,
      "euler_path_exists": true
    },
    "symmetry_scores": {
      "bilateral": 0.0,
      "rotational": 0.0,
      "radial": 0.0
    }
  }
}
```

## Frontend Components

### 1. KolamStudio Component
```jsx
const KolamStudio = () => {
  const [currentTool, setCurrentTool] = useState('pen');
  const [currentColor, setCurrentColor] = useState('#DC143C');
  const [brushSize, setBrushSize] = useState(3);
  const [analysisResults, setAnalysisResults] = useState(null);
  const canvasRef = useRef(null);
  
  // Drawing functions
  const startDrawing = (e) => { /* ... */ };
  const draw = (e) => { /* ... */ };
  const stopDrawing = () => { /* ... */ };
  
  // Analysis functions
  const analyzePattern = async () => { /* ... */ };
  const performAdvancedAnalysis = async () => { /* ... */ };
  
  // Pattern generation
  const generateCulturalPattern = async () => { /* ... */ };
  const generateFestivalPattern = async () => { /* ... */ };
  
  return (
    <StudioContainer>
      <ToolPanel>
        {/* Drawing tools */}
      </ToolPanel>
      
      <Canvas
        ref={canvasRef}
        onMouseDown={startDrawing}
        onMouseMove={draw}
        onMouseUp={stopDrawing}
      />
      
      <AnalysisPanel>
        {/* Analysis results */}
      </AnalysisPanel>
    </StudioContainer>
  );
};
```

### 2. ImageUpload Component
```jsx
const ImageUpload = ({ onAnalysisComplete }) => {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResults, setAnalysisResults] = useState(null);
  
  const handleDrop = (e) => { /* ... */ };
  const handleFileSelect = (e) => { /* ... */ };
  const analyzeImage = async () => { /* ... */ };
  
  return (
    <UploadContainer>
      {!uploadedImage ? (
        <DropZone
          onDrop={handleDrop}
          onClick={() => document.getElementById('file-input').click()}
        >
          <UploadIcon />
          <UploadText>
            Drop your Kolam image here or click to browse
          </UploadText>
          <HiddenInput
            id="file-input"
            type="file"
            onChange={handleFileSelect}
          />
        </DropZone>
      ) : (
        <PreviewContainer>
          <img src={uploadedImage.url} alt="Uploaded Kolam" />
          <ActionButtons>
            <Button onClick={analyzeImage} disabled={isAnalyzing}>
              {isAnalyzing ? 'Analyzing...' : 'Analyze Pattern'}
            </Button>
          </ActionButtons>
        </PreviewContainer>
      )}
      
      {analysisResults && (
        <ResultsPanel>
          {/* Display analysis results */}
        </ResultsPanel>
      )}
    </UploadContainer>
  );
};
```

## Performance Metrics

### Analysis Performance
- **Image Processing**: ~200-500ms per image
- **Dot Detection**: ~50-150ms
- **Skeletonization**: ~100-300ms
- **Graph Construction**: ~50-150ms
- **Symmetry Analysis**: ~50-100ms
- **Cultural Classification**: ~20-50ms
- **Total Analysis Time**: ~500-1200ms

### Generation Performance
- **Grid Creation**: ~10-30ms
- **Path Generation**: ~100-300ms
- **Styling Application**: ~50-100ms
- **Total Generation Time**: ~200-500ms

### System Requirements
- **Minimum**: 2GB RAM, 1GHz CPU
- **Recommended**: 4GB RAM, 2GHz dual-core CPU
- **Storage**: ~100MB for application, ~10MB per saved pattern
- **Network**: Basic internet connection for web interface

