import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { FaChartLine, FaCog, FaDownload, FaPlay, FaStop, FaInfoCircle, FaMagic } from 'react-icons/fa';

const AnalysisContainer = styled.div`
  padding: 2rem 0;
`;

const AnalysisHeader = styled.div`
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: ${props => props.theme.colors.text};
  display: flex;
  align-items: center;
  gap: 0.75rem;
`;

const Subtitle = styled.p`
  font-size: 1.125rem;
  color: ${props => props.theme.colors.textSecondary};
  margin-bottom: 2rem;
`;

const AnalysisContent = styled.div`
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 2rem;

  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
`;

const MainAnalysis = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const AnalysisCard = styled.div`
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  overflow: hidden;
`;

const CardHeader = styled.div`
  padding: 1.5rem;
  border-bottom: 1px solid ${props => props.theme.colors.border};
  display: flex;
  justify-content: between;
  align-items: center;
`;

const CardTitle = styled.h3`
  font-size: 1.25rem;
  color: ${props => props.theme.colors.text};
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const CardBody = styled.div`
  padding: 1.5rem;
`;

const PatternPreview = styled.div`
  width: 100%;
  height: 300px;
  background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
  color: ${props => props.theme.colors.primary};
  margin-bottom: 1rem;
`;

const AnalysisGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
`;

const AnalysisItem = styled.div`
  background: ${props => props.theme.colors.background};
  padding: 1rem;
  border-radius: 0.5rem;
  text-align: center;
`;

const AnalysisLabel = styled.div`
  font-size: 0.875rem;
  color: ${props => props.theme.colors.textSecondary};
  margin-bottom: 0.5rem;
  font-weight: 500;
`;

const AnalysisValue = styled.div`
  font-size: 1.5rem;
  font-weight: 700;
  color: ${props => props.theme.colors.text};
`;

const ProgressBar = styled.div`
  width: 100%;
  height: 8px;
  background: ${props => props.theme.colors.border};
  border-radius: 4px;
  overflow: hidden;
  margin-top: 0.5rem;
`;

const ProgressFill = styled.div`
  height: 100%;
  background: linear-gradient(90deg, ${props => props.theme.colors.primary}, ${props => props.theme.colors.secondary});
  width: ${props => props.percentage}%;
  transition: width 0.3s ease;
`;

const SymmetryVisualization = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-top: 1rem;
`;

const SymmetryItem = styled.div`
  background: ${props => props.active ? props.theme.colors.primary : props.theme.colors.background};
  color: ${props => props.active ? 'white' : props.theme.colors.text};
  padding: 1rem;
  border-radius: 0.5rem;
  text-align: center;
  font-weight: 500;
  transition: all 0.2s ease;
`;

const FractalVisualization = styled.div`
  width: 100%;
  height: 200px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
  margin-top: 1rem;
`;

const Sidebar = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const ControlPanel = styled.div`
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
`;

const ControlTitle = styled.h3`
  font-size: 1.25rem;
  margin-bottom: 1rem;
  color: ${props => props.theme.colors.text};
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const ControlButton = styled.button`
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s ease;
  background: ${props => props.primary ? props.theme.colors.primary : 'white'};
  color: ${props => props.primary ? 'white' : props.theme.colors.text};
  border: 2px solid ${props => props.primary ? props.theme.colors.primary : props.theme.colors.border};
  margin-bottom: 1rem;

  &:hover {
    background: ${props => props.primary ? '#7C3AED' : props.theme.colors.background};
    transform: translateY(-1px);
  }
`;

const AnalysisResults = styled.div`
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
`;

const ResultItem = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid ${props => props.theme.colors.border};

  &:last-child {
    border-bottom: none;
  }
`;

const ResultLabel = styled.span`
  font-weight: 500;
  color: ${props => props.theme.colors.text};
`;

const ResultValue = styled.span`
  font-weight: 600;
  color: ${props => props.theme.colors.primary};
`;

const CulturalInfo = styled.div`
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  padding: 1.5rem;
  border-radius: 1rem;
  border-left: 4px solid #F59E0B;
  margin-top: 2rem;
`;

const CulturalTitle = styled.h4`
  font-size: 1.125rem;
  color: #92400E;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const CulturalText = styled.p`
  color: #92400E;
  line-height: 1.6;
  margin-bottom: 1rem;
