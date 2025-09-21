import React from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import { FaPalette, FaChartLine, FaImages, FaRocket, FaCode, FaHeart } from 'react-icons/fa';

const HomeContainer = styled.div`
  padding: 2rem 0;
`;

const Hero = styled.section`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 0;
  text-align: center;
  margin-bottom: 4rem;
`;

const HeroTitle = styled.h1`
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.1;

  @media (max-width: 768px) {
    font-size: 2.5rem;
  }
`;

const HeroSubtitle = styled.p`
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
`;

const ProblemStatement = styled.div`
  background: rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  border-radius: 1rem;
  margin: 2rem auto;
  max-width: 800px;
  backdrop-filter: blur(10px);
`;

const ProblemTitle = styled.h3`
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #FBBF24;
`;

const ProblemText = styled.p`
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 1rem;
`;

const ProblemOrg = styled.div`
  font-size: 0.875rem;
  opacity: 0.8;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
`;

const CTAButtons = styled.div`
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 2rem;
`;

const Features = styled.section`
  padding: 4rem 0;
`;

const SectionTitle = styled.h2`
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 3rem;
  color: ${props => props.theme.colors.text};
`;

const FeaturesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
`;

const FeatureCard = styled.div`
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: 1px solid ${props => props.theme.colors.border};

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  }
`;

const FeatureIcon = styled.div`
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #8B5CF6, #7C3AED);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  color: white;
  font-size: 2rem;
`;

const FeatureTitle = styled.h3`
  font-size: 1.25rem;
  margin-bottom: 1rem;
  color: ${props => props.theme.colors.text};
`;

const FeatureDescription = styled.p`
  color: ${props => props.theme.colors.textSecondary};
  line-height: 1.6;
`;

const Stats = styled.section`
  background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%);
  padding: 4rem 0;
  margin: 4rem 0;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  text-align: center;
`;

const StatItem = styled.div`
  padding: 1.5rem;
`;

const StatNumber = styled.div`
  font-size: 3rem;
  font-weight: 700;
  color: ${props => props.theme.colors.primary};
  margin-bottom: 0.5rem;
`;

const StatLabel = styled.div`
  font-size: 1rem;
  color: ${props => props.theme.colors.textSecondary};
  font-weight: 500;
`;

const CulturalSignificance = styled.section`
  padding: 4rem 0;
  background: white;
`;

const CulturalGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
`;

const CulturalCard = styled.div`
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  padding: 2rem;
  border-radius: 1rem;
  text-align: center;
  border: 2px solid #F59E0B;
`;

const CulturalTitle = styled.h4`
  font-size: 1.25rem;
  margin-bottom: 1rem;
  color: #92400E;
`;

const CulturalDescription = styled.p`
  color: #92400E;
  line-height: 1.6;
`;

function Home({ onPatternSelect, analysisResults }) {
  const features = [
    {
      icon: FaPalette,
      title: "Interactive Design Studio",
      description: "Create beautiful Kolam patterns with our intuitive drawing tools, symmetry guides, and pattern templates."
    },
    {
      icon: FaChartLine,
      title: "Mathematical Analysis",
      description: "Analyze patterns for symmetry, fractal properties, and mathematical principles using advanced algorithms."
    },
    {
      icon: FaImages,
      title: "Pattern Gallery",
      description: "Explore traditional Kolam designs from different regions of India with cultural significance."
    },
    {
      icon: FaCode,
      title: "Design Principles",
      description: "Learn about the mathematical foundations behind Kolam art including symmetry, fractals, and geometry."
    }
  ];

  const culturalRegions = [
    {
      title: "Tamil Nadu",
      description: "Radial symmetry patterns, circular designs, and traditional Sikku Kolam with continuous lines."
    },
    {
      title: "Karnataka", 
      description: "Bilateral symmetry, geometric precision, and mathematical Muggu patterns."
    },
    {
      title: "Andhra Pradesh",
      description: "Rotational symmetry, floral motifs, and nature-inspired Rangoli designs."
    },
    {
      title: "Kerala",
      description: "Asymmetric patterns, free-form designs, and organic natural flow patterns."
    }
  ];

  return (
    <HomeContainer>
      <Hero>
        <div className="container">
          <HeroTitle>Kolam Art Studio</HeroTitle>
          <HeroSubtitle>
            Discover the mathematical beauty of traditional Indian Kolam art through 
            interactive design, analysis, and cultural exploration.
          </HeroSubtitle>
          
          <ProblemStatement>
            <ProblemTitle>AICTE Problem Statement 25107</ProblemTitle>
            <ProblemText>
              "Develop computer programs to identify the design principles behind 
              the Kolam designs and recreate the kolams."
            </ProblemText>
            <ProblemText>
              Kolams (known by other names as muggu, rangoli and rangavalli) are 
              significant cultural traditions of India, blending art, ingenuity, and culture.
            </ProblemText>
            <ProblemOrg>
              <strong>Organization:</strong> AICTE - Indian Knowledge Systems (IKS)<br/>
              <strong>Category:</strong> Software | <strong>Theme:</strong> Heritage & Culture
            </ProblemOrg>
          </ProblemStatement>

          <CTAButtons>
            <Link to="/studio" className="btn btn-primary">
              <FaPalette /> Start Creating
            </Link>
            <Link to="/gallery" className="btn btn-outline" style={{color: 'white', borderColor: 'white'}}>
              <FaImages /> Explore Gallery
            </Link>
            <Link to="/analysis" className="btn btn-outline" style={{color: 'white', borderColor: 'white'}}>
              <FaChartLine /> View Analysis
            </Link>
          </CTAButtons>
        </div>
      </Hero>

      <Features>
        <div className="container">
          <SectionTitle>Key Features</SectionTitle>
          <FeaturesGrid>
            {features.map((feature, index) => (
              <FeatureCard key={index}>
                <FeatureIcon>
                  <feature.icon />
                </FeatureIcon>
                <FeatureTitle>{feature.title}</FeatureTitle>
                <FeatureDescription>{feature.description}</FeatureDescription>
              </FeatureCard>
            ))}
          </FeaturesGrid>
        </div>
      </Features>

      <Stats>
        <div className="container">
          <SectionTitle>System Capabilities</SectionTitle>
          <StatsGrid>
            <StatItem>
              <StatNumber>4+</StatNumber>
              <StatLabel>Symmetry Types</StatLabel>
            </StatItem>
            <StatItem>
              <StatNumber>100+</StatNumber>
              <StatLabel>Pattern Templates</StatLabel>
            </StatItem>
            <StatItem>
              <StatNumber>6</StatNumber>
              <StatLabel>Design Principles</StatLabel>
            </StatItem>
            <StatItem>
              <StatNumber>4</StatNumber>
              <StatLabel>Regional Styles</StatLabel>
            </StatItem>
          </StatsGrid>
        </div>
      </Stats>

      <CulturalSignificance>
        <div className="container">
          <SectionTitle>Cultural Significance</SectionTitle>
          <CulturalGrid>
            {culturalRegions.map((region, index) => (
              <CulturalCard key={index}>
                <CulturalTitle>{region.title}</CulturalTitle>
                <CulturalDescription>{region.description}</CulturalDescription>
              </CulturalCard>
            ))}
          </CulturalGrid>
        </div>
      </CulturalSignificance>
    </HomeContainer>
  );
}

export default Home;
