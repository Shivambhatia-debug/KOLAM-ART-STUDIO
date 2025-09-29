import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import styled, { css } from 'styled-components';
import { 
  FaHome, FaPalette, FaChartLine, FaInfoCircle, FaBars, FaTimes,
  FaSearch, FaMoon, FaSun, FaCog, FaGlobe, FaImage
} from 'react-icons/fa';
import { professionalDesignSystem as ds } from '../styles/ProfessionalDesignSystem';
import ProfessionalButton from './ui/ProfessionalButton';

const HeaderContainer = styled.header`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: ${ds.zIndex.sticky};
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid ${ds.colors.neutral[200]};
  box-shadow: ${ds.boxShadow.sm};
  transition: all ${ds.animation.duration.normal} ${ds.animation.easing.easeInOut};
  
  ${props => props.scrolled && css`
    background: rgba(255, 255, 255, 0.98);
    box-shadow: ${ds.boxShadow.md};
  `}
`;

const HeaderContent = styled.div`
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 ${ds.spacing[4]};
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
  
  @media (min-width: ${ds.breakpoints.lg}) {
    padding: 0 ${ds.spacing[8]};
  }
`;

const Brand = styled(Link)`
  display: flex;
  align-items: center;
  gap: ${ds.spacing[3]};
  text-decoration: none;
  color: ${ds.colors.neutral[900]};
  font-weight: ${ds.typography.fontWeight.bold};
  font-size: ${ds.typography.fontSize.xl[0]};
  transition: all ${ds.animation.duration.fast} ${ds.animation.easing.easeInOut};
  
  &:hover {
    color: ${ds.colors.primary[600]};
    transform: scale(1.02);
  }
  
  &:focus-visible {
    outline: ${ds.accessibility.focusRing.width} ${ds.accessibility.focusRing.style} ${ds.colors.primary[500]};
    outline-offset: ${ds.accessibility.focusRing.offset};
    border-radius: ${ds.borderRadius.md};
  }
`;

const BrandIcon = styled.div`
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, ${ds.colors.primary[500]} 0%, ${ds.colors.secondary[500]} 100%);
  border-radius: ${ds.borderRadius.kolam};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
  box-shadow: ${ds.boxShadow.md};
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, 
      transparent 30%, 
      rgba(255, 255, 255, 0.2) 50%, 
      transparent 70%
    );
    transform: translateX(-100%);
    transition: transform ${ds.animation.duration.slow} ${ds.animation.easing.easeInOut};
  }
  
  ${Brand}:hover &::before {
    transform: translateX(100%);
  }
`;

const BrandText = styled.div`
  display: flex;
  flex-direction: column;
  
  .main {
    font-family: ${ds.typography.fontFamily.heading.join(', ')};
    font-size: ${ds.typography.fontSize.lg[0]};
    font-weight: ${ds.typography.fontWeight.bold};
    line-height: 1;
  }
  
  .sub {
    font-size: ${ds.typography.fontSize.xs[0]};
    color: ${ds.colors.neutral[600]};
    font-weight: ${ds.typography.fontWeight.medium};
    letter-spacing: ${ds.typography.letterSpacing.wide};
    text-transform: uppercase;
  }
`;

const Navigation = styled.nav`
  display: none;
  align-items: center;
  gap: ${ds.spacing[2]};
  
  @media (min-width: ${ds.breakpoints.lg}) {
    display: flex;
  }
`;

const NavLink = styled(Link)`
  display: flex;
  align-items: center;
  gap: ${ds.spacing[2]};
  padding: ${ds.spacing[3]} ${ds.spacing[4]};
  border-radius: ${ds.borderRadius.lg};
  text-decoration: none;
  color: ${ds.colors.neutral[700]};
  font-weight: ${ds.typography.fontWeight.medium};
  font-size: ${ds.typography.fontSize.sm[0]};
  transition: all ${ds.animation.duration.fast} ${ds.animation.easing.easeInOut};
  position: relative;
  
  &:hover {
    color: ${ds.colors.primary[600]};
    background: ${ds.colors.primary[50]};
    transform: translateY(-1px);
  }
  
  &:focus-visible {
    outline: ${ds.accessibility.focusRing.width} ${ds.accessibility.focusRing.style} ${ds.colors.primary[500]};
    outline-offset: ${ds.accessibility.focusRing.offset};
  }
  
  ${props => props.active && css`
    color: ${ds.colors.primary[600]};
    background: ${ds.colors.primary[100]};
    
    &::after {
      content: '';
      position: absolute;
      bottom: -8px;
      left: 50%;
      transform: translateX(-50%);
      width: 6px;
      height: 6px;
      background: ${ds.colors.primary[500]};
      border-radius: 50%;
    }
  `}
`;