`;

const CulturalStats = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
`;

const CulturalStat = styled.div`
  text-align: center;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 0.5rem;
`;

const CulturalStatValue = styled.div`
  font-size: 1.25rem;
  font-weight: 700;
  color: #92400E;
`;

const CulturalStatLabel = styled.div`
  font-size: 0.75rem;
  color: #92400E;
  text-transform: uppercase;
  letter-spacing: 0.05em;
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 4rem 2rem;
  color: ${props => props.theme.colors.textSecondary};
`;

const EmptyIcon = styled.div`
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
`;

function Analysis({ analysisResults, currentPattern }) {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisData, setAnalysisData] = useState(analysisResults);

  useEffect(() => {
    if (analysisResults) {
      setAnalysisData(analysisResults);
    }
  }, [analysisResults]);

  const runAnalysis = async () => {
    setIsAnalyzing(true);
    
    // Simulate analysis process
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const mockResults = {
      symmetryType: 'Bilateral',
      fractalDimension: 1.2,
      complexity: 'Medium',
      pointCount: 25,
      lineCount: 18,
      culturalRegion: 'Tamil Nadu',
      confidence: 0.85,
      selfSimilarity: true,
      recursiveStructure: 0.7,
      geometricComplexity: 0.6,
      culturalSignificance: 'Traditional Tamil Kolam with bilateral symmetry, often used in daily rituals and festivals. The pattern represents cosmic order and harmony.',
      regionalScores: {
        'Tamil Nadu': 0.85,
        'Karnataka': 0.45,
        'Andhra Pradesh': 0.30,
        'Kerala': 0.20
      }
    };
    
    setAnalysisData(mockResults);
    setIsAnalyzing(false);
  };

  const downloadAnalysis = () => {
    const dataStr = JSON.stringify(analysisData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'kolam-analysis-results.json';
    link.click();
  };

  if (!analysisData && !currentPattern) {
    return (
      <AnalysisContainer>
        <div className="container">
          <EmptyState>
            <EmptyIcon>📊</EmptyIcon>
            <h3>No Analysis Data</h3>
            <p>Create a pattern in the studio or select one from the gallery to view analysis results</p>
          </EmptyState>
        </div>
      </AnalysisContainer>
    );
  }

  return (
    <AnalysisContainer>
      <div className="container">
        <AnalysisHeader>
          <Title>
            <FaChartLine />
            Pattern Analysis
          </Title>
          <Subtitle>
            Mathematical analysis of Kolam patterns including symmetry detection, 
            fractal properties, and cultural significance.
          </Subtitle>
        </AnalysisHeader>

        <AnalysisContent>
          <MainAnalysis>
            <AnalysisCard>
              <CardHeader>
                <CardTitle>
                  <FaMagic />
                  Pattern Visualization
                </CardTitle>
              </CardHeader>
              <CardBody>
                <PatternPreview>
                  {currentPattern ? '🎨' : '📊'}
                </PatternPreview>
                <AnalysisGrid>
                  <AnalysisItem>
                    <AnalysisLabel>Symmetry Type</AnalysisLabel>
                    <AnalysisValue>{analysisData?.symmetryType || 'Unknown'}</AnalysisValue>
                  </AnalysisItem>
                  <AnalysisItem>
                    <AnalysisLabel>Fractal Dimension</AnalysisLabel>
                    <AnalysisValue>{analysisData?.fractalDimension?.toFixed(2) || '0.00'}</AnalysisValue>
                  </AnalysisItem>
                  <AnalysisItem>
                    <AnalysisLabel>Complexity</AnalysisLabel>
                    <AnalysisValue>{analysisData?.complexity || 'Unknown'}</AnalysisValue>
                  </AnalysisItem>
                  <AnalysisItem>
                    <AnalysisLabel>Cultural Region</AnalysisLabel>
                    <AnalysisValue>{analysisData?.culturalRegion || 'Unknown'}</AnalysisValue>
                  </AnalysisItem>
                </AnalysisGrid>
              </CardBody>
            </AnalysisCard>

            <AnalysisCard>
              <CardHeader>
                <CardTitle>
                  <FaCog />
                  Symmetry Analysis
                </CardTitle>
              </CardHeader>
              <CardBody>
                <SymmetryVisualization>
                  <SymmetryItem active={analysisData?.symmetryType === 'Radial'}>
                    Radial
                  </SymmetryItem>
                  <SymmetryItem active={analysisData?.symmetryType === 'Bilateral'}>
                    Bilateral
                  </SymmetryItem>
                  <SymmetryItem active={analysisData?.symmetryType === 'Rotational'}>
                    Rotational
                  </SymmetryItem>
                  <SymmetryItem active={analysisData?.symmetryType === 'Asymmetric'}>
                    Asymmetric
                  </SymmetryItem>
                </SymmetryVisualization>
              </CardBody>
            </AnalysisCard>

            <AnalysisCard>
              <CardHeader>
                <CardTitle>
                  <FaChartLine />
                  Fractal Properties
                </CardTitle>
              </CardHeader>
              <CardBody>
                <FractalVisualization>
                  Fractal Dimension: {analysisData?.fractalDimension?.toFixed(2) || '0.00'}
                </FractalVisualization>
                <div style={{marginTop: '1rem'}}>
                  <AnalysisLabel>Self-Similarity</AnalysisLabel>
                  <ProgressBar>
                    <ProgressFill percentage={analysisData?.selfSimilarity ? 80 : 20} />
                  </ProgressBar>
                </div>
                <div style={{marginTop: '1rem'}}>
                  <AnalysisLabel>Recursive Structure</AnalysisLabel>
                  <ProgressBar>
                    <ProgressFill percentage={(analysisData?.recursiveStructure || 0) * 100} />
                  </ProgressBar>
                </div>
              </CardBody>
            </AnalysisCard>
          </MainAnalysis>

          <Sidebar>
            <ControlPanel>
              <ControlTitle>
                <FaCog />
                Analysis Controls
              </ControlTitle>
              <ControlButton 
                primary 
                onClick={runAnalysis}
                disabled={isAnalyzing}
              >
                {isAnalyzing ? <FaStop /> : <FaPlay />}
                {isAnalyzing ? 'Analyzing...' : 'Run Analysis'}
              </ControlButton>
              <ControlButton onClick={downloadAnalysis}>
                <FaDownload />
                Download Results
              </ControlButton>
            </ControlPanel>

            <AnalysisResults>
              <CardTitle>
                <FaInfoCircle />
                Analysis Results
              </CardTitle>
              <ResultItem>
                <ResultLabel>Points</ResultLabel>
                <ResultValue>{analysisData?.pointCount || 0}</ResultValue>
              </ResultItem>
              <ResultItem>
                <ResultLabel>Lines</ResultLabel>
                <ResultValue>{analysisData?.lineCount || 0}</ResultValue>
              </ResultItem>
              <ResultItem>
                <ResultLabel>Confidence</ResultLabel>
                <ResultValue>{(analysisData?.confidence || 0) * 100}%</ResultValue>
              </ResultItem>
              <ResultItem>
                <ResultLabel>Geometric Complexity</ResultLabel>
                <ResultValue>{((analysisData?.geometricComplexity || 0) * 100).toFixed(0)}%</ResultValue>
              </ResultItem>
            </AnalysisResults>

            <CulturalInfo>
              <CulturalTitle>
                <FaInfoCircle />
                Cultural Significance
              </CulturalTitle>
              <CulturalText>
                {analysisData?.culturalSignificance || 'No cultural analysis available.'}
              </CulturalText>
              
              <CulturalStats>
                <CulturalStat>
                  <CulturalStatValue>{analysisData?.culturalRegion || 'Unknown'}</CulturalStatValue>
                  <CulturalStatLabel>Most Likely Region</CulturalStatLabel>
                </CulturalStat>
                <CulturalStat>
                  <CulturalStatValue>{((analysisData?.confidence || 0) * 100).toFixed(0)}%</CulturalStatValue>
                  <CulturalStatLabel>Confidence</CulturalStatLabel>
                </CulturalStat>
              </CulturalStats>
            </CulturalInfo>
          </Sidebar>
        </AnalysisContent>
      </div>
    </AnalysisContainer>
  );
}

export default Analysis;
