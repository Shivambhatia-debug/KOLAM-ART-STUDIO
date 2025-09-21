import React from 'react';
import styled from 'styled-components';
import { FaCode, FaGraduationCap, FaHeart, FaAward, FaUsers, FaGlobe, FaBook, FaLightbulb } from 'react-icons/fa';

const AboutContainer = styled.div`
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
  padding: 2rem;
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

const Section = styled.section`
  padding: 4rem 0;
`;

const SectionTitle = styled.h2`
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 3rem;
  color: ${props => props.theme.colors.text};
`;

const ContentGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
`;

const ContentCard = styled.div`
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

const CardIcon = styled.div`
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

const CardTitle = styled.h3`
  font-size: 1.25rem;
  margin-bottom: 1rem;
  color: ${props => props.theme.colors.text};
`;

const CardDescription = styled.p`
  color: ${props => props.theme.colors.textSecondary};
  line-height: 1.6;
`;

const FeatureList = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
`;

const FeatureItem = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: ${props => props.theme.colors.background};
  border-radius: 0.5rem;
  border-left: 4px solid ${props => props.theme.colors.primary};
`;

const FeatureIcon = styled.div`
  color: ${props => props.theme.colors.primary};
  font-size: 1.25rem;
`;

const FeatureText = styled.span`
  font-weight: 500;
  color: ${props => props.theme.colors.text};
`;

const TechStack = styled.div`
  background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%);
  padding: 4rem 0;
  margin: 4rem 0;
`;

const TechGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  text-align: center;
`;

const TechItem = styled.div`
  padding: 1.5rem;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
`;

const TechName = styled.div`
  font-size: 1.25rem;
  font-weight: 600;
  color: ${props => props.theme.colors.text};
  margin-bottom: 0.5rem;
`;

const TechDescription = styled.div`
  font-size: 0.875rem;
  color: ${props => props.theme.colors.textSecondary};
`;

const TeamSection = styled.div`
  background: white;
  padding: 4rem 0;
  border-radius: 1rem;
  margin: 4rem 0;
`;

const TeamGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
`;

const TeamMember = styled.div`
  text-align: center;
  padding: 2rem;
  background: ${props => props.theme.colors.background};
  border-radius: 1rem;
  border: 1px solid ${props => props.theme.colors.border};
`;

const MemberAvatar = styled.div`
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #8B5CF6, #7C3AED);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  color: white;
  font-size: 2rem;
`;

const MemberName = styled.h4`
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: ${props => props.theme.colors.text};
`;

const MemberRole = styled.p`
  color: ${props => props.theme.colors.textSecondary};
  font-size: 0.875rem;
  margin-bottom: 1rem;
`;

const MemberBio = styled.p`
  color: ${props => props.theme.colors.textSecondary};
  font-size: 0.875rem;
  line-height: 1.5;
`;

const StatsSection = styled.div`
  background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
  color: white;
  padding: 4rem 0;
  margin: 4rem 0;
  border-radius: 1rem;
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
  margin-bottom: 0.5rem;
`;

const StatLabel = styled.div`
  font-size: 1rem;
  opacity: 0.9;
  font-weight: 500;
`;

const ContactSection = styled.div`
  background: white;
  padding: 4rem 0;
  border-radius: 1rem;
  margin: 4rem 0;
  text-align: center;
`;

const ContactGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
`;

const ContactItem = styled.div`
  padding: 2rem;
  background: ${props => props.theme.colors.background};
  border-radius: 1rem;
  border: 1px solid ${props => props.theme.colors.border};
`;

const ContactIcon = styled.div`
  color: ${props => props.theme.colors.primary};
  font-size: 2rem;
  margin-bottom: 1rem;
`;

const ContactTitle = styled.h4`
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: ${props => props.theme.colors.text};
`;

const ContactText = styled.p`
  color: ${props => props.theme.colors.textSecondary};
  font-size: 0.875rem;
