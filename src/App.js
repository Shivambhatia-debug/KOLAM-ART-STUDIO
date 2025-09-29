import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import styled, { ThemeProvider, createGlobalStyle } from 'styled-components';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Professional Components
import ProfessionalHeader from './components/ProfessionalHeader';
import ProfessionalHome from './pages/ProfessionalHome';
import ProfessionalKolamStudio from './pages/ProfessionalKolamStudio';
import ImageAnalysis from './pages/ImageAnalysis';
import PatternGallery from './pages/PatternGallery';
import Analysis from './pages/Analysis';
import About from './pages/About';
import KolamDiffusion from './pages/KolamDiffusion';

// Professional Design System
import { professionalDesignSystem } from './styles/ProfessionalDesignSystem';

const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: ${professionalDesignSystem.typography.fontFamily.primary.join(', ')};
    background-color: ${professionalDesignSystem.colors.neutral[50]};
    color: ${professionalDesignSystem.colors.neutral[900]};
    line-height: ${professionalDesignSystem.typography.lineHeight.normal};
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    line-height: 1.2;
  }

  button {
    font-family: inherit;
    cursor: pointer;
    border: none;
    outline: none;
  }

  input, textarea, select {
    font-family: inherit;
    outline: none;
  }

  a {
    text-decoration: none;
    color: inherit;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
  }

  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: ${professionalDesignSystem.spacing[3]} ${professionalDesignSystem.spacing[6]};
    border-radius: ${professionalDesignSystem.borderRadius.lg};
    font-weight: ${professionalDesignSystem.typography.fontWeight.medium};
    transition: all ${professionalDesignSystem.animation.duration.normal} ${professionalDesignSystem.animation.easing.easeInOut};
    text-decoration: none;
    border: none;
    cursor: pointer;
    font-size: ${professionalDesignSystem.typography.fontSize.base[0]};
    box-shadow: ${professionalDesignSystem.boxShadow.md};
  }

  .btn-primary {
    background: linear-gradient(135deg, ${professionalDesignSystem.colors.primary[500]} 0%, ${professionalDesignSystem.colors.primary[600]} 100%);
    color: white;
  }

  .btn-primary:hover {
    background: linear-gradient(135deg, ${professionalDesignSystem.colors.primary[600]} 0%, ${professionalDesignSystem.colors.primary[700]} 100%);
    transform: translateY(-2px);
    box-shadow: ${professionalDesignSystem.boxShadow.lg};
  }

  .btn-secondary {
    background: linear-gradient(135deg, ${professionalDesignSystem.colors.secondary[500]} 0%, ${professionalDesignSystem.colors.secondary[600]} 100%);
    color: white;
  }

  .btn-secondary:hover {
    background: linear-gradient(135deg, ${professionalDesignSystem.colors.secondary[600]} 0%, ${professionalDesignSystem.colors.secondary[700]} 100%);
    transform: translateY(-2px);
    box-shadow: ${professionalDesignSystem.boxShadow.lg};
  }

  .btn-outline {
    background-color: transparent;
    color: ${professionalDesignSystem.colors.primary[600]};
    border: 2px solid ${professionalDesignSystem.colors.primary[500]};
    box-shadow: none;
  }

  .btn-outline:hover {
    background-color: ${professionalDesignSystem.colors.primary[500]};
    color: white;
    transform: translateY(-1px);
    box-shadow: ${professionalDesignSystem.boxShadow.md};
  }

  .card {
    background-color: white;
    border-radius: ${professionalDesignSystem.borderRadius['2xl']};
    box-shadow: ${professionalDesignSystem.boxShadow.lg};
    border: 1px solid ${professionalDesignSystem.colors.neutral[200]};
    overflow: hidden;
    transition: all ${professionalDesignSystem.animation.duration.normal} ${professionalDesignSystem.animation.easing.easeInOut};
  }

  .card:hover {
    box-shadow: ${professionalDesignSystem.boxShadow.xl};
    transform: translateY(-4px);
  }

  .card-header {
    padding: ${professionalDesignSystem.spacing[6]};
    border-bottom: 1px solid ${professionalDesignSystem.colors.neutral[200]};
  }

  .card-body {
    padding: ${professionalDesignSystem.spacing[6]};
  }

  .grid {
    display: grid;
    gap: ${professionalDesignSystem.spacing[6]};
  }

  .grid-2 {
    grid-template-columns: repeat(2, 1fr);
  }

  .grid-3 {
    grid-template-columns: repeat(3, 1fr);
  }

  .grid-4 {
    grid-template-columns: repeat(4, 1fr);
  }

  @media (max-width: ${professionalDesignSystem.breakpoints.md}) {
    .grid-2,
    .grid-3,
    .grid-4 {
      grid-template-columns: 1fr;
    }
  }
`;

const AppContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: ${professionalDesignSystem.colors.neutral[50]};
`;

const MainContent = styled.main`
  flex: 1;
  padding-top: 72px; /* Account for professional header */
`;

function App() {
  const [currentPattern, setCurrentPattern] = useState(null);
  const [analysisResults, setAnalysisResults] = useState(null);

  return (
    <ThemeProvider theme={professionalDesignSystem}>
      <GlobalStyle />
      <Router>
        <AppContainer>
          <ProfessionalHeader />
          <MainContent>
            <Routes>
              <Route 
                path="/" 
                element={
                  <ProfessionalHome 
                    onPatternSelect={setCurrentPattern}
                    analysisResults={analysisResults}
                  />
                } 
              />
              <Route 
                path="/kolam-studio" 
                element={
                  <ProfessionalKolamStudio 
                    currentPattern={currentPattern}
                    onPatternChange={setCurrentPattern}
                    onAnalysisComplete={setAnalysisResults}
                  />
                } 
              />
              <Route 
                path="/image-analysis" 
                element={<ImageAnalysis />} 
              />
              <Route 
                path="/pattern-gallery" 
                element={
                  <PatternGallery 
                    onPatternSelect={setCurrentPattern}
                  />
                } 
              />
              <Route 
                path="/analysis" 
                element={
                  <Analysis 
                    analysisResults={analysisResults}
                    currentPattern={currentPattern}
                  />
                } 
              />
              <Route path="/about" element={<About />} />
              <Route path="/ai-diffusion" element={<KolamDiffusion />} />
            </Routes>
          </MainContent>
          <ToastContainer
            position="top-right"
            autoClose={3000}
            hideProgressBar={false}
            newestOnTop={false}
            closeOnClick
            rtl={false}
            pauseOnFocusLoss
            draggable
            pauseOnHover
          />
        </AppContainer>
      </Router>
    </ThemeProvider>
  );
}

export default App;
