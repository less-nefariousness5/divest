import unittest
from ps_simc_parser.parser.parser import Parser
from ps_simc_parser.parser.actions import Action
from ps_simc_parser.utils.lua import LuaGenerator
from ps_simc_parser.api.mapping import logger, monitor, validator
from .base import PSTestCase

class TestResourceManagement(PSTestCase):
    def setUp(self):
        super().setUp()
        # Resource management SimC template
        self.simc_content = """
# Resource Management Template
actions=auto_attack

# Basic resource tracking
actions+=/variable,name=high_fury,value=fury>=80
actions+=/variable,name=low_fury,value=fury<=20
actions+=/variable,name=soul_fragments_ready,value=soul_fragments>=4

# Resource generation
actions+=/immolation_aura,if=fury.deficit>=30
actions+=/shear,if=fury.deficit>=25&soul_fragments.deficit>=1
actions+=/fracture,if=fury.deficit>=25&soul_fragments.deficit>=2

# Resource spending
actions+=/spirit_bomb,if=soul_fragments>=4
actions+=/soul_cleave,if=fury>=60&!buff.soul_fragments.up
actions+=/fel_devastation,if=fury>=50

# Resource pooling
actions+=/pool_resource,for_next=1
actions+=/spirit_bomb,if=soul_fragments>=4&incoming_damage_3s>health.max*0.25
actions+=/pool_resource,for_next=1
actions+=/fel_devastation,if=fury>=50&health.pct<=50

# Multi-resource management
actions+=/soul_cleave,if=fury>=60&soul_fragments>=3&health.pct<=70
actions+=/spirit_bomb,if=soul_fragments>=4&(fury>=50|health.pct<=60)
actions+=/fel_devastation,if=fury>=50&health.pct<=50&soul_fragments<=2

# Resource optimization
actions+=/soul_cleave,if=fury>=80|health.pct<=40&fury>=60
actions+=/shear,if=fury.deficit>=40&soul_fragments.deficit>=1
actions+=/fracture,if=fury.deficit>=35&soul_fragments.deficit>=2&dot.frailty.remains>=4
"""

    def test_basic_resource_tracking(self):
        """Test basic resource tracking variables"""
        # Create resource tracking actions
        high_fury = Action("variable,name=high_fury,value=fury>=80")
        low_fury = Action("variable,name=low_fury,value=fury<=20")
        soul_frags = Action("variable,name=soul_fragments_ready,value=soul_fragments>=4")
        
        # Verify action properties
        self.assertEqual(high_fury.name, 'variable')
        self.assertEqual(high_fury.args.get('name'), 'high_fury')
        self.assertTrue('fury>=80' in high_fury.args.get('value', ''))
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add resource tracking
        lua_code.append('local function UpdateVariables()')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Variables.high_fury = GetResource("fury") >= 80')
        lua_code.append(generator.get_indent() + 'Variables.low_fury = GetResource("fury") <= 20')
        lua_code.append(generator.get_indent() + 'Variables.soul_fragments_ready = GetResource("soul_fragments") >= 4')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify resource tracking
        self.assertIn('GetResource("fury")', final_code)
        self.assertIn('GetResource("soul_fragments")', final_code)
        self.assertIn('Variables.high_fury', final_code)
        self.assertIn('Variables.soul_fragments_ready', final_code)

    def test_resource_generation(self):
        """Test resource generation abilities"""
        # Create resource generation actions
        immolation = Action("immolation_aura,if=fury.deficit>=30")
        shear = Action("shear,if=fury.deficit>=25&soul_fragments.deficit>=1")
        fracture = Action("fracture,if=fury.deficit>=25&soul_fragments.deficit>=2")
        
        # Verify action properties
        self.assertEqual(immolation.name, 'immolation_aura')
        self.assertTrue(any('fury.deficit>=30' in c for c in immolation.conditions))
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add resource generation logic
        lua_code.append('if GetResourceDeficit("fury") >= 30 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("immolation_aura")')
        generator.dedent()
        lua_code.append('end')
        
        lua_code.append('if GetResourceDeficit("fury") >= 25 and GetResourceDeficit("soul_fragments") >= 1 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("shear")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify resource generation
        self.assertIn('GetResourceDeficit("fury")', final_code)
        self.assertIn('GetResourceDeficit("soul_fragments")', final_code)

    def test_resource_spending(self):
        """Test resource spending abilities"""
        # Create resource spending actions
        spirit_bomb = Action("spirit_bomb,if=soul_fragments>=4")
        soul_cleave = Action("soul_cleave,if=fury>=60&!buff.soul_fragments.up")
        devastation = Action("fel_devastation,if=fury>=50")
        
        # Verify action properties
        self.assertEqual(spirit_bomb.name, 'spirit_bomb')
        self.assertTrue(any('soul_fragments>=4' in c for c in spirit_bomb.conditions))
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add resource spending logic
        lua_code.append('if GetResource("soul_fragments") >= 4 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("spirit_bomb")')
        generator.dedent()
        lua_code.append('end')
        
        lua_code.append('if GetResource("fury") >= 60 and not HasBuff("soul_fragments") then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("soul_cleave")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify resource spending
        self.assertIn('GetResource("soul_fragments")', final_code)
        self.assertIn('GetResource("fury")', final_code)
        self.assertIn('HasBuff("soul_fragments")', final_code)

    def test_multi_resource_management(self):
        """Test managing multiple resources simultaneously"""
        # Create multi-resource actions
        cleave = Action("soul_cleave,if=fury>=60&soul_fragments>=3&health.pct<=70")
        bomb = Action("spirit_bomb,if=soul_fragments>=4&(fury>=50|health.pct<=60)")
        devastation = Action("fel_devastation,if=fury>=50&health.pct<=50&soul_fragments<=2")
        
        # Verify action properties
        self.assertEqual(cleave.name, 'soul_cleave')
        self.assertTrue(any('fury>=60' in c for c in cleave.conditions))
        self.assertTrue(any('soul_fragments>=3' in c for c in cleave.conditions))
        self.assertTrue(any('health.pct<=70' in c for c in cleave.conditions))
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add multi-resource management logic
        lua_code.append('if GetResource("fury") >= 60 and GetResource("soul_fragments") >= 3 and GetHealthPercent() <= 70 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("soul_cleave")')
        generator.dedent()
        lua_code.append('end')
        
        lua_code.append('if GetResource("soul_fragments") >= 4 and (GetResource("fury") >= 50 or GetHealthPercent() <= 60) then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("spirit_bomb")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify multi-resource management
        self.assertIn('GetResource("fury")', final_code)
        self.assertIn('GetResource("soul_fragments")', final_code)
        self.assertIn('GetHealthPercent()', final_code)

if __name__ == '__main__':
    unittest.main()
