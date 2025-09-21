import React, { useState, useRef, useEffect, useCallback } from 'react';
import styled from 'styled-components';
import { FaPlay, FaStop, FaDownload, FaUpload, FaUndo, FaRedo, FaMagic, FaRuler, FaCircle, FaSquare, FaPalette, FaCog, FaInfoCircle, FaEraser, FaSprayCan, FaVectorSquare, FaDrawPolygon, FaExpand, FaCompress, FaGrid3X3, FaMagnet, FaSave, FaFolderOpen, FaImage } from 'react-icons/fa';
import { ChromePicker } from 'react-color';
import { toast } from 'react-toastify';
import axios from 'axios';
import { professionalDesignSystem as ds } from '../styles/ProfessionalDesignSystem';
import ProfessionalButton from '../components/ui/ProfessionalButton';
import ProfessionalCard from '../components/ui/ProfessionalCard';
import ProfessionalImageUpload from '../components/ProfessionalImageUpload';

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

const StudioHeader = styled.div`
  background: white;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
`;

const Title = styled.h1`
  font-size: 2rem;
  color: ${props => props.theme.colors.text};
  display: flex;
  align-items: center;
  gap: 0.75rem;
`;

const Toolbar = styled.div`
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
`;

const ToolButton = styled.button`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s ease;
  background: ${props => props.active ? props.theme.colors.primary : 'white'};
  color: ${props => props.active ? 'white' : props.theme.colors.text};
  border: 2px solid ${props => props.active ? props.theme.colors.primary : props.theme.colors.border};

  &:hover {
    background: ${props => props.active ? props.theme.colors.primary : props.theme.colors.background};
    transform: translateY(-1px);
  }
`;

const StudioContent = styled.div`
  display: grid;
  grid-template-columns: 300px 1fr 300px;
  gap: 2rem;
  height: calc(100vh - 200px);

  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
    height: auto;
  }
`;

const SidebarPanel = styled.div`
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  height: fit-content;
  max-height: calc(100vh - 200px);
  overflow-y: auto;
`;

const SidebarTitle = styled.h3`
  font-size: 1.25rem;
  margin-bottom: 1rem;
  color: ${props => props.theme.colors.text};
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const ToolGroup = styled.div`
  margin-bottom: 2rem;
`;

const ToolGroupTitle = styled.h4`
  font-size: 1rem;
  margin-bottom: 0.75rem;
  color: ${props => props.theme.colors.textSecondary};
  text-transform: uppercase;
  letter-spacing: 0.05em;
`;

const ToolGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
`;

const ToolItem = styled.button`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  border: 2px solid ${props => props.active ? props.theme.colors.primary : props.theme.colors.border};
  background: ${props => props.active ? props.theme.colors.primary : 'white'};
  color: ${props => props.active ? 'white' : props.theme.colors.text};
  transition: all 0.2s ease;

  &:hover {
    border-color: ${props => props.theme.colors.primary};
    transform: translateY(-1px);
  }
`;

const CanvasContainer = styled.div`
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
`;

const Canvas = styled.canvas`
  border: 2px solid ${props => props.theme.colors.border};
  border-radius: 0.5rem;
  cursor: crosshair;
  background: white;
`;

const CanvasControls = styled.div`
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  align-items: center;
`;

const ColorPicker = styled.div`
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 10;
`;

const PropertiesPanel = styled.div`
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  height: fit-content;
  max-height: calc(100vh - 200px);
  overflow-y: auto;
`;

const PropertyGroup = styled.div`
  margin-bottom: 1.5rem;
`;

const PropertyLabel = styled.label`
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: ${props => props.theme.colors.text};
`;

const PropertyInput = styled.input`
  width: 100%;
  padding: 0.75rem;
  border: 2px solid ${props => props.theme.colors.border};
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: border-color 0.2s ease;

  &:focus {
    border-color: ${props => props.theme.colors.primary};
  }
`;

const PropertySelect = styled.select`
  width: 100%;
  padding: 0.75rem;
  border: 2px solid ${props => props.theme.colors.border};
  border-radius: 0.5rem;
  font-size: 0.875rem;
  background: white;
  transition: border-color 0.2s ease;

  &:focus {
    border-color: ${props => props.theme.colors.primary};
  }
`;

const SymmetryGuide = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 2px;
  height: 100%;
  background: rgba(139, 92, 246, 0.3);
  pointer-events: none;
  display: ${props => props.show ? 'block' : 'none'};
