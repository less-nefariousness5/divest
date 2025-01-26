"""Test action parser functionality."""

import unittest
from ps_simc_parser.parser.actions import Action, ActionList, ActionType, ActionParser
from ps_simc_parser.api.mapping import SpellMapping
from ps_simc_parser.api.spells import Spells
from ps_simc_parser.utils.lua import LuaGenerator
from .base import PSTestCase

class TestActionParser(PSTestCase):
    """Test action parser functionality."""
    
    def setUp(self):
        """Set up test cases."""
        super().setUp()
        self.parser = ActionParser()
        self.generator = LuaGenerator()
        
    def test_generate_simple_action(self):
        """Test generating Lua code for a simple action."""
        actions = [Action("immolation_aura")]
        
        lua_code = self.parser.generate_lua(actions)
        self.assertIn("function Rotation:Execute()", lua_code)
        self.assertIn("local PS = ...", lua_code)
        self.assertIn("local Player = PS.Player", lua_code)
        self.assertIn("local Target = Player.Target", lua_code)
        self.assertIn("if Player:Cast(Spells.immolation_aura) then", lua_code)
        
    def test_generate_action_with_condition(self):
        """Test generating Lua code for an action with conditions."""
        actions = [Action("spirit_bomb,if=soul_fragments>=4")]
        
        lua_code = self.parser.generate_lua(actions)
        self.assertIn("if soul_fragments >= 4 then", lua_code)
        self.assertIn("if Player:Cast(Spells.spirit_bomb) then", lua_code)
        
    def test_generate_action_with_args(self):
        """Test generating Lua code for an action with arguments."""
        actions = [Action("sigil_of_flame,if=!debuff.sigil_of_flame.up,target=ground")]
        
        lua_code = self.parser.generate_lua(actions)
        self.assertIn("if !debuff.sigil_of_flame.up then", lua_code)
        self.assertIn("if Player:Cast(Spells.sigil_of_flame, 'ground') then", lua_code)
        
    def test_generate_multiple_actions(self):
        """Test generating Lua code for multiple actions."""
        actions = [
            Action("immolation_aura"),
            Action("spirit_bomb,if=soul_fragments>=4"),
            Action("sigil_of_flame,if=!debuff.sigil_of_flame.up,target=ground")
        ]
        
        lua_code = self.parser.generate_lua(actions)
        self.assertIn("if Player:Cast(Spells.immolation_aura) then", lua_code)
        self.assertIn("if soul_fragments >= 4 then", lua_code)
        self.assertIn("if Player:Cast(Spells.spirit_bomb) then", lua_code)
        self.assertIn("if !debuff.sigil_of_flame.up then", lua_code)
        self.assertIn("if Player:Cast(Spells.sigil_of_flame, 'ground') then", lua_code)
        
    def test_generate_variable(self):
        """Test generating Lua code for variable definitions."""
        actions = [
            Action("variable,name=test_var,value=5+buff.test_buff.stack"),
            Action("variable,name=another_var,value=test_var*2")
        ]
        
        lua_code = self.parser.generate_lua(actions)
        self.assertIn("Cache:Set('test_var', 5+buff.test_buff.stack)", lua_code)
        self.assertIn("Cache:Set('another_var', test_var*2)", lua_code)
        
    def test_generate_complex_conditions(self):
        """Test generating Lua code for complex conditions."""
        actions = [Action("spirit_bomb,if=soul_fragments>=4&!buff.metamorphosis.up&target.time_to_die>10")]
        
        lua_code = self.parser.generate_lua(actions)
        self.assertIn("if soul_fragments >= 4 and !buff.metamorphosis.up and target.time_to_die > 10 then", lua_code)
        self.assertIn("if Player:Cast(Spells.spirit_bomb) then", lua_code)

