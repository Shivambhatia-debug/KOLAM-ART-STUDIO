import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import { FaPlay, FaStop, FaDownload, FaMagic, FaSpinner } from 'react-icons/fa';
import { toast } from 'react-toastify';
import axios from 'axios';
import { professionalDesignSystem as ds } from '../styles/ProfessionalDesignSystem';
import ProfessionalButton from './ui/ProfessionalButton';
import ProfessionalCard from './ui/ProfessionalCard';

const SpiralContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${ds.spacing[6]};
  max-width: 1200px;
  margin: 0 auto;
  padding: ${ds.spacing[6]};
`;

const ControlsSection = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: ${ds.spacing[4]};
`;

const CanvasSection = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: ${ds.spacing[4]};
`;

const CanvasContainer = styled.div`
  background: white;
  border-radius: ${ds.borderRadius.xl};
  padding: ${ds.spacing[6]};
  box-shadow: ${ds.boxShadow.lg};
  border: 2px solid ${ds.colors.neutral[200]};
  position: relative;
  overflow: hidden;
`;

const Canvas = styled.canvas`
  border: 2px solid ${ds.colors.neutral[300]};
  border-radius: ${ds.borderRadius.lg};
  background: black;
  display: block;
  cursor: crosshair;
  
  &:hover {
    border-color: ${ds.colors.primary[400]};
  }
`;

const ControlGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${ds.spacing[2]};
`;

const Label = styled.label`
  font-weight: ${ds.typography.fontWeight.medium};
  color: ${ds.colors.neutral[700]};
  font-size: ${ds.typography.fontSize.sm[0]};
`;

const Input = styled.input`
  padding: ${ds.spacing[3]};
  border: 2px solid ${ds.colors.neutral[300]};
  border-radius: ${ds.borderRadius.lg};
  font-family: ${ds.typography.fontFamily.primary.join(', ')};
  font-size: ${ds.typography.fontSize.sm[0]};
  transition: all ${ds.animation.duration.fast} ${ds.animation.easing.easeInOut};
  
  &:focus {
    outline: none;
    border-color: ${ds.colors.primary[400]};
    box-shadow: 0 0 0 3px rgba(255, 193, 7, 0.1);
  }
`;

const RangeInput = styled(Input)`
  width: 100%;
  height: 6px;
  background: ${ds.colors.neutral[200]};
  border: none;
  border-radius: 3px;
  outline: none;
  cursor: pointer;
  
  &::-webkit-slider-thumb {
    appearance: none;
    width: 20px;
    height: 20px;
    background: ${ds.colors.primary[500]};
    border-radius: 50%;
    cursor: pointer;
    box-shadow: ${ds.boxShadow.sm};
  }
  
  &::-moz-range-thumb {
    width: 20px;
    height: 20px;
    background: ${ds.colors.primary[500]};
    border-radius: 50%;
    cursor: pointer;
    border: none;
    box-shadow: ${ds.boxShadow.sm};
  }
`;

// const AnimationControls = styled.div`
//   display: flex;
//   gap: ${ds.spacing[3]};
//   align-items: center;
//   justify-content: center;
//   flex-wrap: wrap;
// `;

const PatternInfo = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: ${ds.spacing[4]};
  margin-top: ${ds.spacing[4]};
`;

const InfoItem = styled.div`
  background: ${ds.colors.neutral[50]};
  padding: ${ds.spacing[4]};
  border-radius: ${ds.borderRadius.lg};
  border-left: 4px solid ${ds.colors.primary[500]};
`;

const InfoLabel = styled.div`
  font-weight: ${ds.typography.fontWeight.medium};
  color: ${ds.colors.neutral[600]};
  font-size: ${ds.typography.fontSize.sm[0]};
  margin-bottom: ${ds.spacing[1]};
`;

const InfoValue = styled.div`
  font-weight: ${ds.typography.fontWeight.bold};
  color: ${ds.colors.neutral[900]};
  font-size: ${ds.typography.fontSize.lg[0]};
`;

const LoadingOverlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: ${ds.borderRadius.lg};
  color: white;
  font-size: ${ds.typography.fontSize.lg[0]};
  font-weight: ${ds.typography.fontWeight.medium};
`;