const HeaderActions = styled.div`
  display: flex;
  align-items: center;
  gap: ${ds.spacing[2]};
`;

const SearchContainer = styled.div`
  position: relative;
  display: none;
  
  @media (min-width: ${ds.breakpoints.md}) {
    display: block;
  }
`;

const SearchInput = styled.input`
  width: 240px;
  padding: ${ds.spacing[2]} ${ds.spacing[3]} ${ds.spacing[2]} ${ds.spacing[10]};
  border: 2px solid ${ds.colors.neutral[200]};
  border-radius: ${ds.borderRadius.full};
  background: ${ds.colors.neutral[50]};
  font-size: ${ds.typography.fontSize.sm[0]};
  transition: all ${ds.animation.duration.fast} ${ds.animation.easing.easeInOut};
  
  &::placeholder {
    color: ${ds.colors.neutral[500]};
  }
  
  &:focus {
    outline: none;
    border-color: ${ds.colors.primary[400]};
    background: white;
    box-shadow: 0 0 0 3px rgba(255, 193, 7, 0.1);
    width: 280px;
  }
`;

const SearchIcon = styled(FaSearch)`
  position: absolute;
  left: ${ds.spacing[3]};
  top: 50%;
  transform: translateY(-50%);
  color: ${ds.colors.neutral[500]};
  font-size: ${ds.typography.fontSize.sm[0]};
`;

const ThemeToggle = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: ${ds.borderRadius.lg};
  background: ${ds.colors.neutral[100]};
  color: ${ds.colors.neutral[700]};
  cursor: pointer;
  transition: all ${ds.animation.duration.fast} ${ds.animation.easing.easeInOut};
  
  &:hover {
    background: ${ds.colors.neutral[200]};
    color: ${ds.colors.primary[600]};
    transform: scale(1.05);
  }
  
  &:focus-visible {
    outline: ${ds.accessibility.focusRing.width} ${ds.accessibility.focusRing.style} ${ds.colors.primary[500]};
    outline-offset: ${ds.accessibility.focusRing.offset};
  }
`;

const MobileMenuButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: ${ds.borderRadius.lg};
  background: ${ds.colors.neutral[100]};
  color: ${ds.colors.neutral[700]};
  cursor: pointer;
  transition: all ${ds.animation.duration.fast} ${ds.animation.easing.easeInOut};
  
  @media (min-width: ${ds.breakpoints.lg}) {
    display: none;
  }
  
  &:hover {
    background: ${ds.colors.neutral[200]};
    color: ${ds.colors.primary[600]};
  }
  
  &:focus-visible {
    outline: ${ds.accessibility.focusRing.width} ${ds.accessibility.focusRing.style} ${ds.colors.primary[500]};
    outline-offset: ${ds.accessibility.focusRing.offset};
  }
`;

const MobileMenu = styled.div`
  position: fixed;
  top: 72px;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid ${ds.colors.neutral[200]};
  padding: ${ds.spacing[4]};
  transform: translateY(-100%);
  opacity: 0;
  visibility: hidden;
  transition: all ${ds.animation.duration.normal} ${ds.animation.easing.easeInOut};
  
  ${props => props.isOpen && css`
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
  `}
  
  @media (min-width: ${ds.breakpoints.lg}) {
    display: none;
  }
`;

const MobileNavList = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${ds.spacing[2]};
  max-width: 400px;
  margin: 0 auto;
