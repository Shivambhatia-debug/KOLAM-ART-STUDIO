import React from 'react';
import styled, { css } from 'styled-components';
import { professionalDesignSystem as ds } from '../../styles/ProfessionalDesignSystem';

const StyledCard = styled.div`
  /* Base Styles */
  display: flex;
  flex-direction: column;
  position: relative;
  transition: all ${ds.animation.duration.normal} ${ds.animation.easing.easeInOut};
  
  /* Variant Styles */
  ${props => (!props.variant || props.variant === 'elevated') && css`
    background: white;
    box-shadow: ${ds.boxShadow.lg};
    border-radius: ${ds.borderRadius['2xl']};
    border: 1px solid ${ds.colors.neutral[200]};
    
    &:hover {
      box-shadow: ${ds.boxShadow.xl};
      transform: translateY(-4px);
    }
  `}
  
  ${props => props.variant === 'outline' && css`
    background: white;
    border: 2px solid ${ds.colors.neutral[300]};
    border-radius: ${ds.borderRadius.xl};
    box-shadow: none;
    
    &:hover {
      border-color: ${ds.colors.primary[300]};
      box-shadow: ${ds.boxShadow.md};
    }
  `}
  
  ${props => props.variant === 'filled' && css`
    background: ${ds.colors.neutral[50]};
    border-radius: ${ds.borderRadius.xl};
    border: 1px solid ${ds.colors.neutral[200]};
    
    &:hover {
      background: white;
      box-shadow: ${ds.boxShadow.md};
    }
  `}
  
  ${props => props.variant === 'cultural' && css`
    background: white;
    box-shadow: ${ds.boxShadow.cultural.golden};
    border-radius: ${ds.borderRadius.kolam};
    border: 2px solid ${ds.colors.primary[200]};
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, 
        ${ds.colors.primary[500]} 0%, 
        ${ds.colors.secondary[500]} 50%, 
        ${ds.colors.accent.emerald[500]} 100%
      );
    }
    
    &:hover {
      box-shadow: ${ds.boxShadow.cultural.sacred};
      transform: translateY(-3px);
      border-color: ${ds.colors.primary[400]};
    }
  `}
  
  ${props => props.variant === 'glass' && css`
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: ${ds.borderRadius['2xl']};
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    
    &:hover {
      background: rgba(255, 255, 255, 0.8);
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
  `}
  
  ${props => props.variant === 'gradient' && css`
    background: linear-gradient(135deg, 
      rgba(255, 193, 7, 0.1) 0%, 
      rgba(255, 152, 0, 0.1) 100%
    );
    border: 1px solid ${ds.colors.primary[200]};
    border-radius: ${ds.borderRadius['2xl']};
    
    &:hover {
      background: linear-gradient(135deg, 
        rgba(255, 193, 7, 0.15) 0%, 
        rgba(255, 152, 0, 0.15) 100%
      );
      border-color: ${ds.colors.primary[300]};
    }
  `}

  /* Interactive States */
  ${props => props.interactive && css`
    cursor: pointer;
    
    &:active {
      transform: translateY(-1px);
    }
  `}

  /* Size Variants */
  ${props => props.size === 'sm' && css`
    padding: ${ds.spacing[4]};
  `}
  
  ${props => (!props.size || props.size === 'md') && css`
    padding: ${ds.spacing[6]};
  `}
  
  ${props => props.size === 'lg' && css`
    padding: ${ds.spacing[8]};
  `}

  /* Focus for accessibility */
  ${props => props.interactive && css`
    &:focus-visible {
      outline: ${ds.accessibility.focusRing.width} ${ds.accessibility.focusRing.style} ${ds.colors.primary[500]};
      outline-offset: ${ds.accessibility.focusRing.offset};
    }
  `}
  
  /* Reduce motion for accessibility */
  @media (prefers-reduced-motion: reduce) {
    transition: box-shadow ${ds.animation.duration.fast} ease;
    
    &:hover {
      transform: none;
    }
  }
`;

const CardHeader = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${ds.spacing[2]};
  margin-bottom: ${ds.spacing[4]};
  
  ${props => props.withDivider && css`
    padding-bottom: ${ds.spacing[4]};
    border-bottom: 1px solid ${ds.colors.neutral[200]};
  `}
`;

const CardTitle = styled.h3`
  font-family: ${ds.typography.fontFamily.heading.join(', ')};
  font-size: ${ds.typography.fontSize.xl[0]};
  font-weight: ${ds.typography.fontWeight.bold};
  color: ${ds.colors.neutral[900]};
  margin: 0;
  line-height: ${ds.typography.lineHeight.tight};
`;

const CardSubtitle = styled.p`
  font-size: ${ds.typography.fontSize.sm[0]};
  color: ${ds.colors.neutral[600]};
  margin: 0;
  line-height: ${ds.typography.lineHeight.normal};
`;

const CardContent = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: ${ds.spacing[3]};
`;

const CardFooter = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: ${ds.spacing[3]};
  margin-top: ${ds.spacing[4]};
  
  ${props => props.withDivider && css`
    padding-top: ${ds.spacing[4]};
    border-top: 1px solid ${ds.colors.neutral[200]};
  `}
  
  ${props => props.center && css`
    justify-content: center;
  `}
  
  ${props => props.end && css`
    justify-content: flex-end;
  `}
`;

const CardImage = styled.div`
  position: relative;
  border-radius: ${ds.borderRadius.lg};
  overflow: hidden;
  margin-bottom: ${ds.spacing[4]};
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform ${ds.animation.duration.normal} ${ds.animation.easing.easeInOut};
  }
  
  ${props => props.aspectRatio && css`
    aspect-ratio: ${props.aspectRatio};
  `}
  
  ${props => props.height && css`
    height: ${props.height};
  `}
  
  &:hover img {
    transform: scale(1.05);
  }
