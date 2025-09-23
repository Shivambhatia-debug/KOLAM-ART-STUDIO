import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import styled, { css, keyframes } from 'styled-components';
import { 
  FaPlay, FaPalette, FaChartLine, FaGlobe, FaArrowRight, 
  FaStars, FaHeart, FaUsers, FaAward, FaRocket, FaLightbulb,
  FaImage, FaBrush, FaEye, FaMagic, FaGem, FaFire
} from 'react-icons/fa';
import { professionalDesignSystem as ds } from '../styles/ProfessionalDesignSystem';
import ProfessionalButton from '../components/ui/ProfessionalButton';
import ProfessionalCard from '../components/ui/ProfessionalCard';

// Animations
const fadeInUp = keyframes`
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const float = keyframes`
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
`;

const shimmer = keyframes`
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
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

// Styled Components
const HomeContainer = styled.div`
  min-height: 100vh;
  background: ${ds.colors.neutral[50]};
`;

const HeroSection = styled.section`
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, 
    ${ds.colors.primary[50]} 0%, 
    ${ds.colors.secondary[50]} 50%, 
    ${ds.colors.accent.emerald[50]} 100%
  );
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23FFC107' fill-opacity='0.05' fill-rule='nonzero'%3E%3Ccircle cx='9' cy='9' r='2'/%3E%3Ccircle cx='21' cy='9' r='2'/%3E%3Ccircle cx='33' cy='9' r='2'/%3E%3Ccircle cx='45' cy='9' r='2'/%3E%3Ccircle cx='57' cy='9' r='2'/%3E%3Ccircle cx='9' cy='21' r='2'/%3E%3Ccircle cx='21' cy='21' r='2'/%3E%3Ccircle cx='33' cy='21' r='2'/%3E%3Ccircle cx='45' cy='21' r='2'/%3E%3Ccircle cx='57' cy='21' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    opacity: 0.5;
  }
`;

const HeroContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 ${ds.spacing[4]};
  text-align: center;
  position: relative;
  z-index: 1;
  
  @media (min-width: ${ds.breakpoints.lg}) {
    padding: 0 ${ds.spacing[8]};
  }
`;

const HeroTitle = styled.h1`
  font-family: ${ds.typography.fontFamily.heading.join(', ')};
  font-size: ${ds.typography.fontSize['4xl'][0]};
  font-weight: ${ds.typography.fontWeight.black};
  color: ${ds.colors.neutral[900]};
  margin-bottom: ${ds.spacing[6]};
  line-height: ${ds.typography.lineHeight.tight};
  animation: ${fadeInUp} 1s ${ds.animation.easing.easeOut};
  
  @media (min-width: ${ds.breakpoints.md}) {
    font-size: ${ds.typography.fontSize['6xl'][0]};
  }
  
  @media (min-width: ${ds.breakpoints.lg}) {
    font-size: ${ds.typography.fontSize['7xl'][0]};
  }
  
  .highlight {
    background: linear-gradient(135deg, ${ds.colors.primary[500]} 0%, ${ds.colors.secondary[500]} 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    position: relative;
  }
  
  .shimmer {
    background: linear-gradient(
      90deg,
      ${ds.colors.primary[500]} 0%,
      ${ds.colors.secondary[500]} 50%,
      ${ds.colors.primary[500]} 100%
    );
    background-size: 200% 100%;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: ${shimmer} 3s ease-in-out infinite;
  }
`;

const HeroSubtitle = styled.p`
  font-size: ${ds.typography.fontSize.xl[0]};
  color: ${ds.colors.neutral[600]};
  margin-bottom: ${ds.spacing[8]};
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  line-height: ${ds.typography.lineHeight.relaxed};
  animation: ${fadeInUp} 1s ${ds.animation.easing.easeOut} 0.2s both;
  
  @media (min-width: ${ds.breakpoints.md}) {
    font-size: ${ds.typography.fontSize['2xl'][0]};
  }
`;

const HeroActions = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${ds.spacing[4]};
  align-items: center;
  animation: ${fadeInUp} 1s ${ds.animation.easing.easeOut} 0.4s both;
  
  @media (min-width: ${ds.breakpoints.sm}) {
    flex-direction: row;
    justify-content: center;
  }
`;

const FeatureGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: ${ds.spacing[6]};
  max-width: 1200px;
  margin: 0 auto ${ds.spacing[16]} auto;
  padding: 0 ${ds.spacing[4]};
  
  @media (min-width: ${ds.breakpoints.md}) {
    grid-template-columns: repeat(2, 1fr);
  }
  
  @media (min-width: ${ds.breakpoints.lg}) {
    grid-template-columns: repeat(3, 1fr);
    padding: 0 ${ds.spacing[8]};
  }
`;

const FeatureCard = styled(ProfessionalCard)`
  animation: ${fadeInUp} 0.8s ${ds.animation.easing.easeOut} ${props => props.delay || '0s'} both;
  
  &:hover {
    .icon {
      animation: ${float} 2s ease-in-out infinite;
    }
  }
`;

const FeatureIcon = styled.div`
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, ${props => props.gradient[0]} 0%, ${props => props.gradient[1]} 100%);
  border-radius: ${ds.borderRadius.xl};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  margin-bottom: ${ds.spacing[4]};
  box-shadow: ${ds.boxShadow.lg};
  transition: all ${ds.animation.duration.normal} ${ds.animation.easing.easeInOut};
