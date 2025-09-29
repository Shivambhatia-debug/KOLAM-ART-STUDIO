import React, { useState, useRef } from 'react';
import styled, { keyframes, css } from 'styled-components';
import { 
  FaUpload, FaImage, FaChartLine, FaPalette, FaGlobe, 
  FaMagic, FaDownload, FaShare, FaHeart, FaEye,
  FaSpinner, FaCheck, FaTimes, FaInfoCircle, FaLightbulb
} from 'react-icons/fa';
import { professionalDesignSystem as ds } from '../styles/ProfessionalDesignSystem';
import ProfessionalButton from '../components/ui/ProfessionalButton';
import ProfessionalCard from '../components/ui/ProfessionalCard';
import { getApiUrl } from '../config/api';

// Animations
const fadeInUp = keyframes`
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const pulse = keyframes`
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
`;

const spin = keyframes`
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
`;

// Styled Components
const Container = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, ${ds.colors.neutral[50]} 0%, ${ds.colors.neutral[100]} 100%);
  padding: ${ds.spacing[20]} ${ds.spacing[16]};
`;

const Header = styled.div`
  text-align: center;
  margin-bottom: ${ds.spacing[32]};
  animation: ${fadeInUp} 0.8s ease-out;
`;

const Title = styled.h1`
  font-size: ${ds.typography.fontSize['4xl'][0]};
  font-weight: ${ds.typography.fontWeight.bold};
  color: ${ds.colors.neutral[900]};
  margin-bottom: ${ds.spacing[6]};
  background: linear-gradient(135deg, ${ds.colors.primary[500]} 0%, ${ds.colors.secondary[500]} 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`;

const Subtitle = styled.p`
  font-size: ${ds.typography.fontSize.lg[0]};
  color: ${ds.colors.neutral[600]};
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
`;

const MainContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: ${ds.spacing[20]};
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    gap: ${ds.spacing[16]};
  }
`;

const UploadSection = styled(ProfessionalCard)`
  padding: ${ds.spacing[20]};
  text-align: center;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    transition: left 0.5s;
  }
  
  &:hover::before {
    left: 100%;
  }
`;

const UploadArea = styled.div`
  border: 3px dashed ${props => props.isDragOver ? ds.colors.primary[500] : ds.colors.neutral[300]};
  border-radius: ${ds.borderRadius.lg};
  padding: ${ds.spacing[32]};
  margin: ${ds.spacing[16]} 0;
  background: ${props => props.isDragOver ? `${ds.colors.primary[500]}10` : 'transparent'};
  transition: all 0.3s ease;
  cursor: pointer;
  
  &:hover {
    border-color: ${ds.colors.primary[500]};
    background: ${ds.colors.primary[500]}05;
  }
`;

const UploadIcon = styled.div`
  font-size: 4rem;
  color: ${ds.colors.primary[500]};
  margin-bottom: ${ds.spacing[6]};
  animation: ${pulse} 2s infinite;
`;

const UploadText = styled.p`
  font-size: ${ds.typography.fontSize.lg[0]};
  color: ${ds.colors.neutral[600]};
  margin-bottom: ${ds.spacing[2]};
`;

const UploadSubtext = styled.p`
  font-size: ${ds.typography.fontSize.sm[0]};
  color: ${ds.colors.neutral[500]};
`;

const HiddenInput = styled.input`
  display: none;
`;

const PreviewImage = styled.img`
  max-width: 100%;
  max-height: 300px;
  border-radius: ${ds.borderRadius.md};
  margin: ${ds.spacing[16]} 0;
  box-shadow: ${ds.boxShadow.md};
`;

const AnalysisSection = styled(ProfessionalCard)`
  padding: ${ds.spacing[20]};
`;

const AnalysisTitle = styled.h3`
  font-size: ${ds.typography.fontSize.xl[0]};
  font-weight: ${ds.typography.fontWeight.bold};
  color: ${ds.colors.neutral[900]};
  margin-bottom: ${ds.spacing[16]};
  display: flex;
  align-items: center;
  gap: ${ds.spacing[2]};
