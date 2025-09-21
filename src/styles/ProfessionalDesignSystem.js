/*
Professional Kolam Design System
===============================

Comprehensive design system based on:
- Material Design 3.0 principles
- Cultural Indian aesthetics  
- Accessibility standards (WCAG 2.1 AA)
- Research-based color psychology
- Traditional Kolam visual elements
*/

export const professionalDesignSystem = {
  // Cultural Color Palettes (Research-Based)
  colors: {
    // Primary Brand Colors (inspired by traditional Kolam)
    primary: {
      50: '#FFF8E1',   // Lightest turmeric
      100: '#FFECB3',  // Light turmeric
      200: '#FFE082',  // Turmeric
      300: '#FFD54F',  // Medium turmeric
      400: '#FFCA28',  // Rich turmeric
      500: '#FFC107',  // Primary turmeric (brand)
      600: '#FFB300',  // Deep turmeric
      700: '#FFA000',  // Darker turmeric
      800: '#FF8F00',  // Very dark turmeric
      900: '#FF6F00'   // Darkest turmeric
    },

    // Secondary Colors (Vermillion inspiration)
    secondary: {
      50: '#FFF3E0',   // Lightest vermillion
      100: '#FFE0B2',  // Light vermillion
      200: '#FFCC80',  // Soft vermillion
      300: '#FFB74D',  // Medium vermillion
      400: '#FFA726',  // Rich vermillion
      500: '#FF9800',  // Primary vermillion
      600: '#FB8C00',  // Deep vermillion
      700: '#F57C00',  // Darker vermillion
      800: '#EF6C00',  // Very dark vermillion
      900: '#E65100'   // Darkest vermillion
    },

    // Accent Colors (Cultural significance)
    accent: {
      emerald: {
        50: '#ECFDF5',   // Light emerald
        500: '#10B981',  // Prosperity green
        600: '#059669',
        700: '#047857'
      },
      ruby: {
        500: '#DC2626',  // Sacred red
        600: '#B91C1C',
        700: '#991B1B'
      },
      sapphire: {
        50: '#EFF6FF',   // Light blue
        500: '#3B82F6',  // Cosmic blue
        600: '#2563EB',
        700: '#1D4ED8'
      },
      amber: {
        50: '#FFFBEB',   // Light amber
        200: '#FDE68A',  // Medium amber
        500: '#F59E0B',  // Rich amber
        600: '#D97706',
        700: '#B45309'
      },
      lotus: {
        500: '#EC4899',  // Lotus pink
        600: '#DB2777',
        700: '#BE185D'
      }
    },

    // Neutral Palette (Modern + Cultural)
    neutral: {
      0: '#FFFFFF',      // Pure white (rice flour)
      50: '#FAFAF9',     // Off white
      100: '#F5F5F4',    // Light gray
      200: '#E7E5E4',    // Lighter gray
      300: '#D6D3D1',    // Light gray
      400: '#A8A29E',    // Medium gray
      500: '#78716C',    // Gray
      600: '#57534E',    // Dark gray
      700: '#44403C',    // Darker gray
      800: '#292524',    // Very dark gray
      900: '#1C1917',    // Almost black
      950: '#0C0A09'     // Pure black (charcoal)
    },

    // Semantic Colors (Cultural meanings)
    semantic: {
      success: {
        50: '#F0FDF4',
        500: '#22C55E',   // Prosperity green
        600: '#16A34A',
        700: '#15803D'
      },
      warning: {
        50: '#FFFBEB',
        500: '#F59E0B',   // Turmeric warning
        600: '#D97706',
        700: '#B45309'
      },
      error: {
        50: '#FEF2F2',
        500: '#EF4444',   // Alert red
        600: '#DC2626',
        700: '#B91C1C'
      },
      info: {
        50: '#EFF6FF',
        500: '#3B82F6',   // Information blue
        600: '#2563EB',
        700: '#1D4ED8'
      }
    },

    // Festival Themes (Research-based)
    festivals: {
      diwali: {
        primary: '#FF6B35',    // Lamp flame
        secondary: '#FFD700',  // Gold prosperity
        accent: '#DC143C',     // Victory red
        background: '#2F1B14'  // Deep warm
      },
      pongal: {
        primary: '#FFD700',    // Harvest gold
        secondary: '#32CD32',  // Crop green
        accent: '#FF6347',     // Celebration orange
        background: '#F5DEB3'  // Warm cream
      },
      onam: {
        primary: '#FFD700',    // Marigold
        secondary: '#FF6347',  // Hibiscus
        accent: '#32CD32',     // Banana leaf
        background: '#F0FFFF'  // Pure white
      },
      sankranti: {
        primary: '#FF4500',    // Kite orange
        secondary: '#1E90FF',  // Sky blue
        accent: '#FFD700',     // Sun gold
        background: '#87CEEB'  // Sky background
      },
      navaratri: {
        primary: '#FF1493',    // Divine feminine
        secondary: '#8B008B',  // Royal purple
        accent: '#FFD700',     // Sacred gold
        background: '#2F1B14'  // Deep mystical
      }
    }
  },

  // Professional Typography (Cultural + Modern)
  typography: {
    fontFamily: {
      primary: ['Inter', 'Segoe UI', 'system-ui', 'sans-serif'],
      heading: ['Playfair Display', 'Georgia', 'serif'],
      mono: ['JetBrains Mono', 'Menlo', 'Monaco', 'monospace'],
      cultural: ['Noto Sans Devanagari', 'Noto Sans Tamil', 'system-ui']
    },

    fontSize: {
      xs: ['0.75rem', { lineHeight: '1rem' }],
      sm: ['0.875rem', { lineHeight: '1.25rem' }],
      base: ['1rem', { lineHeight: '1.5rem' }],
      lg: ['1.125rem', { lineHeight: '1.75rem' }],
      xl: ['1.25rem', { lineHeight: '1.75rem' }],
      '2xl': ['1.5rem', { lineHeight: '2rem' }],
      '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
      '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
      '5xl': ['3rem', { lineHeight: '1' }],
      '6xl': ['3.75rem', { lineHeight: '1' }],
      '7xl': ['4.5rem', { lineHeight: '1' }],
      '8xl': ['6rem', { lineHeight: '1' }],
      '9xl': ['8rem', { lineHeight: '1' }]
    },

    fontWeight: {
      thin: '100',
      extralight: '200',
      light: '300',
      normal: '400',
      medium: '500',
      semibold: '600',
      bold: '700',
      extrabold: '800',
      black: '900'
    },

    letterSpacing: {
      tighter: '-0.05em',
      tight: '-0.025em',
      normal: '0em',
      wide: '0.025em',
      wider: '0.05em',
      widest: '0.1em'
    },

    lineHeight: {
      none: '1',
      tight: '1.25',
      snug: '1.375',
      normal: '1.5',
      relaxed: '1.625',
      loose: '2'
    }
  },

  // Professional Spacing System
  spacing: {
    0: '0px',
    1: '0.25rem',    // 4px
    2: '0.5rem',     // 8px
    3: '0.75rem',    // 12px
    4: '1rem',       // 16px
    5: '1.25rem',    // 20px
    6: '1.5rem',     // 24px
    7: '1.75rem',    // 28px
    8: '2rem',       // 32px
    9: '2.25rem',    // 36px
    10: '2.5rem',    // 40px
    11: '2.75rem',   // 44px
    12: '3rem',      // 48px
    14: '3.5rem',    // 56px
    16: '4rem',      // 64px
    20: '5rem',      // 80px
    24: '6rem',      // 96px
    28: '7rem',      // 112px
    32: '8rem',      // 128px
    36: '9rem',      // 144px
    40: '10rem',     // 160px
    44: '11rem',     // 176px
    48: '12rem',     // 192px
    52: '13rem',     // 208px
    56: '14rem',     // 224px
    60: '15rem',     // 240px
    64: '16rem',     // 256px
    72: '18rem',     // 288px
    80: '20rem',     // 320px
    96: '24rem'      // 384px
  },

  // Border Radius (Organic Kolam-inspired)
  borderRadius: {
    none: '0px',
    sm: '0.125rem',    // 2px
    base: '0.25rem',   // 4px
    md: '0.375rem',    // 6px
    lg: '0.5rem',      // 8px
    xl: '0.75rem',     // 12px
    '2xl': '1rem',     // 16px
    '3xl': '1.5rem',   // 24px
    kolam: '1.25rem',  // 20px - Kolam-inspired curves
    full: '9999px'     // Perfect circle
  },

  // Professional Shadows (Depth)
  boxShadow: {
    none: 'none',
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    base: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
    
    // Cultural shadows (warm undertones)
    cultural: {
      warm: '0 4px 6px -1px rgba(255, 107, 53, 0.1), 0 2px 4px -1px rgba(255, 107, 53, 0.06)',
      golden: '0 10px 15px -3px rgba(255, 193, 7, 0.1), 0 4px 6px -2px rgba(255, 193, 7, 0.05)',
      sacred: '0 20px 25px -5px rgba(220, 20, 60, 0.1), 0 10px 10px -5px rgba(220, 20, 60, 0.04)'
    }
  },

  // Responsive Breakpoints
  breakpoints: {
    xs: '475px',
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px'
  },

  // Z-Index Scale
  zIndex: {
    hide: '-1',
    auto: 'auto',
    base: '0',
    docked: '10',
    dropdown: '1000',
    sticky: '1100',
    banner: '1200',
    overlay: '1300',
    modal: '1400',
    popover: '1500',
    skipLink: '1600',
    toast: '1700',
    tooltip: '1800'
  },

  // Professional Animations
  animation: {
    duration: {
      instant: '0ms',
      fast: '150ms',
      normal: '300ms',
      slow: '500ms',
      slower: '750ms',
      slowest: '1000ms'
    },
    
    easing: {
      linear: 'linear',
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
      easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
      
      // Cultural easing (inspired by Kolam flow)
      kolam: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
      organic: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
    }
  },

  // Component Variants (Professional)
  components: {
    button: {
      sizes: {
        xs: {
          padding: '0.375rem 0.75rem',
          fontSize: '0.75rem',
          borderRadius: '0.25rem'
        },
        sm: {
          padding: '0.5rem 1rem',
          fontSize: '0.875rem',
          borderRadius: '0.375rem'
        },
        md: {
          padding: '0.75rem 1.5rem',
          fontSize: '1rem',
          borderRadius: '0.5rem'
        },
        lg: {
          padding: '1rem 2rem',
          fontSize: '1.125rem',
          borderRadius: '0.75rem'
        },
        xl: {
          padding: '1.25rem 2.5rem',
          fontSize: '1.25rem',
          borderRadius: '1rem'
        }
      },
      
      variants: {
        primary: {
          background: 'primary.500',
          color: 'white',
          '&:hover': { background: 'primary.600' },
          '&:active': { background: 'primary.700' }
        },
        secondary: {
          background: 'secondary.500',
          color: 'white',
          '&:hover': { background: 'secondary.600' },
          '&:active': { background: 'secondary.700' }
        },
        outline: {
          background: 'transparent',
          color: 'primary.500',
          border: '2px solid',
          borderColor: 'primary.500',
          '&:hover': { 
            background: 'primary.500',
            color: 'white'
          }
        },
        ghost: {
          background: 'transparent',
          color: 'neutral.700',
          '&:hover': { background: 'neutral.100' }
        },
        cultural: {
          background: 'festivals.diwali.primary',
          color: 'white',
          boxShadow: 'cultural.warm'
        }
      }
    },

    card: {
      variants: {
        elevated: {
          background: 'white',
          boxShadow: 'lg',
          borderRadius: '2xl',
          border: '1px solid',
          borderColor: 'neutral.200'
        },
        outline: {
          background: 'white',
          border: '1px solid',
          borderColor: 'neutral.300',
          borderRadius: 'xl'
        },
        filled: {
          background: 'neutral.50',
          borderRadius: 'xl'
        },
        cultural: {
          background: 'white',
          boxShadow: 'cultural.golden',
          borderRadius: 'kolam',
          border: '2px solid',
          borderColor: 'primary.200'
        }
      }
    },

    input: {
      sizes: {
        sm: {
          padding: '0.5rem 0.75rem',
          fontSize: '0.875rem',
          borderRadius: '0.375rem'
        },
        md: {
          padding: '0.75rem 1rem',
          fontSize: '1rem',
          borderRadius: '0.5rem'
        },
        lg: {
          padding: '1rem 1.25rem',
          fontSize: '1.125rem',
          borderRadius: '0.75rem'
        }
      },
      
      variants: {
        outline: {
          border: '2px solid',
          borderColor: 'neutral.300',
          '&:focus': {
            borderColor: 'primary.500',
            boxShadow: '0 0 0 3px rgba(255, 193, 7, 0.1)'
          }
        },
        filled: {
          background: 'neutral.50',
          border: '2px solid transparent',
          '&:focus': {
            background: 'white',
            borderColor: 'primary.500'
          }
        }
      }
    }
  },

  // Cultural Design Tokens
  cultural: {
    patterns: {
      kolam: {
        dotSpacing: '24px',
        lineWidth: '3px',
        cornerRadius: '50%'
      },
      mandala: {
        centerRadius: '8px',
        ringSpacing: '16px',
        petalCurve: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
      }
    },
    
    symbolism: {
      prosperity: 'primary.500',  // Gold/Yellow
      purity: 'neutral.0',        // White
      energy: 'accent.ruby.500',  // Red
      nature: 'accent.emerald.500', // Green
      cosmos: 'accent.sapphire.500', // Blue
      devotion: 'secondary.500'   // Orange
    }
  },

  // Accessibility Features
  accessibility: {
    focusRing: {
      width: '2px',
      style: 'solid',
      color: 'primary.500',
      offset: '2px'
    },
    
    contrast: {
      aa: '4.5:1',     // WCAG AA standard
      aaa: '7:1'       // WCAG AAA standard
    },
    
    motionReduced: {
      duration: '0.01ms',
      easing: 'linear'
    }
  }
};

// Professional CSS-in-JS helpers
export const createTheme = (customizations = {}) => ({
  ...professionalDesignSystem,
  ...customizations
});

export const getColor = (path, theme = professionalDesignSystem) => {
  return path.split('.').reduce((obj, key) => obj?.[key], theme.colors);
};

export const getSpacing = (value, theme = professionalDesignSystem) => {
  return theme.spacing[value] || value;
};

export const getFontSize = (size, theme = professionalDesignSystem) => {
  return theme.typography.fontSize[size] || theme.typography.fontSize.base;
};

export const getBreakpoint = (bp, theme = professionalDesignSystem) => {
  return theme.breakpoints[bp];
};

// Cultural theme variants
export const culturalThemes = {
  tamil: createTheme({
    colors: {
      primary: {
        500: '#DC143C',  // Traditional Tamil red
        600: '#B91C1C'
      }
    }
  }),
  
  karnataka: createTheme({
    colors: {
      primary: {
        500: '#8B0000',  // Deep Karnataka red
        600: '#7F0000'
      }
    }
  }),
  
  kerala: createTheme({
    colors: {
      primary: {
        500: '#228B22',  // Kerala green
        600: '#1F7A1F'
      }
    }
  })
};

export default professionalDesignSystem;
