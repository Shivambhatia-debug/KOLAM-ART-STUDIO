import React, { useState, useRef, useEffect, useCallback } from 'react';
import styled from 'styled-components';
import { 
  FaStop, FaDownload, FaUndo, FaRedo, FaMagic, FaRuler, 
  FaCircle, FaSquare, FaPalette, FaEraser, FaImage, FaSprayCan,
  FaVectorSquare
} from 'react-icons/fa';
import { ChromePicker } from 'react-color';
import { toast } from 'react-toastify';
import axios from 'axios';
import { professionalDesignSystem as ds } from '../styles/ProfessionalDesignSystem';
import ProfessionalButton from '../components/ui/ProfessionalButton';
import ProfessionalCard from '../components/ui/ProfessionalCard';
import ProfessionalImageUpload from '../components/ProfessionalImageUpload';
import TopologicalPatternGenerator from '../components/TopologicalPatternGenerator';
import SpiralKolamGenerator from '../components/SpiralKolamGenerator';

const StudioContainer = styled.div`
  padding: ${ds.spacing[8]} ${ds.spacing[4]};
  min-height: calc(100vh - 72px);
  background: ${ds.colors.neutral[50]};
  
  @media (min-width: ${ds.breakpoints.lg}) {
    padding: ${ds.spacing[8]} ${ds.spacing[8]};
  }
`;

const StudioLayout = styled.div`
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: ${ds.spacing[6]};
  
  @media (max-width: ${ds.breakpoints.lg}) {
    grid-template-columns: 1fr;
    gap: ${ds.spacing[4]};
  }
`;

const Sidebar = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${ds.spacing[4]};
  
  @media (max-width: ${ds.breakpoints.lg}) {
    order: 2;
  }
`;

const MainCanvas = styled.div`
  @media (max-width: ${ds.breakpoints.lg}) {
    order: 1;
  }
`;

const CanvasContainer = styled.div`
  background: white;
  border-radius: ${ds.borderRadius.xl};
  padding: ${ds.spacing[6]};
  box-shadow: ${ds.boxShadow.lg};
  border: 1px solid ${ds.colors.neutral[200]};
`;

const Canvas = styled.canvas`
  border: 2px solid ${ds.colors.neutral[300]};
  border-radius: ${ds.borderRadius.lg};
  cursor: crosshair;
  background: white;
  display: block;
  margin: 0 auto;
  
  &:hover {
    border-color: ${ds.colors.primary[400]};
  }
`;

const ToolGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: ${ds.spacing[2]};
`;

const ColorPickerContainer = styled.div`
  .react-colorful {
    width: 100% !important;
    height: 200px !important;
  }
`;

const AnalysisResults = styled.div`
  margin-top: ${ds.spacing[4]};
  padding: ${ds.spacing[4]};
  background: ${ds.colors.primary[50]};
  border-radius: ${ds.borderRadius.lg};
  border-left: 4px solid ${ds.colors.primary[500]};
`;

const RegionSelector = styled.select`
  width: 100%;
  padding: ${ds.spacing[3]};
  border: 2px solid ${ds.colors.neutral[300]};
  border-radius: ${ds.borderRadius.lg};
  background: white;
  font-family: ${ds.typography.fontFamily.primary.join(', ')};
  font-size: ${ds.typography.fontSize.sm[0]};
  
  &:focus {
    outline: none;
    border-color: ${ds.colors.primary[400]};
    box-shadow: 0 0 0 3px rgba(255, 193, 7, 0.1);
  }
`;

const FestivalSelector = styled(RegionSelector)``;

// const PatternPreview = styled.div`
//   width: 100%;
//   height: 150px;
//   background: ${ds.colors.neutral[100]};
//   border-radius: ${ds.borderRadius.lg};
//   display: flex;
//   align-items: center;
//   justify-content: center;
//   border: 2px dashed ${ds.colors.neutral[300]};
//   margin-top: ${ds.spacing[3]};
//   position: relative;
//   overflow: hidden;
  
//   svg {
//     width: 100%;
//     height: 100%;
//     object-fit: contain;
//   }
// `;