`;

const AnalysisGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: ${ds.spacing[6]};
  margin-bottom: ${ds.spacing[16]};
`;

const AnalysisCard = styled.div`
  background: ${ds.colors.neutral[0]};
  border: 1px solid ${ds.colors.neutral[200]};
  border-radius: ${ds.borderRadius.md};
  padding: ${ds.spacing[6]};
  text-align: center;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: ${ds.boxShadow.md};
    border-color: ${ds.colors.primary[500]};
  }
`;

const AnalysisIcon = styled.div`
  font-size: 2rem;
  color: ${ds.colors.primary[500]};
  margin-bottom: ${ds.spacing[2]};
`;

const AnalysisLabel = styled.div`
  font-size: ${ds.typography.fontSize.sm[0]};
  color: ${ds.colors.neutral[500]};
  margin-bottom: ${ds.spacing[1]};
`;

const AnalysisValue = styled.div`
  font-size: ${ds.typography.fontSize.lg[0]};
  font-weight: ${ds.typography.fontWeight.bold};
  color: ${ds.colors.neutral[900]};
`;

const ConfidenceBar = styled.div`
  width: 100%;
  height: 8px;
  background: ${ds.colors.neutral[100]};
  border-radius: ${ds.borderRadius.sm};
  overflow: hidden;
  margin-top: ${ds.spacing[2]};
`;

const ConfidenceFill = styled.div`
  height: 100%;
  background: linear-gradient(90deg, ${ds.colors.semantic.success[500]} 0%, ${ds.colors.primary[500]} 100%);
  width: ${props => props.confidence * 100}%;
  transition: width 0.5s ease;
`;

const LoadingSpinner = styled.div`
  display: inline-block;
  animation: ${spin} 1s linear infinite;
  margin-right: ${ds.spacing[2]};
`;

const StatusMessage = styled.div`
  padding: ${ds.spacing[6]};
  border-radius: ${ds.borderRadius.md};
  margin: ${ds.spacing[6]} 0;
  display: flex;
  align-items: center;
  gap: ${ds.spacing[2]};
  
  ${props => props.type === 'success' && css`
    background: ${ds.colors.semantic.success[50]};
    color: ${ds.colors.semantic.success[500]};
    border: 1px solid ${ds.colors.semantic.success[200]};
  `}
  
  ${props => props.type === 'error' && css`
    background: ${ds.colors.semantic.error[50]};
    color: ${ds.colors.semantic.error[500]};
    border: 1px solid ${ds.colors.semantic.error[200]};
  `}
  
  ${props => props.type === 'info' && css`
    background: ${ds.colors.semantic.info[50]};
    color: ${ds.colors.semantic.info[500]};
    border: 1px solid ${ds.colors.semantic.info[200]};
  `}
`;

// Similar Patterns Styled Components
const SimilarPatternsSection = styled.section`
  margin: ${ds.spacing[12]} 0;
  padding: ${ds.spacing[8]};
  background: ${ds.colors.neutral[50]};
  border-radius: ${ds.borderRadius.lg};
  border: 1px solid ${ds.colors.neutral[200]};
`;

const PatternsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: ${ds.spacing[6]};
  margin: ${ds.spacing[8]} 0;
`;

const PatternCard = styled.div`
  background: ${ds.colors.neutral[0]};
  border-radius: ${ds.borderRadius.lg};
  overflow: hidden;
  box-shadow: ${ds.shadows.sm};
  transition: all ${ds.animation.duration.normal} ${ds.animation.easing.easeInOut};
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: ${ds.shadows.lg};
  }
`;

const PatternImage = styled.div`
  width: 100%;
  height: 200px;
  background: ${ds.colors.neutral[100]};
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
`;

const PatternInfo = styled.div`
  padding: ${ds.spacing[6]};
`;

const PatternTitle = styled.h3`
  font-family: ${ds.typography.fontFamily.heading.join(', ')};
  font-size: ${ds.typography.fontSize.lg[0]};
  font-weight: ${ds.typography.fontWeight.bold};
  color: ${ds.colors.neutral[900]};
  margin-bottom: ${ds.spacing[4]};
