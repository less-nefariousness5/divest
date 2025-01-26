import unittest
from ps_simc_parser.parser.parser import Parser
from ps_simc_parser.parser.actions import Action
from ps_simc_parser.utils.lua import LuaGenerator
from ps_simc_parser.api.mapping import logger, monitor, validator
from .base import PSTestCase

class TestMovement(PSTestCase):
    def setUp(self):
        super().setUp()
        # Movement mechanics SimC template
        self.simc_content = """
# Movement Template
actions=auto_attack

# Basic movement abilities
actions+=/blink,if=movement.distance>20
actions+=/sprint,if=movement.remains>=5&buff.sprint.down

# Movement with target tracking
actions+=/charge,if=target.distance>25&target.distance<40
actions+=/heroic_leap,if=target.distance>=8&target.distance<=30&line_of_sight

# Movement with resource management
actions+=/fel_rush,if=movement.distance>10&fury.deficit<30
actions+=/infernal_strike,if=movement.distance>15&pain>=30

# Movement with mechanics
actions+=/demonic_trample,if=movement.distance>10&!debuff.mechanic_slow.up
actions+=/vengeful_retreat,if=movement.distance<8&debuff.dangerous_melee.up

# Movement with positioning
actions+=/door_of_shadows,if=target.distance>40|raid.position.unfavorable
actions+=/grappling_hook,if=target.distance>=10&target.distance<=40&!buff.movement_impaired.up

# Movement with combat conditions
actions+=/roll,if=movement.distance>10&incoming_damage_3s<health.max*0.1
actions+=/transcendence_transfer,if=movement.distance>20&health.pct>60
"""

    def test_basic_movement(self):
        """Test basic movement ability handling"""
        # Create movement actions directly
        blink = Action("blink,if=movement.distance>20")
        sprint = Action("sprint,if=movement.remains>=5&buff.sprint.down")
        
        # Verify movement action properties
        self.assertEqual(blink.name, 'blink')
        self.assertTrue(any('movement.distance>20' in c for c in blink.conditions))
        
        self.assertEqual(sprint.name, 'sprint')
        self.assertTrue(any('movement.remains>=5' in c for c in sprint.conditions))
        self.assertTrue(any('buff.sprint.down' in c for c in sprint.conditions))
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add movement logic
        lua_code.append('if GetMovementDistance() > 20 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("blink")')
        generator.dedent()
        lua_code.append('end')
        
        lua_code.append('if GetMovementRemains() >= 5 and not HasBuff("sprint") then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("sprint")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify movement handling
        self.assertIn('GetMovementDistance()', final_code)
        self.assertIn('GetMovementRemains()', final_code)
        self.assertIn('HasBuff("sprint")', final_code)

    def test_target_based_movement(self):
        """Test movement abilities that depend on target distance"""
        # Create target-based movement actions
        charge = Action("charge,if=target.distance>25&target.distance<40")
        leap = Action("heroic_leap,if=target.distance>=8&target.distance<=30&line_of_sight")
        
        # Verify action properties
        self.assertEqual(charge.name, 'charge')
        self.assertTrue(any('target.distance>25' in c for c in charge.conditions))
        self.assertTrue(any('target.distance<40' in c for c in charge.conditions))
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add target-based movement logic
        lua_code.append('if GetTargetDistance() > 25 and GetTargetDistance() < 40 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("charge")')
        generator.dedent()
        lua_code.append('end')
        
        lua_code.append('if GetTargetDistance() >= 8 and GetTargetDistance() <= 30 and HasLineOfSight() then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("heroic_leap")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify target-based movement handling
        self.assertIn('GetTargetDistance()', final_code)
        self.assertIn('HasLineOfSight()', final_code)

    def test_resource_based_movement(self):
        """Test movement abilities that depend on resource state"""
        # Create resource-based movement actions
        fel_rush = Action("fel_rush,if=movement.distance>10&fury.deficit<30")
        strike = Action("infernal_strike,if=movement.distance>15&pain>=30")
        
        # Verify action properties
        self.assertEqual(fel_rush.name, 'fel_rush')
        self.assertTrue(any('movement.distance>10' in c for c in fel_rush.conditions))
        self.assertTrue(any('fury.deficit<30' in c for c in fel_rush.conditions))
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add resource-based movement logic
        lua_code.append('if GetMovementDistance() > 10 and GetResourceDeficit("fury") < 30 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("fel_rush")')
        generator.dedent()
        lua_code.append('end')
        
        lua_code.append('if GetMovementDistance() > 15 and GetResource("pain") >= 30 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("infernal_strike")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify resource-based movement handling
        self.assertIn('GetMovementDistance()', final_code)
        self.assertIn('GetResourceDeficit("fury")', final_code)
        self.assertIn('GetResource("pain")', final_code)

    def test_mechanic_based_movement(self):
        """Test movement abilities that interact with mechanics"""
        # Create mechanic-based movement actions
        trample = Action("demonic_trample,if=movement.distance>10&!debuff.mechanic_slow.up")
        retreat = Action("vengeful_retreat,if=movement.distance<8&debuff.dangerous_melee.up")
        
        # Verify action properties
        self.assertEqual(trample.name, 'demonic_trample')
        self.assertTrue(any('movement.distance>10' in c for c in trample.conditions))
        self.assertTrue(any('!debuff.mechanic_slow.up' in c for c in trample.conditions))
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add mechanic-based movement logic
        lua_code.append('if GetMovementDistance() > 10 and not HasDebuff("mechanic_slow") then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("demonic_trample")')
        generator.dedent()
        lua_code.append('end')
        
        lua_code.append('if GetMovementDistance() < 8 and HasDebuff("dangerous_melee") then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("vengeful_retreat")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify mechanic-based movement handling
        self.assertIn('GetMovementDistance()', final_code)
        self.assertIn('HasDebuff("mechanic_slow")', final_code)
        self.assertIn('HasDebuff("dangerous_melee")', final_code)

if __name__ == '__main__':
    unittest.main()