`;

const CardBadge = styled.span`
  position: absolute;
  top: ${ds.spacing[3]};
  right: ${ds.spacing[3]};
  background: ${ds.colors.primary[500]};
  color: white;
  padding: ${ds.spacing[1]} ${ds.spacing[3]};
  border-radius: ${ds.borderRadius.full};
  font-size: ${ds.typography.fontSize.xs[0]};
  font-weight: ${ds.typography.fontWeight.medium};
  z-index: 10;
  
  ${props => props.variant === 'success' && css`
    background: ${ds.colors.semantic.success[500]};
  `}
  
  ${props => props.variant === 'warning' && css`
    background: ${ds.colors.semantic.warning[500]};
  `}
  
  ${props => props.variant === 'error' && css`
    background: ${ds.colors.semantic.error[500]};
  `}
  
  ${props => props.variant === 'cultural' && css`
    background: linear-gradient(135deg, ${ds.colors.festivals.diwali.primary} 0%, ${ds.colors.secondary[500]} 100%);
  `}
`;

// Main Card Component
const ProfessionalCard = React.forwardRef(({
  children,
  variant = 'elevated',
  size = 'md',
  interactive = false,
  className,
  onClick,
  ...props
}, ref) => {
  return (
    <StyledCard
      ref={ref}
      variant={variant}
      size={size}
      interactive={interactive || !!onClick}
      onClick={onClick}
      className={className}
      tabIndex={interactive || onClick ? 0 : undefined}
      role={interactive || onClick ? 'button' : undefined}
      {...props}
    >
      {children}
    </StyledCard>
  );
});

// Compound Components
ProfessionalCard.Header = CardHeader;
ProfessionalCard.Title = CardTitle;
ProfessionalCard.Subtitle = CardSubtitle;
ProfessionalCard.Content = CardContent;
ProfessionalCard.Footer = CardFooter;
ProfessionalCard.Image = CardImage;
ProfessionalCard.Badge = CardBadge;

ProfessionalCard.displayName = 'ProfessionalCard';

export default ProfessionalCard;