class TestActions(PSTestCase):
    def setUp(self):
        super().setUp()
        self.spell = SpellMapping('TestSpell', 'test_spell', spell_id=12345)
    
    def test_basic_action_creation(self):
        """Test creating a basic action"""
        action = Action('spell_name=test_spell')
        self.assertEqual(action.spell_name, 'test_spell')
        self.assertEqual(action.action_type, ActionType.SPELL)
        
    def test_action_with_conditions(self):
        """Test action with conditions"""
        action = Action('spell_name=test_spell,if=buff.test_buff.up&cooldown.test_cd.ready')
        self.assertEqual(action.spell_name, 'test_spell')
        self.assertTrue(action.has_conditions())
        self.assertIn('buff.test_buff.up', action.conditions)
        self.assertIn('cooldown.test_cd.ready', action.conditions)
        
    def test_variable_action(self):
        """Test variable action parsing"""
        action = Action('variable,name=test_var,value=5+buff.test_buff.stack')
        self.assertEqual(action.action_type, ActionType.VARIABLE)
        self.assertEqual(action.var_name, 'test_var')
        self.assertEqual(action.var_value, '5+buff.test_buff.stack')
        
    def test_pool_action(self):
        """Test resource pooling action"""
        action = Action('pool_resource,for_next=1,extra_amount=20')
        self.assertEqual(action.action_type, ActionType.POOL)
        self.assertTrue(action.pool_for_next)
        self.assertEqual(action.pool_extra_amount, 20)
        
    def test_call_action_list(self):
        """Test call action list"""
        action = Action('call_action_list,name=cleave,if=active_enemies>1')
        self.assertEqual(action.action_type, ActionType.CALL_ACTION_LIST)
        self.assertEqual(action.action_list_name, 'cleave')
        self.assertIn('active_enemies>1', action.conditions)
        
    def test_run_action_list(self):
        """Test run action list"""
        action = Action('run_action_list,name=st,strict=1')
        self.assertEqual(action.action_type, ActionType.RUN_ACTION_LIST)
        self.assertEqual(action.action_list_name, 'st')
        self.assertTrue(action.strict)
        
    def test_action_list_management(self):
        """Test action list management"""
        action_list = ActionList('test_list')
        action_list.add_action(Action('spell_name=test_spell'))
        action_list.add_action(Action('variable,name=test_var,value=5'))
        
        self.assertEqual(len(action_list.actions), 2)
        self.assertEqual(action_list.actions[0].spell_name, 'test_spell')
        self.assertEqual(action_list.actions[1].var_name, 'test_var')
        
    def test_action_list_preconditions(self):
        """Test action list preconditions"""
        action_list = ActionList('test_list', preconditions='buff.test_buff.up')
        self.assertEqual(action_list.preconditions, 'buff.test_buff.up')
        
    def test_action_validation(self):
        """Test action validation"""
        valid_action = Action('spell_name=test_spell')
        self.assertTrue(valid_action.is_valid())
        
        valid_var = Action('variable,name=test_var,value=5')
        self.assertTrue(valid_var.is_valid())
        
        invalid_var = Action('variable,value=5')  # Missing name
        self.assertFalse(invalid_var.is_valid())
        
    def test_complex_conditions(self):
        """Test complex condition parsing"""
        action = Action('spell_name=test_spell,if=buff.test_buff.up&cooldown.test_cd.ready|target.health.pct<20')
        self.assertTrue(action.has_conditions())
        self.assertEqual(len(action.conditions), 3)
        
    def test_target_conditions(self):
        """Test target-specific conditions"""
        action = Action('spell_name=test_spell,target_if=min:debuff.test_debuff.remains')
        self.assertEqual(action.target_condition, 'min:debuff.test_debuff.remains')
        
    def test_cycle_targets(self):
        """Test cycle_targets flag"""
        action = Action('spell_name=test_spell,cycle_targets=1')
        self.assertTrue(action.cycle_targets)
        
    def test_action_line_numbers(self):
        """Test line number tracking"""
        action = Action('spell_name=test_spell')
        action.line_number = 42
        self.assertEqual(action.line_number, 42)
        
    def test_action_comments(self):
        """Test action comments"""
        action = Action('spell_name=test_spell')
        action.comment = '# Test comment'
        self.assertEqual(action.comment, '# Test comment')
        
    def test_variable_operations(self):
        """Test different variable operations"""
        set_var = Action('variable,name=test_var,value=5,op=set')
        self.assertEqual(set_var.var_op, 'set')
        
        add_var = Action('variable,name=test_var,value=1,op=add')
        self.assertEqual(add_var.var_op, 'add')
        
        reset_var = Action('variable,name=test_var,op=reset')
        self.assertEqual(reset_var.var_op, 'reset')
