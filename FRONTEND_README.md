# Kolam Art Studio - React Frontend

A modern, interactive React frontend for the Kolam Design Analysis system addressing AICTE Problem Statement 25107.

## 🎨 Features

### Interactive Design Studio
- **Canvas Drawing**: HTML5 Canvas-based drawing tools
- **Symmetry Tools**: Real-time symmetry guides and helpers
- **Pattern Templates**: Pre-built traditional Kolam patterns
- **Color Picker**: Advanced color selection with react-color
- **Export Options**: Download patterns as PNG/JSON

### Pattern Gallery
- **Regional Patterns**: Traditional designs from different Indian states
- **Cultural Information**: Detailed cultural significance for each pattern
- **Search & Filter**: Find patterns by type, region, or complexity
- **Pattern Preview**: Visual previews with metadata

### Mathematical Analysis
- **Symmetry Detection**: Automatic detection of radial, bilateral, and rotational symmetry
- **Fractal Analysis**: Calculation of fractal dimensions and self-similarity
- **Complexity Metrics**: Pattern complexity assessment
- **Cultural Classification**: Regional pattern recognition

### Educational Content
- **Design Principles**: Learn about mathematical foundations
- **Cultural Significance**: Understand regional variations
- **Interactive Learning**: Hands-on pattern creation and analysis

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ 
- npm or yarn
- Python 3.8+ (for backend)

### Installation

1. **Install Frontend Dependencies**
```bash
npm install
```

2. **Start Development Server**
```bash
npm start
```

3. **Start Backend API** (in separate terminal)
```bash
cd backend
pip install -r requirements.txt
python app.py
```

4. **Open Browser**
Navigate to `http://localhost:3000`

## 📁 Project Structure

```
src/
├── components/
│   └── Header.js              # Navigation header
├── pages/
│   ├── Home.js               # Landing page
│   ├── KolamStudio.js        # Interactive drawing studio
│   ├── PatternGallery.js     # Pattern gallery and templates
│   ├── Analysis.js           # Mathematical analysis results
│   └── About.js              # About page and project info
├── App.js                    # Main app component
└── index.js                  # React entry point
```

## 🛠️ Technologies Used

### Frontend
- **React 18** - UI framework
- **React Router** - Client-side routing
- **Styled Components** - CSS-in-JS styling
- **Fabric.js** - Canvas manipulation
- **React Color** - Color picker component
- **React Icons** - Icon library
- **Axios** - HTTP client

### Backend
- **Flask** - Python web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Pillow** - Image processing
- **NumPy** - Numerical computing
- **Matplotlib** - Data visualization
- **SciPy** - Scientific computing

## 🎯 Key Components

### KolamStudio
Interactive drawing canvas with:
- Multiple drawing tools (pen, line, circle, square, triangle)
- Real-time symmetry guides
- Color picker and brush size controls
- Pattern templates and presets
- Export functionality

### PatternGallery
Comprehensive pattern library featuring:
- Traditional patterns from 4 Indian regions
- Cultural significance information
- Search and filtering capabilities
- Pattern metadata and statistics

### Analysis
Mathematical analysis dashboard with:
- Symmetry visualization
- Fractal dimension calculation
- Cultural region classification
- Pattern complexity metrics
- Export analysis results

## 🔧 Configuration

### Environment Variables
Create `.env` file in root directory:
```
REACT_APP_API_URL=http://localhost:5000
REACT_APP_VERSION=1.0.0
```

### API Integration
The frontend communicates with the Python backend via REST API:
- `POST /api/analyze` - Analyze pattern
- `POST /api/generate` - Generate new pattern
- `GET /api/patterns` - Get pattern templates
- `POST /api/cultural-analysis` - Cultural analysis

## 🎨 Design System

### Color Palette
- Primary: #8B5CF6 (Purple)
- Secondary: #F59E0B (Amber)
- Accent: #10B981 (Emerald)
- Background: #F8FAFC (Gray-50)
- Surface: #FFFFFF (White)

### Typography
- Font Family: Inter
- Headings: 600 weight
- Body: 400 weight
- Small text: 0.875rem

### Components
- Cards with subtle shadows
- Rounded corners (0.5rem - 1rem)
- Smooth transitions (0.2s ease)
- Hover effects with transform

## 📱 Responsive Design

The application is fully responsive with breakpoints:
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## 🧪 Testing

### Run Tests
```bash
npm test
```

### Build for Production
```bash
npm run build
```

## 🚀 Deployment

### Build and Deploy
```bash
npm run build
# Deploy build/ folder to your hosting service
```

### Docker Support
```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🔗 API Endpoints

### Pattern Analysis
```javascript
POST /api/analyze
{
  "image": "data:image/png;base64,..."
}
```

### Pattern Generation
```javascript
POST /api/generate
{
  "type": "radial",
  "grid_size": [5, 5],
  "symmetry_type": "radial"
}
```

### Cultural Analysis
```javascript
POST /api/cultural-analysis
{
  "pattern": { /* pattern data */ }
}
```

## 🎓 Educational Value

This frontend serves as an educational platform for:
- **Mathematical Concepts**: Symmetry, fractals, geometry
- **Cultural Heritage**: Traditional Indian art forms
- **Computational Thinking**: Algorithm-based pattern analysis
- **Interactive Learning**: Hands-on pattern creation

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is developed for educational purposes as part of the AICTE challenge.

## 🏆 AICTE Problem Statement 25107

**Organization**: AICTE - Indian Knowledge Systems (IKS)  
**Category**: Software  
**Theme**: Heritage & Culture  
**Objective**: Develop computer programs to identify design principles behind Kolam designs and recreate them

---

**Built with ❤️ for preserving Indian cultural heritage through technology**






