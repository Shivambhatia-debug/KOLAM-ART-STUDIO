import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import styled from 'styled-components';
import { FaPalette, FaHome, FaCog, FaImages, FaChartLine, FaInfoCircle, FaBars, FaTimes } from 'react-icons/fa';

const HeaderContainer = styled.header`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  padding: 0 1rem;
`;

const Nav = styled.nav`
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 80px;
`;

const Logo = styled(Link)`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: white;
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: 700;
  
  svg {
    font-size: 2rem;
  }
`;

const NavLinks = styled.div`
  display: flex;
  align-items: center;
  gap: 2rem;

  @media (max-width: 768px) {
    display: ${props => props.isOpen ? 'flex' : 'none'};
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    flex-direction: column;
    padding: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    gap: 1rem;
  }
`;

const NavLink = styled(Link)`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: ${props => props.active ? '#FBBF24' : 'white'};
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
  
  &:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: #FBBF24;
  }

  @media (max-width: 768px) {
    color: ${props => props.active ? '#8B5CF6' : '#374151'};
    width: 100%;
    justify-content: center;
  }
`;

const MobileMenuButton = styled.button`
  display: none;
  background: none;
  color: white;
  font-size: 1.5rem;
  padding: 0.5rem;

  @media (max-width: 768px) {
    display: block;
  }
`;

const ProblemStatement = styled.div`
  background: rgba(255, 255, 255, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  color: white;
  text-align: center;
  margin-left: 1rem;

  @media (max-width: 768px) {
    display: none;
  }
`;

function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);

  const navItems = [
    { path: '/', label: 'Home', icon: FaHome },
    { path: '/studio', label: 'Kolam Studio', icon: FaPalette },
    { path: '/gallery', label: 'Gallery', icon: FaImages },
    { path: '/analysis', label: 'Analysis', icon: FaChartLine },
    { path: '/about', label: 'About', icon: FaInfoCircle }
  ];

  return (
    <HeaderContainer>
      <Nav>
        <Logo to="/">
          <FaPalette />
          Kolam Art Studio
        </Logo>
        
        <NavLinks isOpen={isMenuOpen}>
          {navItems.map(({ path, label, icon: Icon }) => (
            <NavLink
              key={path}
              to={path}
              active={location.pathname === path ? 1 : 0}
              onClick={() => setIsMenuOpen(false)}
            >
              <Icon />
              {label}
            </NavLink>
          ))}
        </NavLinks>

        <ProblemStatement>
          AICTE Problem Statement 25107
        </ProblemStatement>

        <MobileMenuButton onClick={toggleMenu}>
          {isMenuOpen ? <FaTimes /> : <FaBars />}
        </MobileMenuButton>
      </Nav>
    </HeaderContainer>
  );
}

export default Header;

