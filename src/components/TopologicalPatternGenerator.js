import React, { useState } from 'react';
import styled from 'styled-components';
import { professionalDesignSystem as ds } from '../styles/ProfessionalDesignSystem';
import ProfessionalButton from './ui/ProfessionalButton';
import ProfessionalCard from './ui/ProfessionalCard';

const GeneratorContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${ds.spacing[4]};
`;

const ControlGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: ${ds.spacing[3]};
`;

const SliderContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${ds.spacing[2]};
`;

const SliderLabel = styled.label`
  font-weight: ${ds.typography.fontWeight.medium};
  color: ${ds.colors.neutral[700]};
  font-size: ${ds.typography.fontSize.sm[0]};
`;

const Slider = styled.input`
  width: 100%;
  height: 6px;
  border-radius: ${ds.borderRadius.full};
  background: ${ds.colors.neutral[200]};
  outline: none;
  -webkit-appearance: none;
  
  &::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: ${ds.colors.primary[500]};
    cursor: pointer;
    box-shadow: ${ds.boxShadow.sm};
  }
  
  &::-moz-range-thumb {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: ${ds.colors.primary[500]};
    cursor: pointer;
    border: none;
    box-shadow: ${ds.boxShadow.sm};
  }
`;

const SelectContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${ds.spacing[2]};
`;

const Select = styled.select`
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

const PatternPreview = styled.div`
  width: 100%;
  height: 300px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border: 2px solid ${ds.colors.primary[200]};
  border-radius: ${ds.borderRadius.xl};
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  
  &:hover {
    border-color: ${ds.colors.primary[300]};
    box-shadow: 
      0 10px 15px -3px rgba(0, 0, 0, 0.1),
      0 4px 6px -2px rgba(0, 0, 0, 0.05),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
    transform: translateY(-1px);
  }
  
  svg {
    width: 100%;
    height: 100%;
    object-fit: contain;
    border-radius: ${ds.borderRadius.lg};
  }
  
  /* Loading animation */
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.4),
      transparent
    );
    animation: shimmer 2s infinite;
  }
  
  @keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
  }
`;

const InfoGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: ${ds.spacing[3]};
  margin-top: ${ds.spacing[4]};
`;

const InfoItem = styled.div`
  padding: ${ds.spacing[4]};
  background: linear-gradient(135deg, ${ds.colors.primary[50]} 0%, ${ds.colors.primary[100]} 100%);
  border-radius: ${ds.borderRadius.xl};
  border-left: 4px solid ${ds.colors.primary[500]};
  box-shadow: 
    0 2px 4px rgba(0, 0, 0, 0.05),
    0 1px 2px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 
      0 4px 8px rgba(0, 0, 0, 0.1),
      0 2px 4px rgba(0, 0, 0, 0.15);
    border-left-color: ${ds.colors.primary[600]};
  }
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, ${ds.colors.primary[400]}, ${ds.colors.primary[600]});
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  &:hover::before {
    opacity: 1;
  }
`;

const InfoLabel = styled.div`
  font-size: ${ds.typography.fontSize.xs[0]};
  color: ${ds.colors.neutral[600]};
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: ${ds.spacing[1]};
`;

const InfoValue = styled.div`
  font-size: ${ds.typography.fontSize.lg[0]};
  font-weight: ${ds.typography.fontWeight.bold};
  color: ${ds.colors.primary[700]};
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  
  &:hover {
    color: ${ds.colors.primary[800]};
    transform: scale(1.05);
  }
`;