`;

const PatternDetails = styled.div`
  margin-bottom: ${ds.spacing[4]};
`;

const DetailItem = styled.div`
  font-size: ${ds.typography.fontSize.sm[0]};
  color: ${ds.colors.neutral[600]};
  margin-bottom: ${ds.spacing[2]};
  
  strong {
    color: ${ds.colors.neutral[800]};
  }
`;

const PatternActions = styled.div`
  display: flex;
  gap: ${ds.spacing[3]};
`;

const SimilarPatternsActions = styled.div`
  display: flex;
  gap: ${ds.spacing[4]};
  justify-content: center;
  margin-top: ${ds.spacing[8]};
`;

const SectionTitle = styled.h2`
  font-family: ${ds.typography.fontFamily.heading.join(', ')};
  font-size: ${ds.typography.fontSize['2xl'][0]};
  font-weight: ${ds.typography.fontWeight.bold};
  color: ${ds.colors.neutral[900]};
  margin-bottom: ${ds.spacing[6]};
  display: flex;
  align-items: center;
  gap: ${ds.spacing[3]};
`;

const ActionButtons = styled.div`
  display: flex;
  gap: ${ds.spacing[6]};
  margin-top: ${ds.spacing[16]};
  flex-wrap: wrap;
`;


const PatternGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: ${ds.spacing[6]};
  margin-top: ${ds.spacing[16]};
`;


const PatternName = styled.div`
  font-size: ${ds.typography.fontSize.sm[0]};
  font-weight: ${ds.typography.fontWeight.medium};
  color: ${ds.colors.neutral[900]};
`;

const PatternSimilarity = styled.div`
  font-size: ${ds.typography.fontSize.xs[0]};
  color: ${ds.colors.neutral[500]};
  margin-top: ${ds.spacing[1]};
`;