`;

const MobileNavLink = styled(Link)`
  display: flex;
  align-items: center;
  gap: ${ds.spacing[3]};
  padding: ${ds.spacing[4]} ${ds.spacing[6]};
  border-radius: ${ds.borderRadius.xl};
  text-decoration: none;
  color: ${ds.colors.neutral[700]};
  font-weight: ${ds.typography.fontWeight.medium};
  background: ${ds.colors.neutral[50]};
  transition: all ${ds.animation.duration.fast} ${ds.animation.easing.easeInOut};
  
  &:hover {
    color: ${ds.colors.primary[600]};
    background: ${ds.colors.primary[50]};
    transform: translateX(8px);
  }
  
  ${props => props.active && css`
    color: ${ds.colors.primary[600]};
    background: ${ds.colors.primary[100]};
    border-left: 4px solid ${ds.colors.primary[500]};
  `}
`;

const CulturalIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: ${ds.spacing[2]};
  padding: ${ds.spacing[2]} ${ds.spacing[3]};
  background: linear-gradient(135deg, ${ds.colors.festivals.diwali.primary} 0%, ${ds.colors.secondary[500]} 100%);
  color: white;
  border-radius: ${ds.borderRadius.full};
  font-size: ${ds.typography.fontSize.xs[0]};
  font-weight: ${ds.typography.fontWeight.medium};
`;

const ProfessionalHeader = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const location = useLocation();

  // Handle scroll effect
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Close mobile menu when route changes
  useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [location.pathname]);

  const navigationItems = [
    { path: '/', label: 'Home', icon: FaHome },
    { path: '/kolam-studio', label: 'Studio', icon: FaPalette },
    { path: '/image-analysis', label: 'Image Analysis', icon: FaImage },
    { path: '/pattern-gallery', label: 'Gallery', icon: FaGlobe },
    { path: '/analysis', label: 'Analysis', icon: FaChartLine },
    { path: '/ai-diffusion', label: 'AI Diffusion', icon: FaCog },
    { path: '/about', label: 'About', icon: FaInfoCircle }
  ];

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
    // Theme implementation would go here
  };

  return (
    <>
      <HeaderContainer scrolled={isScrolled}>
        <HeaderContent>
          {/* Brand */}
          <Brand to="/">
            <BrandIcon>
              🎨
            </BrandIcon>
            <BrandText>
              <div className="main">Kolam Studio</div>
              <div className="sub">Research Based</div>
            </BrandText>
          </Brand>

          {/* Desktop Navigation */}
          <Navigation>
            {navigationItems.map(({ path, label, icon: Icon }) => (
              <NavLink
                key={path}
                to={path}
                active={location.pathname === path}
              >
                <Icon size={16} />
                {label}
              </NavLink>
            ))}
          </Navigation>

          {/* Header Actions */}
          <HeaderActions>
            {/* Search */}
            <SearchContainer>
              <SearchIcon />
              <SearchInput 
                type="text" 
                placeholder="Search patterns, regions..."
                aria-label="Search Kolam patterns"
              />
            </SearchContainer>

            {/* Cultural Indicator */}
            <CulturalIndicator>
              <FaGlobe size={12} />
              Tamil Nadu
            </CulturalIndicator>

            {/* Theme Toggle */}
            <ThemeToggle 
              onClick={toggleTheme}
              aria-label={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {isDarkMode ? <FaSun size={18} /> : <FaMoon size={18} />}
            </ThemeToggle>

            {/* Settings */}
            <ProfessionalButton
              variant="ghost"
              size="sm"
              iconOnly
              aria-label="Settings"
            >
              <FaCog size={18} />
            </ProfessionalButton>

            {/* Mobile Menu Button */}
            <MobileMenuButton 
              onClick={toggleMobileMenu}
              aria-label="Toggle mobile menu"
              aria-expanded={isMobileMenuOpen}
            >
              {isMobileMenuOpen ? <FaTimes size={18} /> : <FaBars size={18} />}
            </MobileMenuButton>
          </HeaderActions>
        </HeaderContent>
      </HeaderContainer>

      {/* Mobile Menu */}
      <MobileMenu isOpen={isMobileMenuOpen}>
        <MobileNavList>
          {navigationItems.map(({ path, label, icon: Icon }) => (
            <MobileNavLink
              key={path}
              to={path}
              active={location.pathname === path}
            >
              <Icon size={20} />
              {label}
            </MobileNavLink>
          ))}
        </MobileNavList>
      </MobileMenu>
    </>
  );
};

export default ProfessionalHeader;



