`;

const SymmetryGuideHorizontal = styled(SymmetryGuide)`
  width: 100%;
  height: 2px;
`;

const PatternTemplates = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
  margin-top: 1rem;
`;

const TemplateButton = styled.button`
  padding: 0.75rem;
  border: 2px solid ${props => props.theme.colors.border};
  border-radius: 0.5rem;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.75rem;

  &:hover {
    border-color: ${props => props.theme.colors.primary};
    background: ${props => props.theme.colors.background};
  }
`;

function KolamStudio({ currentPattern, onPatternChange, onAnalysisComplete }) {
  const canvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [currentTool, setCurrentTool] = useState('pen');
  const [currentColor, setCurrentColor] = useState('#000000');
  const [brushSize, setBrushSize] = useState(2);
  const [showColorPicker, setShowColorPicker] = useState(false);
  const [showSymmetryGuide, setShowSymmetryGuide] = useState(false);
  const [symmetryType, setSymmetryType] = useState('none');
  const [patternData, setPatternData] = useState(null);
  const [history, setHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const [startPoint, setStartPoint] = useState(null);
  const [showGrid, setShowGrid] = useState(true);
  const [gridSize, setGridSize] = useState(20);
  const [snapToGrid, setSnapToGrid] = useState(true);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [savedPatterns, setSavedPatterns] = useState([]);
  const [showPatternGallery, setShowPatternGallery] = useState(false);
  const [showImageUpload, setShowImageUpload] = useState(false);

  const tools = [
    { id: 'pen', icon: FaCircle, label: 'Pen', category: 'drawing' },
    { id: 'line', icon: FaRuler, label: 'Line', category: 'shapes' },
    { id: 'circle', icon: FaCircle, label: 'Circle', category: 'shapes' },
    { id: 'square', icon: FaSquare, label: 'Square', category: 'shapes' },
    { id: 'polygon', icon: FaDrawPolygon, label: 'Polygon', category: 'shapes' },
    { id: 'eraser', icon: FaEraser, label: 'Eraser', category: 'drawing' },
    { id: 'spray', icon: FaSprayCan, label: 'Spray', category: 'drawing' },
    { id: 'curve', icon: FaVectorSquare, label: 'Curve', category: 'shapes' },
    { id: 'text', icon: FaInfoCircle, label: 'Text', category: 'tools' }
  ];

  const symmetryTypes = [
    { value: 'none', label: 'No Symmetry' },
    { value: 'horizontal', label: 'Horizontal' },
    { value: 'vertical', label: 'Vertical' },
    { value: 'radial', label: 'Radial' },
    { value: 'rotational', label: 'Rotational' }
  ];

  const patternTemplates = [
    { name: 'Basic Grid', type: 'grid', region: 'Traditional' },
    { name: 'Radial Kolam', type: 'radial', region: 'Tamil Nadu' },
    { name: 'Bilateral Muggu', type: 'bilateral', region: 'Karnataka' },
    { name: 'Floral Rangoli', type: 'floral', region: 'Andhra Pradesh' },
    { name: 'Sikku Kolam', type: 'sikku', region: 'Tamil Nadu' },
    { name: 'Fractal Pattern', type: 'fractal', region: 'Modern' },
    { name: 'Festival Design', type: 'festival', region: 'All Regions' },
    { name: 'Geometric Pattern', type: 'geometric', region: 'Kerala' }
  ];

  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      canvas.width = 600;
      canvas.height = 600;
      
      // Set up drawing context
      ctx.strokeStyle = currentColor;
      ctx.lineWidth = brushSize;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      
      // Draw grid if enabled
      if (showGrid) {
        drawGrid(ctx);
      }
    }
  }, [currentColor, brushSize, showGrid, gridSize]);

  // Load saved patterns from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('savedPatterns');
    if (saved) {
      try {
        setSavedPatterns(JSON.parse(saved));
      } catch (error) {
        console.error('Error loading saved patterns:', error);
      }
    }
  }, []);

  // Load patterns from backend gallery
  const loadPatternsFromGallery = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/patterns');
      if (response.data.success) {
        const galleryPatterns = response.data.patterns.map(pattern => ({
          id: pattern.id,
          name: pattern.name,
          type: pattern.type,
          region: pattern.region,
          description: pattern.description,
          complexity: pattern.complexity,
          points: pattern.points,
          lines: pattern.lines
        }));
        setSavedPatterns(prev => [...prev, ...galleryPatterns]);
        toast.success('Gallery patterns loaded successfully!');
      }
    } catch (error) {
      console.error('Error loading gallery patterns:', error);
      toast.error('Failed to load gallery patterns');
    }
  };

  // Save current state to history
  const saveToHistory = useCallback(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      const dataURL = canvas.toDataURL();
      const newHistory = history.slice(0, historyIndex + 1);
      newHistory.push(dataURL);
      setHistory(newHistory);
      setHistoryIndex(newHistory.length - 1);
    }
  }, [history, historyIndex]);

  // Draw grid
  const drawGrid = useCallback((ctx) => {
    if (!showGrid) return;
    
    ctx.save();
    ctx.strokeStyle = '#E5E7EB';
    ctx.lineWidth = 0.5;
    
    for (let x = 0; x <= 600; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, 600);
      ctx.stroke();
    }
    
    for (let y = 0; y <= 600; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(600, y);
      ctx.stroke();
    }
    
    ctx.restore();
  }, [showGrid, gridSize]);

  // Snap point to grid
  const snapToGridPoint = useCallback((x, y) => {
    if (!snapToGrid) return { x, y };
    
    const snappedX = Math.round(x / gridSize) * gridSize;
    const snappedY = Math.round(y / gridSize) * gridSize;
    return { x: snappedX, y: snappedY };
  }, [snapToGrid, gridSize]);

  const startDrawing = (e) => {
    setIsDrawing(true);
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    let x = e.clientX - rect.left;
    let y = e.clientY - rect.top;
    
    // Snap to grid if enabled
    const snapped = snapToGridPoint(x, y);
    x = snapped.x;
    y = snapped.y;
    
    setStartPoint({ x, y });
    
    const ctx = canvas.getContext('2d');
    ctx.strokeStyle = currentColor;
    ctx.lineWidth = brushSize;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    
    // Save state before drawing
    saveToHistory();
    
    if (currentTool === 'pen' || currentTool === 'spray') {
      ctx.beginPath();
      ctx.moveTo(x, y);
    } else if (currentTool === 'eraser') {
      ctx.globalCompositeOperation = 'destination-out';
      ctx.beginPath();
      ctx.moveTo(x, y);
    }
  };

  const draw = (e) => {
    if (!isDrawing) return;
    
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    let x = e.clientX - rect.left;
    let y = e.clientY - rect.top;
    
    // Snap to grid if enabled
    const snapped = snapToGridPoint(x, y);
    x = snapped.x;
    y = snapped.y;
    
    const ctx = canvas.getContext('2d');
    
    if (currentTool === 'pen' || currentTool === 'eraser') {
      ctx.lineTo(x, y);
      ctx.stroke();
    } else if (currentTool === 'spray') {
      // Spray effect
      for (let i = 0; i < 5; i++) {
        const offsetX = (Math.random() - 0.5) * brushSize;
        const offsetY = (Math.random() - 0.5) * brushSize;
        ctx.beginPath();
        ctx.arc(x + offsetX, y + offsetY, 1, 0, 2 * Math.PI);
        ctx.fill();
      }
    }
  };

  const stopDrawing = () => {
    if (!isDrawing) return;
    
    setIsDrawing(false);
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Reset composite operation
    ctx.globalCompositeOperation = 'source-over';
    
    // Draw shapes if applicable
    if (startPoint && currentTool !== 'pen' && currentTool !== 'eraser' && currentTool !== 'spray') {
      const rect = canvas.getBoundingClientRect();
      const endX = startPoint.x;
      const endY = startPoint.y;
      
      ctx.beginPath();
      
      switch (currentTool) {
        case 'line':
          ctx.moveTo(startPoint.x, startPoint.y);
          ctx.lineTo(endX, endY);
          ctx.stroke();
          break;
        case 'circle':
          const radius = Math.sqrt(Math.pow(endX - startPoint.x, 2) + Math.pow(endY - startPoint.y, 2));
          ctx.arc(startPoint.x, startPoint.y, radius, 0, 2 * Math.PI);
          ctx.stroke();
          break;
        case 'square':
          const width = endX - startPoint.x;
          const height = endY - startPoint.y;
          ctx.rect(startPoint.x, startPoint.y, width, height);
          ctx.stroke();
          break;
      }
    }
    
    setStartPoint(null);
    
    const dataURL = canvas.toDataURL();
    setPatternData(dataURL);
    onPatternChange && onPatternChange(dataURL);
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Redraw grid if enabled
    if (showGrid) {
      drawGrid(ctx);
    }
    
    setPatternData(null);
    saveToHistory();
  };

  // Undo functionality
  const undo = () => {
    if (historyIndex > 0) {
      const newIndex = historyIndex - 1;
      setHistoryIndex(newIndex);
      
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      const img = new Image();
      img.onload = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0);
        
        // Redraw grid if enabled
        if (showGrid) {
          drawGrid(ctx);
        }
      };
      img.src = history[newIndex];
    }
  };

  // Redo functionality
  const redo = () => {
    if (historyIndex < history.length - 1) {
      const newIndex = historyIndex + 1;
      setHistoryIndex(newIndex);
      
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      const img = new Image();
      img.onload = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0);
        
        // Redraw grid if enabled
        if (showGrid) {
          drawGrid(ctx);
        }
      };
      img.src = history[newIndex];
    }
  };

  const downloadPattern = () => {
    const canvas = canvasRef.current;
    const link = document.createElement('a');
    link.download = 'kolam-pattern.png';
    link.href = canvas.toDataURL();
    link.click();
    toast.success('Pattern downloaded successfully!');
  };

  const analyzePattern = async () => {
    if (!patternData) {
      toast.error('Please create a pattern first!');
      return;
    }

    setIsAnalyzing(true);
    try {
      const response = await axios.post('http://localhost:5000/api/analyze', {
        image: patternData
      }, { timeout: 30000 });
      
      if (response.data.success) {
        const analysisResults = response.data.analysis;
        setAnalysisResults(analysisResults);
        onAnalysisComplete && onAnalysisComplete(analysisResults);
        toast.success('Pattern analyzed successfully!');
      } else {
        throw new Error(response.data.message || 'Analysis failed');
      }
    } catch (error) {
      console.error('Analysis error:', error);
      toast.error('Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Save pattern
  const savePattern = () => {
    if (!patternData) {
      toast.error('No pattern to save!');
      return;
    }

    const patternName = prompt('Enter pattern name:');
    if (patternName) {
      const newPattern = {
        id: Date.now(),
        name: patternName,
        data: patternData,
        timestamp: new Date().toISOString(),
        analysis: analysisResults
      };
      
      const updatedPatterns = [...savedPatterns, newPattern];
      setSavedPatterns(updatedPatterns);
      localStorage.setItem('savedPatterns', JSON.stringify(updatedPatterns));
      toast.success('Pattern saved successfully!');
    }
  };

  // Load pattern
  const loadPattern = (pattern) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const img = new Image();
    
    img.onload = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0);
      
      // Redraw grid if enabled
      if (showGrid) {
        drawGrid(ctx);
      }
      
      setPatternData(pattern.data);
      setAnalysisResults(pattern.analysis);
      onPatternChange && onPatternChange(pattern.data);
      toast.success(`Loaded pattern: ${pattern.name}`);
    };
    
    img.src = pattern.data;
  };

  const loadTemplate = (templateType) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw template based on type
    ctx.strokeStyle = currentColor;
    ctx.lineWidth = brushSize;
    ctx.fillStyle = currentColor;
    
    switch (templateType) {
      case 'grid':
        drawGridTemplate(ctx);
        break;
      case 'radial':
        drawRadialPattern(ctx);
        break;
      case 'bilateral':
        drawBilateralPattern(ctx);
        break;
      case 'floral':
        drawFloralPattern(ctx);
        break;
      case 'sikku':
        drawSikkuPattern(ctx);
        break;
      case 'fractal':
        drawFractalPattern(ctx);
        break;
      case 'festival':
        drawFestivalPattern(ctx);
        break;
      case 'geometric':
        drawGeometricPattern(ctx);
        break;
    }
    
    // Redraw grid if enabled
    if (showGrid) {
      drawGrid(ctx);
    }
    
    const dataURL = canvas.toDataURL();
    setPatternData(dataURL);
    onPatternChange && onPatternChange(dataURL);
    saveToHistory();
  };

  const drawGridTemplate = (ctx) => {
    const spacing = 50;
    for (let x = 0; x < 600; x += spacing) {
      for (let y = 0; y < 600; y += spacing) {
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, 2 * Math.PI);
        ctx.fill();
      }
    }
  };

  const drawRadialPattern = (ctx) => {
    const centerX = 300;
    const centerY = 300;
    const radius = 200;
    
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.stroke();
    
    for (let i = 0; i < 8; i++) {
      const angle = (i * Math.PI) / 4;
      const x = centerX + radius * Math.cos(angle);
      const y = centerY + radius * Math.sin(angle);
      
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(x, y);
      ctx.stroke();
    }
  };

  const drawBilateralPattern = (ctx) => {
    const centerX = 300;
    const centerY = 300;
    
    // Draw symmetric pattern
    ctx.beginPath();
    ctx.arc(centerX - 100, centerY, 50, 0, 2 * Math.PI);
    ctx.stroke();
    
    ctx.beginPath();
    ctx.arc(centerX + 100, centerY, 50, 0, 2 * Math.PI);
    ctx.stroke();
    
    ctx.beginPath();
    ctx.moveTo(centerX - 100, centerY);
    ctx.lineTo(centerX + 100, centerY);
    ctx.stroke();
  };

  const drawFractalPattern = (ctx) => {
    const centerX = 300;
    const centerY = 300;
    
    // Draw simple fractal pattern
    for (let i = 0; i < 4; i++) {
      const angle = (i * Math.PI) / 2;
      const x = centerX + 100 * Math.cos(angle);
      const y = centerY + 100 * Math.sin(angle);
      
      ctx.beginPath();
      ctx.arc(x, y, 30, 0, 2 * Math.PI);
      ctx.stroke();
    }
  };

  const drawFloralPattern = (ctx) => {
    const centerX = 300;
    const centerY = 300;
    
    // Draw floral pattern with petals
    for (let i = 0; i < 8; i++) {
      const angle = (i * Math.PI) / 4;
      const x = centerX + 120 * Math.cos(angle);
      const y = centerY + 120 * Math.sin(angle);
      
      // Draw petal
      ctx.beginPath();
      ctx.ellipse(x, y, 40, 20, angle, 0, 2 * Math.PI);
      ctx.stroke();
      
      // Draw center circle
      ctx.beginPath();
      ctx.arc(centerX, centerY, 30, 0, 2 * Math.PI);
      ctx.stroke();
    }
  };

  const drawSikkuPattern = (ctx) => {
    const centerX = 300;
    const centerY = 300;
    
    // Draw Sikku Kolam (continuous line pattern)
    ctx.beginPath();
    ctx.moveTo(centerX - 100, centerY - 100);
    ctx.lineTo(centerX + 100, centerY - 100);
    ctx.lineTo(centerX + 100, centerY + 100);
    ctx.lineTo(centerX - 100, centerY + 100);
    ctx.lineTo(centerX - 100, centerY - 100);
    
    // Inner square
    ctx.moveTo(centerX - 50, centerY - 50);
    ctx.lineTo(centerX + 50, centerY - 50);
    ctx.lineTo(centerX + 50, centerY + 50);
    ctx.lineTo(centerX - 50, centerY + 50);
    ctx.lineTo(centerX - 50, centerY - 50);
    
    // Diagonal lines
    ctx.moveTo(centerX - 100, centerY - 100);
    ctx.lineTo(centerX + 100, centerY + 100);
    ctx.moveTo(centerX + 100, centerY - 100);
    ctx.lineTo(centerX - 100, centerY + 100);
    
    ctx.stroke();
  };

  const drawFestivalPattern = (ctx) => {
    const centerX = 300;
    const centerY = 300;
    
    // Draw festival pattern with multiple circles and decorations
    for (let r = 50; r <= 150; r += 25) {
      ctx.beginPath();
      ctx.arc(centerX, centerY, r, 0, 2 * Math.PI);
      ctx.stroke();
    }
    
    // Draw decorative elements
    for (let i = 0; i < 12; i++) {
      const angle = (i * Math.PI) / 6;
      const x = centerX + 180 * Math.cos(angle);
      const y = centerY + 180 * Math.sin(angle);
      
      ctx.beginPath();
      ctx.arc(x, y, 15, 0, 2 * Math.PI);
      ctx.fill();
    }
  };

  const drawGeometricPattern = (ctx) => {
    const centerX = 300;
    const centerY = 300;
    
    // Draw geometric Kerala pattern
    const size = 80;
    
    // Outer square
    ctx.beginPath();
    ctx.rect(centerX - size, centerY - size, size * 2, size * 2);
    ctx.stroke();
    
    // Inner diamond
    ctx.beginPath();
    ctx.moveTo(centerX, centerY - size);
    ctx.lineTo(centerX + size, centerY);
    ctx.lineTo(centerX, centerY + size);
    ctx.lineTo(centerX - size, centerY);
    ctx.closePath();
    ctx.stroke();
    
    // Center circle
    ctx.beginPath();
    ctx.arc(centerX, centerY, size / 2, 0, 2 * Math.PI);
    ctx.stroke();
    
    // Corner decorations
    const corners = [
      { x: centerX - size, y: centerY - size },
      { x: centerX + size, y: centerY - size },
      { x: centerX + size, y: centerY + size },
      { x: centerX - size, y: centerY + size }
    ];
    
    corners.forEach(corner => {
      ctx.beginPath();
      ctx.arc(corner.x, corner.y, 20, 0, 2 * Math.PI);
      ctx.stroke();
    });
  };

  return (
    <StudioContainer>
      <div className="container">
        <StudioHeader>
          <Title>
            <FaPalette />
            Kolam Studio
          </Title>
          <Toolbar>
            <ToolButton onClick={undo} disabled={historyIndex <= 0}>
              <FaUndo />
              Undo
            </ToolButton>
            <ToolButton onClick={redo} disabled={historyIndex >= history.length - 1}>
              <FaRedo />
              Redo
            </ToolButton>
            <ToolButton onClick={clearCanvas}>
              <FaStop />
              Clear
            </ToolButton>
            <ToolButton onClick={savePattern}>
              <FaSave />
              Save
            </ToolButton>
            <ToolButton onClick={() => setShowPatternGallery(!showPatternGallery)}>
              <FaFolderOpen />
              Gallery
            </ToolButton>
            <ToolButton onClick={loadPatternsFromGallery}>
              <FaUpload />
              Load Gallery
            </ToolButton>
            <ToolButton onClick={downloadPattern}>
              <FaDownload />
              Download
            </ToolButton>
            <ToolButton 
              onClick={analyzePattern} 
              className="btn-primary"
              disabled={isAnalyzing}
            >
              <FaMagic />
              {isAnalyzing ? 'Analyzing...' : 'Analyze'}
            </ToolButton>
          </Toolbar>
        </StudioHeader>

        <StudioContent>
          <SidebarPanel>
            <SidebarTitle>
              <FaCircle />
              Drawing Tools
            </SidebarTitle>
            
            <ToolGroup>
              <ToolGroupTitle>Drawing Tools</ToolGroupTitle>
              <ToolGrid>
                {tools.filter(tool => tool.category === 'drawing').map(tool => (
                  <ToolItem
                    key={tool.id}
                    active={currentTool === tool.id}
                    onClick={() => setCurrentTool(tool.id)}
                  >
                    <tool.icon />
                    <span>{tool.label}</span>
                  </ToolItem>
                ))}
              </ToolGrid>
            </ToolGroup>

            <ToolGroup>
              <ToolGroupTitle>Shapes</ToolGroupTitle>
              <ToolGrid>
                {tools.filter(tool => tool.category === 'shapes').map(tool => (
                  <ToolItem
                    key={tool.id}
                    active={currentTool === tool.id}
                    onClick={() => setCurrentTool(tool.id)}
                  >
                    <tool.icon />
                    <span>{tool.label}</span>
                  </ToolItem>
                ))}
              </ToolGrid>
            </ToolGroup>

            <ToolGroup>
              <ToolGroupTitle>Other Tools</ToolGroupTitle>
              <ToolGrid>
                {tools.filter(tool => tool.category === 'tools').map(tool => (
                  <ToolItem
                    key={tool.id}
                    active={currentTool === tool.id}
                    onClick={() => setCurrentTool(tool.id)}
                  >
                    <tool.icon />
                    <span>{tool.label}</span>
                  </ToolItem>
                ))}
              </ToolGrid>
            </ToolGroup>

            <ToolGroup>
              <ToolGroupTitle>Properties</ToolGroupTitle>
              <PropertyGroup>
                <PropertyLabel>Brush Size</PropertyLabel>
                <PropertyInput
                  type="range"
                  min="1"
                  max="20"
                  value={brushSize}
                  onChange={(e) => setBrushSize(parseInt(e.target.value))}
                />
                <div style={{textAlign: 'center', fontSize: '0.75rem', color: '#6B7280'}}>
                  {brushSize}px
                </div>
              </PropertyGroup>

              <PropertyGroup>
                <PropertyLabel>Color</PropertyLabel>
                <ToolButton
                  onClick={() => setShowColorPicker(!showColorPicker)}
                  style={{width: '100%', justifyContent: 'center'}}
                >
                  <div style={{
                    width: '20px',
                    height: '20px',
                    backgroundColor: currentColor,
                    borderRadius: '50%',
                    border: '2px solid white',
                    boxShadow: '0 0 0 1px #E5E7EB'
                  }} />
                  Choose Color
                </ToolButton>
              </PropertyGroup>

              <PropertyGroup>
                <PropertyLabel>Symmetry</PropertyLabel>
                <PropertySelect
                  value={symmetryType}
                  onChange={(e) => {
                    setSymmetryType(e.target.value);
                    setShowSymmetryGuide(e.target.value !== 'none');
                  }}
                >
                  {symmetryTypes.map(type => (
                    <option key={type.value} value={type.value}>
                      {type.label}
                    </option>
                  ))}
                </PropertySelect>
              </PropertyGroup>

              <PropertyGroup>
                <PropertyLabel>Grid Settings</PropertyLabel>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                  <input
                    type="checkbox"
                    checked={showGrid}
                    onChange={(e) => setShowGrid(e.target.checked)}
                  />
                  <span style={{ fontSize: '0.875rem' }}>Show Grid</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                  <input
                    type="checkbox"
                    checked={snapToGrid}
                    onChange={(e) => setSnapToGrid(e.target.checked)}
                  />
                  <span style={{ fontSize: '0.875rem' }}>Snap to Grid</span>
                </div>
                <PropertyLabel>Grid Size</PropertyLabel>
                <PropertyInput
                  type="range"
                  min="10"
                  max="50"
                  value={gridSize}
                  onChange={(e) => setGridSize(parseInt(e.target.value))}
                />
                <div style={{textAlign: 'center', fontSize: '0.75rem', color: '#6B7280'}}>
                  {gridSize}px
                </div>
              </PropertyGroup>
            </ToolGroup>

            <ToolGroup>
              <ToolGroupTitle>Pattern Templates</ToolGroupTitle>
              <PatternTemplates>
                {patternTemplates.map(template => (
                  <TemplateButton
                    key={template.type}
                    onClick={() => loadTemplate(template.type)}
                    title={`${template.name} - ${template.region}`}
                  >
                    <div style={{ fontSize: '0.75rem', fontWeight: '500' }}>
                      {template.name}
                    </div>
                    <div style={{ fontSize: '0.65rem', color: '#6B7280' }}>
                      {template.region}
                    </div>
                  </TemplateButton>
                ))}
              </PatternTemplates>
            </ToolGroup>
          </SidebarPanel>

          <CanvasContainer>
            <Canvas
              ref={canvasRef}
              onMouseDown={startDrawing}
              onMouseMove={draw}
              onMouseUp={stopDrawing}
              onMouseLeave={stopDrawing}
            />
            <SymmetryGuide show={showSymmetryGuide && symmetryType === 'vertical'} />
            <SymmetryGuideHorizontal show={showSymmetryGuide && symmetryType === 'horizontal'} />
            
            <CanvasControls>
              <ToolButton onClick={() => setShowColorPicker(!showColorPicker)}>
                <div style={{
                  width: '20px',
                  height: '20px',
                  backgroundColor: currentColor,
                  borderRadius: '50%',
                  border: '2px solid white',
                  boxShadow: '0 0 0 1px #E5E7EB'
                }} />
                Color
              </ToolButton>
            </CanvasControls>

            {showColorPicker && (
              <ColorPicker>
                <ChromePicker
                  color={currentColor}
                  onChange={(color) => setCurrentColor(color.hex)}
                />
              </ColorPicker>
            )}
          </CanvasContainer>

          <PropertiesPanel>
            <SidebarTitle>
              <FaMagic />
              Pattern Properties
            </SidebarTitle>
            
            <PropertyGroup>
              <PropertyLabel>Current Tool</PropertyLabel>
              <div style={{
                padding: '0.75rem',
                background: '#F3F4F6',
                borderRadius: '0.5rem',
                textAlign: 'center',
                fontWeight: '500'
              }}>
                {tools.find(t => t.id === currentTool)?.label}
              </div>
            </PropertyGroup>

            <PropertyGroup>
              <PropertyLabel>Canvas Size</PropertyLabel>
              <div style={{
                padding: '0.75rem',
                background: '#F3F4F6',
                borderRadius: '0.5rem',
                textAlign: 'center',
                fontSize: '0.875rem'
              }}>
                600 × 600 pixels
              </div>
            </PropertyGroup>

            <PropertyGroup>
              <PropertyLabel>Symmetry Guide</PropertyLabel>
              <div style={{
                padding: '0.75rem',
                background: '#F3F4F6',
                borderRadius: '0.5rem',
                textAlign: 'center',
                fontSize: '0.875rem'
              }}>
                {symmetryType === 'none' ? 'Disabled' : symmetryTypes.find(s => s.value === symmetryType)?.label}
              </div>
            </PropertyGroup>

            {patternData && (
              <PropertyGroup>
                <PropertyLabel>Pattern Status</PropertyLabel>
                <div style={{
                  padding: '0.75rem',
                  background: '#D1FAE5',
                  borderRadius: '0.5rem',
                  textAlign: 'center',
                  fontSize: '0.875rem',
                  color: '#065F46',
                  fontWeight: '500'
                }}>
                  ✓ Pattern Created
                </div>
              </PropertyGroup>
            )}

            {analysisResults && (
              <PropertyGroup>
                <PropertyLabel>Analysis Results</PropertyLabel>
                <div style={{
                  padding: '0.75rem',
                  background: '#F3F4F6',
                  borderRadius: '0.5rem',
                  fontSize: '0.875rem'
                }}>
                  <div style={{ marginBottom: '0.5rem' }}>
                    <strong>Symmetry:</strong> {analysisResults.symmetry_type}
                  </div>
                  <div style={{ marginBottom: '0.5rem' }}>
                    <strong>Complexity:</strong> {analysisResults.complexity}
                  </div>
                  <div style={{ marginBottom: '0.5rem' }}>
                    <strong>Fractal Dimension:</strong> {analysisResults.fractal_dimension}
                  </div>
                  <div style={{ marginBottom: '0.5rem' }}>
                    <strong>Region:</strong> {analysisResults.cultural_region}
                  </div>
                  <div style={{ marginBottom: '0.5rem' }}>
                    <strong>Confidence:</strong> {(analysisResults.confidence * 100).toFixed(1)}%
                  </div>
                </div>
              </PropertyGroup>
            )}

            {showPatternGallery && savedPatterns.length > 0 && (
              <PropertyGroup>
                <PropertyLabel>Pattern Gallery</PropertyLabel>
                <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
                  {savedPatterns.map(pattern => (
                    <div
                      key={pattern.id}
                      style={{
                        padding: '0.75rem',
                        border: '1px solid #E5E7EB',
                        borderRadius: '0.5rem',
                        marginBottom: '0.75rem',
                        cursor: 'pointer',
                        fontSize: '0.875rem',
                        transition: 'all 0.2s ease'
                      }}
                      onClick={() => pattern.data ? loadPattern(pattern) : null}
                      onMouseEnter={(e) => {
                        e.target.style.borderColor = '#8B5CF6';
                        e.target.style.backgroundColor = '#F3F4F6';
                      }}
                      onMouseLeave={(e) => {
                        e.target.style.borderColor = '#E5E7EB';
                        e.target.style.backgroundColor = 'white';
                      }}
                    >
                      <div style={{ fontWeight: '500', marginBottom: '0.25rem' }}>
                        {pattern.name}
                      </div>
                      {pattern.region && (
                        <div style={{ color: '#8B5CF6', fontSize: '0.75rem', marginBottom: '0.25rem' }}>
                          {pattern.region}
                        </div>
                      )}
                      {pattern.complexity && (
                        <div style={{ color: '#6B7280', fontSize: '0.75rem', marginBottom: '0.25rem' }}>
                          Complexity: {pattern.complexity}
                        </div>
                      )}
                      {pattern.timestamp && (
                        <div style={{ color: '#6B7280', fontSize: '0.75rem' }}>
                          {new Date(pattern.timestamp).toLocaleDateString()}
                        </div>
                      )}
                      {pattern.description && (
                        <div style={{ color: '#6B7280', fontSize: '0.75rem', marginTop: '0.25rem' }}>
                          {pattern.description}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </PropertyGroup>
            )}
          </PropertiesPanel>
        </StudioContent>
      </div>
    </StudioContainer>
  );
}

export default KolamStudio;
