import React, { useState } from 'react';
import styled from 'styled-components';
import { FaSearch, FaFilter, FaDownload, FaHeart, FaShare, FaInfoCircle, FaImages, FaCircle, FaRuler } from 'react-icons/fa';

const GalleryContainer = styled.div`
  padding: 2rem 0;
`;

const GalleryHeader = styled.div`
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

const SearchAndFilter = styled.div`
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
`;

const SearchInput = styled.div`
  position: relative;
  flex: 1;
  min-width: 300px;
`;

const SearchField = styled.input`
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 2px solid ${props => props.theme.colors.border};
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.2s ease;

  &:focus {
    border-color: ${props => props.theme.colors.primary};
  }
`;

const SearchIcon = styled(FaSearch)`
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: ${props => props.theme.colors.textSecondary};
`;

const FilterSelect = styled.select`
  padding: 0.75rem 1rem;
  border: 2px solid ${props => props.theme.colors.border};
  border-radius: 0.5rem;
  font-size: 1rem;
  background: white;
  min-width: 150px;

  &:focus {
    border-color: ${props => props.theme.colors.primary};
  }
`;

const GalleryGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
`;

const PatternCard = styled.div`
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  }
`;

const PatternImage = styled.div`
  height: 200px;
  background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
`;

const PatternPreview = styled.div`
  width: 150px;
  height: 150px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: ${props => props.theme.colors.primary};
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
`;

const PatternOverlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  opacity: 0;
  transition: opacity 0.2s ease;

  ${PatternCard}:hover & {
    opacity: 1;
  }
`;

const OverlayButton = styled.button`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: white;
  color: ${props => props.theme.colors.text};
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s ease;

  &:hover {
    background: ${props => props.theme.colors.primary};
    color: white;
    transform: translateY(-1px);
  }
`;

const PatternInfo = styled.div`
  padding: 1.5rem;
`;

const PatternTitle = styled.h3`
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: ${props => props.theme.colors.text};
`;

const PatternDescription = styled.p`
  color: ${props => props.theme.colors.textSecondary};
  margin-bottom: 1rem;
  line-height: 1.5;
`;

const PatternMeta = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
`;

const PatternType = styled.span`
  background: ${props => props.theme.colors.primary};
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
`;

const PatternRegion = styled.span`
  background: ${props => props.theme.colors.secondary};
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
`;

const PatternStats = styled.div`
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: ${props => props.theme.colors.textSecondary};
`;

const StatItem = styled.div`
  display: flex;
  align-items: center;
  gap: 0.25rem;
`;

const CulturalInfo = styled.div`
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  padding: 1rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
  border-left: 4px solid #F59E0B;
`;

const CulturalTitle = styled.h4`
  font-size: 0.875rem;
  font-weight: 600;
  color: #92400E;
  margin-bottom: 0.5rem;
`;