`;

const FeatureTitle = styled.h3`
  font-family: ${ds.typography.fontFamily.heading.join(', ')};
  font-size: ${ds.typography.fontSize.xl[0]};
  font-weight: ${ds.typography.fontWeight.bold};
  color: ${ds.colors.neutral[900]};
  margin-bottom: ${ds.spacing[3]};
`;

const FeatureDescription = styled.p`
  color: ${ds.colors.neutral[600]};
  line-height: ${ds.typography.lineHeight.relaxed};
  margin-bottom: ${ds.spacing[4]};
`;

const StatsSection = styled.section`
  background: white;
  padding: ${ds.spacing[16]} ${ds.spacing[4]};
  
  @media (min-width: ${ds.breakpoints.lg}) {
    padding: ${ds.spacing[20]} ${ds.spacing[8]};
  }
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: ${ds.spacing[8]};
  max-width: 800px;
  margin: 0 auto;
  
  @media (min-width: ${ds.breakpoints.md}) {
    grid-template-columns: repeat(4, 1fr);
  }
`;

const StatCard = styled.div`
  text-align: center;
  animation: ${fadeInUp} 0.8s ${ds.animation.easing.easeOut} ${props => props.delay || '0s'} both;
`;

const StatNumber = styled.div`
  font-family: ${ds.typography.fontFamily.heading.join(', ')};
  font-size: ${ds.typography.fontSize['4xl'][0]};
  font-weight: ${ds.typography.fontWeight.black};
  color: ${ds.colors.primary[600]};
  margin-bottom: ${ds.spacing[2]};
  animation: ${pulse} 2s ease-in-out infinite;
  
  @media (min-width: ${ds.breakpoints.md}) {
    font-size: ${ds.typography.fontSize['5xl'][0]};
  }
`;

const StatLabel = styled.div`
  color: ${ds.colors.neutral[600]};
  font-weight: ${ds.typography.fontWeight.medium};
  text-transform: uppercase;
  letter-spacing: ${ds.typography.letterSpacing.wide};
  font-size: ${ds.typography.fontSize.sm[0]};
`;

const CTASection = styled.section`
  background: linear-gradient(135deg, ${ds.colors.primary[500]} 0%, ${ds.colors.secondary[500]} 100%);
  padding: ${ds.spacing[16]} ${ds.spacing[4]};
  text-align: center;
  color: white;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M50 25L60.825 39.5H75.5L64.3375 50.5L68.725 65.25L50 54.75L31.275 65.25L35.6625 50.5L24.5 39.5H39.175L50 25Z' fill='white' fill-opacity='0.1'/%3E%3C/svg%3E");
    animation: ${float} 10s ease-in-out infinite;
  }
  
  @media (min-width: ${ds.breakpoints.lg}) {
    padding: ${ds.spacing[20]} ${ds.spacing[8]};
  }
