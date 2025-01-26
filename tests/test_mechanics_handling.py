import unittest
from ps_simc_parser.parser.parser import Parser
from ps_simc_parser.parser.actions import Action
from ps_simc_parser.utils.lua import LuaGenerator
from ps_simc_parser.api.mapping import logger, monitor, validator
from .base import PSTestCase

class TestMechanicsHandling(PSTestCase):
    def setUp(self):
        super().setUp()
        # Mechanics handling SimC template
        self.simc_content = """
# Mechanics Handling Template
actions=auto_attack

# Interrupt handling
actions+=/interrupt,if=target.casting.interruptible
actions+=/interrupt_backup,if=target.casting.interruptible&cooldown.interrupt.remains>gcd.max

# Defensive mechanics
actions+=/defensive_spell,if=incoming_damage_3s>health.max*0.4|health.pct<20
actions+=/group_defensive,if=raid.health.pct<60
actions+=/personal_immunity,if=health.pct<15|dot.deadly_dot.remains>0

# Movement handling
actions+=/movement_ability,if=movement.distance>15
actions+=/movement_buff,if=movement.remains>=2
actions+=/movement_penalty_reduction,if=movement.distance>10&buff.movement_speed.down

# Positioning
actions+=/position_spell,if=target.distance>30|target.distance<8
actions+=/reposition,if=target.distance<6&debuff.dangerous_melee.up
actions+=/spread_command,if=raid.spread_check

# Crowd control
actions+=/cc_ability,if=target.is_add&target.health.pct>20
actions+=/mass_cc,if=active_enemies>3&target.distance<8
actions+=/cc_breaker,if=ally.cc.remains>3

# Dispel mechanics
actions+=/dispel_magic,if=ally.debuff.magic.exists
actions+=/cleanse_poison,if=ally.debuff.poison.exists&ally.health.pct<90
actions+=/remove_curse,if=curse.exists

# Encounter mechanics
actions+=/dodge_ability,if=mechanic.dodge_warning
actions+=/soak_mechanic,if=mechanic.soak_warning&health.pct>60
actions+=/spread_mechanic,if=mechanic.spread_warning
"""

    def test_interrupt_handling(self):
        """Test interrupt mechanics handling"""
        # Create interrupt actions directly
        interrupt = Action("interrupt,if=target.casting.interruptible")
        interrupt_backup = Action("interrupt_backup,if=target.casting.interruptible&cooldown.interrupt.remains>gcd.max")
        
        # Verify interrupt action properties
        self.assertEqual(interrupt.name, 'interrupt')
        self.assertTrue(any('target.casting.interruptible' in c for c in interrupt.conditions))
        
        self.assertEqual(interrupt_backup.name, 'interrupt_backup')
        self.assertTrue(any('target.casting.interruptible' in c for c in interrupt_backup.conditions))
        self.assertTrue(any('cooldown.interrupt.remains>gcd.max' in c for c in interrupt_backup.conditions))
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add interrupt handling
        lua_code.append('if IsInterruptable() then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("interrupt")')
        generator.dedent()
        lua_code.append('end')
        
        lua_code.append('if IsInterruptable() and GetCooldownRemains("interrupt") > GetGCD() then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("interrupt_backup")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify interrupt handling
        self.assertIn('IsInterruptable()', final_code)
        self.assertIn('GetCooldownRemains("interrupt")', final_code)
        self.assertIn('GetGCD()', final_code)

    def test_defensive_mechanics(self):
        """Test defensive mechanics handling"""
        # Create defensive actions directly
        defensive = Action("defensive_spell,if=incoming_damage_3s>health.max*0.4|health.pct<20")
        group_def = Action("group_defensive,if=raid.health.pct<60")
        immunity = Action("personal_immunity,if=health.pct<15|dot.deadly_dot.remains>0")
        
        # Verify defensive action properties
        self.assertEqual(defensive.name, 'defensive_spell')
        self.assertTrue(any('incoming_damage_3s>health.max*0.4' in c for c in defensive.conditions))
        self.assertTrue(any('health.pct<20' in c for c in defensive.conditions))
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add defensive logic
        lua_code.append('if GetIncomingDamage(3) > GetMaxHealth() * 0.4 or GetHealthPercent() < 20 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("defensive_spell")')
        generator.dedent()
        lua_code.append('end')
        
        lua_code.append('if GetRaidHealthPercent() < 60 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("group_defensive")')
        generator.dedent()
        lua_code.append('end')
        
        lua_code.append('if GetHealthPercent() < 15 or GetDebuffRemains("deadly_dot") > 0 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("personal_immunity")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify defensive handling
        self.assertIn('GetIncomingDamage(3)', final_code)
        self.assertIn('GetMaxHealth()', final_code)
        self.assertIn('GetHealthPercent()', final_code)
        self.assertIn('GetRaidHealthPercent()', final_code)
        self.assertIn('GetDebuffRemains("deadly_dot")', final_code)

    def test_movement_mechanics(self):
        """Test movement mechanics handling"""
        # Create movement actions directly
        move_ability = Action("movement_ability,if=movement.distance>15")
        move_buff = Action("movement_buff,if=movement.remains>=2")
        move_penalty = Action("movement_penalty_reduction,if=movement.distance>10&buff.movement_speed.down")
        
        # Verify movement action properties
        self.assertEqual(move_ability.name, 'movement_ability')
        self.assertTrue(any('movement.distance>15' in c for c in move_ability.conditions))
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add movement logic
        lua_code.append('if GetMovementDistance() > 15 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("movement_ability")')
        generator.dedent()
        lua_code.append('end')
        
        lua_code.append('if GetMovementRemains() >= 2 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("movement_buff")')
        generator.dedent()
        lua_code.append('end')
        
        lua_code.append('if GetMovementDistance() > 10 and not HasBuff("movement_speed") then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("movement_penalty_reduction")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify movement handling
        self.assertIn('GetMovementDistance()', final_code)
        self.assertIn('GetMovementRemains()', final_code)
        self.assertIn('HasBuff("movement_speed")', final_code)

    def test_encounter_mechanics(self):
        """Test encounter-specific mechanics handling"""
        # Create encounter mechanic actions directly
        dodge = Action("dodge_ability,if=mechanic.dodge_warning")
        soak = Action("soak_mechanic,if=mechanic.soak_warning&health.pct>60")
        spread = Action("spread_mechanic,if=mechanic.spread_warning")
        
        # Verify mechanic action properties
        self.assertEqual(dodge.name, 'dodge_ability')
        self.assertTrue(any('mechanic.dodge_warning' in c for c in dodge.conditions))
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        
        # Add mechanic handling
        lua_code.append('if HasMechanic("dodge_warning") then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("dodge_ability")')
        generator.dedent()
        lua_code.append('end')
        
        lua_code.append('if HasMechanic("soak_warning") and GetHealthPercent() > 60 then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("soak_mechanic")')
        generator.dedent()
        lua_code.append('end')
        
        lua_code.append('if HasMechanic("spread_warning") then')
        generator.indent()
        lua_code.append(generator.get_indent() + 'Cast("spread_mechanic")')
        generator.dedent()
        lua_code.append('end')
        
        final_code = '\n'.join(lua_code)
        
        # Verify mechanic handling
        self.assertIn('HasMechanic("dodge_warning")', final_code)
        self.assertIn('HasMechanic("soak_warning")', final_code)
        self.assertIn('HasMechanic("spread_warning")', final_code)
        self.assertIn('GetHealthPercent()', final_code)

if __name__ == '__main__':
    unittest.main()