const ProfessionalKolamStudio = ({ currentPattern, onPatternChange, onAnalysisComplete }) => {
  const canvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [currentTool, setCurrentTool] = useState('pen');
  const [currentColor, setCurrentColor] = useState('#DC143C');
  const [brushSize, setBrushSize] = useState(3);
  const [showColorPicker, setShowColorPicker] = useState(false);
  const [showImageUpload, setShowImageUpload] = useState(false);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [selectedRegion, setSelectedRegion] = useState('tamil_nadu');
  const [selectedFestival, setSelectedFestival] = useState('diwali');
  const [generatedPattern, setGeneratedPattern] = useState(null);
  const [canvasHistory, setCanvasHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const [availablePatterns, setAvailablePatterns] = useState([]);
  const [culturalAnalysis, setCulturalAnalysis] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [advancedAnalysis, setAdvancedAnalysis] = useState(null);
  const [isAdvancedAnalyzing, setIsAdvancedAnalyzing] = useState(false);
  const [showTopologicalGenerator, setShowTopologicalGenerator] = useState(false);
  const [showSpiralGenerator, setShowSpiralGenerator] = useState(false);
  const [isAnimating, setIsAnimating] = useState(false);
  const [animationSpeed, setAnimationSpeed] = useState(100);

  const saveToHistory = useCallback(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      const imageData = canvas.toDataURL();
      const newHistory = canvasHistory.slice(0, historyIndex + 1);
      newHistory.push(imageData);
      setCanvasHistory(newHistory);
      setHistoryIndex(newHistory.length - 1);
    }
  }, [canvasHistory, historyIndex]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      console.log('Canvas initialized:', canvas);
      canvas.width = 600;
      canvas.height = 400;
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = 'white';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      console.log('Canvas context initialized:', ctx);
      console.log('Canvas dimensions set to:', canvas.width, 'x', canvas.height);
      saveToHistory();
    } else {
      console.error('Canvas not found during initialization!');
    }
    
    // Load available patterns from backend
    loadAvailablePatterns();
  }, [saveToHistory]);

  const loadAvailablePatterns = async () => {
    try {
      console.log('Fetching patterns from backend...');
      const response = await axios.get('/api/patterns');
      console.log('Backend response:', response.data);
      
      if (response.data.success) {
        // Add special patterns to backend patterns
        const specialPatterns = [
          {
            id: 'brahma-knot',
            name: "Brahma's Knot (Python)",
            description: "Eternal Knot generated using Python topological analysis",
            points: 25,
            type: "eternal_knot",
            region: "Tamil Nadu",
            complexity: "high"
          },
          {
            id: 'colorful-kolam',
            name: "Colorful Kolam (Turtle)",
            description: "Vibrant circular patterns using Turtle graphics",
            points: 162,
            type: "colorful_kolam",
            region: "South India",
            complexity: "medium"
          },
          {
            id: 'enhanced-kolam',
            name: "Enhanced Kolam (Turtle)",
            description: "Multi-center colorful patterns with advanced geometry",
            points: 220,
            type: "enhanced_kolam",
            region: "South India",
            complexity: "high"
          }
        ];
        
        const allPatterns = [...response.data.patterns, ...specialPatterns];
        setAvailablePatterns(allPatterns);
        console.log('All patterns loaded:', allPatterns);
      } else {
        console.error('Backend returned error:', response.data);
      }
    } catch (error) {
      console.error('Failed to load patterns:', error);
      // Fallback to special patterns only
      const fallbackPatterns = [
        {
          id: 'brahma-knot',
          name: "Brahma's Knot (Python)",
          description: "Eternal Knot generated using Python topological analysis",
          points: 25,
          type: "eternal_knot",
          region: "Tamil Nadu",
          complexity: "high"
        },
        {
          id: 'colorful-kolam',
          name: "Colorful Kolam (Turtle)",
          description: "Vibrant circular patterns using Turtle graphics",
          points: 162,
          type: "colorful_kolam",
          region: "South India",
          complexity: "medium"
        },
        {
          id: 'enhanced-kolam',
          name: "Enhanced Kolam (Turtle)",
          description: "Multi-center colorful patterns with advanced geometry",
          points: 220,
          type: "enhanced_kolam",
          region: "South India",
          complexity: "high"
        }
      ];
      setAvailablePatterns(fallbackPatterns);
    }
  };

  const startDrawing = (e) => {
    setIsDrawing(true);
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const ctx = canvas.getContext('2d');
    ctx.beginPath();
    ctx.moveTo(x, y);
  };

  const draw = (e) => {
    if (!isDrawing) return;
    
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const ctx = canvas.getContext('2d');
    ctx.strokeStyle = currentColor;
    ctx.lineWidth = brushSize;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    
    if (currentTool === 'pen') {
      ctx.lineTo(x, y);
      ctx.stroke();
    } else if (currentTool === 'circle') {
      ctx.beginPath();
      ctx.arc(x, y, brushSize * 2, 0, 2 * Math.PI);
      ctx.fillStyle = currentColor;
      ctx.fill();
    }
  };

  const stopDrawing = () => {
    if (isDrawing) {
      setIsDrawing(false);
      saveToHistory();
    }
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    saveToHistory();
    toast.success('Canvas cleared!');
  };

  const undoAction = () => {
    if (historyIndex > 0) {
      setHistoryIndex(historyIndex - 1);
      loadFromHistory(historyIndex - 1);
    }
  };

  const redoAction = () => {
    if (historyIndex < canvasHistory.length - 1) {
      setHistoryIndex(historyIndex + 1);
      loadFromHistory(historyIndex + 1);
    }
  };

  const loadFromHistory = (index) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const img = new Image();
    img.onload = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0);
    };
    img.src = canvasHistory[index];
  };

  const analyzePattern = async () => {
    const canvas = canvasRef.current;
    const imageData = canvas.toDataURL();
    
    setIsAnalyzing(true);
    try {
      const response = await axios.post('http://localhost:5000/api/analyze', {
        image: imageData
      }, { timeout: 30000 });

      if (response.data.success) {
        setAnalysisResults(response.data.analysis);
        onAnalysisComplete && onAnalysisComplete(response.data.analysis);
        toast.success('Pattern analyzed successfully!');
      } else {
        toast.error('Analysis failed');
      }
    } catch (error) {
      console.error('Analysis error:', error);
      toast.error('Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const performAdvancedAnalysis = async () => {
    // const canvas = canvasRef.current;
    // const imageData = canvas.toDataURL();
    
    setIsAdvancedAnalyzing(true);
    try {
      // Use the generated pattern if available, otherwise use canvas data
      const patternData = generatedPattern || {
        points: [],
        paths: [],
        lines: [],
        colors: ['#DC143C']
      };
      
      console.log('Sending pattern data for analysis:', patternData);
      
      const response = await axios.post('http://127.0.0.1:5000/api/advanced-analysis', {
        pattern: patternData,
        type: 'comprehensive'
      }, { timeout: 60000 });

      console.log('Advanced analysis response:', response.data);

      if (response.data.success) {
        setAdvancedAnalysis(response.data.analysis);
        toast.success('Advanced analysis completed!');
        
        // Show processing steps
        if (response.data.analysis.processing_steps) {
          response.data.analysis.processing_steps.forEach((step, index) => {
            setTimeout(() => {
              toast.info(step, { autoClose: 2000 });
            }, index * 500);
          });
        }
      } else {
        console.error('Advanced analysis failed:', response.data);
        toast.error('Advanced analysis failed');
      }
    } catch (error) {
      console.error('Advanced analysis error:', error);
      if (error.code === 'ECONNABORTED') {
        toast.error('Analysis is taking longer than expected. The pattern may be complex. Please wait and try again.');
      } else if (error.response?.status === 500) {
        toast.error('Server processing error. Using fallback analysis...');
      } else {
        toast.error('Advanced analysis failed. Please check your connection and try again.');
      }
    } finally {
      setIsAdvancedAnalyzing(false);
    }
  };

  const generateCulturalPattern = async (region = selectedRegion) => {
    setIsGenerating(true);
    try {
      console.log('Generating cultural pattern for region:', region);
      
      // Ensure region is a string, not a React component
      const regionName = typeof region === 'string' ? region : 'tamil_nadu';
      
      // Use new production backend API
      const response = await axios.post('http://127.0.0.1:5000/api/generate', {
        type: 'cultural',
        pattern: regionName
      });
      
      if (response.data.success) {
        console.log('Cultural pattern generated:', response.data.pattern);
        console.log('Cultural pattern data structure:', {
          hasPoints: !!response.data.pattern.points,
          pointsCount: response.data.pattern.points?.length || 0,
          hasPaths: !!response.data.pattern.paths,
          pathsCount: response.data.pattern.paths?.length || 0,
          hasLines: !!response.data.pattern.lines,
          linesCount: response.data.pattern.lines?.length || 0
        });
        setGeneratedPattern(response.data.pattern);
        drawGeneratedPattern(response.data.pattern);
        toast.success(`Cultural pattern for ${regionName} generated!`);
        
        // Perform cultural analysis on generated pattern
        performCulturalAnalysis(response.data.pattern);
      } else {
        console.error('Failed to generate cultural pattern:', response.data.error);
        toast.error('Failed to generate cultural pattern');
      }
    } catch (error) {
      console.error('Error generating cultural pattern:', error);
      toast.error('Failed to generate cultural pattern: ' + error.message);
    } finally {
      setIsGenerating(false);
    }
  };

  const performCulturalAnalysis = async (pattern) => {
    try {
      const response = await axios.post('http://localhost:5000/api/cultural-analysis', {
        pattern: pattern
      }, { timeout: 10000 });

      if (response.data.success) {
        setCulturalAnalysis(response.data.cultural_analysis);
      }
    } catch (error) {
      console.error('Cultural analysis error:', error);
    }
  };

  // Animated drawing function
  const drawAnimatedPattern = async (patternData) => {
    const canvas = canvasRef.current;
    if (!canvas || !patternData) return;

    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Calculate pattern bounds for scaling
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    
    if (patternData.points && patternData.points.length > 0) {
      patternData.points.forEach(point => {
        const x = Array.isArray(point) ? point[0] : point.x;
        const y = Array.isArray(point) ? point[1] : point.y;
        minX = Math.min(minX, x);
        minY = Math.min(minY, y);
        maxX = Math.max(maxX, x);
        maxY = Math.max(maxY, y);
      });
    }

    // Add padding and calculate scale
    const padding = 50;
    const patternWidth = maxX - minX;
    const patternHeight = maxY - minY;
    const scaleX = (canvas.width - 2 * padding) / Math.max(patternWidth, 1);
    const scaleY = (canvas.height - 2 * padding) / Math.max(patternHeight, 1);
    const scale = Math.min(scaleX, scaleY, 1);

    // Center the pattern
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const patternCenterX = (minX + maxX) / 2;
    const patternCenterY = (minY + maxY) / 2;

    // Animate points appearing
    if (patternData.points && patternData.points.length > 0) {
      ctx.fillStyle = '#DC143C';
      for (let i = 0; i < patternData.points.length; i++) {
        const point = patternData.points[i];
        const x = Array.isArray(point) ? point[0] : point.x;
        const y = Array.isArray(point) ? point[1] : point.y;
        const canvasX = centerX + (x - patternCenterX) * scale;
        const canvasY = centerY + (y - patternCenterY) * scale;
        
        // Animate point growing
        for (let size = 0; size <= 6; size += 0.5) {
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          
          // Redraw previous points
          for (let j = 0; j < i; j++) {
            const prevPoint = patternData.points[j];
            const prevX = Array.isArray(prevPoint) ? prevPoint[0] : prevPoint.x;
            const prevY = Array.isArray(prevPoint) ? prevPoint[1] : prevPoint.y;
            const canvasPrevX = centerX + (prevX - patternCenterX) * scale;
            const canvasPrevY = centerY + (prevY - patternCenterY) * scale;
            
            ctx.beginPath();
            ctx.arc(canvasPrevX, canvasPrevY, 6, 0, 2 * Math.PI);
            ctx.fill();
          }
          
          // Draw current point growing
          ctx.beginPath();
          ctx.arc(canvasX, canvasY, size, 0, 2 * Math.PI);
          ctx.fill();
          
          await new Promise(resolve => setTimeout(resolve, 10));
        }
        
        await new Promise(resolve => setTimeout(resolve, animationSpeed));
      }
    }

    // Animate lines drawing
    if (patternData.lines && patternData.lines.length > 0) {
      ctx.strokeStyle = '#DC143C';
      ctx.lineWidth = 3;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      
      for (let lineIndex = 0; lineIndex < patternData.lines.length; lineIndex++) {
        const line = patternData.lines[lineIndex];
        if (line.length >= 2) {
          for (let i = 1; i < line.length; i++) {
            const startPoint = line[i - 1];
            const endPoint = line[i];
            const startX = Array.isArray(startPoint) ? startPoint[0] : startPoint.x;
            const startY = Array.isArray(startPoint) ? startPoint[1] : startPoint.y;
            const endX = Array.isArray(endPoint) ? endPoint[0] : endPoint.x;
            const endY = Array.isArray(endPoint) ? endPoint[1] : endPoint.y;
            
            const canvasStartX = centerX + (startX - patternCenterX) * scale;
            const canvasStartY = centerY + (startY - patternCenterY) * scale;
            const canvasEndX = centerX + (endX - patternCenterX) * scale;
            const canvasEndY = centerY + (endY - patternCenterY) * scale;
            
            // Animate line drawing
            const steps = 20;
            for (let step = 0; step <= steps; step++) {
              const progress = step / steps;
              const currentX = canvasStartX + (canvasEndX - canvasStartX) * progress;
              const currentY = canvasStartY + (canvasEndY - canvasStartY) * progress;
              
              ctx.beginPath();
              ctx.moveTo(canvasStartX, canvasStartY);
              ctx.lineTo(currentX, currentY);
              ctx.stroke();
              
              await new Promise(resolve => setTimeout(resolve, animationSpeed / 10));
            }
          }
        }
      }
    }

    // Animate paths drawing
    if (patternData.paths && patternData.paths.length > 0) {
      ctx.strokeStyle = '#B22222';
      ctx.lineWidth = 2;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      
      for (let pathIndex = 0; pathIndex < patternData.paths.length; pathIndex++) {
        const path = patternData.paths[pathIndex];
        if (path.length >= 2) {
          for (let i = 1; i < path.length; i++) {
            const startPoint = path[i - 1];
            const endPoint = path[i];
            const startX = Array.isArray(startPoint) ? startPoint[0] : startPoint.x;
            const startY = Array.isArray(startPoint) ? startPoint[1] : startPoint.y;
            const endX = Array.isArray(endPoint) ? endPoint[0] : endPoint.x;
            const endY = Array.isArray(endPoint) ? endPoint[1] : endPoint.y;
            
            const canvasStartX = centerX + (startX - patternCenterX) * scale;
            const canvasStartY = centerY + (startY - patternCenterY) * scale;
            const canvasEndX = centerX + (endX - patternCenterX) * scale;
            const canvasEndY = centerY + (endY - patternCenterY) * scale;
            
            // Animate path drawing
            const steps = 20;
            for (let step = 0; step <= steps; step++) {
              const progress = step / steps;
              const currentX = canvasStartX + (canvasEndX - canvasStartX) * progress;
              const currentY = canvasStartY + (canvasEndY - canvasStartY) * progress;
              
              ctx.beginPath();
              ctx.moveTo(canvasStartX, canvasStartY);
              ctx.lineTo(currentX, currentY);
              ctx.stroke();
              
              await new Promise(resolve => setTimeout(resolve, animationSpeed / 10));
            }
          }
        }
      }
    }
  };

  // Animation control functions
  const startAnimation = async () => {
    if (generatedPattern) {
      setIsAnimating(true);
      await drawAnimatedPattern(generatedPattern);
      setIsAnimating(false);
    }
  };

  const stopAnimation = () => {
    setIsAnimating(false);
    if (generatedPattern) {
      drawGeneratedPattern(generatedPattern);
    }
  };

  // Python-style generation functions
  const generatePythonBrahma = async () => {
    try {
      setIsGenerating(true);
      console.log('Generating Python-style Brahma\'s Knot...');
      
      const response = await axios.post('http://127.0.0.1:5000/api/generate-python-brahma');
      console.log('Response received:', response.data);
      
      if (response.data && response.data.pattern) {
        const patternData = response.data.pattern;
        console.log('Python Brahma pattern:', patternData);
        
        setGeneratedPattern(patternData);
        drawGeneratedPattern(patternData);
        toast.success('Python-style Brahma\'s Knot generated!');
      } else {
        console.error('Invalid response format:', response.data);
        toast.error('Invalid response from server');
      }
    } catch (error) {
      console.error('Python Brahma generation error:', error);
      console.error('Error details:', error.response?.data || error.message);
      toast.error(`Failed to generate Python Brahma's Knot: ${error.message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  const generatePythonTurtle = async () => {
    try {
      setIsGenerating(true);
      console.log('Generating Python-style Turtle Kolam...');
      
      const response = await axios.post('http://127.0.0.1:5000/api/generate-python-turtle');
      console.log('Response received:', response.data);
      
      if (response.data && response.data.pattern) {
        const patternData = response.data.pattern;
        console.log('Python Turtle pattern:', patternData);
        
        setGeneratedPattern(patternData);
        drawGeneratedPattern(patternData);
        toast.success('Python-style Turtle Kolam generated!');
      } else {
        console.error('Invalid response format:', response.data);
        toast.error('Invalid response from server');
      }
    } catch (error) {
      console.error('Python Turtle generation error:', error);
      console.error('Error details:', error.response?.data || error.message);
      toast.error(`Failed to generate Python Turtle Kolam: ${error.message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  // Production Backend Integration Functions
  // const generateAdvancedPattern = async (patternType, patternName, params = {}) => {
  //   try {
  //     setIsGenerating(true);
  //     console.log(`Generating ${patternType} pattern: ${patternName}`, params);
  //     
  //     // Ensure all parameters are serializable
  //     const cleanParams = {};
  //     Object.keys(params).forEach(key => {
  //       const value = params[key];
  //       if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') {
  //         cleanParams[key] = value;
  //       }
  //     });
  //     
  //     const response = await axios.post('http://127.0.0.1:5000/api/generate', {
  //       type: patternType,
  //       pattern: patternName,
  //       ...cleanParams
  //     });
  //
  //     if (response.data.success) {
  //       console.log(`${patternName} generated successfully:`, response.data.pattern);
  //       console.log('Pattern data structure:', {
  //         hasPoints: !!response.data.pattern.points,
  //         pointsCount: response.data.pattern.points?.length || 0,
  //         hasPaths: !!response.data.pattern.paths,
  //         pathsCount: response.data.pattern.paths?.length || 0,
  //         hasLines: !!response.data.pattern.lines,
  //         linesCount: response.data.pattern.lines?.length || 0
  //       });
  //       setGeneratedPattern(response.data.pattern);
  //       drawGeneratedPattern(response.data.pattern);
  //       toast.success(`${patternName} generated successfully!`);
  //     } else {
  //       console.error(`Failed to generate ${patternName}:`, response.data.error);
  //       toast.error(`Failed to generate ${patternName}`);
  //     }
  //   } catch (error) {
  //     console.error(`Error generating ${patternName}:`, error);
  //     toast.error(`Failed to generate ${patternName}: ` + (error.response?.data?.error || error.message));
  //   } finally {
  //     setIsGenerating(false);
  //   }
  // };

  const generateBasicPattern = async (patternName, size = 5) => {
    setIsGenerating(true);
    try {
      console.log('Generating basic pattern:', patternName, 'size:', size);
      
      // Ensure patternName is a string
      const pattern = typeof patternName === 'string' ? patternName : 'radial';
      
      // Use new production backend API
      const response = await axios.post('http://127.0.0.1:5000/api/generate', {
        type: 'basic',
        pattern: pattern,
        size: size
      });
      
      if (response.data.success) {
        console.log('Basic pattern generated:', response.data.pattern);
        console.log('Basic pattern data structure:', {
          hasPoints: !!response.data.pattern.points,
          pointsCount: response.data.pattern.points?.length || 0,
          hasPaths: !!response.data.pattern.paths,
          pathsCount: response.data.pattern.paths?.length || 0,
          hasLines: !!response.data.pattern.lines,
          linesCount: response.data.pattern.lines?.length || 0
        });
        setGeneratedPattern(response.data.pattern);
        drawGeneratedPattern(response.data.pattern);
        toast.success(`Basic pattern ${pattern} generated!`);
      } else {
        console.error('Failed to generate basic pattern:', response.data.error);
        toast.error('Failed to generate basic pattern');
      }
    } catch (error) {
      console.error('Error generating basic pattern:', error);
      toast.error('Failed to generate basic pattern: ' + error.message);
    } finally {
      setIsGenerating(false);
    }
  };

  const generateFestivalPattern = async (festival = selectedFestival) => {
    setIsGenerating(true);
    try {
      console.log('Generating festival pattern for:', festival);
      
      // Ensure festival is a string, not a React component
      const festivalName = typeof festival === 'string' ? festival : 'diwali';
      
      // Use new production backend API
      const response = await axios.post('http://127.0.0.1:5000/api/generate', {
        type: 'festival',
        pattern: festivalName
      });

      if (response.data.success) {
        console.log('Festival pattern generated:', response.data.pattern);
        console.log('Festival pattern data structure:', {
          hasPoints: !!response.data.pattern.points,
          pointsCount: response.data.pattern.points?.length || 0,
          hasPaths: !!response.data.pattern.paths,
          pathsCount: response.data.pattern.paths?.length || 0,
          hasLines: !!response.data.pattern.lines,
          linesCount: response.data.pattern.lines?.length || 0
        });
        setGeneratedPattern(response.data.pattern);
        drawGeneratedPattern(response.data.pattern);
        toast.success(`Festival pattern for ${festivalName} generated!`);
      } else {
        console.error('Failed to generate festival pattern:', response.data.error);
        toast.error('Failed to generate festival pattern');
      }
    } catch (error) {
      console.error('Error generating festival pattern:', error);
      toast.error('Failed to generate festival pattern: ' + error.message);
    } finally {
      setIsGenerating(false);
    }
  };


  const loadPatternTemplate = async (patternId) => {
    try {
      // Special handling for Brahma's Knot - use Python-generated data
      if (patternId === 'brahma-knot') {
        console.log('Loading Brahma\'s Knot with Python-generated data...');
        
        // Load the Python-generated data
        try {
          const response = await fetch('/brahma_knot_frontend_data.json');
          const patternData = await response.json();
          
          console.log('Python-generated pattern data:', patternData);
          console.log('Pattern paths:', patternData.paths);
          console.log('Pattern points:', patternData.points);
          console.log('Pattern lines:', patternData.lines);
          
          // Set and draw the pattern
          setGeneratedPattern(patternData);
          drawGeneratedPattern(patternData);
          toast.success('Brahma\'s Knot loaded with Python analysis!');
          return;
        } catch (jsonError) {
          console.log('JSON file not found, using fallback data...');
        }
      }
      
      // Special handling for Colorful Kolam - use Turtle-generated data
      if (patternId === 'colorful-kolam') {
        console.log('Loading Colorful Kolam with Turtle-generated data...');
        
        try {
          const response = await fetch('/turtle_kolam_frontend_data.json');
          const patternData = await response.json();
          
          console.log('Turtle-generated pattern data:', patternData);
          console.log('Pattern paths:', patternData.paths);
          console.log('Pattern points:', patternData.points);
          
          // Set and draw the pattern
          setGeneratedPattern(patternData);
          drawGeneratedPattern(patternData);
          toast.success('Colorful Kolam loaded with Turtle graphics!');
          return;
        } catch (jsonError) {
          console.log('Turtle JSON file not found, using fallback data...');
        }
      }
      
      // Special handling for Enhanced Kolam - use enhanced Turtle data
      if (patternId === 'enhanced-kolam') {
        console.log('Loading Enhanced Kolam with Turtle-generated data...');
        
        try {
          const response = await fetch('/enhanced_turtle_kolam_data.json');
          const patternData = await response.json();
          
          console.log('Enhanced Turtle pattern data:', patternData);
          console.log('Pattern paths:', patternData.paths);
          console.log('Pattern points:', patternData.points);
          
          // Set and draw the pattern
          setGeneratedPattern(patternData);
          drawGeneratedPattern(patternData);
          toast.success('Enhanced Kolam loaded with Turtle graphics!');
          return;
        } catch (jsonError) {
          console.log('Enhanced JSON file not found, using fallback data...');
        }
      }
      
      // Get template data
      const template = availablePatterns.find(p => p.id === patternId);
      if (template) {
        console.log('Loading template:', template);
        
        // Create pattern data from template
        const patternData = {
          points: template.dot_positions || [],
          lines: template.suggested_junctions || [],
          colors: ['#DC143C', '#B22222', '#8B0000', '#FF6347'], // Red tones like in the image
          cultural_info: {
            traditional_name: template.name,
            symbolism: template.cultural_significance,
            region: template.region
          },
          mathematical_properties: {
            symmetry_type: template.type,
            dot_count: template.points,
            path_count: template.suggested_junctions ? template.suggested_junctions.length : 0
          },
          region: template.region.toLowerCase().replace(' ', '_'),
          complexity: template.complexity
        };
        
        console.log('Generated pattern data:', patternData);
        console.log('Pattern paths:', patternData.paths);
        console.log('Pattern points:', patternData.points);
        console.log('Pattern lines:', patternData.lines);
        
        // Set and draw the pattern
        setGeneratedPattern(patternData);
        drawGeneratedPattern(patternData);
        toast.success(`${template.name} loaded!`);
      }
    } catch (error) {
      console.error('Template loading error:', error);
      toast.error('Failed to load template');
    }
  };


  const drawGeneratedPattern = (pattern) => {
    console.log('drawGeneratedPattern called with:', pattern);
    const canvas = canvasRef.current;
    
    if (!canvas) {
      console.error('Canvas not found!');
      return;
    }
    
    console.log('Canvas found:', canvas);
    console.log('Canvas dimensions:', canvas.width, 'x', canvas.height);
    
    const ctx = canvas.getContext('2d');
    
    if (!ctx) {
      console.error('Canvas context not found!');
      return;
    }
    
    console.log('Canvas context found:', ctx);
    
    // Clear canvas
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    console.log('Canvas cleared');
    
    // Calculate pattern bounds
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    
    console.log('Pattern points:', pattern.points);
    console.log('Pattern paths:', pattern.paths);
    console.log('Pattern lines:', pattern.lines);
    
    if (pattern.points && pattern.points.length > 0) {
      console.log('Processing', pattern.points.length, 'points');
      pattern.points.forEach((point, index) => {
        // Handle both array format [x, y] and object format {x, y}
        const x = Array.isArray(point) ? point[0] : point.x;
        const y = Array.isArray(point) ? point[1] : point.y;
        
        console.log(`Point ${index}:`, { x, y });
        
        minX = Math.min(minX, x);
        maxX = Math.max(maxX, x);
        minY = Math.min(minY, y);
        maxY = Math.max(maxY, y);
      });
    } else {
      console.log('No points found in pattern');
    }
    
    // Calculate pattern dimensions
    const patternWidth = maxX - minX;
    const patternHeight = maxY - minY;
    const patternCenter = [(minX + maxX) / 2, (minY + maxY) / 2];
    
    console.log('Pattern bounds:', { minX, maxX, minY, maxY });
    console.log('Pattern dimensions:', { patternWidth, patternHeight });
    console.log('Pattern center:', patternCenter);
    
    // Calculate scale to fit canvas with padding
    const padding = 50;
    const scaleX = (canvas.width - 2 * padding) / Math.max(patternWidth, 100);
    const scaleY = (canvas.height - 2 * padding) / Math.max(patternHeight, 100);
    const scale = Math.min(scaleX, scaleY, 2.0); // Cap at 2.0 for visibility
    
    const offsetX = canvas.width / 2;
    const offsetY = canvas.height / 2;
    
    console.log('Scale calculations:', { scaleX, scaleY, scale });
    console.log('Canvas offset:', { offsetX, offsetY });
    
        // Draw paths first (so they appear behind dots)
        if (pattern.paths && pattern.paths.length > 0) {
          console.log('Drawing paths:', pattern.paths.length);
          ctx.lineWidth = 4;
          ctx.lineCap = 'round';
          ctx.lineJoin = 'round';
          
          pattern.paths.forEach((path, index) => {
            if (path && path.length >= 2) {
              console.log(`Path ${index}: ${path.length} points`);
              // Use pattern colors for paths
              const color = pattern.colors ? pattern.colors[index % pattern.colors.length] : '#DC143C';
              ctx.strokeStyle = color;
              
              ctx.beginPath();
              path.forEach((point, pointIndex) => {
                // Handle both array format [x, y] and object format {x, y}
                const pointX = Array.isArray(point) ? point[0] : point.x;
                const pointY = Array.isArray(point) ? point[1] : point.y;
                
                const x = offsetX + (pointX - patternCenter[0]) * scale;
                const y = offsetY + (pointY - patternCenter[1]) * scale;
                
                if (pointIndex === 0) {
                  ctx.moveTo(x, y);
                } else {
                  ctx.lineTo(x, y);
                }
              });
              ctx.stroke();
            }
          });
        } else {
          console.log('No paths to draw');
        }
    
    // Draw points (dots)
    if (pattern.points && pattern.points.length > 0) {
      console.log('Drawing points:', pattern.points.length);
      pattern.points.forEach((point, index) => {
        // Handle both array format [x, y] and object format {x, y}
        const pointX = Array.isArray(point) ? point[0] : point.x;
        const pointY = Array.isArray(point) ? point[1] : point.y;
        
        const x = offsetX + (pointX - patternCenter[0]) * scale;
        const y = offsetY + (pointY - patternCenter[1]) * scale;
        
        console.log(`Drawing point ${index}:`, { pointX, pointY, x, y });
        
        // Use pattern colors if available, otherwise use default
        const color = pattern.colors ? pattern.colors[index % pattern.colors.length] : '#DC143C';
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(x, y, 8, 0, 2 * Math.PI);
        ctx.fill();
        
        // Add a white center for better visibility
        ctx.fillStyle = 'white';
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, 2 * Math.PI);
        ctx.fill();
      });
      console.log('Points drawn successfully');
    } else {
      console.log('No points to draw');
    }
    
    // Draw junctions (if available)
    if (pattern.junctions && pattern.junctions.length > 0) {
      pattern.junctions.forEach((junction, index) => {
        const x = offsetX + (junction.position[0] - patternCenter[0]) * scale;
        const y = offsetY + (junction.position[1] - patternCenter[1]) * scale;
        
        ctx.fillStyle = '#FFD700';
        ctx.beginPath();
        ctx.arc(x, y, 6, 0, 2 * Math.PI);
        ctx.fill();
        
        // Draw junction arms
        ctx.strokeStyle = '#FFD700';
        ctx.lineWidth = 3;
        junction.arms.forEach(arm => {
          ctx.beginPath();
          ctx.moveTo(x, y);
          ctx.lineTo(x + arm[0] * 15, y + arm[1] * 15);
          ctx.stroke();
        });
      });
    }
    
    // Draw lines connecting points (if we have lines data and no paths)
    if ((!pattern.paths || pattern.paths.length === 0) && pattern.lines && pattern.lines.length > 0) {
      ctx.lineWidth = 4;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      
      pattern.lines.forEach((line, index) => {
        if (line.length >= 2) {
          const startPoint = pattern.points[line[0]];
          const endPoint = pattern.points[line[1]];
          
          if (startPoint && endPoint) {
            // Use pattern colors for lines
            const color = pattern.colors ? pattern.colors[index % pattern.colors.length] : '#DC143C';
            ctx.strokeStyle = color;
            
            // Handle both array format [x, y] and object format {x, y}
            const startX = offsetX + ((Array.isArray(startPoint) ? startPoint[0] : startPoint.x) - patternCenter[0]) * scale;
            const startY = offsetY + ((Array.isArray(startPoint) ? startPoint[1] : startPoint.y) - patternCenter[1]) * scale;
            const endX = offsetX + ((Array.isArray(endPoint) ? endPoint[0] : endPoint.x) - patternCenter[0]) * scale;
            const endY = offsetY + ((Array.isArray(endPoint) ? endPoint[1] : endPoint.y) - patternCenter[1]) * scale;
            
            ctx.beginPath();
            ctx.moveTo(startX, startY);
            ctx.lineTo(endX, endY);
            ctx.stroke();
          }
        }
      });
    }
    
    // If no lines or paths, draw a simple radial pattern
    if ((!pattern.lines || pattern.lines.length === 0) && (!pattern.paths || pattern.paths.length === 0)) {
      ctx.lineWidth = 4;
      
      // Draw lines from center to each point
      if (pattern.points && pattern.points.length > 0) {
        const centerX = offsetX;
        const centerY = offsetY;
        
        pattern.points.forEach((point, index) => {
          // Use pattern colors for radial lines
          const color = pattern.colors ? pattern.colors[index % pattern.colors.length] : '#DC143C';
          ctx.strokeStyle = color;
          
          // Handle both array format [x, y] and object format {x, y}
          const pointX = Array.isArray(point) ? point[0] : point.x;
          const pointY = Array.isArray(point) ? point[1] : point.y;
          
          const x = offsetX + (pointX - patternCenter[0]) * scale;
          const y = offsetY + (pointY - patternCenter[1]) * scale;
          
          ctx.beginPath();
          ctx.moveTo(centerX, centerY);
          ctx.lineTo(x, y);
          ctx.stroke();
        });
      }
    }
    
    saveToHistory();
  };

  // const drawGeneratedPatternFromTemplate = (pattern) => {
  //   const canvas = canvasRef.current;
  //   const ctx = canvas.getContext('2d');
  //   
  //   // Clear canvas
  //   ctx.fillStyle = 'white';
  //   ctx.fillRect(0, 0, canvas.width, canvas.height);
  //   
  //   // Draw template-based pattern
  //   if (pattern.points) {
  //     // Draw points
  //     pattern.points.forEach((point) => {
  //       ctx.fillStyle = point.is_center ? '#FF6B35' : '#DC143C';
  //       ctx.beginPath();
  //       ctx.arc(point.x, point.y, point.is_center ? 6 : 4, 0, 2 * Math.PI);
  //       ctx.fill();
  //     });
  //     
  //     // Draw lines connecting points
  //     if (pattern.lines) {
  //       ctx.strokeStyle = '#DC143C';
  //       ctx.lineWidth = 2;
  //       ctx.lineCap = 'round';
  //       
  //       pattern.lines.forEach((line) => {
  //         const [startIdx, endIdx] = line;
  //         if (startIdx < pattern.points.length && endIdx < pattern.points.length) {
  //           const startPoint = pattern.points[startIdx];
  //           const endPoint = pattern.points[endIdx];
  //           
  //           ctx.beginPath();
  //           ctx.moveTo(startPoint.x, startPoint.y);
  //           ctx.lineTo(endPoint.x, endPoint.y);
  //           ctx.stroke();
  //         }
  //       });
  //     }
  //   }
  //   
  //   saveToHistory();
  // };

  const downloadPattern = () => {
    const canvas = canvasRef.current;
    const link = document.createElement('a');
    link.download = `kolam-pattern-${Date.now()}.png`;
    link.href = canvas.toDataURL();
    link.click();
    toast.success('Pattern downloaded!');
  };

  const tools = [
    { id: 'pen', icon: FaSprayCan, label: 'Pen' },
    { id: 'circle', icon: FaCircle, label: 'Circle' },
    { id: 'line', icon: FaRuler, label: 'Line' },
    { id: 'square', icon: FaSquare, label: 'Square' }
  ];

  const regions = [
    { value: 'tamil_nadu', label: 'Tamil Nadu (Sikku Kolam)' },
    { value: 'karnataka', label: 'Karnataka (Muggu)' },
    { value: 'kerala', label: 'Kerala (Pookalam)' },
    { value: 'andhra_pradesh', label: 'Andhra Pradesh (Muggulu)' },
    { value: 'telangana', label: 'Telangana (Gorintaku)' }
  ];

  const festivals = [
    { value: 'diwali', label: 'Diwali (Festival of Lights)' },
    { value: 'pongal', label: 'Pongal (Harvest Festival)' },
    { value: 'onam', label: 'Onam (Kerala Festival)' },
    { value: 'sankranti', label: 'Sankranti (Kite Festival)' },
    { value: 'navaratri', label: 'Navaratri (Nine Nights)' }
  ];

  return (
    <StudioContainer>
      <StudioLayout>
        <Sidebar>
          {/* Tools Panel */}
          <ProfessionalCard variant="elevated">
            <ProfessionalCard.Header>
              <ProfessionalCard.Title>🛠️ Drawing Tools</ProfessionalCard.Title>
            </ProfessionalCard.Header>
            <ProfessionalCard.Content>
              <ToolGrid>
                {tools.map(tool => (
                  <ProfessionalButton
                    key={tool.id}
                    variant={currentTool === tool.id ? 'primary' : 'outline'}
                    size="sm"
                    leftIcon={<tool.icon />}
                    onClick={() => setCurrentTool(tool.id)}
                  >
                    {tool.label}
                  </ProfessionalButton>
                ))}
              </ToolGrid>
              
              <div style={{ marginTop: ds.spacing[4] }}>
                <label style={{ 
                  display: 'block', 
                  marginBottom: ds.spacing[2],
                  fontWeight: ds.typography.fontWeight.medium,
                  color: ds.colors.neutral[700]
                }}>
                  Brush Size: {brushSize}px
                </label>
                <input
                  type="range"
                  min="1"
                  max="20"
                  value={brushSize}
                  onChange={(e) => setBrushSize(parseInt(e.target.value))}
                  style={{ width: '100%' }}
                />
              </div>
            </ProfessionalCard.Content>
          </ProfessionalCard>

          {/* Color Picker */}
          <ProfessionalCard variant="elevated">
            <ProfessionalCard.Header>
              <ProfessionalCard.Title>🎨 Colors</ProfessionalCard.Title>
            </ProfessionalCard.Header>
            <ProfessionalCard.Content>
              <ProfessionalButton
                variant={showColorPicker ? 'primary' : 'outline'}
                size="sm"
                leftIcon={<FaPalette />}
                onClick={() => setShowColorPicker(!showColorPicker)}
                fullWidth
                style={{ 
                  marginBottom: ds.spacing[3],
                  backgroundColor: currentColor,
                  color: 'white',
                  border: `2px solid ${currentColor}`
                }}
              >
                Current: {currentColor}
              </ProfessionalButton>
              
              {showColorPicker && (
                <ColorPickerContainer>
                  <ChromePicker
                    color={currentColor}
                    onChange={(color) => setCurrentColor(color.hex)}
                    width="100%"
                  />
                </ColorPickerContainer>
              )}
            </ProfessionalCard.Content>
          </ProfessionalCard>

          {/* Cultural Patterns */}
          <ProfessionalCard variant="cultural">
            <ProfessionalCard.Header>
              <ProfessionalCard.Title>🏛️ Cultural Patterns</ProfessionalCard.Title>
            </ProfessionalCard.Header>
            <ProfessionalCard.Content>
              <div style={{ marginBottom: ds.spacing[3] }}>
                <label style={{ 
                  display: 'block', 
                  marginBottom: ds.spacing[2],
                  fontWeight: ds.typography.fontWeight.medium,
                  color: ds.colors.neutral[700]
                }}>
                  Select Region:
                </label>
                <RegionSelector
                  value={selectedRegion}
                  onChange={(e) => setSelectedRegion(e.target.value)}
                >
                  {regions.map(region => (
                    <option key={region.value} value={region.value}>
                      {region.label}
                    </option>
                  ))}
                </RegionSelector>
              </div>

              <ProfessionalButton
                variant="cultural"
                size="sm"
                leftIcon={<FaMagic />}
                onClick={generateCulturalPattern}
                fullWidth
                disabled={isGenerating}
              >
                {isGenerating ? 'Generating...' : 'Generate Regional Pattern'}
              </ProfessionalButton>
            </ProfessionalCard.Content>
          </ProfessionalCard>

          {/* Festival Patterns */}
          <ProfessionalCard variant="gradient">
            <ProfessionalCard.Header>
              <ProfessionalCard.Title>🎉 Festival Themes</ProfessionalCard.Title>
            </ProfessionalCard.Header>
            <ProfessionalCard.Content>
              <div style={{ marginBottom: ds.spacing[3] }}>
                <label style={{ 
                  display: 'block', 
                  marginBottom: ds.spacing[2],
                  fontWeight: ds.typography.fontWeight.medium,
                  color: ds.colors.neutral[700]
                }}>
                  Select Festival:
                </label>
                <FestivalSelector
                  value={selectedFestival}
                  onChange={(e) => setSelectedFestival(e.target.value)}
                >
                  {festivals.map(festival => (
                    <option key={festival.value} value={festival.value}>
                      {festival.label}
                    </option>
                  ))}
                </FestivalSelector>
              </div>

              <ProfessionalButton
                variant="secondary"
                size="sm"
                leftIcon={<FaMagic />}
                onClick={generateFestivalPattern}
                fullWidth
                disabled={isGenerating}
              >
                {isGenerating ? 'Generating...' : 'Generate Festival Pattern'}
              </ProfessionalButton>
            </ProfessionalCard.Content>
          </ProfessionalCard>

          {/* Python-Style Generation */}
          <ProfessionalCard variant="elevated">
            <ProfessionalCard.Header>
              <ProfessionalCard.Title>🐍 Python-Style Generation</ProfessionalCard.Title>
            </ProfessionalCard.Header>
            <ProfessionalCard.Content>
              <div style={{ display: 'flex', flexDirection: 'column', gap: ds.spacing[3] }}>
                <ProfessionalButton
                  variant="primary"
                  size="md"
                  onClick={generatePythonBrahma}
                  disabled={isGenerating}
                  fullWidth
                  style={{ 
                    background: 'linear-gradient(135deg, #DC143C 0%, #B22222 100%)',
                    color: 'white',
                    fontWeight: 'bold'
                  }}
                >
                  {isGenerating ? '⏳ Generating...' : '🐍 Generate Python Brahma\'s Knot'}
                </ProfessionalButton>
                
                <ProfessionalButton
                  variant="secondary"
                  size="md"
                  onClick={generatePythonTurtle}
                  disabled={isGenerating}
                  fullWidth
                  style={{ 
                    background: 'linear-gradient(135deg, #4ECDC4 0%, #45B7D1 100%)',
                    color: 'white',
                    fontWeight: 'bold'
                  }}
                >
                  {isGenerating ? '⏳ Generating...' : '🎨 Generate Python Turtle Kolam'}
                </ProfessionalButton>
                
                <div style={{ 
                  fontSize: ds.typography.fontSize.sm[0],
                  color: ds.colors.neutral[600],
                  textAlign: 'center',
                  padding: ds.spacing[2],
                  backgroundColor: ds.colors.neutral[100],
                  borderRadius: ds.borderRadius.md
                }}>
                  Generate patterns exactly like Python terminal
                </div>
              </div>
            </ProfessionalCard.Content>
          </ProfessionalCard>

          {/* Production Backend Integration */}
          <ProfessionalCard title="Production Backend Patterns" icon={<FaMagic />}>
            <ProfessionalCard.Content>
              <div style={{ marginBottom: ds.spacing[4] }}>
                <h4 style={{ 
                  fontSize: ds.typography.fontSize.sm[0],
                  fontWeight: ds.typography.fontWeight.semibold,
                  color: ds.colors.neutral[700],
                  marginBottom: ds.spacing[2]
                }}>
                  Basic Patterns
                </h4>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: ds.spacing[2] }}>
                  <ProfessionalButton
                    variant="outline"
                    size="sm"
                    onClick={() => generateBasicPattern('radial', 8)}
                    disabled={isGenerating}
                    fullWidth
                  >
                    Radial
                  </ProfessionalButton>
                  <ProfessionalButton
                    variant="outline"
                    size="sm"
                    onClick={() => generateBasicPattern('bilateral', 6)}
                    disabled={isGenerating}
                    fullWidth
                  >
                    Bilateral
                  </ProfessionalButton>
                  <ProfessionalButton
                    variant="outline"
                    size="sm"
                    onClick={() => generateBasicPattern('grid', 5)}
                    disabled={isGenerating}
                    fullWidth
                  >
                    Grid
                  </ProfessionalButton>
                  <ProfessionalButton
                    variant="outline"
                    size="sm"
                    onClick={() => generateBasicPattern('circular', 7)}
                    disabled={isGenerating}
                    fullWidth
                  >
                    Circular
                  </ProfessionalButton>
                </div>
              </div>

              <div style={{ marginBottom: ds.spacing[4] }}>
                <h4 style={{ 
                  fontSize: ds.typography.fontSize.sm[0],
                  fontWeight: ds.typography.fontWeight.semibold,
                  color: ds.colors.neutral[700],
                  marginBottom: ds.spacing[2]
                }}>
                  Cultural Patterns
                </h4>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: ds.spacing[2] }}>
                  <ProfessionalButton
                    variant="outline"
                    size="sm"
                    onClick={() => generateCulturalPattern('tamil_nadu')}
                    disabled={isGenerating}
                    fullWidth
                  >
                    Tamil Nadu
                  </ProfessionalButton>
                  <ProfessionalButton
                    variant="outline"
                    size="sm"
                    onClick={() => generateCulturalPattern('kerala')}
                    disabled={isGenerating}
                    fullWidth
                  >
                    Kerala
                  </ProfessionalButton>
                  <ProfessionalButton
                    variant="outline"
                    size="sm"
                    onClick={() => generateCulturalPattern('karnataka')}
                    disabled={isGenerating}
                    fullWidth
                  >
                    Karnataka
                  </ProfessionalButton>
                  <ProfessionalButton
                    variant="outline"
                    size="sm"
                    onClick={() => generateCulturalPattern('andhra_pradesh')}
                    disabled={isGenerating}
                    fullWidth
                  >
                    Andhra Pradesh
                  </ProfessionalButton>
                </div>
              </div>

              <div>
                <h4 style={{ 
                  fontSize: ds.typography.fontSize.sm[0],
                  fontWeight: ds.typography.fontWeight.semibold,
                  color: ds.colors.neutral[700],
                  marginBottom: ds.spacing[2]
                }}>
                  Festival Patterns
                </h4>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: ds.spacing[2] }}>
                  <ProfessionalButton
                    variant="outline"
                    size="sm"
                    onClick={() => generateFestivalPattern('diwali')}
                    disabled={isGenerating}
                    fullWidth
                  >
                    Diwali
                  </ProfessionalButton>
                  <ProfessionalButton
                    variant="outline"
                    size="sm"
                    onClick={() => generateFestivalPattern('pongal')}
                    disabled={isGenerating}
                    fullWidth
                  >
                    Pongal
                  </ProfessionalButton>
                  <ProfessionalButton
                    variant="outline"
                    size="sm"
                    onClick={() => generateFestivalPattern('onam')}
                    disabled={isGenerating}
                    fullWidth
                  >
                    Onam
                  </ProfessionalButton>
                  <ProfessionalButton
                    variant="outline"
                    size="sm"
                    onClick={() => generateFestivalPattern('ugadi')}
                    disabled={isGenerating}
                    fullWidth
                  >
                    Ugadi
                  </ProfessionalButton>
                </div>
              </div>
            </ProfessionalCard.Content>
          </ProfessionalCard>

          {/* Animation Controls */}
          <ProfessionalCard variant="elevated">
            <ProfessionalCard.Header>
              <ProfessionalCard.Title>🎬 Animation Controls</ProfessionalCard.Title>
            </ProfessionalCard.Header>
            <ProfessionalCard.Content>
              <div style={{ display: 'flex', flexDirection: 'column', gap: ds.spacing[3] }}>
                <div style={{ display: 'flex', gap: ds.spacing[2] }}>
                  <ProfessionalButton
                    variant="primary"
                    size="sm"
                    onClick={startAnimation}
                    disabled={!generatedPattern || isAnimating}
                    style={{ flex: 1 }}
                  >
                    {isAnimating ? '⏳ Animating...' : '▶️ Start Animation'}
                  </ProfessionalButton>
                  <ProfessionalButton
                    variant="secondary"
                    size="sm"
                    onClick={stopAnimation}
                    disabled={!isAnimating}
                    style={{ flex: 1 }}
                  >
                    ⏹️ Stop
                  </ProfessionalButton>
                </div>
                
                <div>
                  <label style={{ 
                    display: 'block', 
                    marginBottom: ds.spacing[2], 
                    fontSize: ds.typography.fontSize.sm[0],
                    color: ds.colors.neutral[700]
                  }}>
                    Animation Speed: {animationSpeed}ms
                  </label>
                  <input
                    type="range"
                    min="50"
                    max="500"
                    value={animationSpeed}
                    onChange={(e) => setAnimationSpeed(parseInt(e.target.value))}
                    style={{
                      width: '100%',
                      height: '6px',
                      borderRadius: '3px',
                      background: ds.colors.neutral[200],
                      outline: 'none',
                      cursor: 'pointer'
                    }}
                  />
                </div>
              </div>
            </ProfessionalCard.Content>
          </ProfessionalCard>

          {/* Pattern Templates */}
          <ProfessionalCard variant="elevated">
            <ProfessionalCard.Header>
              <ProfessionalCard.Title>📐 Pattern Templates</ProfessionalCard.Title>
            </ProfessionalCard.Header>
            <ProfessionalCard.Content>
              <div style={{ display: 'flex', flexDirection: 'column', gap: ds.spacing[2] }}>
                {availablePatterns.map(pattern => (
                  <ProfessionalButton
                    key={pattern.id}
                    variant="ghost"
                    size="sm"
                    onClick={() => loadPatternTemplate(pattern.id)}
                    fullWidth
                    style={{
                      textAlign: 'left',
                      justifyContent: 'flex-start',
                      padding: ds.spacing[3],
                      border: `1px solid ${ds.colors.neutral[200]}`,
                      borderRadius: ds.borderRadius.lg,
                      backgroundColor: 'white'
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: ds.typography.fontWeight.medium, color: ds.colors.neutral[900] }}>
                        {pattern.name}
                      </div>
                      <div style={{ fontSize: ds.typography.fontSize.xs[0], color: ds.colors.neutral[600] }}>
                        {pattern.region} • {pattern.complexity}
                      </div>
                    </div>
                  </ProfessionalButton>
                ))}
                
                {availablePatterns.length === 0 && (
                  <div style={{ 
                    textAlign: 'center', 
                    color: ds.colors.neutral[500],
                    fontSize: ds.typography.fontSize.sm[0],
                    padding: ds.spacing[4]
                  }}>
                    Loading templates...
                  </div>
                )}
              </div>
            </ProfessionalCard.Content>
          </ProfessionalCard>

          {/* Actions */}
          <ProfessionalCard variant="elevated">
            <ProfessionalCard.Header>
              <ProfessionalCard.Title>⚡ Actions</ProfessionalCard.Title>
            </ProfessionalCard.Header>
            <ProfessionalCard.Content>
              <div style={{ display: 'flex', flexDirection: 'column', gap: ds.spacing[2] }}>
                <ProfessionalButton
                  variant="success"
                  size="sm"
                  leftIcon={<FaImage />}
                  onClick={() => setShowImageUpload(!showImageUpload)}
                  fullWidth
                >
                  Upload & Analyze Image
                </ProfessionalButton>
                
                <ProfessionalButton
                  variant="primary"
                  size="sm"
                  leftIcon={<FaVectorSquare />}
                  onClick={() => setShowTopologicalGenerator(!showTopologicalGenerator)}
                  fullWidth
                >
                  {showTopologicalGenerator ? 'Hide' : 'Show'} Topological Generator
                </ProfessionalButton>
                
                <ProfessionalButton
                  variant="secondary"
                  size="sm"
                  leftIcon={<FaMagic />}
                  onClick={() => setShowSpiralGenerator(!showSpiralGenerator)}
                  fullWidth
                  style={{ 
                    background: 'linear-gradient(135deg, #4ECDC4 0%, #45B7D1 100%)',
                    color: 'white',
                    fontWeight: 'bold'
                  }}
                >
                  {showSpiralGenerator ? 'Hide' : 'Show'} Spiral Kolam Generator
                </ProfessionalButton>
                
                <ProfessionalButton
                  variant="primary"
                  size="sm"
                  leftIcon={isAnalyzing ? <FaStop /> : <FaMagic />}
                  onClick={analyzePattern}
                  disabled={isAnalyzing}
                  fullWidth
                >
                  {isAnalyzing ? 'Analyzing...' : 'Basic Analysis'}
                </ProfessionalButton>
                
                <ProfessionalButton
                  variant="success"
                  size="sm"
                  leftIcon={isAdvancedAnalyzing ? <FaStop /> : <FaVectorSquare />}
                  onClick={performAdvancedAnalysis}
                  disabled={isAdvancedAnalyzing}
                  fullWidth
                >
                  {isAdvancedAnalyzing ? 'Processing...' : 'Advanced Analysis'}
                </ProfessionalButton>
                
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: ds.spacing[2] }}>
                  <ProfessionalButton
                    variant="ghost"
                    size="sm"
                    iconOnly
                    onClick={undoAction}
                    disabled={historyIndex <= 0}
                    title="Undo"
                  >
                    <FaUndo />
                  </ProfessionalButton>
                  
                  <ProfessionalButton
                    variant="ghost"
                    size="sm"
                    iconOnly
                    onClick={redoAction}
                    disabled={historyIndex >= canvasHistory.length - 1}
                    title="Redo"
                  >
                    <FaRedo />
                  </ProfessionalButton>
                </div>
                
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: ds.spacing[2] }}>
                  <ProfessionalButton
                    variant="warning"
                    size="sm"
                    leftIcon={<FaEraser />}
                    onClick={clearCanvas}
                  >
                    Clear
                  </ProfessionalButton>
                  
                  <ProfessionalButton
                    variant="secondary"
                    size="sm"
                    leftIcon={<FaDownload />}
                    onClick={downloadPattern}
                  >
                    Export
                  </ProfessionalButton>
                </div>
              </div>
            </ProfessionalCard.Content>
          </ProfessionalCard>
        </Sidebar>

        <MainCanvas>
          {/* Header */}
          <div style={{ marginBottom: ds.spacing[6] }}>
            <h1 style={{
              fontFamily: ds.typography.fontFamily.heading.join(', '),
              fontSize: ds.typography.fontSize['3xl'][0],
              fontWeight: ds.typography.fontWeight.bold,
              color: ds.colors.neutral[900],
              marginBottom: ds.spacing[2]
            }}>
              🎨 Professional Kolam Studio
            </h1>
            <p style={{
              fontSize: ds.typography.fontSize.lg[0],
              color: ds.colors.neutral[600]
            }}>
              Create authentic Kolam patterns with research-based tools and cultural authenticity
            </p>
          </div>

          {/* Image Upload Section */}
          {showImageUpload && (
            <div style={{ marginBottom: ds.spacing[6] }}>
              <ProfessionalImageUpload 
                onAnalysisComplete={setAnalysisResults}
                onPatternGenerated={(pattern) => {
                  drawGeneratedPattern(pattern);
                  setShowImageUpload(false);
                }}
              />
            </div>
          )}

          {/* Topological Pattern Generator Section */}
          {showTopologicalGenerator && (
            <div style={{ marginBottom: ds.spacing[6] }}>
              <TopologicalPatternGenerator
                onPatternGenerated={(pattern) => {
                  drawGeneratedPattern(pattern);
                  setShowTopologicalGenerator(false);
                }}
                onAnalysisComplete={setAdvancedAnalysis}
              />
            </div>
          )}

          {/* Spiral Kolam Generator Section */}
          {showSpiralGenerator && (
            <div style={{ marginBottom: ds.spacing[6] }}>
              <SpiralKolamGenerator />
            </div>
          )}

          {/* Canvas Section */}
          <CanvasContainer>
            <Canvas
              ref={canvasRef}
              onMouseDown={startDrawing}
              onMouseMove={draw}
              onMouseUp={stopDrawing}
              onMouseLeave={stopDrawing}
            />
          </CanvasContainer>

          {/* Advanced Analysis Results */}
          {advancedAnalysis && (
            <div style={{ marginTop: ds.spacing[6] }}>
              <ProfessionalCard variant="gradient">
                <ProfessionalCard.Header>
                  <ProfessionalCard.Title>🔬 Advanced Analysis Results</ProfessionalCard.Title>
                </ProfessionalCard.Header>
                <ProfessionalCard.Content>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: ds.spacing[4] }}>
                    <div>
                      <strong>🎯 Quality Score:</strong>
                      <div style={{ color: ds.colors.accent.emerald[600], fontWeight: ds.typography.fontWeight.bold, fontSize: ds.typography.fontSize.lg[0] }}>
                        {advancedAnalysis.quality_score ? `${(advancedAnalysis.quality_score * 100).toFixed(1)}%` : 'N/A'}
                      </div>
                    </div>
                    
                    <div>
                      <strong>🔗 Eulerian Path:</strong>
                      <div style={{ color: advancedAnalysis.eulerian_analysis?.euler_path_exists ? ds.colors.accent.emerald[600] : ds.colors.accent.ruby[600] }}>
                        {advancedAnalysis.eulerian_analysis?.euler_path_exists ? '✅ Yes' : '❌ No'}
                      </div>
                    </div>
                    
                    <div>
                      <strong>📐 Graph Nodes:</strong>
                      <div style={{ color: ds.colors.secondary[600] }}>
                        {advancedAnalysis.geometric_properties?.graph_nodes || 0}
                      </div>
                    </div>
                    
                    <div>
                      <strong>🏛️ Cultural Region:</strong>
                      <div style={{ color: ds.colors.primary[600], textTransform: 'capitalize' }}>
                        {advancedAnalysis.cultural_classification?.region?.replace('_', ' ') || 'Unknown'}
                      </div>
                    </div>
                  </div>
                  
                  {advancedAnalysis.recommendations && Array.isArray(advancedAnalysis.recommendations) && (
                    <div style={{ marginTop: ds.spacing[4], padding: ds.spacing[3], backgroundColor: ds.colors.accent.sapphire[50], borderRadius: ds.borderRadius.lg }}>
                      <strong>💡 Expert Recommendations:</strong>
                      <ul style={{ marginTop: ds.spacing[2], paddingLeft: ds.spacing[4] }}>
                        {advancedAnalysis.recommendations.slice(0, 3).map((rec, index) => (
                          <li key={index} style={{ color: ds.colors.neutral[700], marginBottom: ds.spacing[1] }}>
                            {rec}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </ProfessionalCard.Content>
              </ProfessionalCard>
            </div>
          )}

          {/* Basic Analysis Results */}
          {analysisResults && !advancedAnalysis && (
            <div style={{ marginTop: ds.spacing[6] }}>
              <ProfessionalCard variant="filled">
                <ProfessionalCard.Header>
                  <ProfessionalCard.Title>📊 Basic Analysis Results</ProfessionalCard.Title>
                </ProfessionalCard.Header>
                <ProfessionalCard.Content>
                  <AnalysisResults>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: ds.spacing[4] }}>
                      <div>
                        <strong>Cultural Region:</strong>
                        <div style={{ color: ds.colors.primary[600], fontWeight: ds.typography.fontWeight.medium }}>
                          {analysisResults.cultural_region || 'Tamil Nadu'}
                        </div>
                      </div>
                      
                      <div>
                        <strong>Symmetry Type:</strong>
                        <div style={{ color: ds.colors.secondary[600], fontWeight: ds.typography.fontWeight.medium }}>
                          {analysisResults.symmetry_type || 'Bilateral'}
                        </div>
                      </div>
                      
                      <div>
                        <strong>Complexity:</strong>
                        <div style={{ color: ds.colors.accent.emerald[600], fontWeight: ds.typography.fontWeight.medium }}>
                          {analysisResults.complexity || 'Medium'}
                        </div>
                      </div>
                      
                      <div>
                        <strong>Confidence:</strong>
                        <div style={{ color: ds.colors.accent.sapphire[600], fontWeight: ds.typography.fontWeight.medium }}>
                          {analysisResults.confidence ? `${(analysisResults.confidence * 100).toFixed(1)}%` : '85%'}
                        </div>
                      </div>
                    </div>
                    
                    <div style={{ marginTop: ds.spacing[4], padding: ds.spacing[3], backgroundColor: ds.colors.accent.amber[50], borderRadius: ds.borderRadius.lg, border: `1px solid ${ds.colors.accent.amber[200]}` }}>
                      <strong>🚀 Want More?</strong> Try the <strong>Advanced Analysis</strong> for Hough Circle Transform, NetworkX Graph Analysis, and Eulerian Path validation!
                    </div>
                  </AnalysisResults>
                </ProfessionalCard.Content>
              </ProfessionalCard>
            </div>
          )}

          {/* Cultural Analysis Results */}
          {culturalAnalysis && (
            <div style={{ marginTop: ds.spacing[6] }}>
              <ProfessionalCard variant="cultural">
                <ProfessionalCard.Header>
                  <ProfessionalCard.Title>🔍 Cultural Analysis</ProfessionalCard.Title>
                </ProfessionalCard.Header>
                <ProfessionalCard.Content>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: ds.spacing[4] }}>
                    <div>
                      <strong>Most Likely Region:</strong>
                      <div style={{ color: ds.colors.primary[600], fontWeight: ds.typography.fontWeight.medium }}>
                        {culturalAnalysis.most_likely_region}
                      </div>
                    </div>
                    
                    <div>
                      <strong>Confidence:</strong>
                      <div style={{ color: ds.colors.secondary[600], fontWeight: ds.typography.fontWeight.medium }}>
                        {(culturalAnalysis.confidence * 100).toFixed(1)}%
                      </div>
                    </div>
                  </div>
                  
                  <div style={{ marginTop: ds.spacing[4] }}>
                    <strong>Cultural Significance:</strong>
                    <p style={{ 
                      marginTop: ds.spacing[2], 
                      color: ds.colors.neutral[700],
                      lineHeight: ds.typography.lineHeight.relaxed
                    }}>
                      {culturalAnalysis.cultural_significance}
                    </p>
                  </div>
                  
                  <div style={{ marginTop: ds.spacing[4] }}>
                    <strong>Regional Scores:</strong>
                    <div style={{ marginTop: ds.spacing[2] }}>
                      {Object.entries(culturalAnalysis.regional_scores || {}).map(([region, score]) => (
                        <div key={region} style={{ 
                          display: 'flex', 
                          justifyContent: 'space-between', 
                          alignItems: 'center',
                          marginBottom: ds.spacing[1]
                        }}>
                          <span style={{ textTransform: 'capitalize' }}>
                            {region.replace('_', ' ')}:
                          </span>
                          <div style={{ display: 'flex', alignItems: 'center', gap: ds.spacing[2] }}>
                            <div style={{
                              width: '100px',
                              height: '6px',
                              backgroundColor: ds.colors.neutral[200],
                              borderRadius: ds.borderRadius.full,
                              overflow: 'hidden'
                            }}>
                              <div style={{
                                width: `${score * 100}%`,
                                height: '100%',
                                backgroundColor: ds.colors.primary[500],
                                borderRadius: ds.borderRadius.full
                              }} />
                            </div>
                            <span style={{ fontSize: ds.typography.fontSize.sm[0], color: ds.colors.neutral[600] }}>
                              {(score * 100).toFixed(1)}%
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </ProfessionalCard.Content>
              </ProfessionalCard>
            </div>
          )}

          {/* Generated Pattern Info */}
          {generatedPattern && (
            <div style={{ marginTop: ds.spacing[6] }}>
              <ProfessionalCard variant="gradient">
                <ProfessionalCard.Header>
                  <ProfessionalCard.Title>🎭 Generated Pattern Info</ProfessionalCard.Title>
                </ProfessionalCard.Header>
                <ProfessionalCard.Content>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: ds.spacing[4] }}>
                    {generatedPattern.cultural_info && (
                      <div>
                        <strong>Traditional Name:</strong>
                        <div style={{ color: ds.colors.primary[600] }}>
                          {generatedPattern.cultural_info.traditional_name}
                        </div>
                        <div style={{ fontSize: ds.typography.fontSize.sm[0], color: ds.colors.neutral[600], marginTop: ds.spacing[1] }}>
                          {generatedPattern.cultural_info.symbolism}
                        </div>
                      </div>
                    )}
                    
                    {generatedPattern.festival_info && (
                      <div>
                        <strong>Festival:</strong>
                        <div style={{ color: ds.colors.secondary[600] }}>
                          {generatedPattern.festival_info.name}
                        </div>
                        <div style={{ fontSize: ds.typography.fontSize.sm[0], color: ds.colors.neutral[600], marginTop: ds.spacing[1] }}>
                          {generatedPattern.festival_info.cultural_significance}
                        </div>
                      </div>
                    )}
                    
                    <div>
                      <strong>Region:</strong>
                      <div style={{ color: ds.colors.accent.emerald[600] }}>
                        {generatedPattern.region || selectedRegion}
                      </div>
                    </div>
                    
                    <div>
                      <strong>Colors Used:</strong>
                      <div style={{ display: 'flex', gap: ds.spacing[1], marginTop: ds.spacing[1], flexWrap: 'wrap' }}>
                        {generatedPattern.colors?.slice(0, 8).map((color, index) => (
                          <div
                            key={index}
                            style={{
                              width: '24px',
                              height: '24px',
                              backgroundColor: color,
                              borderRadius: '50%',
                              border: '2px solid white',
                              boxShadow: ds.boxShadow.sm
                            }}
                            title={color}
                          />
                        ))}
                      </div>
                    </div>
                  </div>
                  
                  {generatedPattern.mathematical_properties && (
                    <div style={{ marginTop: ds.spacing[4], paddingTop: ds.spacing[4], borderTop: `1px solid ${ds.colors.neutral[200]}` }}>
                      <strong>Mathematical Properties:</strong>
                      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: ds.spacing[3], marginTop: ds.spacing[2] }}>
                        <div>
                          <span style={{ fontSize: ds.typography.fontSize.sm[0], color: ds.colors.neutral[600] }}>
                            Symmetry: {generatedPattern.mathematical_properties.symmetry_type}
                          </span>
                        </div>
                        <div>
                          <span style={{ fontSize: ds.typography.fontSize.sm[0], color: ds.colors.neutral[600] }}>
                            Dots: {generatedPattern.mathematical_properties.dot_count}
                          </span>
                        </div>
                        <div>
                          <span style={{ fontSize: ds.typography.fontSize.sm[0], color: ds.colors.neutral[600] }}>
                            Paths: {generatedPattern.mathematical_properties.path_count}
                          </span>
                        </div>
                      </div>
                    </div>
                  )}
                </ProfessionalCard.Content>
              </ProfessionalCard>
            </div>
          )}
        </MainCanvas>
      </StudioLayout>
    </StudioContainer>
  );
};

export default ProfessionalKolamStudio;
