import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import { 
  FaPlay, FaStop, FaDownload, FaUndo, FaRedo, FaMagic, FaRuler, 
  FaCircle, FaSquare, FaPalette, FaEraser, FaImage, FaSprayCan,
  FaVectorSquare, FaFolderOpen, FaCog, FaInfoCircle
} from 'react-icons/fa';
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

const PatternPreview = styled.div`
  width: 100%;
  height: 150px;
  background: ${ds.colors.neutral[100]};
  border-radius: ${ds.borderRadius.lg};
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed ${ds.colors.neutral[300]};
  margin-top: ${ds.spacing[3]};
  position: relative;
  overflow: hidden;
  
  svg {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
`;

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

  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      canvas.width = 600;
      canvas.height = 400;
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = 'white';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      saveToHistory();
    }
    
    // Load available patterns from backend
    loadAvailablePatterns();
  }, []);

  const loadAvailablePatterns = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/patterns');
      if (response.data.success) {
        setAvailablePatterns(response.data.patterns);
      }
    } catch (error) {
      console.error('Failed to load patterns:', error);
    }
  };

  const saveToHistory = () => {
    const canvas = canvasRef.current;
    if (canvas) {
      const imageData = canvas.toDataURL();
      const newHistory = canvasHistory.slice(0, historyIndex + 1);
      newHistory.push(imageData);
      setCanvasHistory(newHistory);
      setHistoryIndex(newHistory.length - 1);
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
    const canvas = canvasRef.current;
    const imageData = canvas.toDataURL();
    
    setIsAdvancedAnalyzing(true);
    try {
      const response = await axios.post('http://localhost:5000/api/advanced-analysis', {
        image: imageData,
        mode: 'deep'
      }, { timeout: 60000 });

      if (response.data.success) {
        setAdvancedAnalysis(response.data.advanced_analysis);
        toast.success('Advanced analysis completed!');
        
        // Show processing steps
        if (response.data.processing_steps) {
          response.data.processing_steps.forEach((step, index) => {
            setTimeout(() => {
              toast.info(step, { autoClose: 2000 });
            }, index * 500);
          });
        }
      } else {
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

  const generateCulturalPattern = async () => {
    setIsGenerating(true);
    try {
      const response = await axios.post('http://localhost:5000/api/generate-cultural', {
        region: selectedRegion,
        grid_size: 5,
        use_colors: true
      }, { timeout: 10000 });

      if (response.data.success) {
        setGeneratedPattern(response.data.pattern);
        drawGeneratedPattern(response.data.pattern);
        toast.success(`${selectedRegion} pattern generated!`);
        
        // Perform cultural analysis on generated pattern
        performCulturalAnalysis(response.data.pattern);
      } else {
        toast.error('Pattern generation failed');
      }
    } catch (error) {
      console.error('Generation error:', error);
      toast.error('Pattern generation failed');
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

  const loadPatternTemplate = async (patternId) => {
    try {
      // Generate pattern based on template
      const template = availablePatterns.find(p => p.id === patternId);
      if (template) {
        const response = await axios.post('http://localhost:5000/api/generate', {
          type: template.type,
          grid_size: [5, 5],
          symmetry_type: template.type
        }, { timeout: 10000 });

        if (response.data.success) {
          setGeneratedPattern(response.data.pattern);
          drawGeneratedPatternFromTemplate(response.data.pattern);
          toast.success(`${template.name} loaded!`);
        }
      }
    } catch (error) {
      console.error('Template loading error:', error);
      toast.error('Failed to load template');
    }
  };

  const generateFestivalPattern = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/generate-festival', {
        festival: selectedFestival,
        region: selectedRegion,
        grid_size: 5
      }, { timeout: 10000 });

      if (response.data.success) {
        setGeneratedPattern(response.data.pattern);
        drawGeneratedPattern(response.data.pattern);
        toast.success(`${selectedFestival} festival pattern generated!`);
      } else {
        toast.error('Festival pattern generation failed');
      }
    } catch (error) {
      console.error('Festival generation error:', error);
      toast.error('Festival pattern generation failed');
    }
  };

  const drawGeneratedPattern = (pattern) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw dots
    if (pattern.dots) {
      pattern.dots.forEach((dot, index) => {
        const color = pattern.colors ? pattern.colors[index % pattern.colors.length] : '#DC143C';
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(dot[0], dot[1], 4, 0, 2 * Math.PI);
        ctx.fill();
      });
    }
    
    // Draw paths
    if (pattern.paths) {
      pattern.paths.forEach((path, index) => {
        if (path.length < 2) return;
        
        const color = pattern.colors ? pattern.colors[index % pattern.colors.length] : '#DC143C';
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        
        ctx.beginPath();
        ctx.moveTo(path[0][0], path[0][1]);
        
        for (let i = 1; i < path.length; i++) {
          ctx.lineTo(path[i][0], path[i][1]);
        }
        
        ctx.stroke();
      });
    }
    
    saveToHistory();
  };

  const drawGeneratedPatternFromTemplate = (pattern) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw template-based pattern
    if (pattern.points) {
      // Draw points
      pattern.points.forEach((point) => {
        ctx.fillStyle = point.is_center ? '#FF6B35' : '#DC143C';
        ctx.beginPath();
        ctx.arc(point.x, point.y, point.is_center ? 6 : 4, 0, 2 * Math.PI);
        ctx.fill();
      });
      
      // Draw lines connecting points
      if (pattern.lines) {
        ctx.strokeStyle = '#DC143C';
        ctx.lineWidth = 2;
        ctx.lineCap = 'round';
        
        pattern.lines.forEach((line) => {
          const [startIdx, endIdx] = line;
          if (startIdx < pattern.points.length && endIdx < pattern.points.length) {
            const startPoint = pattern.points[startIdx];
            const endPoint = pattern.points[endIdx];
            
            ctx.beginPath();
            ctx.moveTo(startPoint.x, startPoint.y);
            ctx.lineTo(endPoint.x, endPoint.y);
            ctx.stroke();
          }
        });
      }
    }
    
    saveToHistory();
  };

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
                  
                  {advancedAnalysis.recommendations && (
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