const TopologicalPatternGenerator = ({ onPatternGenerated, onAnalysisComplete }) => {
  const [numDots, setNumDots] = useState(3);
  const [numJunctions, setNumJunctions] = useState(1);
  const [bondTypes, setBondTypes] = useState(['CROSS', 'DOUBLE', 'BROKEN']);
  const [symmetryType, setSymmetryType] = useState('RADIAL');
  const [culturalRegion, setCulturalRegion] = useState('tamil_nadu');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedPattern, setGeneratedPattern] = useState(null);
  const [patternInfo, setPatternInfo] = useState(null);

  const regions = [
    { value: 'tamil_nadu', label: 'Tamil Nadu (Sikku Kolam)' },
    { value: 'karnataka', label: 'Karnataka (Muggu)' },
    { value: 'kerala', label: 'Kerala (Pookalam)' },
    { value: 'andhra_pradesh', label: 'Andhra Pradesh (Muggulu)' },
    { value: 'telangana', label: 'Telangana (Gorintaku)' }
  ];

  const symmetryTypes = [
    { value: 'RADIAL', label: 'Radial (Point Symmetry)' },
    { value: 'ROTATIONAL', label: 'Rotational (N-fold)' },
    { value: 'BILATERAL', label: 'Bilateral (Mirror)' },
    { value: 'ASYMMETRIC', label: 'Asymmetric (Free-form)' }
  ];

  const bondTypeOptions = [
    { value: 'CROSS', label: 'Cross Bond (X)', description: 'Lines crossing at junction' },
    { value: 'DOUBLE', label: 'Double Bond (D)', description: 'Two parallel lines' },
    { value: 'BROKEN', label: 'Broken Bond (B)', description: 'No connection' }
  ];

  const generatePattern = async () => {
    setIsGenerating(true);
    try {
      const response = await fetch('http://localhost:5000/api/generate-topological', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          num_dots: numDots,
          num_junctions: numJunctions,
          bond_types: bondTypes,
          symmetry_type: symmetryType,
          cultural_region: culturalRegion
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setGeneratedPattern(data.pattern);
        setPatternInfo(data.pattern_info);
        onPatternGenerated && onPatternGenerated(data.pattern);
        onAnalysisComplete && onAnalysisComplete(data.pattern_info);
      } else {
        console.error('Pattern generation failed:', data.error);
      }
    } catch (error) {
      console.error('Generation error:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const renderPatternPreview = () => {
    if (!generatedPattern) {
      return (
        <div style={{ 
          textAlign: 'center', 
          color: ds.colors.neutral[500],
          fontSize: ds.typography.fontSize.sm[0],
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100%',
          flexDirection: 'column',
          gap: ds.spacing[2]
        }}>
          <div style={{ fontSize: '2rem', opacity: 0.3 }}>🔬</div>
          <div>Click "Generate Pattern" to create a topological kolam</div>
        </div>
      );
    }

    // Calculate bounds for proper centering
    const allPoints = [
      ...(generatedPattern.points || []),
      ...(generatedPattern.junctions || []).map(j => ({ x: j.position[0], y: j.position[1] }))
    ];
    
    if (generatedPattern.paths) {
      generatedPattern.paths.forEach(path => {
        path.forEach(point => {
          allPoints.push({ x: point[0], y: point[1] });
        });
      });
    }

    const minX = Math.min(...allPoints.map(p => p.x)) - 20;
    const maxX = Math.max(...allPoints.map(p => p.x)) + 20;
    const minY = Math.min(...allPoints.map(p => p.y)) - 20;
    const maxY = Math.max(...allPoints.map(p => p.y)) + 20;
    
    const width = maxX - minX;
    const height = maxY - minY;
    // const centerX = (minX + maxX) / 2;
    // const centerY = (minY + maxY) / 2;

    return (
      <svg 
        viewBox={`${minX} ${minY} ${width} ${height}`} 
        style={{ 
          width: '100%', 
          height: '100%',
          background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
          borderRadius: ds.borderRadius.lg,
          boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.1)'
        }}
      >
        {/* Background grid */}
        <defs>
          <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e2e8f0" strokeWidth="0.5" opacity="0.3"/>
          </pattern>
          
          {/* Gradient definitions */}
          <linearGradient id="pathGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#DC143C" stopOpacity="0.8"/>
            <stop offset="100%" stopColor="#B22222" stopOpacity="0.6"/>
          </linearGradient>
          
          <radialGradient id="dotGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#FF6B35" stopOpacity="1"/>
            <stop offset="100%" stopColor="#DC143C" stopOpacity="0.8"/>
          </radialGradient>
          
          <radialGradient id="junctionGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#FFD700" stopOpacity="1"/>
            <stop offset="100%" stopColor="#FF8C00" stopOpacity="0.8"/>
          </radialGradient>
          
          {/* Drop shadow filter */}
          <filter id="dropshadow" x="-50%" y="-50%" width="200%" height="200%">
            <feDropShadow dx="2" dy="2" stdDeviation="2" floodColor="#000000" floodOpacity="0.2"/>
          </filter>
        </defs>
        
        {/* Background grid */}
        <rect width="100%" height="100%" fill="url(#grid)" />
        
        {/* Draw paths with enhanced styling */}
        {generatedPattern.paths && generatedPattern.paths.map((path, pathIndex) => {
          const pathData = path.map((point, index) => 
            `${index === 0 ? 'M' : 'L'} ${point[0]} ${point[1]}`
          ).join(' ');
          
          return (
            <g key={pathIndex}>
              {/* Path shadow */}
              <path
                d={pathData}
                stroke="rgba(0,0,0,0.1)"
                strokeWidth="4"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                transform="translate(1, 1)"
              />
              {/* Main path */}
              <path
                d={pathData}
                stroke={generatedPattern.colors ? generatedPattern.colors[pathIndex % generatedPattern.colors.length] : '#DC143C'}
                strokeWidth="3"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                filter="url(#dropshadow)"
                style={{
                  strokeDasharray: pathIndex % 2 === 0 ? 'none' : '5,5',
                  animation: `drawPath 2s ease-in-out ${pathIndex * 0.1}s both`
                }}
              />
            </g>
          );
        })}
        
        {/* Draw dots with enhanced styling */}
        {generatedPattern.points && generatedPattern.points.map((point, pointIndex) => (
          <g key={pointIndex}>
            {/* Dot shadow */}
            <circle
              cx={point.x + 1}
              cy={point.y + 1}
              r={point.is_center ? 8 : 6}
              fill="rgba(0,0,0,0.2)"
            />
            {/* Main dot */}
            <circle
              cx={point.x}
              cy={point.y}
              r={point.is_center ? 7 : 5}
              fill={point.is_center ? "url(#dotGradient)" : "#DC143C"}
              stroke="white"
              strokeWidth="2"
              filter="url(#dropshadow)"
              style={{
                animation: `pulseDot 2s ease-in-out ${pointIndex * 0.1}s both`
              }}
            />
            {/* Inner highlight */}
            <circle
              cx={point.x - 1}
              cy={point.y - 1}
              r={point.is_center ? 3 : 2}
              fill="rgba(255,255,255,0.6)"
            />
          </g>
        ))}
        
        {/* Draw junctions with enhanced styling */}
        {generatedPattern.junctions && generatedPattern.junctions.map((junction, junctionIndex) => (
          <g key={`junction-${junctionIndex}`}>
            {/* Junction shadow */}
            <circle
              cx={junction.position[0] + 1}
              cy={junction.position[1] + 1}
              r="4"
              fill="rgba(0,0,0,0.2)"
            />
            {/* Main junction */}
            <circle
              cx={junction.position[0]}
              cy={junction.position[1]}
              r="4"
              fill="url(#junctionGradient)"
              stroke="white"
              strokeWidth="1.5"
              filter="url(#dropshadow)"
              style={{
                animation: `pulseJunction 2s ease-in-out ${junctionIndex * 0.2}s both`
              }}
            />
            {/* Junction center */}
            <circle
              cx={junction.position[0]}
              cy={junction.position[1]}
              r="1.5"
              fill="rgba(255,255,255,0.8)"
            />
          </g>
        ))}
        
        {/* Animation styles */}
        <style>
          {`
            @keyframes drawPath {
              0% { stroke-dasharray: 1000; stroke-dashoffset: 1000; }
              100% { stroke-dasharray: 1000; stroke-dashoffset: 0; }
            }
            
            @keyframes pulseDot {
              0% { transform: scale(0); opacity: 0; }
              50% { transform: scale(1.2); opacity: 1; }
              100% { transform: scale(1); opacity: 1; }
            }
            
            @keyframes pulseJunction {
              0% { transform: scale(0); opacity: 0; }
              50% { transform: scale(1.3); opacity: 1; }
              100% { transform: scale(1); opacity: 1; }
            }
          `}
        </style>
      </svg>
    );
  };

  return (
    <GeneratorContainer>
      <ProfessionalCard variant="elevated">
        <ProfessionalCard.Header>
          <ProfessionalCard.Title>🔬 Topological Pattern Generator</ProfessionalCard.Title>
          <ProfessionalCard.Subtitle>
            Research-based 5-step method for perfect kolam generation
          </ProfessionalCard.Subtitle>
        </ProfessionalCard.Header>
        <ProfessionalCard.Content>
          <ControlGrid>
            <SliderContainer>
              <SliderLabel>Number of Dots (N): {numDots}</SliderLabel>
              <Slider
                type="range"
                min="2"
                max="10"
                value={numDots}
                onChange={(e) => setNumDots(parseInt(e.target.value))}
              />
              <div style={{ fontSize: ds.typography.fontSize.xs[0], color: ds.colors.neutral[500] }}>
                More dots = more complex patterns
              </div>
            </SliderContainer>

            <SliderContainer>
              <SliderLabel>Junctions per Pair (J): {numJunctions}</SliderLabel>
              <Slider
                type="range"
                min="1"
                max="3"
                value={numJunctions}
                onChange={(e) => setNumJunctions(parseInt(e.target.value))}
              />
              <div style={{ fontSize: ds.typography.fontSize.xs[0], color: ds.colors.neutral[500] }}>
                More junctions = more connections
              </div>
            </SliderContainer>

            <SelectContainer>
              <SliderLabel>Symmetry Type</SliderLabel>
              <Select
                value={symmetryType}
                onChange={(e) => setSymmetryType(e.target.value)}
              >
                {symmetryTypes.map(type => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </Select>
            </SelectContainer>

            <SelectContainer>
              <SliderLabel>Cultural Region</SliderLabel>
              <Select
                value={culturalRegion}
                onChange={(e) => setCulturalRegion(e.target.value)}
              >
                {regions.map(region => (
                  <option key={region.value} value={region.value}>
                    {region.label}
                  </option>
                ))}
              </Select>
            </SelectContainer>
          </ControlGrid>

          <div style={{ marginTop: ds.spacing[4] }}>
            <SliderLabel>Bond Types (Select multiple)</SliderLabel>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: ds.spacing[2], marginTop: ds.spacing[2] }}>
              {bondTypeOptions.map(bond => (
                <label key={bond.value} style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: ds.spacing[1],
                  padding: ds.spacing[2],
                  border: `1px solid ${ds.colors.neutral[300]}`,
                  borderRadius: ds.borderRadius.lg,
                  cursor: 'pointer',
                  backgroundColor: bondTypes.includes(bond.value) ? ds.colors.primary[50] : 'white'
                }}>
                  <input
                    type="checkbox"
                    checked={bondTypes.includes(bond.value)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setBondTypes([...bondTypes, bond.value]);
                      } else {
                        setBondTypes(bondTypes.filter(t => t !== bond.value));
                      }
                    }}
                  />
                  <div>
                    <div style={{ fontWeight: ds.typography.fontWeight.medium }}>
                      {bond.label}
                    </div>
                    <div style={{ fontSize: ds.typography.fontSize.xs[0], color: ds.colors.neutral[600] }}>
                      {bond.description}
                    </div>
                  </div>
                </label>
              ))}
            </div>
          </div>

          <ProfessionalButton
            variant="primary"
            size="lg"
            onClick={generatePattern}
            disabled={isGenerating || bondTypes.length === 0}
            fullWidth
            style={{ marginTop: ds.spacing[4] }}
          >
            {isGenerating ? 'Generating...' : 'Generate Topological Pattern'}
          </ProfessionalButton>
        </ProfessionalCard.Content>
      </ProfessionalCard>

      <ProfessionalCard variant="gradient">
        <ProfessionalCard.Header>
          <ProfessionalCard.Title>🎨 Pattern Preview</ProfessionalCard.Title>
        </ProfessionalCard.Header>
        <ProfessionalCard.Content>
          <PatternPreview>
            {renderPatternPreview()}
          </PatternPreview>
        </ProfessionalCard.Content>
      </ProfessionalCard>

      {patternInfo && (
        <ProfessionalCard variant="cultural">
          <ProfessionalCard.Header>
            <ProfessionalCard.Title>📊 Pattern Analysis</ProfessionalCard.Title>
          </ProfessionalCard.Header>
          <ProfessionalCard.Content>
            <InfoGrid>
              <InfoItem>
                <InfoLabel>Parent Type</InfoLabel>
                <InfoValue>{patternInfo.parent_type}</InfoValue>
              </InfoItem>
              
              <InfoItem>
                <InfoLabel>Symmetry</InfoLabel>
                <InfoValue>{patternInfo.symmetry_type}</InfoValue>
              </InfoItem>
              
              <InfoItem>
                <InfoLabel>Dots</InfoLabel>
                <InfoValue>{patternInfo.mathematical_properties?.dot_count || 0}</InfoValue>
              </InfoItem>
              
              <InfoItem>
                <InfoLabel>Junctions</InfoLabel>
                <InfoValue>{patternInfo.mathematical_properties?.junction_count || 0}</InfoValue>
              </InfoItem>
              
              <InfoItem>
                <InfoLabel>Paths</InfoLabel>
                <InfoValue>{patternInfo.mathematical_properties?.path_count || 0}</InfoValue>
              </InfoItem>
              
              <InfoItem>
                <InfoLabel>Complexity</InfoLabel>
                <InfoValue>
                  {patternInfo.mathematical_properties?.complexity_score 
                    ? `${(patternInfo.mathematical_properties.complexity_score * 100).toFixed(1)}%`
                    : 'N/A'
                  }
                </InfoValue>
              </InfoItem>
            </InfoGrid>

            {patternInfo.cultural_metadata && (
              <div style={{ marginTop: ds.spacing[4], padding: ds.spacing[3], backgroundColor: ds.colors.accent.amber[50], borderRadius: ds.borderRadius.lg }}>
                <div style={{ fontWeight: ds.typography.fontWeight.bold, marginBottom: ds.spacing[2] }}>
                  Cultural Significance
                </div>
                <div style={{ fontSize: ds.typography.fontSize.sm[0], color: ds.colors.neutral[700] }}>
                  <strong>{patternInfo.cultural_metadata.name}:</strong> {patternInfo.cultural_metadata.symbolism}
                </div>
                <div style={{ fontSize: ds.typography.fontSize.sm[0], color: ds.colors.neutral[600], marginTop: ds.spacing[1] }}>
                  {patternInfo.cultural_metadata.mathematical_significance}
                </div>
              </div>
            )}

            {patternInfo.numeric_representation && (
              <div style={{ marginTop: ds.spacing[4], padding: ds.spacing[3], backgroundColor: ds.colors.accent.sapphire[50], borderRadius: ds.borderRadius.lg }}>
                <div style={{ fontWeight: ds.typography.fontWeight.bold, marginBottom: ds.spacing[2] }}>
                  Numeric Representation (Yanagisawa & Nagata)
                </div>
                <div style={{ 
                  fontFamily: 'monospace', 
                  fontSize: ds.typography.fontSize.sm[0], 
                  color: ds.colors.neutral[700],
                  wordBreak: 'break-all'
                }}>
                  {patternInfo.numeric_representation}
                </div>
              </div>
            )}
          </ProfessionalCard.Content>
        </ProfessionalCard>
      )}
    </GeneratorContainer>
  );
};

export default TopologicalPatternGenerator;









