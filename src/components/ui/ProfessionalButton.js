import React from 'react';
import styled, { css } from 'styled-components';
import { professionalDesignSystem as ds } from '../../styles/ProfessionalDesignSystem';

const StyledButton = styled.button`
  /* Base Styles */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: ${ds.spacing[2]};
  font-family: ${ds.typography.fontFamily.primary.join(', ')};
  font-weight: ${ds.typography.fontWeight.medium};
  text-decoration: none;
  border: none;
  cursor: pointer;
  outline: none;
  transition: all ${ds.animation.duration.normal} ${ds.animation.easing.easeInOut};
  position: relative;
  overflow: hidden;
  
  /* Focus Ring for Accessibility */
  &:focus-visible {
    outline: ${ds.accessibility.focusRing.width} ${ds.accessibility.focusRing.style} ${ds.colors.primary[500]};
    outline-offset: ${ds.accessibility.focusRing.offset};
  }
  
  /* Disabled State */
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }

  /* Size Variants */
  ${props => props.size === 'xs' && css`
    padding: ${ds.spacing[1]} ${ds.spacing[3]};
    font-size: ${ds.typography.fontSize.xs[0]};
    border-radius: ${ds.borderRadius.sm};
    min-height: 2rem;
  `}
  
  ${props => props.size === 'sm' && css`
    padding: ${ds.spacing[2]} ${ds.spacing[4]};
    font-size: ${ds.typography.fontSize.sm[0]};
    border-radius: ${ds.borderRadius.md};
    min-height: 2.25rem;
  `}
  
  ${props => (!props.size || props.size === 'md') && css`
    padding: ${ds.spacing[3]} ${ds.spacing[6]};
    font-size: ${ds.typography.fontSize.base[0]};
    border-radius: ${ds.borderRadius.lg};
    min-height: 2.75rem;
  `}
  
  ${props => props.size === 'lg' && css`
    padding: ${ds.spacing[4]} ${ds.spacing[8]};
    font-size: ${ds.typography.fontSize.lg[0]};
    border-radius: ${ds.borderRadius.xl};
    min-height: 3.25rem;
  `}
  
  ${props => props.size === 'xl' && css`
    padding: ${ds.spacing[5]} ${ds.spacing[10]};
    font-size: ${ds.typography.fontSize.xl[0]};
    border-radius: ${ds.borderRadius['2xl']};
    min-height: 3.75rem;
  `}

  /* Variant Styles */
  ${props => (!props.variant || props.variant === 'primary') && css`
    background: linear-gradient(135deg, ${ds.colors.primary[500]} 0%, ${ds.colors.primary[600]} 100%);
    color: white;
    box-shadow: ${ds.boxShadow.md};
    
    &:hover:not(:disabled) {
      background: linear-gradient(135deg, ${ds.colors.primary[600]} 0%, ${ds.colors.primary[700]} 100%);
      transform: translateY(-2px);
      box-shadow: ${ds.boxShadow.lg};
    }
    
    &:active:not(:disabled) {
      transform: translateY(0);
      box-shadow: ${ds.boxShadow.md};
    }
  `}
  
  ${props => props.variant === 'secondary' && css`
    background: linear-gradient(135deg, ${ds.colors.secondary[500]} 0%, ${ds.colors.secondary[600]} 100%);
    color: white;
    box-shadow: ${ds.boxShadow.md};
    
    &:hover:not(:disabled) {
      background: linear-gradient(135deg, ${ds.colors.secondary[600]} 0%, ${ds.colors.secondary[700]} 100%);
      transform: translateY(-2px);
      box-shadow: ${ds.boxShadow.lg};
    }
    
    &:active:not(:disabled) {
      transform: translateY(0);
      box-shadow: ${ds.boxShadow.md};
    }
  `}
  
  ${props => props.variant === 'outline' && css`
    background: transparent;
    color: ${ds.colors.primary[600]};
    border: 2px solid ${ds.colors.primary[500]};
    box-shadow: none;
    
    &:hover:not(:disabled) {
      background: ${ds.colors.primary[500]};
      color: white;
      transform: translateY(-1px);
      box-shadow: ${ds.boxShadow.md};
    }
    
    &:active:not(:disabled) {
      transform: translateY(0);
    }
  `}
  
  ${props => props.variant === 'ghost' && css`
    background: transparent;
    color: ${ds.colors.neutral[700]};
    border: none;
    box-shadow: none;
    
    &:hover:not(:disabled) {
      background: ${ds.colors.neutral[100]};
      transform: translateY(-1px);
    }
    
    &:active:not(:disabled) {
      background: ${ds.colors.neutral[200]};
      transform: translateY(0);
    }
  `}
  
  ${props => props.variant === 'cultural' && css`
    background: linear-gradient(135deg, ${ds.colors.festivals.diwali.primary} 0%, ${ds.colors.secondary[500]} 100%);
    color: white;
    box-shadow: ${ds.boxShadow.cultural.warm};
    border-radius: ${ds.borderRadius.kolam};
    
    &:hover:not(:disabled) {
      background: linear-gradient(135deg, ${ds.colors.secondary[500]} 0%, ${ds.colors.festivals.diwali.primary} 100%);
      transform: translateY(-2px);
      box-shadow: ${ds.boxShadow.cultural.golden};
    }
    
    &:active:not(:disabled) {
      transform: translateY(0);
      box-shadow: ${ds.boxShadow.cultural.warm};
    }
  `}
  
  ${props => props.variant === 'success' && css`
    background: linear-gradient(135deg, ${ds.colors.semantic.success[500]} 0%, ${ds.colors.accent.emerald[600]} 100%);
    color: white;
    box-shadow: ${ds.boxShadow.md};
    
    &:hover:not(:disabled) {
      background: linear-gradient(135deg, ${ds.colors.accent.emerald[600]} 0%, ${ds.colors.accent.emerald[700]} 100%);
      transform: translateY(-2px);
      box-shadow: ${ds.boxShadow.lg};
    }
  `}
  
  ${props => props.variant === 'warning' && css`
    background: linear-gradient(135deg, ${ds.colors.semantic.warning[500]} 0%, ${ds.colors.secondary[600]} 100%);
    color: white;
    box-shadow: ${ds.boxShadow.md};
    
    &:hover:not(:disabled) {
      background: linear-gradient(135deg, ${ds.colors.secondary[600]} 0%, ${ds.colors.secondary[700]} 100%);
      transform: translateY(-2px);
      box-shadow: ${ds.boxShadow.lg};
    }
  `}
  
  ${props => props.variant === 'error' && css`
    background: linear-gradient(135deg, ${ds.colors.semantic.error[500]} 0%, ${ds.colors.accent.ruby[600]} 100%);
    color: white;
    box-shadow: ${ds.boxShadow.md};
    
    &:hover:not(:disabled) {
      background: linear-gradient(135deg, ${ds.colors.accent.ruby[600]} 0%, ${ds.colors.accent.ruby[700]} 100%);
      transform: translateY(-2px);
      box-shadow: ${ds.boxShadow.lg};
    }
  `}

  /* Loading State */
  ${props => props.loading && css`
    color: transparent;
    position: relative;
    
    &::after {
      content: '';
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 1rem;
      height: 1rem;
      border: 2px solid transparent;
      border-top: 2px solid currentColor;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      color: white;
    }
    
    @keyframes spin {
      to {
        transform: translate(-50%, -50%) rotate(360deg);
      }
    }
  `}

  /* Full Width */
  ${props => props.fullWidth && css`
    width: 100%;
  `}

  /* Icon Only */
  ${props => props.iconOnly && css`
    padding: ${ds.spacing[3]};
    aspect-ratio: 1;
    min-width: auto;
  `}
  
  /* Reduce motion for accessibility */
  @media (prefers-reduced-motion: reduce) {
    transition: color ${ds.animation.duration.fast} ease;
    
    &:hover:not(:disabled) {
      transform: none;
    }
  }
`;

const IconWrapper = styled.span`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  
  ${props => props.iconPosition === 'left' && css`
    margin-right: ${ds.spacing[1]};
  `}
  
  ${props => props.iconPosition === 'right' && css`
    margin-left: ${ds.spacing[1]};
  `}
`;

const ProfessionalButton = React.forwardRef(({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  fullWidth = false,
  iconOnly = false,
  leftIcon,
  rightIcon,
  className,
  ...props
}, ref) => {
  return (
    <StyledButton
      ref={ref}
      variant={variant}
      size={size}
      loading={loading}
      disabled={disabled || loading}
      fullWidth={fullWidth}
      iconOnly={iconOnly}
      className={className}
      {...props}
    >
      {leftIcon && (
        <IconWrapper iconPosition="left">
          {leftIcon}
        </IconWrapper>
      )}
      
      {!iconOnly && children}
      {iconOnly && !children && (leftIcon || rightIcon)}
      
      {rightIcon && !iconOnly && (
        <IconWrapper iconPosition="right">
          {rightIcon}
        </IconWrapper>
      )}
    </StyledButton>
  );
});

ProfessionalButton.displayName = 'ProfessionalButton';

export default ProfessionalButton;


















