import React, { useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import { toast } from 'react-toastify';
import { getApiUrl } from '../config/api';

const DiffusionContainer = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const DiffusionCard = styled.div`
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 1200px;
  margin-bottom: 2rem;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  color: #2d3748;
  text-align: center;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
`;

const Subtitle = styled.p`
  font-size: 1.1rem;
  color: #718096;
  text-align: center;
  margin-bottom: 2rem;
`;

const UploadArea = styled.div`
  border: 3px dashed ${props => props.isDragOver ? '#667eea' : '#e2e8f0'};
  border-radius: 12px;
  padding: 3rem;
  text-align: center;
  background: ${props => props.isDragOver ? '#f7fafc' : '#fafafa'};
  transition: all 0.3s ease;
  cursor: pointer;
  margin-bottom: 2rem;

  &:hover {
    border-color: #667eea;
    background: #f7fafc;
  }
`;

const UploadText = styled.div`
  font-size: 1.2rem;
  color: #4a5568;
  margin-bottom: 1rem;
`;

const UploadIcon = styled.div`
  font-size: 3rem;
  margin-bottom: 1rem;
`;

const FileInput = styled.input`
  display: none;
`;

const SelectedFile = styled.div`
  background: #f0fff4;
  border: 2px solid #68d391;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const FileInfo = styled.div`
  flex: 1;
`;

const FileName = styled.div`
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 0.25rem;
`;

const FileSize = styled.div`
  font-size: 0.875rem;
  color: #718096;
`;

const RemoveButton = styled.button`
  background: #fed7d7;
  color: #c53030;
  border: none;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;

  &:hover {
    background: #feb2b2;
  }
`;

const GenerateButton = styled.button`
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const LoadingSpinner = styled.div`
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const ResultsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
`;

const ResultCard = styled.div`
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;

  &:hover {
    transform: translateY(-5px);
  }
`;

const ResultImage = styled.img`
  width: 100%;
  height: 250px;
  object-fit: cover;
`;

const ResultContent = styled.div`
  padding: 1.5rem;
`;

const ResultTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 0.5rem;
`;

const ResultPrompt = styled.p`
  color: #718096;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 1rem;
`;

const ResultActions = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const DownloadButton = styled.button`
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.3s ease;

  &:hover {
    background: #5a67d8;
  }
`;

const ImageSize = styled.span`
  color: #a0aec0;
  font-size: 0.875rem;
`;

const LoadingCard = styled.div`
  background: white;
  border-radius: 16px;
  padding: 3rem;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
`;

const LoadingTitle = styled.h3`
  font-size: 1.5rem;
  color: #2d3748;
  margin-bottom: 1rem;
`;

const LoadingText = styled.p`
  color: #718096;
  margin-bottom: 2rem;
`;

const ProgressBar = styled.div`
  width: 100%;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
`;

const ProgressFill = styled.div`
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 4px;
  animation: progress 2s ease-in-out infinite;

  @keyframes progress {
    0% { width: 0%; }
    50% { width: 70%; }
    100% { width: 100%; }
  }
`;

const ErrorMessage = styled.div`
  background: #fed7d7;
  border: 2px solid #feb2b2;
  border-radius: 8px;
  padding: 1rem;
  color: #c53030;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const KolamDiffusionGenerator = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      validateAndSetFile(file);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragOver(false);
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
      validateAndSetFile(files[0]);
    }
  };

  const validateAndSetFile = (file) => {
    // Validate file type
    if (!file.type.startsWith('image/')) {
      setError('Please select a valid image file');
      return;
    }
    
    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB');
      return;
    }
    
    setSelectedFile(file);
    setError(null);
    setResults(null);
  };

  const removeFile = () => {
    setSelectedFile(null);
    setError(null);
    setResults(null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    if (!selectedFile) {
      setError('Please select an image file');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const formData = new FormData();
      formData.append('image', selectedFile);

      const response = await axios.post(getApiUrl('/api/diffusion/generate'), formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 300000, // 5 minutes timeout
      });

      if (response.data.success) {
        setResults(response.data);
        toast.success('Kolam variants generated successfully!');
      } else {
        setError(response.data.error || 'Failed to generate variants');
        toast.error(response.data.error || 'Failed to generate variants');
      }
    } catch (err) {
      console.error('Error generating variants:', err);
      let errorMessage = 'An unexpected error occurred';
      
      if (err.response) {
        errorMessage = err.response.data.error || 'Server error';
      } else if (err.request) {
        errorMessage = 'Unable to connect to server. Please check if the API is running.';
      }
      
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const downloadImage = (url, filename) => {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    toast.success('Image downloaded successfully!');
  };

  return (
    <DiffusionContainer>
      <DiffusionCard>
        <Title>🎨 AI Kolam Diffusion Generator</Title>
        <Subtitle>
          Upload a Kolam image and generate 3 unique artistic variants using Stable Diffusion + ControlNet
        </Subtitle>

        <form onSubmit={handleSubmit}>
          <UploadArea
            isDragOver={isDragOver}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => document.getElementById('file-input').click()}
          >
            <UploadIcon>📁</UploadIcon>
            <UploadText>
              {isDragOver ? 'Drop your image here' : 'Click to upload or drag and drop'}
            </UploadText>
            <p style={{ color: '#a0aec0', fontSize: '0.875rem' }}>
              Supported formats: JPG, PNG, GIF. Max size: 10MB
            </p>
          </UploadArea>

          <FileInput
            id="file-input"
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
          />

          {selectedFile && (
            <SelectedFile>
              <div style={{ fontSize: '1.5rem' }}>📄</div>
              <FileInfo>
                <FileName>{selectedFile.name}</FileName>
                <FileSize>{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</FileSize>
              </FileInfo>
              <RemoveButton onClick={removeFile}>Remove</RemoveButton>
            </SelectedFile>
          )}

          {error && (
            <ErrorMessage>
              <span>⚠️</span>
              {error}
            </ErrorMessage>
          )}

          <GenerateButton
            type="submit"
            disabled={!selectedFile || loading}
          >
            {loading ? (
              <>
                <LoadingSpinner />
                Generating Variants...
              </>
            ) : (
              <>
                <span>🚀</span>
                Generate AI Kolam Variants
              </>
            )}
          </GenerateButton>
        </form>

        {loading && (
          <LoadingCard>
            <LoadingTitle>🎨 Generating Your Kolam Variants</LoadingTitle>
            <LoadingText>
              This may take 1-3 minutes depending on your hardware...
            </LoadingText>
            <ProgressBar>
              <ProgressFill />
            </ProgressBar>
          </LoadingCard>
        )}

        {results && (
          <div>
            <h2 style={{ 
              fontSize: '1.5rem', 
              fontWeight: '600', 
              color: '#2d3748', 
              textAlign: 'center',
              marginBottom: '1rem'
            }}>
              Generated Kolam Variants
            </h2>
            {results.session_id && (
              <p style={{ 
                color: '#718096', 
                textAlign: 'center', 
                marginBottom: '2rem' 
              }}>
                Session ID: {results.session_id}
              </p>
            )}
            {results.message && (
              <p style={{ 
                color: '#38a169', 
                textAlign: 'center', 
                marginBottom: '2rem',
                fontSize: '0.875rem'
              }}>
                ℹ️ {results.message}
              </p>
            )}
            
            <ResultsGrid>
              {(results.variants || results.generated_images || []).map((image, index) => (
                <ResultCard key={index}>
                  <ResultImage
                    src={image.url}
                    alt={`Kolam Variant ${image.variant || index + 1}`}
                    onError={(e) => {
                      e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjNmNGY2Ii8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzY2NjY2NiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlIG5vdCBmb3VuZDwvdGV4dD48L3N2Zz4=';
                    }}
                  />
                  <ResultContent>
                    <ResultTitle>{image.name || `Variant ${image.variant || index + 1}`}</ResultTitle>
                    <ResultPrompt>{image.prompt || image.description || 'AI Generated Kolam Variant'}</ResultPrompt>
                    <ResultActions>
                      <DownloadButton
                        onClick={() => downloadImage(image.url, image.filename || `kolam_variant_${index + 1}.png`)}
                      >
                        Download
                      </DownloadButton>
                      <ImageSize>
                        {image.size ? `${image.size[0]} × ${image.size[1]}` : 'Unknown size'}
                      </ImageSize>
                    </ResultActions>
                  </ResultContent>
                </ResultCard>
              ))}
            </ResultsGrid>
          </div>
        )}
      </DiffusionCard>
    </DiffusionContainer>
  );
};

export default KolamDiffusionGenerator;



