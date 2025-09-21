"""
Colorful Kolam Visualizer
=========================

Advanced visualization system for colorful Kolam patterns based on research:
- Traditional color schemes from different regions
- Cultural significance of colors
- Festival-specific palettes
- Interactive SVG generation
- Animation capabilities for drawing process
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, FancyBboxPatch, Polygon
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as path_effects
import seaborn as sns
import cv2
from PIL import Image, ImageDraw, ImageFont
import json
import math
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import svgwrite
from datetime import datetime

class FestivalTheme(Enum):
    DIWALI = "diwali"
    PONGAL = "pongal"
    ONAM = "onam"
    SANKRANTI = "sankranti"
    NAVARATRI = "navaratri"
    GENERAL = "general"

class ColorSymbolism(Enum):
    RED = "prosperity_energy"
    YELLOW = "knowledge_learning"
    WHITE = "purity_peace"
    GREEN = "nature_growth"
    BLUE = "cosmic_infinity"
    ORANGE = "devotion_spirituality"
    PINK = "love_compassion"
    PURPLE = "royalty_dignity"

@dataclass
class KolamVisualizationConfig:
    """Configuration for Kolam visualization"""
    width: int = 800
    height: int = 800
    background_color: str = "#F8F5F0"
    festival_theme: FestivalTheme = FestivalTheme.GENERAL
    use_gradients: bool = True
    use_shadows: bool = True
    use_textures: bool = False
    animation_speed: float = 1.0
    cultural_region: str = "tamil_nadu"
    time_of_day: str = "morning"  # affects color intensity
    
@dataclass
class ColorPalette:
    """Cultural color palette"""
    primary_colors: List[str]
    secondary_colors: List[str]
    accent_colors: List[str]
    background_colors: List[str]
    symbolic_meanings: Dict[str, str]
    cultural_significance: str

class ColorfulKolamVisualizer:
    """
    Advanced colorful Kolam visualizer with cultural authenticity
    """
    
    def __init__(self):
        self.festival_palettes = self._initialize_festival_palettes()
        self.regional_palettes = self._initialize_regional_palettes()
        self.time_modifiers = {
            "dawn": {"brightness": 0.7, "saturation": 0.8},
            "morning": {"brightness": 1.0, "saturation": 1.0},
            "noon": {"brightness": 1.2, "saturation": 0.9},
            "evening": {"brightness": 0.9, "saturation": 1.1},
            "night": {"brightness": 0.6, "saturation": 0.7}
        }
        
    def _initialize_festival_palettes(self) -> Dict[FestivalTheme, ColorPalette]:
        """Initialize festival-specific color palettes based on research"""
        palettes = {}
        
        # Diwali - Festival of Lights
        palettes[FestivalTheme.DIWALI] = ColorPalette(
            primary_colors=["#FF6B35", "#FFD700", "#FF4500", "#FFA500"],
            secondary_colors=["#DC143C", "#FF1493", "#8B0000"],
            accent_colors=["#FFFFFF", "#F0F8FF", "#FFFAF0"],
            background_colors=["#2F1B14", "#1A1A1A", "#0D0D0D"],
            symbolic_meanings={
                "#FF6B35": "lamp_flame_victory_over_darkness",
                "#FFD700": "prosperity_wealth_goddess_lakshmi",
                "#FF4500": "energy_enthusiasm_celebration",
                "#DC143C": "power_strength_durga_shakti"
            },
            cultural_significance="Colors representing light conquering darkness, prosperity, and divine blessings"
        )
        
        # Pongal - Tamil Harvest Festival
        palettes[FestivalTheme.PONGAL] = ColorPalette(
            primary_colors=["#FFD700", "#FFA500", "#32CD32", "#8FBC8F"],
            secondary_colors=["#FF6347", "#FFFF00", "#9ACD32"],
            accent_colors=["#FFFFFF", "#F5FFFA", "#FFFACD"],
            background_colors=["#F0E68C", "#F5DEB3", "#FFF8DC"],
            symbolic_meanings={
                "#FFD700": "ripe_grain_abundance_sun_energy",
                "#32CD32": "new_crops_fertility_nature",
                "#FFA500": "turmeric_auspiciousness_prosperity",
                "#FF6347": "sugarcane_sweetness_joy"
            },
            cultural_significance="Harvest festival colors celebrating agricultural abundance and gratitude to nature"
        )
        
        # Onam - Kerala Festival
        palettes[FestivalTheme.ONAM] = ColorPalette(
            primary_colors=["#FFD700", "#FF6347", "#32CD32", "#FFFFFF"],
            secondary_colors=["#FF1493", "#00CED1", "#9370DB"],
            accent_colors=["#FFFACD", "#F0FFFF", "#E6E6FA"],
            background_colors=["#228B22", "#2E8B57", "#3CB371"],
            symbolic_meanings={
                "#FFD700": "marigold_prosperity_king_mahabali",
                "#FF6347": "hibiscus_devotion_sacrifice",
                "#32CD32": "banana_leaf_nature_abundance",
                "#FFFFFF": "jasmine_purity_peace"
            },
            cultural_significance="Floral Pookalam colors representing the golden age of King Mahabali"
        )
        
        # Sankranti - Kite Festival
        palettes[FestivalTheme.SANKRANTI] = ColorPalette(
            primary_colors=["#FF4500", "#FFD700", "#1E90FF", "#32CD32"],
            secondary_colors=["#FF1493", "#8A2BE2", "#FF6347"],
            accent_colors=["#FFFFFF", "#F0F8FF", "#FFFAF0"],
            background_colors=["#87CEEB", "#87CEFA", "#B0E0E6"],
            symbolic_meanings={
                "#FF4500": "kite_paper_celebration_freedom",
                "#1E90FF": "winter_sky_vastness_possibility",
                "#FFD700": "sun_god_surya_new_beginnings",
                "#32CD32": "fresh_crops_spring_renewal"
            },
            cultural_significance="Vibrant kite colors celebrating the sun's northward journey and harvest season"
        )
        
        # Navaratri - Nine Nights Festival
        palettes[FestivalTheme.NAVARATRI] = ColorPalette(
            primary_colors=["#FF0000", "#FFA500", "#FFD700", "#32CD32", "#0000FF", "#4B0082", "#8B008B", "#FF1493", "#FFFFFF"],
            secondary_colors=["#DC143C", "#FF6347", "#FFFF00"],
            accent_colors=["#F0F8FF", "#FFFAF0", "#F5F5DC"],
            background_colors=["#2F1B14", "#1A1A2E", "#16213E"],
            symbolic_meanings={
                "#FF0000": "day1_shailaputri_energy_strength",
                "#FFA500": "day2_brahmacharini_devotion_penance",
                "#FFD700": "day3_chandraghanta_prosperity_peace",
                "#32CD32": "day4_kushmanda_nature_creativity",
                "#0000FF": "day5_skandamata_stability_depth",
                "#4B0082": "day6_katyayani_intuition_wisdom",
                "#8B008B": "day7_kaalratri_transformation_mystery",
                "#FF1493": "day8_mahagauri_compassion_purity",
                "#FFFFFF": "day9_siddhidatri_completion_perfection"
            },
            cultural_significance="Nine sacred colors representing different forms of Divine Feminine over nine nights"
        )
        
        return palettes
    
    def _initialize_regional_palettes(self) -> Dict[str, ColorPalette]:
        """Initialize region-specific color palettes"""
        palettes = {}
        
        # Tamil Nadu Traditional
        palettes["tamil_nadu"] = ColorPalette(
            primary_colors=["#DC143C", "#FFD700", "#FFFFFF", "#FF6347"],
            secondary_colors=["#8B0000", "#FFA500", "#32CD32"],
            accent_colors=["#F0F8FF", "#FFFACD"],
            background_colors=["#F5F5DC", "#FFF8DC"],
            symbolic_meanings={
                "#DC143C": "vermillion_married_women_prosperity",
                "#FFD700": "turmeric_auspiciousness_purity",
                "#FFFFFF": "rice_flour_abundance_peace"
            },
            cultural_significance="Traditional Tamil colors used in daily Kolam practice"
        )
        
        # Karnataka Traditional
        palettes["karnataka"] = ColorPalette(
            primary_colors=["#8B0000", "#FF6347", "#FFFF00", "#32CD32"],
            secondary_colors=["#FF4500", "#FFD700", "#FFFFFF"],
            accent_colors=["#F0FFFF", "#FFFAF0"],
            background_colors=["#F5F5DC", "#FAEBD7"],
            symbolic_meanings={
                "#8B0000": "dark_red_kumkum_devotion",
                "#FFFF00": "yellow_turmeric_prosperity",
                "#32CD32": "green_leaves_nature_life"
            },
            cultural_significance="Karnataka Muggu colors representing geometric precision and cultural heritage"
        )
        
        # Kerala Traditional
        palettes["kerala"] = ColorPalette(
            primary_colors=["#228B22", "#FFD700", "#FF4500", "#FFFFFF"],
            secondary_colors=["#32CD32", "#FFA500", "#FF1493"],
            accent_colors=["#F0FFFF", "#FFFACD"],
            background_colors=["#F0F8FF", "#F5FFFA"],
            symbolic_meanings={
                "#228B22": "banana_leaf_abundance_hospitality",
                "#FFD700": "coconut_prosperity_purity",
                "#FF4500": "flowers_devotion_beauty"
            },
            cultural_significance="Kerala Pookalam colors inspired by tropical flowers and nature"
        )
        
        return palettes
    
    def get_color_palette(self, config: KolamVisualizationConfig) -> ColorPalette:
        """Get appropriate color palette based on configuration"""
        if config.festival_theme != FestivalTheme.GENERAL:
            palette = self.festival_palettes[config.festival_theme]
        else:
            palette = self.regional_palettes.get(config.cultural_region, 
                                               self.regional_palettes["tamil_nadu"])
        
        # Apply time-of-day modifications
        if config.time_of_day in self.time_modifiers:
            modifier = self.time_modifiers[config.time_of_day]
            palette = self._modify_palette_brightness(palette, modifier)
        
        return palette
    
    def _modify_palette_brightness(self, palette: ColorPalette, modifier: Dict[str, float]) -> ColorPalette:
        """Modify palette brightness and saturation based on time of day"""
        def modify_color(hex_color: str) -> str:
            # Convert hex to RGB
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            
            # Apply brightness modifier
            r = int(min(255, r * modifier["brightness"]))
            g = int(min(255, g * modifier["brightness"]))
            b = int(min(255, b * modifier["brightness"]))
            
            # Convert back to hex
            return f"#{r:02x}{g:02x}{b:02x}"
        
        modified_palette = ColorPalette(
            primary_colors=[modify_color(c) for c in palette.primary_colors],
            secondary_colors=[modify_color(c) for c in palette.secondary_colors],
            accent_colors=[modify_color(c) for c in palette.accent_colors],
            background_colors=palette.background_colors,  # Keep background unchanged
            symbolic_meanings=palette.symbolic_meanings,
            cultural_significance=palette.cultural_significance
        )
        
        return modified_palette
    
    def visualize_kolam(self, kolam_data: Dict[str, Any], config: KolamVisualizationConfig) -> plt.Figure:
        """
        Create beautiful colorful visualization of Kolam pattern
        """
        # Get color palette
        palette = self.get_color_palette(config)
        
        # Create figure with cultural background
        fig, ax = plt.subplots(figsize=(12, 12))
        ax.set_xlim(0, config.width)
        ax.set_ylim(0, config.height)
        ax.set_aspect('equal')
        
        # Set background with gradient if enabled
        if config.use_gradients:
            self._create_gradient_background(ax, config, palette)
        else:
            ax.set_facecolor(palette.background_colors[0])
        
        # Draw dots (pulli) with cultural styling
        if 'dots' in kolam_data:
            self._draw_cultural_dots(ax, kolam_data['dots'], palette, config)
        
        # Draw paths (kambi) with colors and effects
        if 'paths' in kolam_data:
            self._draw_colorful_paths(ax, kolam_data['paths'], palette, config)
        
        # Add cultural decorations
        self._add_cultural_decorations(ax, config, palette)
        
        # Add title with cultural context
        self._add_cultural_title(ax, config, palette)
        
        # Remove axes for clean look
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        return fig
    
    def _create_gradient_background(self, ax: plt.Axes, config: KolamVisualizationConfig, palette: ColorPalette):
        """Create gradient background effect"""
        # Create radial gradient from center
        center_x, center_y = config.width // 2, config.height // 2
        
        # Create gradient mesh
        x = np.linspace(0, config.width, 100)
        y = np.linspace(0, config.height, 100)
        X, Y = np.meshgrid(x, y)
        
        # Calculate distance from center
        distances = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
        max_distance = np.sqrt(center_x**2 + center_y**2)
        normalized_distances = distances / max_distance
        
        # Create custom colormap
        colors = [palette.background_colors[0], palette.accent_colors[0]]
        n_bins = 256
        cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)
        
        # Apply gradient
        ax.contourf(X, Y, normalized_distances, levels=50, cmap=cmap, alpha=0.3)
    
    def _draw_cultural_dots(self, ax: plt.Axes, dots: List[Tuple[float, float]], 
                           palette: ColorPalette, config: KolamVisualizationConfig):
        """Draw dots with cultural styling"""
        dot_colors = palette.primary_colors
        
        for i, (x, y) in enumerate(dots):
            color = dot_colors[i % len(dot_colors)]
            
            # Main dot
            circle = Circle((x, y), radius=6, facecolor=color, 
                          edgecolor='white', linewidth=2, zorder=10)
            ax.add_patch(circle)
            
            # Add shadow if enabled
            if config.use_shadows:
                shadow = Circle((x + 2, y - 2), radius=6, facecolor='gray', 
                              alpha=0.3, zorder=5)
                ax.add_patch(shadow)
            
            # Add inner highlight
            highlight = Circle((x - 1, y + 1), radius=2, facecolor='white', 
                             alpha=0.7, zorder=15)
            ax.add_patch(highlight)
    
    def _draw_colorful_paths(self, ax: plt.Axes, paths: List[List[Tuple[float, float]]], 
                           palette: ColorPalette, config: KolamVisualizationConfig):
        """Draw paths with beautiful colors and effects"""
        path_colors = palette.primary_colors + palette.secondary_colors
        
        for i, path in enumerate(paths):
            if len(path) < 2:
                continue
            
            color = path_colors[i % len(path_colors)]
            
            # Convert path to arrays
            x_coords = [p[0] for p in path]
            y_coords = [p[1] for p in path]
            
            # Draw main path with gradient effect
            if config.use_gradients and len(path) > 2:
                self._draw_gradient_path(ax, x_coords, y_coords, color, config)
            else:
                # Simple colored line
                line = ax.plot(x_coords, y_coords, color=color, linewidth=4, 
                             solid_capstyle='round', solid_joinstyle='round', zorder=8)[0]
                
                # Add glow effect
                glow_line = ax.plot(x_coords, y_coords, color=color, linewidth=8, 
                                  alpha=0.3, solid_capstyle='round', solid_joinstyle='round', zorder=7)[0]
            
            # Add path effects
            if config.use_shadows:
                shadow_x = [x + 1 for x in x_coords]
                shadow_y = [y - 1 for y in y_coords]
                ax.plot(shadow_x, shadow_y, color='gray', linewidth=4, 
                       alpha=0.3, zorder=6)
    
    def _draw_gradient_path(self, ax: plt.Axes, x_coords: List[float], y_coords: List[float], 
                          color: str, config: KolamVisualizationConfig):
        """Draw path with gradient color effect"""
        # Create gradient along the path
        for i in range(len(x_coords) - 1):
            # Calculate gradient from start to end
            t = i / (len(x_coords) - 1)
            
            # Interpolate color intensity
            alpha = 0.8 + 0.2 * math.sin(t * math.pi * 4)  # Varying intensity
            
            # Draw segment
            ax.plot([x_coords[i], x_coords[i+1]], [y_coords[i], y_coords[i+1]], 
                   color=color, linewidth=5, alpha=alpha, 
                   solid_capstyle='round', zorder=8)
    
    def _add_cultural_decorations(self, ax: plt.Axes, config: KolamVisualizationConfig, palette: ColorPalette):
        """Add cultural decorative elements"""
        # Add corner decorations
        corner_color = palette.accent_colors[0]
        
        # Traditional border pattern
        border_width = 20
        
        # Top border
        for x in range(0, config.width, 40):
            if x < config.width - border_width:
                decoration = FancyBboxPatch((x, config.height - border_width), 30, 15,
                                         boxstyle="round,pad=2", 
                                         facecolor=corner_color, alpha=0.6, zorder=2)
                ax.add_patch(decoration)
        
        # Side borders
        for y in range(border_width, config.height - border_width, 40):
            # Left side
            decoration = FancyBboxPatch((0, y), 15, 30,
                                     boxstyle="round,pad=2", 
                                     facecolor=corner_color, alpha=0.6, zorder=2)
            ax.add_patch(decoration)
            
            # Right side  
            decoration = FancyBboxPatch((config.width - 15, y), 15, 30,
                                     boxstyle="round,pad=2", 
                                     facecolor=corner_color, alpha=0.6, zorder=2)
            ax.add_patch(decoration)
    
    def _add_cultural_title(self, ax: plt.Axes, config: KolamVisualizationConfig, palette: ColorPalette):
        """Add culturally appropriate title"""
        title_map = {
            FestivalTheme.DIWALI: "दीपावली कोलम्",
            FestivalTheme.PONGAL: "பொங்கல் கோலம்",
            FestivalTheme.ONAM: "ഓണം പൂക്കളം",
            FestivalTheme.SANKRANTI: "సంక్రాంతి ముగ్గు",
            FestivalTheme.NAVARATRI: "नवरात्रि रंगोली",
            FestivalTheme.GENERAL: "पारंपरिक कोलम्"
        }
        
        title = title_map.get(config.festival_theme, "Traditional Kolam")
        
        # Add title with shadow effect
        title_text = ax.text(config.width // 2, config.height - 30, title,
                           fontsize=20, fontweight='bold', ha='center', va='center',
                           color=palette.primary_colors[0], zorder=20)
        
        # Add shadow
        shadow_text = ax.text(config.width // 2 + 2, config.height - 32, title,
                            fontsize=20, fontweight='bold', ha='center', va='center',
                            color='gray', alpha=0.5, zorder=19)
    
    def create_animated_drawing(self, kolam_data: Dict[str, Any], config: KolamVisualizationConfig) -> animation.FuncAnimation:
        """
        Create animated visualization showing the drawing process
        """
        fig, ax = plt.subplots(figsize=(12, 12))
        ax.set_xlim(0, config.width)
        ax.set_ylim(0, config.height)
        ax.set_aspect('equal')
        
        palette = self.get_color_palette(config)
        
        # Set background
        if config.use_gradients:
            self._create_gradient_background(ax, config, palette)
        else:
            ax.set_facecolor(palette.background_colors[0])
        
        # Prepare animation data
        all_points = []
        colors = []
        
        # Add dots first
        if 'dots' in kolam_data:
            for i, dot in enumerate(kolam_data['dots']):
                all_points.append(('dot', dot, palette.primary_colors[i % len(palette.primary_colors)]))
        
        # Add path points
        if 'paths' in kolam_data:
            path_colors = palette.primary_colors + palette.secondary_colors
            for i, path in enumerate(kolam_data['paths']):
                color = path_colors[i % len(path_colors)]
                for j, point in enumerate(path):
                    all_points.append(('path', point, color, i, j))
        
        def animate(frame):
            ax.clear()
            ax.set_xlim(0, config.width)
            ax.set_ylim(0, config.height)
            ax.set_aspect('equal')
            
            # Redraw background
            if config.use_gradients:
                self._create_gradient_background(ax, config, palette)
            else:
                ax.set_facecolor(palette.background_colors[0])
            
            # Draw elements up to current frame
            for i in range(min(frame, len(all_points))):
                element = all_points[i]
                
                if element[0] == 'dot':
                    x, y = element[1]
                    color = element[2]
                    circle = Circle((x, y), radius=6, facecolor=color, 
                                  edgecolor='white', linewidth=2, zorder=10)
                    ax.add_patch(circle)
                
                elif element[0] == 'path':
                    x, y = element[1]
                    color = element[2]
                    # Draw point as part of path
                    circle = Circle((x, y), radius=2, facecolor=color, alpha=0.8, zorder=8)
                    ax.add_patch(circle)
            
            # Remove axes
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)
        
        # Create animation
        anim = animation.FuncAnimation(fig, animate, frames=len(all_points) + 10, 
                                     interval=50 / config.animation_speed, repeat=True)
        
        return anim
    
    def export_svg(self, kolam_data: Dict[str, Any], config: KolamVisualizationConfig, filename: str):
        """
        Export Kolam as high-quality SVG with cultural colors
        """
        palette = self.get_color_palette(config)
        
        # Create SVG drawing
        dwg = svgwrite.Drawing(filename, size=(f'{config.width}px', f'{config.height}px'))
        
        # Add background
        dwg.add(dwg.rect(insert=(0, 0), size=(config.width, config.height), 
                        fill=palette.background_colors[0]))
        
        # Add gradient definitions
        if config.use_gradients:
            grad = dwg.defs.add(dwg.radialGradient(id='bg_gradient', center=(0.5, 0.5)))
            grad.add_stop_color(offset=0, color=palette.accent_colors[0], opacity=0.3)
            grad.add_stop_color(offset=1, color=palette.background_colors[0], opacity=0.1)
            
            dwg.add(dwg.rect(insert=(0, 0), size=(config.width, config.height), 
                           fill='url(#bg_gradient)'))
        
        # Draw paths
        if 'paths' in kolam_data:
            path_colors = palette.primary_colors + palette.secondary_colors
            for i, path in enumerate(kolam_data['paths']):
                if len(path) < 2:
                    continue
                
                color = path_colors[i % len(path_colors)]
                
                # Create path string
                path_string = f"M {path[0][0]} {path[0][1]}"
                for point in path[1:]:
                    path_string += f" L {point[0]} {point[1]}"
                
                # Add path with effects
                if config.use_shadows:
                    # Shadow path
                    shadow_string = f"M {path[0][0]+2} {path[0][1]-2}"
                    for point in path[1:]:
                        shadow_string += f" L {point[0]+2} {point[1]-2}"
                    
                    dwg.add(dwg.path(d=shadow_string, stroke='gray', stroke_width=4, 
                                   fill='none', opacity=0.3))
                
                # Main path
                dwg.add(dwg.path(d=path_string, stroke=color, stroke_width=4, 
                               fill='none', stroke_linecap='round', stroke_linejoin='round'))
        
        # Draw dots
        if 'dots' in kolam_data:
            dot_colors = palette.primary_colors
            for i, (x, y) in enumerate(kolam_data['dots']):
                color = dot_colors[i % len(dot_colors)]
                
                # Shadow
                if config.use_shadows:
                    dwg.add(dwg.circle(center=(x+2, y-2), r=6, fill='gray', opacity=0.3))
                
                # Main dot
                dwg.add(dwg.circle(center=(x, y), r=6, fill=color, stroke='white', stroke_width=2))
                
                # Highlight
                dwg.add(dwg.circle(center=(x-1, y+1), r=2, fill='white', opacity=0.7))
        
        # Add cultural metadata
        dwg.add(dwg.text(f'Cultural Region: {config.cultural_region}', 
                        insert=(10, config.height - 60), font_size=12, fill=palette.primary_colors[0]))
        dwg.add(dwg.text(f'Festival Theme: {config.festival_theme.value}', 
                        insert=(10, config.height - 40), font_size=12, fill=palette.primary_colors[0]))
        dwg.add(dwg.text(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 
                        insert=(10, config.height - 20), font_size=10, fill=palette.secondary_colors[0]))
        
        # Save SVG
        dwg.save()
        
        return filename
    
    def create_color_analysis_report(self, palette: ColorPalette) -> Dict[str, Any]:
        """
        Create detailed color analysis report with cultural significance
        """
        report = {
            "palette_analysis": {
                "primary_colors": palette.primary_colors,
                "secondary_colors": palette.secondary_colors,
                "accent_colors": palette.accent_colors,
                "color_count": len(palette.primary_colors) + len(palette.secondary_colors),
                "dominant_hue": self._analyze_dominant_hue(palette.primary_colors),
                "color_harmony": self._analyze_color_harmony(palette.primary_colors),
                "cultural_authenticity_score": self._calculate_cultural_authenticity(palette)
            },
            "symbolic_meanings": palette.symbolic_meanings,
            "cultural_significance": palette.cultural_significance,
            "color_psychology": self._analyze_color_psychology(palette.primary_colors),
            "festival_appropriateness": self._analyze_festival_appropriateness(palette),
            "accessibility": self._analyze_color_accessibility(palette)
        }
        
        return report
    
    def _analyze_dominant_hue(self, colors: List[str]) -> str:
        """Analyze dominant hue in color palette"""
        hue_counts = {"red": 0, "orange": 0, "yellow": 0, "green": 0, "blue": 0, "purple": 0}
        
        for color in colors:
            # Simple hue analysis based on RGB values
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)  
            b = int(color[5:7], 16)
            
            if r > g and r > b:
                if g > b:
                    hue_counts["orange"] += 1
                else:
                    hue_counts["red"] += 1
            elif g > r and g > b:
                hue_counts["green"] += 1
            elif b > r and b > g:
                hue_counts["blue"] += 1
            elif r > 200 and g > 200:
                hue_counts["yellow"] += 1
            else:
                hue_counts["purple"] += 1
        
        return max(hue_counts, key=hue_counts.get)
    
    def _analyze_color_harmony(self, colors: List[str]) -> str:
        """Analyze color harmony type"""
        # Simplified harmony analysis
        if len(colors) <= 3:
            return "triadic"
        elif len(colors) <= 4:
            return "tetradic"
        else:
            return "complex_harmony"
    
    def _calculate_cultural_authenticity(self, palette: ColorPalette) -> float:
        """Calculate cultural authenticity score"""
        # Based on traditional color usage
        traditional_colors = ["#DC143C", "#FFD700", "#FF6347", "#32CD32", "#FFFFFF"]
        
        score = 0.0
        for color in palette.primary_colors:
            if color in traditional_colors:
                score += 0.2
        
        return min(score, 1.0)
    
    def _analyze_color_psychology(self, colors: List[str]) -> Dict[str, str]:
        """Analyze psychological effects of colors"""
        psychology = {
            "#DC143C": "energy_passion_strength",
            "#FFD700": "optimism_prosperity_enlightenment", 
            "#FF6347": "warmth_enthusiasm_creativity",
            "#32CD32": "harmony_growth_renewal",
            "#FFFFFF": "purity_peace_simplicity",
            "#FF4500": "vibrance_celebration_energy",
            "#8B0000": "depth_tradition_stability"
        }
        
        return {color: psychology.get(color, "neutral_balance") for color in colors}
    
    def _analyze_festival_appropriateness(self, palette: ColorPalette) -> Dict[str, float]:
        """Analyze appropriateness for different festivals"""
        scores = {}
        
        # Diwali prefers warm colors (reds, oranges, golds)
        warm_colors = sum(1 for c in palette.primary_colors 
                         if c in ["#DC143C", "#FF6347", "#FFD700", "#FF4500", "#FFA500"])
        scores["diwali"] = min(warm_colors / len(palette.primary_colors), 1.0)
        
        # Pongal prefers harvest colors (yellows, greens, oranges)
        harvest_colors = sum(1 for c in palette.primary_colors 
                           if c in ["#FFD700", "#32CD32", "#FFA500", "#FFFF00"])
        scores["pongal"] = min(harvest_colors / len(palette.primary_colors), 1.0)
        
        return scores
    
    def _analyze_color_accessibility(self, palette: ColorPalette) -> Dict[str, Any]:
        """Analyze color accessibility and contrast"""
        accessibility = {
            "high_contrast_pairs": [],
            "low_contrast_warnings": [],
            "colorblind_friendly": True,
            "readability_score": 0.8  # Simplified score
        }
        
        # Check contrast between primary and background colors
        for primary in palette.primary_colors:
            for bg in palette.background_colors:
                if self._calculate_contrast_ratio(primary, bg) > 4.5:
                    accessibility["high_contrast_pairs"].append((primary, bg))
                else:
                    accessibility["low_contrast_warnings"].append((primary, bg))
        
        return accessibility
    
    def _calculate_contrast_ratio(self, color1: str, color2: str) -> float:
        """Calculate contrast ratio between two colors (simplified)"""
        # Simplified contrast calculation
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        # Luminance calculation (simplified)
        l1 = 0.299 * r1 + 0.587 * g1 + 0.114 * b1
        l2 = 0.299 * r2 + 0.587 * g2 + 0.114 * b2
        
        # Contrast ratio
        lighter = max(l1, l2)
        darker = min(l1, l2)
        
        return (lighter + 5) / (darker + 5)

# Example usage
if __name__ == "__main__":
    visualizer = ColorfulKolamVisualizer()
    
    # Test configuration
    config = KolamVisualizationConfig(
        width=800,
        height=800,
        festival_theme=FestivalTheme.DIWALI,
        use_gradients=True,
        use_shadows=True,
        cultural_region="tamil_nadu",
        time_of_day="morning"
    )
    
    # Sample Kolam data
    kolam_data = {
        'dots': [(200, 200), (300, 200), (200, 300), (300, 300), (250, 250)],
        'paths': [
            [(200, 200), (300, 200), (300, 300), (200, 300), (200, 200)],
            [(250, 250), (250, 150), (350, 250), (250, 350), (150, 250), (250, 250)]
        ]
    }
    
    try:
        # Get palette and create visualization
        palette = visualizer.get_color_palette(config)
        fig = visualizer.visualize_kolam(kolam_data, config)
        
        # Create color analysis report
        report = visualizer.create_color_analysis_report(palette)
        
        print("Colorful Kolam Visualizer Test Successful!")
        print(f"Dominant hue: {report['palette_analysis']['dominant_hue']}")
        print(f"Cultural authenticity: {report['palette_analysis']['cultural_authenticity_score']:.2f}")
        print(f"Festival appropriateness for Diwali: {report['festival_appropriateness'].get('diwali', 0):.2f}")
        
        # Export SVG
        svg_file = visualizer.export_svg(kolam_data, config, "test_kolam.svg")
        print(f"SVG exported to: {svg_file}")
        
        plt.show()
        
    except Exception as e:
        print(f"Visualization failed: {e}")
        import traceback
        traceback.print_exc()





