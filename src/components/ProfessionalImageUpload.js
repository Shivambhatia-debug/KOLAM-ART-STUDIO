import React, { useState, useCallback } from 'react';
import styled, { css } from 'styled-components';
import { FaUpload, FaImage, FaTimes, FaCheck, FaSpinner, FaMagic, FaVectorSquare } from 'react-icons/fa';
import { professionalDesignSystem as ds } from '../styles/ProfessionalDesignSystem';
import ProfessionalButton from './ui/ProfessionalButton';
import ProfessionalCard from './ui/ProfessionalCard';
import { toast } from 'react-toastify';
import axios from 'axios';

const UploadContainer = styled.div`
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
`;

const DropZone = styled.div`
  border: 2px dashed ${props => props.isDragging ? ds.colors.primary[400] : ds.colors.neutral[300]};
  border-radius: ${ds.borderRadius.xl};
  padding: ${ds.spacing[8]};
  text-align: center;
  background: ${props => props.isDragging ? ds.colors.primary[50] : ds.colors.neutral[50]};
  transition: all ${ds.animation.duration.normal} ${ds.animation.easing.easeInOut};
  cursor: pointer;
  position: relative;
  
  &:hover {
    border-color: ${ds.colors.primary[400]};
    background: ${ds.colors.primary[50]};
    transform: translateY(-2px);
  }
  
  ${props => props.disabled && css`
    opacity: 0.6;
    cursor: not-allowed;
    pointer-events: none;
  `}
`;

const UploadIcon = styled.div`
  width: 64px;
  height: 64px;
  margin: 0 auto ${ds.spacing[4]} auto;
  border-radius: ${ds.borderRadius.full};
  background: linear-gradient(135deg, ${ds.colors.primary[500]} 0%, ${ds.colors.secondary[500]} 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  transition: all ${ds.animation.duration.normal} ${ds.animation.easing.easeInOut};
  
  ${DropZone}:hover & {
    transform: scale(1.1);
    box-shadow: ${ds.boxShadow.lg};
  }
`;

const UploadText = styled.div`
  h3 {
    font-family: ${ds.typography.fontFamily.heading.join(', ')};
    font-size: ${ds.typography.fontSize.lg[0]};
    font-weight: ${ds.typography.fontWeight.bold};
    color: ${ds.colors.neutral[900]};
    margin-bottom: ${ds.spacing[2]};
  }
  
  p {
    color: ${ds.colors.neutral[600]};
    margin-bottom: ${ds.spacing[4]};
  }
  
  .supported-formats {
    font-size: ${ds.typography.fontSize.sm[0]};
    color: ${ds.colors.neutral[500]};
  }
`;

const HiddenInput = styled.input`
  display: none;
`;

const PreviewContainer = styled.div`
  margin-top: ${ds.spacing[6]};
`;

const ImagePreview = styled.div`
  position: relative;
  border-radius: ${ds.borderRadius.xl};
  overflow: hidden;
  background: white;
  box-shadow: ${ds.boxShadow.lg};
  
  img {
    width: 100%;
    height: 300px;
    object-fit: contain;
    background: ${ds.colors.neutral[50]};
  }
`;

const PreviewActions = styled.div`
  position: absolute;
  top: ${ds.spacing[3]};
  right: ${ds.spacing[3]};
  display: flex;
  gap: ${ds.spacing[2]};
`;

const ActionButton = styled.button`
  width: 36px;
  height: 36px;
  border-radius: ${ds.borderRadius.full};
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all ${ds.animation.duration.fast} ${ds.animation.easing.easeInOut};
  
  ${props => props.variant === 'remove' && css`
    background: ${ds.colors.semantic.error[500]};
    color: white;
    
    &:hover {
      background: ${ds.colors.semantic.error[600]};
      transform: scale(1.05);
    }
  `}
  
  ${props => props.variant === 'analyze' && css`
    background: ${ds.colors.primary[500]};
    color: white;
    
    &:hover {
      background: ${ds.colors.primary[600]};
      transform: scale(1.05);
    }
  `}
`;

const AnalysisResults = styled.div`
  margin-top: ${ds.spacing[6]};
`;

const LoadingOverlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: ${ds.borderRadius.xl};
`;

const LoadingContent = styled.div`
  text-align: center;
  
  .spinner {
    margin-bottom: ${ds.spacing[3]};
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
`;

const ProfessionalImageUpload = ({ onAnalysisComplete, onPatternGenerated }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isAdvancedAnalyzing, setIsAdvancedAnalyzing] = useState(false);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [advancedAnalysisResults, setAdvancedAnalysisResults] = useState(null);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = Array.from(e.dataTransfer.files);
    const imageFile = files.find(file => file.type.startsWith('image/'));
    
    if (imageFile) {
      handleImageUpload(imageFile);
    } else {
      toast.error('Please upload a valid image file');
    }
  }, [handleImageUpload]);

  const handleFileSelect = useCallback((e) => {
    const file = e.target.files[0];
    if (file) {
      handleImageUpload(file);
    }
  }, [handleImageUpload]);

  const handleImageUpload = useCallback((file) => {
    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      toast.error('Image size should be less than 10MB');
      return;
    }

    // Validate file type
    if (!file.type.startsWith('image/')) {
      toast.error('Please upload a valid image file');
      return;
    }

    // Create preview URL
    const reader = new FileReader();
    reader.onload = (e) => {
      setUploadedImage({
        file,
        url: e.target.result,
        name: file.name
      });
      toast.success('Image uploaded successfully!');
    };
    reader.readAsDataURL(file);
  }, []);

  const analyzeImage = useCallback(async () => {
    if (!uploadedImage) return;

    setIsAnalyzing(true);
    
    try {
      // Convert image to base64
      const reader = new FileReader();
      reader.onload = async (e) => {
        const imageData = e.target.result;
        
        try {
          const response = await axios.post('http://localhost:5000/api/analyze', {
            image: imageData,
            type: 'image_upload'
          }, { timeout: 30000 });

          if (response.data.success) {
            setAnalysisResults(response.data.analysis);
            onAnalysisComplete && onAnalysisComplete(response.data.analysis);
            toast.success('Image analysis completed successfully!');
          } else {
            toast.error(response.data.message || 'Analysis failed');
          }
        } catch (error) {
          console.error('Analysis error:', error);
          if (error.code === 'ECONNABORTED') {
            toast.error('Analysis timed out. Please try again.');
          } else {
            toast.error('Analysis failed. Please check your connection.');
          }
        }
      };
      
      reader.readAsDataURL(uploadedImage.file);
    } catch (error) {
      console.error('Error reading file:', error);
      toast.error('Error reading image file');
    } finally {
      setIsAnalyzing(false);
    }
  }, [uploadedImage, onAnalysisComplete]);

  const performAdvancedAnalysis = useCallback(async () => {
    if (!uploadedImage) return;

    setIsAdvancedAnalyzing(true);
    
    try {
      // Convert image to base64
      const reader = new FileReader();
      reader.onload = async (e) => {
        const imageData = e.target.result;
        
        try {
          const response = await axios.post('http://localhost:5000/api/advanced-analysis', {
            image: imageData,
            type: 'image_upload',
            mode: 'deep'
          }, { timeout: 60000 });

          if (response.data.success) {
            setAdvancedAnalysisResults(response.data.advanced_analysis);
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
            toast.error(response.data.message || 'Advanced analysis failed');
          }
        } catch (error) {
          console.error('Advanced analysis error:', error);
          if (error.code === 'ECONNABORTED') {
            toast.error('Analysis is taking longer than expected. The system may be processing a complex pattern. Please wait and try again.');
          } else if (error.response?.status === 500) {
            toast.error('Server processing error. Using fallback analysis method...');
            // Could add fallback logic here
          } else {
            toast.error('Advanced analysis failed. Please check your connection and try again.');
          }
        }
      };
      
      reader.readAsDataURL(uploadedImage.file);
    } catch (error) {
      console.error('Error reading file:', error);
      toast.error('Error reading image file');
    } finally {
      setIsAdvancedAnalyzing(false);
    }
  }, [uploadedImage]);

  const removeImage = useCallback(() => {
    setUploadedImage(null);
    setAnalysisResults(null);
    setAdvancedAnalysisResults(null);
    // Reset file input
    const fileInput = document.getElementById('image-upload-input');
    if (fileInput) {
      fileInput.value = '';
    }
  }, []);

  return (
    <UploadContainer>
      <ProfessionalCard variant="cultural">
        <ProfessionalCard.Header>
          <ProfessionalCard.Title>
            🎨 Professional Kolam Image Analysis
          </ProfessionalCard.Title>
          <ProfessionalCard.Subtitle>
            Upload your Kolam image for advanced AI-powered analysis including cultural classification, 
            symmetry detection, and authenticity scoring.
          </ProfessionalCard.Subtitle>
        </ProfessionalCard.Header>

        <ProfessionalCard.Content>
          {!uploadedImage ? (
            <DropZone
              isDragging={isDragging}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => document.getElementById('image-upload-input').click()}
            >
              <UploadIcon>
                <FaUpload />
              </UploadIcon>
              
              <UploadText>
                <h3>Drop your Kolam image here</h3>
                <p>or click to browse and select an image</p>
                <div className="supported-formats">
                  Supports JPG, PNG, WEBP • Max size: 10MB
                </div>
              </UploadText>

              <HiddenInput
                id="image-upload-input"
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
              />
            </DropZone>
          ) : (
            <PreviewContainer>
              <ImagePreview>
                <img src={uploadedImage.url} alt="Uploaded Kolam" />
                
                <PreviewActions>
                  <ActionButton
                    variant="analyze"
                    onClick={analyzeImage}
                    disabled={isAnalyzing || isAdvancedAnalyzing}
                    title="Basic Analysis"
                  >
                    {isAnalyzing ? <FaSpinner className="spinner" /> : <FaCheck />}
                  </ActionButton>
                  
                  <ActionButton
                    variant="advanced"
                    onClick={performAdvancedAnalysis}
                    disabled={isAnalyzing || isAdvancedAnalyzing}
                    title="Advanced Analysis (Hough+NetworkX)"
                    style={{
                      background: isAdvancedAnalyzing ? ds.colors.accent.emerald[500] : ds.colors.accent.emerald[600],
                      color: 'white'
                    }}
                  >
                    {isAdvancedAnalyzing ? <FaSpinner className="spinner" /> : <FaVectorSquare />}
                  </ActionButton>
                  
                  <ActionButton
                    variant="remove"
                    onClick={removeImage}
                    title="Remove Image"
                  >
                    <FaTimes />
                  </ActionButton>
                </PreviewActions>

                {(isAnalyzing || isAdvancedAnalyzing) && (
                  <LoadingOverlay>
                    <LoadingContent>
                      <div className="spinner">
                        <FaSpinner size={32} color={isAdvancedAnalyzing ? ds.colors.accent.emerald[500] : ds.colors.primary[500]} />
                      </div>
                      <div style={{ 
                        color: ds.colors.neutral[700],
                        fontWeight: ds.typography.fontWeight.medium 
                      }}>
                        {isAdvancedAnalyzing ? 'Advanced Analysis Processing...' : 'Analyzing Kolam Pattern...'}
                      </div>
                      <div style={{ 
                        fontSize: ds.typography.fontSize.sm[0],
                        color: ds.colors.neutral[600],
                        marginTop: ds.spacing[2]
                      }}>
                        {isAdvancedAnalyzing 
                          ? 'Running Advanced AI Analysis - Pattern Recognition, Graph Theory & Cultural Classification'
                          : 'Detecting cultural style, symmetry, and authenticity'
                        }
                      </div>
                    </LoadingContent>
                  </LoadingOverlay>
                )}
              </ImagePreview>
            </PreviewContainer>
          )}

          {/* Advanced Analysis Results */}
          {advancedAnalysisResults && (
            <AnalysisResults>
              <ProfessionalCard variant="gradient">
                <ProfessionalCard.Header withDivider>
                  <ProfessionalCard.Title>
                    🔬 Advanced Analysis Results
                  </ProfessionalCard.Title>
                </ProfessionalCard.Header>
                
                <ProfessionalCard.Content>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: ds.spacing[4] }}>
                    <div>
                      <strong>🎯 Quality Score:</strong>
                      <div style={{ color: ds.colors.accent.emerald[600], fontWeight: ds.typography.fontWeight.bold, fontSize: ds.typography.fontSize.lg[0] }}>
                        {advancedAnalysisResults.quality_score ? `${(advancedAnalysisResults.quality_score * 100).toFixed(1)}%` : 'N/A'}
                      </div>
                    </div>
                    
                    <div>
                      <strong>🔗 Eulerian Path:</strong>
                      <div style={{ color: advancedAnalysisResults.eulerian_analysis?.euler_path_exists ? ds.colors.accent.emerald[600] : ds.colors.accent.ruby[600] }}>
                        {advancedAnalysisResults.eulerian_analysis?.euler_path_exists ? '✅ Yes' : '❌ No'}
                      </div>
                    </div>
                    
                    <div>
                      <strong>📐 Graph Nodes:</strong>
                      <div style={{ color: ds.colors.secondary[600] }}>
                        {advancedAnalysisResults.geometric_properties?.graph_nodes || 0}
                      </div>
                    </div>
                    
                    <div>
                      <strong>🏛️ Cultural Region:</strong>
                      <div style={{ color: ds.colors.primary[600], textTransform: 'capitalize' }}>
                        {advancedAnalysisResults.cultural_classification?.region?.replace('_', ' ') || 'Unknown'}
                      </div>
                    </div>
                  </div>
                  
                  {advancedAnalysisResults.recommendations && (
                    <div style={{ marginTop: ds.spacing[4], padding: ds.spacing[3], backgroundColor: ds.colors.accent.sapphire[50], borderRadius: ds.borderRadius.lg }}>
                      <strong>💡 Expert Recommendations:</strong>
                      <ul style={{ marginTop: ds.spacing[2], paddingLeft: ds.spacing[4] }}>
                        {advancedAnalysisResults.recommendations.slice(0, 3).map((rec, index) => (
                          <li key={index} style={{ color: ds.colors.neutral[700], marginBottom: ds.spacing[1] }}>
                            {rec}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </ProfessionalCard.Content>
                
                <ProfessionalCard.Footer>
                  <ProfessionalButton
                    variant="success"
                    size="sm"
                    leftIcon={<FaMagic />}
                    onClick={() => onPatternGenerated && onPatternGenerated(advancedAnalysisResults)}
                  >
                    Generate Advanced Pattern
                  </ProfessionalButton>
                </ProfessionalCard.Footer>
              </ProfessionalCard>
            </AnalysisResults>
          )}

          {/* Basic Analysis Results */}
          {analysisResults && !advancedAnalysisResults && (
            <AnalysisResults>
              <ProfessionalCard variant="filled">
                <ProfessionalCard.Header withDivider>
                  <ProfessionalCard.Title>
                    📊 Basic Analysis Results
                  </ProfessionalCard.Title>
                </ProfessionalCard.Header>
                
                <ProfessionalCard.Content>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: ds.spacing[4] }}>
                    <div>
                      <strong>Cultural Region:</strong>
                      <div style={{ color: ds.colors.primary[600], fontWeight: ds.typography.fontWeight.medium }}>
                        {analysisResults.cultural_region || 'Unknown'}
                      </div>
                    </div>
                    
                    <div>
                      <strong>Symmetry Type:</strong>
                      <div style={{ color: ds.colors.secondary[600], fontWeight: ds.typography.fontWeight.medium }}>
                        {analysisResults.symmetry_type || 'Unknown'}
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
                        {analysisResults.confidence ? `${(analysisResults.confidence * 100).toFixed(1)}%` : 'N/A'}
                      </div>
                    </div>
                  </div>
                  
                  {analysisResults.point_count && (
                    <div style={{ marginTop: ds.spacing[4] }}>
                      <div style={{ display: 'flex', gap: ds.spacing[6] }}>
                        <span><strong>Points:</strong> {analysisResults.point_count}</span>
                        <span><strong>Lines:</strong> {analysisResults.line_count || 0}</span>
                        <span><strong>Fractal Dimension:</strong> {analysisResults.fractal_dimension || 'N/A'}</span>
                      </div>
                    </div>
                  )}
                  
                  <div style={{ marginTop: ds.spacing[4], padding: ds.spacing[3], backgroundColor: ds.colors.accent.amber[50], borderRadius: ds.borderRadius.lg, border: `1px solid ${ds.colors.accent.amber[200]}` }}>
                    <strong>🚀 Want More?</strong> Try the <strong>Advanced Analysis</strong> for Hough Circle Transform, NetworkX Graph Analysis, and Eulerian Path validation!
                  </div>
                </ProfessionalCard.Content>
                
                <ProfessionalCard.Footer>
                  <ProfessionalButton
                    variant="cultural"
                    size="sm"
                    leftIcon={<FaImage />}
                    onClick={() => onPatternGenerated && onPatternGenerated(analysisResults)}
                  >
                    Generate Similar Pattern
                  </ProfessionalButton>
                </ProfessionalCard.Footer>
              </ProfessionalCard>
            </AnalysisResults>
          )}
        </ProfessionalCard.Content>
      </ProfessionalCard>
    </UploadContainer>
  );
};

export default ProfessionalImageUpload;