const SpiralKolamGenerator = () => {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);
  
  // Pattern parameters
  const [turns, setTurns] = useState(6);
  const [stepAngle, setStepAngle] = useState(15);
  const [stepLength, setStepLength] = useState(8);
  const [animationSpeed, setAnimationSpeed] = useState(50);
  
  // State management
  const [isGenerating, setIsGenerating] = useState(false);
  const [isAnimating, setIsAnimating] = useState(false);
  const [patternData, setPatternData] = useState(null);
  const [generationTime, setGenerationTime] = useState(0);
  
  // Initialize canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      canvas.width = 800;
      canvas.height = 600;
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = 'black';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
  }, []);

  // Generate spiral pattern from backend
  const generateSpiralPattern = async () => {
    setIsGenerating(true);
    try {
      // const startTime = Date.now();
      
      const response = await axios.post('/api/generate-spiral-kolam', {
        turns,
        step_angle: stepAngle,
        step_length: stepLength,
        animation: true
      });

      if (response.data.success) {
        setPatternData(response.data.pattern);
        setGenerationTime(response.data.generation_time);
        drawSpiralPattern(response.data.pattern);
        toast.success('Spiral Kolam generated successfully!');
      } else {
        toast.error('Failed to generate pattern');
      }
    } catch (error) {
      console.error('Generation error:', error);
      toast.error('Failed to generate pattern: ' + error.message);
    } finally {
      setIsGenerating(false);
    }
  };

  // Draw spiral pattern on canvas
  const drawSpiralPattern = (pattern) => {
    const canvas = canvasRef.current;
    if (!canvas || !pattern) return;

    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    
    const metadata = pattern.metadata;
    const totalSteps = metadata.total_steps;
    
    // Draw spiral
    ctx.strokeStyle = metadata.colors.spiral;
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.beginPath();
    
    let x = centerX;
    let y = centerY;
    let angle = 0;
    
    for (let i = 0; i < totalSteps; i++) {
      ctx.lineTo(x, y);
      
      // Move forward
      x += Math.cos(angle * Math.PI / 180) * metadata.step_length;
      y += Math.sin(angle * Math.PI / 180) * metadata.step_length;
      angle += metadata.step_angle;
      
      // Draw dotted squares every 15 steps
      if (i % 15 === 0 && i > 5) {
        drawDottedSquare(ctx, x, y, 15, 3);
      }
    }
    
    ctx.stroke();
  };

  // Draw dotted square
  const drawDottedSquare = (ctx, x, y, size, dots) => {
    ctx.fillStyle = 'white';
    const dotSize = 3;
    const step = size / dots;
    
    // Draw square with dots
    for (let side = 0; side < 4; side++) {
      for (let i = 0; i < dots; i++) {
        const dotX = x + Math.cos(side * Math.PI / 2) * (i * step);
        const dotY = y + Math.sin(side * Math.PI / 2) * (i * step);
        
        ctx.beginPath();
        ctx.arc(dotX, dotY, dotSize, 0, 2 * Math.PI);
        ctx.fill();
      }
    }
  };

  // Animate pattern generation
  const animatePattern = async () => {
    if (!patternData) {
      toast.error('Please generate a pattern first!');
      return;
    }

    setIsAnimating(true);
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const metadata = patternData.metadata;
    const totalSteps = metadata.total_steps;
    
    // Animate spiral drawing
    ctx.strokeStyle = metadata.colors.spiral;
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    
    let x = centerX;
    let y = centerY;
    let angle = 0;
    
    for (let i = 0; i < totalSteps; i++) {
      // Draw current segment
      ctx.beginPath();
      ctx.moveTo(x, y);
      
      const nextX = x + Math.cos(angle * Math.PI / 180) * metadata.step_length;
      const nextY = y + Math.sin(angle * Math.PI / 180) * metadata.step_length;
      
      ctx.lineTo(nextX, nextY);
      ctx.stroke();
      
      // Update position
      x = nextX;
      y = nextY;
      angle += metadata.step_angle;
      
      // Draw dotted squares
      if (i % 15 === 0 && i > 5) {
        drawDottedSquare(ctx, x, y, 15, 3);
      }
      
      // Animation delay
      await new Promise(resolve => setTimeout(resolve, animationSpeed));
    }
    
    setIsAnimating(false);
  };

  // Stop animation
  const stopAnimation = () => {
    setIsAnimating(false);
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }
  };

  // Download pattern
  const downloadPattern = () => {
    const canvas = canvasRef.current;
    const link = document.createElement('a');
    link.download = `spiral-kolam-${Date.now()}.png`;
    link.href = canvas.toDataURL();
    link.click();
    toast.success('Pattern downloaded!');
  };

  return (
    <SpiralContainer>
      <ProfessionalCard variant="elevated">
        <ProfessionalCard.Header>
          <ProfessionalCard.Title>🎨 Spiral Kolam Generator</ProfessionalCard.Title>
        </ProfessionalCard.Header>
        <ProfessionalCard.Content>
          <ControlsSection>
            {/* Pattern Parameters */}
            <ControlGroup>
              <Label>Turns: {turns}</Label>
              <RangeInput
                type="range"
                min="3"
                max="12"
                value={turns}
                onChange={(e) => setTurns(parseInt(e.target.value))}
              />
            </ControlGroup>

            <ControlGroup>
              <Label>Step Angle: {stepAngle}°</Label>
              <RangeInput
                type="range"
                min="5"
                max="30"
                value={stepAngle}
                onChange={(e) => setStepAngle(parseInt(e.target.value))}
              />
            </ControlGroup>

            <ControlGroup>
              <Label>Step Length: {stepLength}px</Label>
              <RangeInput
                type="range"
                min="3"
                max="15"
                value={stepLength}
                onChange={(e) => setStepLength(parseInt(e.target.value))}
              />
            </ControlGroup>

            <ControlGroup>
              <Label>Animation Speed: {animationSpeed}ms</Label>
              <RangeInput
                type="range"
                min="10"
                max="200"
                value={animationSpeed}
                onChange={(e) => setAnimationSpeed(parseInt(e.target.value))}
              />
            </ControlGroup>
          </ControlsSection>

          {/* Action Buttons */}
          <div style={{ display: 'flex', gap: ds.spacing[3], justifyContent: 'center', marginTop: ds.spacing[4] }}>
            <ProfessionalButton
              variant="primary"
              leftIcon={<FaMagic />}
              onClick={generateSpiralPattern}
              disabled={isGenerating}
            >
              {isGenerating ? 'Generating...' : 'Generate Pattern'}
            </ProfessionalButton>

            <ProfessionalButton
              variant="secondary"
              leftIcon={isAnimating ? <FaStop /> : <FaPlay />}
              onClick={isAnimating ? stopAnimation : animatePattern}
              disabled={!patternData || isGenerating}
            >
              {isAnimating ? 'Stop Animation' : 'Animate Pattern'}
            </ProfessionalButton>

            <ProfessionalButton
              variant="outline"
              leftIcon={<FaDownload />}
              onClick={downloadPattern}
              disabled={!patternData}
            >
              Download
            </ProfessionalButton>
          </div>
        </ProfessionalCard.Content>
      </ProfessionalCard>

      {/* Canvas Section */}
      <CanvasSection>
        <CanvasContainer>
          {isGenerating && (
            <LoadingOverlay>
              <FaSpinner className="fa-spin" style={{ marginRight: ds.spacing[2] }} />
              Generating beautiful spiral pattern...
            </LoadingOverlay>
          )}
          <Canvas ref={canvasRef} />
        </CanvasContainer>

        {/* Pattern Information */}
        {patternData && (
          <ProfessionalCard variant="gradient" style={{ width: '100%' }}>
            <ProfessionalCard.Header>
              <ProfessionalCard.Title>📊 Pattern Information</ProfessionalCard.Title>
            </ProfessionalCard.Header>
            <ProfessionalCard.Content>
              <PatternInfo>
                <InfoItem>
                  <InfoLabel>Pattern Type</InfoLabel>
                  <InfoValue>{patternData.type}</InfoValue>
                </InfoItem>
                
                <InfoItem>
                  <InfoLabel>Turns</InfoLabel>
                  <InfoValue>{patternData.metadata.turns}</InfoValue>
                </InfoItem>
                
                <InfoItem>
                  <InfoLabel>Step Angle</InfoLabel>
                  <InfoValue>{patternData.metadata.step_angle}°</InfoValue>
                </InfoItem>
                
                <InfoItem>
                  <InfoLabel>Step Length</InfoLabel>
                  <InfoValue>{patternData.metadata.step_length}px</InfoValue>
                </InfoItem>
                
                <InfoItem>
                  <InfoLabel>Total Steps</InfoLabel>
                  <InfoValue>{patternData.metadata.total_steps}</InfoValue>
                </InfoItem>
                
                <InfoItem>
                  <InfoLabel>Generation Time</InfoLabel>
                  <InfoValue>{generationTime.toFixed(3)}s</InfoValue>
                </InfoItem>
                
                <InfoItem>
                  <InfoLabel>Spiral Color</InfoLabel>
                  <InfoValue style={{ color: patternData.metadata.colors.spiral }}>
                    {patternData.metadata.colors.spiral}
                  </InfoValue>
                </InfoItem>
                
                <InfoItem>
                  <InfoLabel>Squares Color</InfoLabel>
                  <InfoValue style={{ color: patternData.metadata.colors.squares }}>
                    {patternData.metadata.colors.squares}
                  </InfoValue>
                </InfoItem>
              </PatternInfo>
            </ProfessionalCard.Content>
          </ProfessionalCard>
        )}
      </CanvasSection>
    </SpiralContainer>
  );
};

export default SpiralKolamGenerator;

