`;

function About() {
  const features = [
    "Interactive Pattern Creation",
    "Mathematical Analysis Engine",
    "Cultural Significance Detection",
    "Regional Pattern Recognition",
    "Fractal Dimension Calculation",
    "Symmetry Detection Algorithms",
    "Pattern Export & Sharing",
    "Educational Resources"
  ];

  const techStack = [
    { name: "React", description: "Frontend Framework" },
    { name: "Python", description: "Backend Analysis" },
    { name: "Fabric.js", description: "Canvas Drawing" },
    { name: "Matplotlib", description: "Data Visualization" },
    { name: "NumPy", description: "Mathematical Computing" },
    { name: "SciPy", description: "Scientific Computing" }
  ];

  const teamMembers = [
    {
      name: "AI Assistant",
      role: "Lead Developer",
      bio: "Developed the complete Kolam analysis system with mathematical algorithms and cultural significance analysis."
    },
    {
      name: "AICTE IKS",
      role: "Problem Sponsor",
      bio: "Indian Knowledge Systems department providing the problem statement and cultural context."
    }
  ];

  return (
    <AboutContainer>
      <Hero>
        <div className="container">
          <HeroTitle>About Kolam Art Studio</HeroTitle>
          <HeroSubtitle>
            A comprehensive solution for analyzing and recreating traditional Indian Kolam art 
            through modern computational methods and cultural preservation.
          </HeroSubtitle>
          
          <ProblemStatement>
            <ProblemTitle>AICTE Problem Statement 25107</ProblemTitle>
            <ProblemText>
              "Develop computer programs (in any language, preferably Python) to identify 
              the design principles behind the Kolam designs and recreate the kolams."
            </ProblemText>
            <ProblemText>
              Kolams (known by other names as muggu, rangoli and rangavalli) are significant 
              cultural traditions of India, blending art, ingenuity, and culture. The designs 
              vary by region, and consist of grids of dots, with symmetry, repetition, and 
              spatial reasoning embedded in them.
            </ProblemText>
            <ProblemOrg>
              <strong>Organization:</strong> AICTE - Indian Knowledge Systems (IKS)<br/>
              <strong>Category:</strong> Software | <strong>Theme:</strong> Heritage & Culture
            </ProblemOrg>
          </ProblemStatement>
        </div>
      </Hero>

      <Section>
        <div className="container">
          <SectionTitle>Our Mission</SectionTitle>
          <ContentGrid>
            <ContentCard>
              <CardIcon>
                <FaHeart />
              </CardIcon>
              <CardTitle>Cultural Preservation</CardTitle>
              <CardDescription>
                Preserve and promote traditional Indian Kolam art through modern technology 
                while maintaining cultural authenticity and significance.
              </CardDescription>
            </ContentCard>
            <ContentCard>
              <CardIcon>
                <FaCode />
              </CardIcon>
              <CardTitle>Mathematical Analysis</CardTitle>
              <CardDescription>
                Apply advanced mathematical algorithms to understand the geometric and 
                fractal properties underlying traditional Kolam designs.
              </CardDescription>
            </ContentCard>
            <ContentCard>
              <CardIcon>
                <FaGraduationCap />
              </CardIcon>
              <CardTitle>Educational Value</CardTitle>
              <CardDescription>
                Provide an interactive platform for learning about the mathematical 
                principles and cultural significance of Kolam art.
              </CardDescription>
            </ContentCard>
          </ContentGrid>
        </div>
      </Section>

      <Section>
        <div className="container">
          <SectionTitle>Key Features</SectionTitle>
          <FeatureList>
            {features.map((feature, index) => (
              <FeatureItem key={index}>
                <FeatureIcon>
                  <FaLightbulb />
                </FeatureIcon>
                <FeatureText>{feature}</FeatureText>
              </FeatureItem>
            ))}
          </FeatureList>
        </div>
      </Section>

      <TechStack>
        <div className="container">
          <SectionTitle>Technology Stack</SectionTitle>
          <TechGrid>
            {techStack.map((tech, index) => (
              <TechItem key={index}>
                <TechName>{tech.name}</TechName>
                <TechDescription>{tech.description}</TechDescription>
              </TechItem>
            ))}
          </TechGrid>
        </div>
      </TechStack>

      <TeamSection>
        <div className="container">
          <SectionTitle>Our Team</SectionTitle>
          <TeamGrid>
            {teamMembers.map((member, index) => (
              <TeamMember key={index}>
                <MemberAvatar>
                  <FaUsers />
                </MemberAvatar>
                <MemberName>{member.name}</MemberName>
                <MemberRole>{member.role}</MemberRole>
                <MemberBio>{member.bio}</MemberBio>
              </TeamMember>
            ))}
          </TeamGrid>
        </div>
      </TeamSection>

      <StatsSection>
        <div className="container">
          <SectionTitle>Project Statistics</SectionTitle>
          <StatsGrid>
            <StatItem>
              <StatNumber>6+</StatNumber>
              <StatLabel>Design Principles</StatLabel>
            </StatItem>
            <StatItem>
              <StatNumber>4</StatNumber>
              <StatLabel>Regional Styles</StatLabel>
            </StatItem>
            <StatItem>
              <StatNumber>100+</StatNumber>
              <StatLabel>Pattern Templates</StatLabel>
            </StatItem>
            <StatItem>
              <StatNumber>8</StatNumber>
              <StatLabel>Analysis Algorithms</StatLabel>
            </StatItem>
          </StatsGrid>
        </div>
      </StatsSection>

      <ContactSection>
        <div className="container">
          <SectionTitle>Get In Touch</SectionTitle>
          <ContactGrid>
            <ContactItem>
              <ContactIcon>
                <FaAward />
              </ContactIcon>
              <ContactTitle>AICTE Problem Statement</ContactTitle>
              <ContactText>Problem Statement 25107 - Indian Knowledge Systems</ContactText>
            </ContactItem>
            <ContactItem>
              <ContactIcon>
                <FaGlobe />
              </ContactIcon>
              <ContactTitle>Cultural Heritage</ContactTitle>
              <ContactText>Preserving traditional Indian art through technology</ContactText>
            </ContactItem>
            <ContactItem>
              <ContactIcon>
                <FaBook />
              </ContactIcon>
              <ContactTitle>Educational Resource</ContactTitle>
              <ContactText>Learning platform for Kolam art and mathematics</ContactText>
            </ContactItem>
          </ContactGrid>
        </div>
      </ContactSection>
    </AboutContainer>
  );
}

export default About;