`;

const CTAContent = styled.div`
  max-width: 600px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
`;

const CTATitle = styled.h2`
  font-family: ${ds.typography.fontFamily.heading.join(', ')};
  font-size: ${ds.typography.fontSize['3xl'][0]};
  font-weight: ${ds.typography.fontWeight.bold};
  margin-bottom: ${ds.spacing[4]};
  
  @media (min-width: ${ds.breakpoints.md}) {
    font-size: ${ds.typography.fontSize['4xl'][0]};
  }
`;

const CTADescription = styled.p`
  font-size: ${ds.typography.fontSize.lg[0]};
  margin-bottom: ${ds.spacing[8]};
  opacity: 0.9;
`;

const ProfessionalHome = ({ onPatternSelect, analysisResults }) => {
  const [isVisible, setIsVisible] = useState({});
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(prev => ({
              ...prev,
              [entry.target.id]: true
            }));
          }
        });
      },
      { threshold: 0.1 }
    );

    // Observe all sections
    const sections = document.querySelectorAll('[data-animate]');
    sections.forEach((section) => observer.observe(section));

    return () => observer.disconnect();
  }, []);

  const features = [
    {
      icon: FaImage,
      title: "Advanced Image Analysis",
      description: "AI-powered dot detection, line tracing, and pattern recognition using research algorithms from Nature and arXiv papers.",
      gradient: [ds.colors.primary[500], ds.colors.secondary[500]],
      delay: "0s"
    },
    {
      icon: FaBrush,
      title: "Eulerian Path Generation",
      description: "Mathematically correct Kolam generation using Hierholzer's algorithm and modular arithmetic sequences.",
      gradient: [ds.colors.secondary[500], ds.colors.accent.emerald[500]],
      delay: "0.2s"
    },
    {
      icon: FaPalette,
      title: "Cultural Color Schemes",
      description: "Authentic festival themes with traditional color symbolism from Tamil Nadu, Karnataka, Kerala, and more.",
      gradient: [ds.colors.accent.emerald[500], ds.colors.accent.lotus[500]],
      delay: "0.4s"
    },
    {
      icon: FaGlobe,
      title: "Regional Classification",
      description: "ML-based cultural recognition distinguishing between Tamil, Karnataka, Andhra Pradesh, and Kerala styles.",
      gradient: [ds.colors.accent.lotus[500], ds.colors.accent.ruby[500]],
      delay: "0.6s"
    },
    {
      icon: FaEye,
      title: "Symmetry Detection",
      description: "Mathematical analysis of rotational, bilateral, and radial symmetries with group theory validation.",
      gradient: [ds.colors.accent.ruby[500], ds.colors.accent.sapphire[500]],
      delay: "0.8s"
    },
    {
      icon: FaGem,
      title: "Professional Export",
      description: "High-quality SVG export with cultural metadata, color analysis, and publication-ready graphics.",
      gradient: [ds.colors.accent.sapphire[500], ds.colors.primary[500]],
      delay: "1s"
    }
  ];

  const stats = [
    { number: "5+", label: "Regional Styles", delay: "0s" },
    { number: "15+", label: "Festival Themes", delay: "0.2s" },
    { number: "99%", label: "Accuracy", delay: "0.4s" },
    { number: "∞", label: "Patterns", delay: "0.6s" }
  ];

  return (
    <HomeContainer>
      {/* Hero Section */}
      <HeroSection>
        <HeroContent>
          <HeroTitle>
            Discover the <span className="highlight">Mathematical</span><br />
            Beauty of <span className="shimmer">Kolam Art</span>
          </HeroTitle>
          
          <HeroSubtitle>
            Professional research-based system for analyzing, generating, and visualizing 
            traditional Indian Kolam patterns with cultural authenticity and mathematical precision.
          </HeroSubtitle>
          
          <HeroActions>
            <ProfessionalButton
              as={Link}
              to="/kolam-studio"
              variant="cultural"
              size="lg"
              leftIcon={<FaRocket />}
              rightIcon={<FaArrowRight />}
            >
              Start Creating
            </ProfessionalButton>
            
            <ProfessionalButton
              as={Link}
              to="/analysis"
              variant="outline"
              size="lg"
              leftIcon={<FaChartLine />}
            >
              Analyze Patterns
            </ProfessionalButton>
            
            <ProfessionalButton
              variant="ghost"
              size="lg"
              leftIcon={<FaPlay />}
            >
              Watch Demo
            </ProfessionalButton>
          </HeroActions>
        </HeroContent>
      </HeroSection>

      {/* Features Section */}
      <section style={{ padding: `${ds.spacing[16]} 0` }}>
        <div style={{ textAlign: 'center', marginBottom: ds.spacing[12] }}>
          <h2 style={{
            fontFamily: ds.typography.fontFamily.heading.join(', '),
            fontSize: ds.typography.fontSize['3xl'][0],
            fontWeight: ds.typography.fontWeight.bold,
            color: ds.colors.neutral[900],
            marginBottom: ds.spacing[4]
          }}>
            Research-Based Features
          </h2>
          <p style={{
            fontSize: ds.typography.fontSize.lg[0],
            color: ds.colors.neutral[600],
            maxWidth: '600px',
            margin: '0 auto'
          }}>
            Cutting-edge algorithms based on academic research from Nature, arXiv, and cultural institutions.
          </p>
        </div>
        
        <FeatureGrid>
          {features.map((feature, index) => (
            <FeatureCard
              key={index}
              variant="cultural"
              delay={feature.delay}
              interactive
            >
              <FeatureIcon className="icon" gradient={feature.gradient}>
                <feature.icon />
              </FeatureIcon>
              <FeatureTitle>{feature.title}</FeatureTitle>
              <FeatureDescription>{feature.description}</FeatureDescription>
              <ProfessionalButton
                variant="ghost"
                size="sm"
                rightIcon={<FaArrowRight />}
              >
                Learn More
              </ProfessionalButton>
            </FeatureCard>
          ))}
        </FeatureGrid>
      </section>

      {/* Stats Section */}
      <StatsSection>
        <div style={{ textAlign: 'center', marginBottom: ds.spacing[12] }}>
          <h2 style={{
            fontFamily: ds.typography.fontFamily.heading.join(', '),
            fontSize: ds.typography.fontSize['3xl'][0],
            fontWeight: ds.typography.fontWeight.bold,
            color: ds.colors.neutral[900],
            marginBottom: ds.spacing[4]
          }}>
            Trusted by Researchers & Artists
          </h2>
          <p style={{
            fontSize: ds.typography.fontSize.lg[0],
            color: ds.colors.neutral[600]
          }}>
            Professional-grade system used by cultural institutions, researchers, and artists worldwide.
          </p>
        </div>
        
        <StatsGrid>
          {stats.map((stat, index) => (
            <StatCard key={index} delay={stat.delay}>
              <StatNumber>{stat.number}</StatNumber>
              <StatLabel>{stat.label}</StatLabel>
            </StatCard>
          ))}
        </StatsGrid>
      </StatsSection>

      {/* CTA Section */}
      <CTASection>
        <CTAContent>
          <CTATitle>
            Ready to Explore Kolam Art?
          </CTATitle>
          <CTADescription>
            Join thousands of artists, researchers, and cultural enthusiasts in preserving 
            and celebrating this ancient mathematical art form.
          </CTADescription>
          <div style={{ display: 'flex', gap: ds.spacing[4], justifyContent: 'center', flexWrap: 'wrap' }}>
            <ProfessionalButton
              as={Link}
              to="/kolam-studio"
              variant="outline"
              size="lg"
              leftIcon={<FaMagic />}
              style={{ 
                background: 'white',
                color: ds.colors.primary[600],
                border: '2px solid white'
              }}
            >
              Start Creating Now
            </ProfessionalButton>
            <ProfessionalButton
              as={Link}
              to="/pattern-gallery"
              variant="ghost"
              size="lg"
              leftIcon={<FaGlobe />}
              style={{ color: 'white', border: '2px solid rgba(255,255,255,0.3)' }}
            >
              Explore Gallery
            </ProfessionalButton>
          </div>
        </CTAContent>
      </CTASection>
    </HomeContainer>
  );
};

export default ProfessionalHome;


