const CulturalText = styled.p`
  font-size: 0.75rem;
  color: #92400E;
  line-height: 1.4;
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

function PatternGallery({ onPatternSelect }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterRegion, setFilterRegion] = useState('all');

  const patterns = [
    {
      id: 1,
      title: 'Traditional Radial Kolam',
      description: 'Classic Tamil Nadu style with radial symmetry and continuous lines',
      type: 'Radial',
      region: 'Tamil Nadu',
      complexity: 'High',
      points: 25,
      lines: 18,
      culturalSignificance: 'Used in daily rituals and festivals, represents cosmic order and harmony',
      preview: '⚪'
    },
    {
      id: 2,
      title: 'Geometric Muggu Pattern',
      description: 'Karnataka style with precise geometric shapes and bilateral symmetry',
      type: 'Bilateral',
      region: 'Karnataka',
      complexity: 'Medium',
      points: 16,
      lines: 24,
      culturalSignificance: 'Mathematical precision reflects the region\'s engineering traditions',
      preview: '⬜'
    },
    {
      id: 3,
      title: 'Floral Rangoli Design',
      description: 'Andhra Pradesh style with rotational symmetry and nature-inspired motifs',
      type: 'Rotational',
      region: 'Andhra Pradesh',
      complexity: 'High',
      points: 36,
      lines: 28,
      culturalSignificance: 'Celebrates nature and agricultural traditions of the region',
      preview: '🌸'
    },
    {
      id: 4,
      title: 'Free-form Kerala Pattern',
      description: 'Asymmetric design with organic flow and natural inspiration',
      type: 'Asymmetric',
      region: 'Kerala',
      complexity: 'Medium',
      points: 20,
      lines: 15,
      culturalSignificance: 'Represents the natural flow and organic beauty of Kerala',
      preview: '🌿'
    },
    {
      id: 5,
      title: 'Fractal Kolam Pattern',
      description: 'Self-similar pattern with recursive geometric elements',
      type: 'Fractal',
      region: 'Modern',
      complexity: 'Very High',
      points: 64,
      lines: 32,
      culturalSignificance: 'Demonstrates mathematical beauty and infinite complexity',
      preview: '🌀'
    },
    {
      id: 6,
      title: 'Sikku Kolam Design',
      description: 'Single continuous line pattern with intricate curves',
      type: 'Continuous',
      region: 'Tamil Nadu',
      complexity: 'Very High',
      points: 12,
      lines: 1,
      culturalSignificance: 'Represents the unbroken flow of life and energy',
      preview: '🔄'
    }
  ];

  const filteredPatterns = patterns.filter(pattern => {
    const matchesSearch = pattern.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         pattern.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = filterType === 'all' || pattern.type.toLowerCase() === filterType.toLowerCase();
    const matchesRegion = filterRegion === 'all' || pattern.region.toLowerCase() === filterRegion.toLowerCase();
    
    return matchesSearch && matchesType && matchesRegion;
  });

  const handlePatternSelect = (pattern) => {
    onPatternSelect && onPatternSelect(pattern);
  };

  return (
    <GalleryContainer>
      <div className="container">
        <GalleryHeader>
          <Title>
            <FaImages />
            Pattern Gallery
          </Title>
          <Subtitle>
            Explore traditional Kolam patterns from different regions of India, 
            each with unique cultural significance and mathematical beauty.
          </Subtitle>
          
          <SearchAndFilter>
            <SearchInput>
              <SearchIcon />
              <SearchField
                type="text"
                placeholder="Search patterns..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </SearchInput>
            
            <FilterSelect
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
            >
              <option value="all">All Types</option>
              <option value="radial">Radial</option>
              <option value="bilateral">Bilateral</option>
              <option value="rotational">Rotational</option>
              <option value="asymmetric">Asymmetric</option>
              <option value="fractal">Fractal</option>
              <option value="continuous">Continuous</option>
            </FilterSelect>
            
            <FilterSelect
              value={filterRegion}
              onChange={(e) => setFilterRegion(e.target.value)}
            >
              <option value="all">All Regions</option>
              <option value="tamil nadu">Tamil Nadu</option>
              <option value="karnataka">Karnataka</option>
              <option value="andhra pradesh">Andhra Pradesh</option>
              <option value="kerala">Kerala</option>
              <option value="modern">Modern</option>
            </FilterSelect>
          </SearchAndFilter>
        </GalleryHeader>

        {filteredPatterns.length === 0 ? (
          <EmptyState>
            <EmptyIcon>🔍</EmptyIcon>
            <h3>No patterns found</h3>
            <p>Try adjusting your search or filter criteria</p>
          </EmptyState>
        ) : (
          <GalleryGrid>
            {filteredPatterns.map(pattern => (
              <PatternCard key={pattern.id} onClick={() => handlePatternSelect(pattern)}>
                <PatternImage>
                  <PatternPreview>{pattern.preview}</PatternPreview>
                  <PatternOverlay>
                    <OverlayButton onClick={(e) => {
                      e.stopPropagation();
                      handlePatternSelect(pattern);
                    }}>
                      <FaInfoCircle />
                      View Details
                    </OverlayButton>
                    <OverlayButton onClick={(e) => {
                      e.stopPropagation();
                      // Handle download
                    }}>
                      <FaDownload />
                      Download
                    </OverlayButton>
                  </PatternOverlay>
                </PatternImage>
                
                <PatternInfo>
                  <PatternTitle>{pattern.title}</PatternTitle>
                  <PatternDescription>{pattern.description}</PatternDescription>
                  
                  <PatternMeta>
                    <PatternType>{pattern.type}</PatternType>
                    <PatternRegion>{pattern.region}</PatternRegion>
                  </PatternMeta>
                  
                  <PatternStats>
                    <StatItem>
                      <FaCircle style={{fontSize: '0.5rem'}} />
                      {pattern.points} points
                    </StatItem>
                    <StatItem>
                      <FaRuler style={{fontSize: '0.5rem'}} />
                      {pattern.lines} lines
                    </StatItem>
                    <StatItem>
                      <FaHeart style={{fontSize: '0.5rem'}} />
                      {pattern.complexity}
                    </StatItem>
                  </PatternStats>
                  
                  <CulturalInfo>
                    <CulturalTitle>Cultural Significance</CulturalTitle>
                    <CulturalText>{pattern.culturalSignificance}</CulturalText>
                  </CulturalInfo>
                </PatternInfo>
              </PatternCard>
            ))}
          </GalleryGrid>
        )}
      </div>
    </GalleryContainer>
  );
}

export default PatternGallery;
