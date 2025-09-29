#!/usr/bin/env python3
"""
Demo of the Topological Kolam Generation System
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_topological_generator():
    """Demonstrate the topological kolam generator"""
    print("🔬 Topological Kolam Generation Demo")
    print("=" * 50)
    
    try:
        from topological_kolam_generator import TopologicalKolamGenerator, BondType, SymmetryType
        
        generator = TopologicalKolamGenerator()
        
        print("✅ Topological generator loaded successfully!")
        
        # Demo 1: 3-dot pattern (N=3)
        print("\n📐 Demo 1: 3-Dot Radial Pattern")
        print("-" * 30)
        
        dots_3 = [(100, 100), (200, 100), (150, 173)]
        pattern_3 = generator.generate_kolam(
            dots=dots_3,
            num_junctions=1,
            bond_types=[BondType.CROSS, BondType.DOUBLE],
            symmetry_type=SymmetryType.RADIAL,
            cultural_region="tamil_nadu"
        )
        
        print(f"🎯 Generated pattern with {len(pattern_3.points)} points")
        print(f"🔗 Created {len(pattern_3.junctions)} junctions")
        print(f"🛤️  Generated {len(pattern_3.paths)} paths")
        print(f"📊 Parent type: {pattern_3.parent_type}")
        print(f"🔄 Symmetry: {pattern_3.symmetry_type.value}")
        print(f"🔢 Numeric representation: {pattern_3.numeric_representation[:50]}...")
        print(f"🏛️  Cultural name: {pattern_3.cultural_metadata['name']}")
        print(f"📈 Complexity score: {pattern_3.mathematical_properties['complexity_score']:.2f}")
        
        # Demo 2: 5-dot pattern (N=5)
        print("\n📐 Demo 2: 5-Dot Rotational Pattern")
        print("-" * 30)
        
        # Generate pentagon points
        import math
        center_x, center_y = 200, 200
        radius = 80
        dots_5 = []
        for i in range(5):
            angle = (i * 2 * math.pi) / 5 - math.pi / 2
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            dots_5.append((x, y))
        
        pattern_5 = generator.generate_kolam(
            dots=dots_5,
            num_junctions=1,
            bond_types=[BondType.CROSS, BondType.DOUBLE, BondType.BROKEN],
            symmetry_type=SymmetryType.ROTATIONAL,
            cultural_region="karnataka"
        )
        
        print(f"🎯 Generated pattern with {len(pattern_5.points)} points")
        print(f"🔗 Created {len(pattern_5.junctions)} junctions")
        print(f"🛤️  Generated {len(pattern_5.paths)} paths")
        print(f"📊 Parent type: {pattern_5.parent_type}")
        print(f"🔄 Symmetry: {pattern_5.symmetry_type.value}")
        print(f"🏛️  Cultural name: {pattern_5.cultural_metadata['name']}")
        print(f"📈 Complexity score: {pattern_5.mathematical_properties['complexity_score']:.2f}")
        
        # Demo 3: Show bond types
        print("\n🔗 Demo 3: Bond Types")
        print("-" * 30)
        
        for bond_type in BondType:
            print(f"• {bond_type.value}: {bond_type.name}")
        
        # Demo 4: Show symmetry types
        print("\n🔄 Demo 4: Symmetry Types")
        print("-" * 30)
        
        for symmetry_type in SymmetryType:
            print(f"• {symmetry_type.value}: {symmetry_type.name}")
        
        # Demo 5: Cultural regions
        print("\n🏛️  Demo 5: Cultural Regions")
        print("-" * 30)
        
        cultural_info = {
            "tamil_nadu": "Sikku Kolam - Cosmic energy and unity",
            "karnataka": "Rangavalli Muggu - Geometric perfection",
            "kerala": "Pookalam - Natural abundance",
            "andhra_pradesh": "Muggulu - Protection and blessing",
            "telangana": "Gorintaku - Traditional heritage"
        }
        
        for region, description in cultural_info.items():
            print(f"• {region.replace('_', ' ').title()}: {description}")
        
        print("\n🎉 Topological Kolam Generation Demo Complete!")
        print("=" * 50)
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importing topological generator: {e}")
        print("💡 Make sure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Error in demo: {e}")
        return False

def demo_rules_validator():
    """Demonstrate the kolam rules validator"""
    print("\n📐 Kolam Rules Validation Demo")
    print("=" * 50)
    
    try:
        from kolam_rules_validator import KolamRulesValidator
        
        validator = KolamRulesValidator()
        
        print("✅ Rules validator loaded successfully!")
        
        # Test with a valid pattern
        points = [(100, 100), (200, 100), (150, 173)]
        paths = [
            [(100, 100), (200, 100), (150, 173), (100, 100)]  # Closed triangle
        ]
        
        result = validator.validate_pattern(points, paths)
        
        print(f"\n🎯 Validation Result:")
        print(f"✅ Valid: {result['valid']}")
        print(f"📊 Score: {result['score']}/100")
        print(f"📋 Issues: {result['summary']['total_issues']}")
        print(f"✅ Valid rules: {result['summary']['valid']}")
        print(f"⚠️  Warnings: {result['summary']['warnings']}")
        print(f"❌ Errors: {result['summary']['errors']}")
        
        print(f"\n📋 Rules Status:")
        for rule, status in result['rules_status'].items():
            print(f"• {rule}: {status}")
        
        if result['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in result['recommendations']:
                print(f"• {rec}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importing rules validator: {e}")
        return False
    except Exception as e:
        print(f"❌ Error in validator demo: {e}")
        return False

def demo_pattern_templates():
    """Demonstrate the pattern templates"""
    print("\n📚 Pattern Templates Demo")
    print("=" * 50)
    
    try:
        from kolam_pattern_templates import KolamPatternTemplates
        
        templates = KolamPatternTemplates()
        
        print("✅ Pattern templates loaded successfully!")
        
        # Show summary
        summary = templates.get_template_summary()
        print(f"\n📊 Template Summary:")
        print(f"• Total templates: {summary['total_templates']}")
        print(f"• By dots: {summary['by_dots']}")
        print(f"• By region: {summary['by_region']}")
        print(f"• By difficulty: {summary['by_difficulty']}")
        
        # Show 3-dot templates
        print(f"\n📐 3-Dot Templates:")
        three_dot_templates = templates.get_templates_by_dots(3)
        for template in three_dot_templates:
            print(f"• {template.name}: {template.description}")
            print(f"  - Difficulty: {template.difficulty_level}")
            print(f"  - Cultural: {template.cultural_region}")
            print(f"  - Significance: {template.cultural_significance}")
        
        # Show Tamil Nadu templates
        print(f"\n🏛️  Tamil Nadu Templates:")
        tamil_templates = templates.get_templates_by_region("tamil_nadu")
        for template in tamil_templates:
            print(f"• {template.name} ({template.num_dots} dots): {template.description}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importing pattern templates: {e}")
        return False
    except Exception as e:
        print(f"❌ Error in templates demo: {e}")
        return False

def main():
    """Run all demos"""
    print("🎨 Topological Kolam Generation System Demo")
    print("=" * 60)
    print("Based on research by Venkatraman Gopalan and Brian K. VanLeeuwen")
    print("AICTE Problem Statement 25107")
    print("=" * 60)
    
    demos = [
        demo_topological_generator,
        demo_rules_validator,
        demo_pattern_templates
    ]
    
    passed = 0
    total = len(demos)
    
    for demo in demos:
        if demo():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Demo Results: {passed}/{total} demos successful")
    
    if passed == total:
        print("🎉 All demos completed successfully!")
        print("🚀 The topological kolam system is ready to use!")
    else:
        print("⚠️  Some demos failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


