const ImageAnalysis = () => {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [similarPatterns, setSimilarPatterns] = useState([]);
  const [statusMessage, setStatusMessage] = useState(null);
  const [generatedSimilarPatterns, setGeneratedSimilarPatterns] = useState([]);
  const [showSimilarPatterns, setShowSimilarPatterns] = useState(false);
  const [generatingSimilar, setGeneratingSimilar] = useState(false);
  
  // Advanced Pattern Generation States (commented out - not currently used)
  // const [advancedPatterns, setAdvancedPatterns] = useState([]);
  // const [showAdvancedPatterns, setShowAdvancedPatterns] = useState(false);
  // const [generatingAdvanced, setGeneratingAdvanced] = useState(false);
  // const [inputType, setInputType] = useState('csv'); // 'csv' or 'image'
  // const [csvData, setCsvData] = useState('');
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handleFileSelect = (file) => {
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          setUploadedImage(e.target.result);
          setAnalysisResult(null);
          setSimilarPatterns([]);
          setStatusMessage(null);
        } catch (error) {
          console.error('Error setting uploaded image:', error);
          setStatusMessage({
            type: 'error',
            text: 'Error processing image. Please try again.'
          });
        }
      };
      reader.onerror = () => {
        setStatusMessage({
          type: 'error',
          text: 'Error reading file. Please try again.'
        });
      };
      reader.readAsDataURL(file);
    } else {
      setStatusMessage({
        type: 'error',
        text: 'Please select a valid image file (PNG, JPG, JPEG)'
      });
    }
  };

  const handleFileInputChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const analyzeImage = async () => {
    if (!uploadedImage) {
      setStatusMessage({
        type: 'error',
        text: 'Please upload an image first'
      });
      return;
    }

    setIsAnalyzing(true);
    setStatusMessage(null);

    try {
      // Use improved analysis endpoint
      const response = await fetch(getApiUrl('/api/improved-analysis'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image: uploadedImage
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        setAnalysisResult(data.analysis);
        setStatusMessage({
          type: 'success',
          text: 'Image analysis completed successfully!'
        });
        
        // Generate similar patterns
        try {
          await generateSimilarPatterns(data.analysis);
        } catch (patternError) {
          console.warn('Error generating similar patterns:', patternError);
          // Don't show error for similar patterns, just log it
        }
      } else {
        setStatusMessage({
          type: 'error',
          text: data.message || 'Analysis failed'
        });
      }
    } catch (error) {
      console.error('Analysis error:', error);
      setStatusMessage({
        type: 'error',
        text: `Failed to analyze image: ${error.message}`
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const generateSimilarPatterns = async (analysis) => {
    try {
      setGeneratingSimilar(true);
      setStatusMessage('Generating similar patterns...');
      
      // Call new backend endpoint for similar pattern generation
      const response = await fetch(getApiUrl('/api/generate-similar'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          reference_pattern: analysis.kolam_type || 'pulli_kolam',
          num_variations: 5,
          include_user_images: true
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        setGeneratedSimilarPatterns(data.similar_patterns || []);
        setShowSimilarPatterns(true);
        setStatusMessage(`Generated ${data.total_generated || 0} similar patterns`);
      } else {
        setStatusMessage('Failed to generate similar patterns');
      }
    } catch (error) {
      console.error('Error generating similar patterns:', error);
      setStatusMessage(`Error: ${error.message}`);
    } finally {
      setGeneratingSimilar(false);
    }
  };

  // const generateSimilarPatternsOld = async (analysis) => {
  //   try {
  //     // Generate similar patterns based on analysis
  //     const patterns = [];
  //     
  //     // Generate patterns based on detected type
  //     const patternTypes = {
  //       'pulli_kolam': ['pulli_kolam', 'sikku_kolam'],
  //       'sikku_kolam': ['sikku_kolam', 'kambi_kolam'],
  //       'neli_kolam': ['neli_kolam', 'grid_pattern'],
  //       'kambi_kolam': ['kambi_kolam', 'sikku_kolam'],
  //       'fractal_kolam': ['fractal_kolam', 'spiral_kolam']
  //     };

  //     const similarTypes = patternTypes[analysis.kolam_type] || ['pulli_kolam', 'sikku_kolam'];
  //     
  //     // Generate fewer patterns to avoid timeout
  //     const maxPatterns = 4;
  //     
  //     for (let i = 0; i < maxPatterns; i++) {
  //       try {
  //         const patternType = similarTypes[i % similarTypes.length];
  //         const response = await fetch(getApiUrl('/api/generate'), {
  //           method: 'POST',
  //           headers: {
  //             'Content-Type': 'application/json',
  //           },
  //           body: JSON.stringify({
  //             type: 'advanced',
  //             pattern: patternType,
  //             size: 5 + Math.floor(Math.random() * 3)
  //           })
  //         });

  //         if (response.ok) {
  //           const patternData = await response.json();
  //           patterns.push({
  //             id: i,
  //             name: patternType.replace('_', ' ').toUpperCase(),
  //             similarity: 0.85 - (i * 0.1),
  //             data: patternData.pattern
  //           });
  //         }
  //       } catch (patternError) {
  //         console.warn(`Error generating pattern ${i}:`, patternError);
  //         // Continue with other patterns
  //       }
  //     }

  //     setSimilarPatterns(patterns);
  //   } catch (error) {
  //     console.error('Error generating similar patterns:', error);
  //     // Set empty array on error
  //     setSimilarPatterns([]);
  //   }
  // };

  const downloadAnalysis = () => {
    if (!analysisResult) {
      setStatusMessage({
        type: 'error',
        text: 'No analysis results to download'
      });
      return;
    }

    try {
      const analysisText = `
Kolam Image Analysis Report
==========================

Kolam Type: ${analysisResult.kolam_type}
Symmetry Type: ${analysisResult.symmetry_type}
Cultural Region: ${analysisResult.cultural_region}
Complexity Score: ${analysisResult.complexity_score}
Eulerian Path: ${analysisResult.eulerian_path ? 'Yes' : 'No'}
Confidence: ${(analysisResult.confidence * 100).toFixed(1)}%

Analysis Method: ${analysisResult.analysis_method}
Generated: ${new Date().toLocaleString()}
      `;

      const blob = new Blob([analysisText], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'kolam_analysis_report.txt';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      setStatusMessage({
        type: 'success',
        text: 'Analysis report downloaded successfully!'
      });
    } catch (error) {
      console.error('Error downloading analysis:', error);
      setStatusMessage({
        type: 'error',
        text: 'Failed to download analysis report'
      });
    }
  };

  const shareAnalysis = () => {
    if (!analysisResult) {
      setStatusMessage({
        type: 'error',
        text: 'No analysis results to share'
      });
      return;
    }

    try {
      if (navigator.share) {
        navigator.share({
          title: 'Kolam Analysis Results',
          text: `Analyzed Kolam: ${analysisResult.kolam_type} (${analysisResult.cultural_region})`,
          url: window.location.href
        }).then(() => {
          setStatusMessage({
            type: 'success',
            text: 'Analysis results shared successfully!'
          });
        }).catch((error) => {
          console.warn('Error sharing:', error);
          // Fallback to clipboard
          copyToClipboard();
        });
      } else {
        // Fallback: copy to clipboard
        copyToClipboard();
      }
    } catch (error) {
      console.error('Error sharing analysis:', error);
      setStatusMessage({
        type: 'error',
        text: 'Failed to share analysis results'
      });
    }
  };

  const copyToClipboard = () => {
    try {
      const text = `Kolam Analysis: ${analysisResult.kolam_type} - ${analysisResult.cultural_region} (${(analysisResult.confidence * 100).toFixed(1)}% confidence)`;
      navigator.clipboard.writeText(text).then(() => {
        setStatusMessage({
          type: 'success',
          text: 'Analysis results copied to clipboard!'
        });
      }).catch((error) => {
        console.error('Error copying to clipboard:', error);
        setStatusMessage({
          type: 'error',
          text: 'Failed to copy to clipboard'
        });
      });
    } catch (error) {
      console.error('Error copying to clipboard:', error);
      setStatusMessage({
        type: 'error',
        text: 'Failed to copy to clipboard'
      });
    }
  };

  return (
    <Container>
      <Header>
        <Title>
          <FaImage /> Image Analysis Studio
        </Title>
        <Subtitle>
          Upload your Kolam image for advanced AI-powered analysis including cultural classification, 
          symmetry detection, and pattern recognition
        </Subtitle>
      </Header>

      <MainContent>
        <UploadSection>
          <h3 style={{ marginBottom: '1rem', color: ds.colors.neutral[900] }}>
            <FaUpload /> Upload Kolam Image
          </h3>
          
          <UploadArea
            isDragOver={isDragOver}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <UploadIcon>
              <FaImage />
            </UploadIcon>
            <UploadText>
              {isDragOver ? 'Drop your image here' : 'Click to upload or drag & drop'}
            </UploadText>
            <UploadSubtext>
              Supports PNG, JPG, JPEG formats
            </UploadSubtext>
          </UploadArea>

          <HiddenInput
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileInputChange}
          />

          {uploadedImage && (
            <>
              <PreviewImage src={uploadedImage} alt="Uploaded Kolam" />
              <ProfessionalButton
                onClick={analyzeImage}
                disabled={isAnalyzing}
                variant="primary"
                size="large"
                style={{ width: '100%' }}
              >
                {isAnalyzing ? (
                  <>
                    <LoadingSpinner><FaSpinner /></LoadingSpinner>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <FaMagic /> Analyze Image
                  </>
                )}
              </ProfessionalButton>
            </>
          )}
        </UploadSection>

        <AnalysisSection>
          <AnalysisTitle>
            <FaChartLine /> Analysis Results
          </AnalysisTitle>

          {statusMessage && (
            <StatusMessage type={statusMessage.type}>
              {statusMessage.type === 'success' && <FaCheck />}
              {statusMessage.type === 'error' && <FaTimes />}
              {statusMessage.type === 'info' && <FaInfoCircle />}
              {statusMessage.text}
            </StatusMessage>
          )}

          {analysisResult ? (
            <>
              <AnalysisGrid>
                <AnalysisCard>
                  <AnalysisIcon><FaPalette /></AnalysisIcon>
                  <AnalysisLabel>Kolam Type</AnalysisLabel>
                  <AnalysisValue>{analysisResult.kolam_type.replace('_', ' ').toUpperCase()}</AnalysisValue>
                </AnalysisCard>

                <AnalysisCard>
                  <AnalysisIcon><FaEye /></AnalysisIcon>
                  <AnalysisLabel>Symmetry</AnalysisLabel>
                  <AnalysisValue>{analysisResult.symmetry_type.toUpperCase()}</AnalysisValue>
                </AnalysisCard>

                <AnalysisCard>
                  <AnalysisIcon><FaGlobe /></AnalysisIcon>
                  <AnalysisLabel>Cultural Region</AnalysisLabel>
                  <AnalysisValue>{analysisResult.cultural_region.replace('_', ' ').toUpperCase()}</AnalysisValue>
                </AnalysisCard>

                <AnalysisCard>
                  <AnalysisIcon><FaLightbulb /></AnalysisIcon>
                  <AnalysisLabel>Complexity</AnalysisLabel>
                  <AnalysisValue>{(analysisResult.complexity_score * 100).toFixed(0)}%</AnalysisValue>
                </AnalysisCard>

                <AnalysisCard>
                  <AnalysisIcon><FaChartLine /></AnalysisIcon>
                  <AnalysisLabel>Eulerian Path</AnalysisLabel>
                  <AnalysisValue>{analysisResult.eulerian_path ? 'YES' : 'NO'}</AnalysisValue>
                </AnalysisCard>

                <AnalysisCard>
                  <AnalysisIcon><FaHeart /></AnalysisIcon>
                  <AnalysisLabel>Confidence</AnalysisLabel>
                  <AnalysisValue>{(analysisResult.confidence * 100).toFixed(1)}%</AnalysisValue>
                  <ConfidenceBar>
                    <ConfidenceFill confidence={analysisResult.confidence} />
                  </ConfidenceBar>
                </AnalysisCard>
              </AnalysisGrid>

              <ActionButtons>
                <ProfessionalButton
                  onClick={downloadAnalysis}
                  variant="secondary"
                  size="medium"
                >
                  <FaDownload /> Download Report
                </ProfessionalButton>
                <ProfessionalButton
                  onClick={shareAnalysis}
                  variant="secondary"
                  size="medium"
                >
                  <FaShare /> Share Results
                </ProfessionalButton>
                <ProfessionalButton
                  onClick={() => generateSimilarPatterns(analysisResult)}
                  variant="primary"
                  size="medium"
                  disabled={generatingSimilar}
                >
                  {generatingSimilar ? (
                    <>
                      <LoadingSpinner />
                      Generating...
                    </>
                  ) : (
                    <>
                      <FaMagic /> Generate Similar Patterns
                    </>
                  )}
                </ProfessionalButton>
              </ActionButtons>
            </>
          ) : (
            <div style={{ textAlign: 'center', padding: '2rem', color: ds.colors.neutral[500] }}>
              <FaImage style={{ fontSize: '3rem', marginBottom: '1rem', opacity: 0.5 }} />
              <p>Upload an image to see analysis results</p>
            </div>
          )}
        </AnalysisSection>

        {/* Similar Patterns Section */}
        {showSimilarPatterns && generatedSimilarPatterns.length > 0 && (
          <SimilarPatternsSection>
            <SectionTitle>
              <FaMagic /> Generated Similar Patterns
            </SectionTitle>
            <PatternsGrid>
              {generatedSimilarPatterns.map((pattern, index) => (
                <PatternCard key={pattern.pattern_id || index}>
                  <PatternImage>
                    {pattern.image_path ? (
                      <img 
                        src={getApiUrl(`/${pattern.image_path}`)} 
                        alt={`Pattern ${index + 1}`}
                        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                      />
                    ) : (
                      <div style={{ 
                        width: '100%', 
                        height: '100%', 
                        background: ds.colors.neutral[100],
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: ds.colors.neutral[500]
                      }}>
                        <FaImage size={24} />
                      </div>
                    )}
                  </PatternImage>
                  <PatternInfo>
                    <PatternTitle>{pattern.kolam_type?.replace('_', ' ').toUpperCase()}</PatternTitle>
                    <PatternDetails>
                      <DetailItem>
                        <strong>Symmetry:</strong> {pattern.symmetry_type?.replace('_', ' ')}
                      </DetailItem>
                      <DetailItem>
                        <strong>Region:</strong> {pattern.cultural_region?.replace('_', ' ')}
                      </DetailItem>
                      <DetailItem>
                        <strong>Complexity:</strong> {(pattern.complexity_score * 100).toFixed(0)}%
                      </DetailItem>
                      <DetailItem>
                        <strong>Similarity:</strong> {(pattern.similarity_score * 100).toFixed(0)}%
                      </DetailItem>
                    </PatternDetails>
                    <PatternActions>
                      <ProfessionalButton
                        size="small"
                        variant="secondary"
                        onClick={() => downloadPattern(pattern)}
                      >
                        <FaDownload /> Download
                      </ProfessionalButton>
                    </PatternActions>
                  </PatternInfo>
                </PatternCard>
              ))}
            </PatternsGrid>
            <SimilarPatternsActions>
              <ProfessionalButton
                onClick={() => setShowSimilarPatterns(false)}
                variant="secondary"
                size="medium"
              >
                Hide Similar Patterns
              </ProfessionalButton>
              <ProfessionalButton
                onClick={() => generateSimilarPatterns(analysisResult)}
                variant="primary"
                size="medium"
                disabled={generatingSimilar}
              >
                {generatingSimilar ? (
                  <>
                    <LoadingSpinner />
                    Generating More...
                  </>
                ) : (
                  <>
                    <FaMagic /> Generate More Patterns
                  </>
                )}
              </ProfessionalButton>
            </SimilarPatternsActions>
          </SimilarPatternsSection>
        )}
      </MainContent>

      {similarPatterns.length > 0 && (
        <SimilarPatternsSection>
          <AnalysisTitle>
            <FaMagic /> Similar Patterns
          </AnalysisTitle>
          <p style={{ color: ds.colors.neutral[600], marginBottom: '1rem' }}>
            Based on your analysis, here are some similar Kolam patterns you might like:
          </p>
          
          <PatternGrid>
            {similarPatterns.map((pattern) => (
              <PatternCard key={pattern.id}>
                <PatternImage>
                  <FaPalette />
                </PatternImage>
                <PatternName>{pattern.name}</PatternName>
                <PatternSimilarity>
                  {(pattern.similarity * 100).toFixed(0)}% similar
                </PatternSimilarity>
              </PatternCard>
            ))}
          </PatternGrid>
        </SimilarPatternsSection>
      )}
    </Container>
  );
};

const downloadPattern = (pattern) => {
  try {
    if (pattern.image_path) {
      // Create download link for pattern image
      const link = document.createElement('a');
      link.href = getApiUrl(`/${pattern.image_path}`);
      link.download = `${pattern.pattern_id || 'pattern'}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } else {
      console.warn('Pattern image not available for download');
    }
  } catch (error) {
    console.error('Error downloading pattern:', error);
  }
};

// Advanced Pattern Generation Functions (commented out - not currently used)
// const generateAdvancedPatterns = async () => {
//   // This will be implemented in the component
// };

// const downloadAdvancedPattern = (pattern) => {
//   try {
//     const link = document.createElement('a');
//     link.href = getApiUrl(`/${pattern.image_path}`);
//     link.download = `${pattern.pattern_id}.png`;
//     document.body.appendChild(link);
//     link.click();
//     document.body.removeChild(link);
//   } catch (error) {
//     console.error('Download error:', error);
//   }
// };

export default ImageAnalysis;
