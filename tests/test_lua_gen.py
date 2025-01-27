"""
Tests for the lua_gen module
"""
import pytest
from ps_simc_parser.lua_gen.generator import LuaGenerator, GeneratorError
from ps_simc_parser.lua_gen.templates import LuaTemplate

def test_lua_template_basic():
    """Test basic template rendering"""
    template = LuaTemplate()
    context = {
        'metadata': {
            'name': 'Test Rotation',
            'profile': 'test',
            'class': 'DemonHunter',
            'spec': 'Vengeance',
            'role': 'tank'
        }
    }
    
    result = template.render(context)
    
    # Check basic structure
    assert "-- Generated by PS SimC Parser" in result
    assert "local PS = ..." in result
    assert "local Spell = PS.Spell" in result
    assert "local Player = PS.Player" in result
    assert "local Target = Player.Target" in result
    assert "local Enemies = Player.Enemies" in result
    
    # Check metadata
    assert 'Name = "Test Rotation"' in result
    assert 'Profile = "test"' in result
    assert 'Class = "DemonHunter"' in result
    assert 'Spec = "Vengeance"' in result
    assert 'Role = "tank"' in result

def test_lua_generator_basic():
    """Test basic Lua code generation"""
    generator = LuaGenerator()
    actions = [
        {
            'action': 'spirit_bomb',
            'type': 'spell',
            'conditions': ['soul_fragments >= 4']
        }
    ]
    context = {
        'metadata': {
            'name': 'Test Rotation',
            'profile': 'test'
        }
    }
    
    result = generator.generate(actions, context)
    
    # Check basic structure
    assert "-- Generated by PS SimC Parser" in result
    assert "local PS = ..." in result
    assert "local Spell = PS.Spell" in result
    
    # Check generated action
    assert "if Player.SoulFragments >= 4 then" in result
    assert "if Spell.SpiritBomb:IsReady() then" in result
    assert "return Cast(Spell.SpiritBomb)" in result

def test_lua_generator_multiple_actions():
    """Test generating multiple actions"""
    generator = LuaGenerator()
    actions = [
        {
            'action': 'immolation_aura',
            'type': 'spell'
        },
        {
            'action': 'spirit_bomb',
            'type': 'spell',
            'conditions': ['soul_fragments >= 4']
        },
        {
            'action': 'sigil_of_flame',
            'type': 'spell',
            'conditions': ['!debuff.sigil_of_flame.up']
        }
    ]
    context = {'metadata': {'name': 'Test'}}
    
    result = generator.generate(actions, context)
    
    # Check all actions are present
    assert "if Spell.ImmolationAura:IsReady() then" in result
    assert "if Player.SoulFragments >= 4 then" in result
    assert "if Spell.SpiritBomb:IsReady() then" in result
    assert "if not Target:DebuffUp(Spell.SigilOfFlame) then" in result
    assert "return Cast(Spell.SigilOfFlame, 'ground')" in result

def test_lua_generator_error_handling():
    """Test error handling in generator"""
    generator = LuaGenerator()
    
    # Test invalid spell
    with pytest.raises(GeneratorError):
        generator.generate([{'action': 'invalid_spell', 'type': 'spell'}], {})

def test_lua_template_cache():
    """Test cache functionality in template"""
    template = LuaTemplate()
    result = template.render({})
    
    # Check cache functions
    assert "function Cache:Get(key, default)" in result
    assert "return self[key] or default" in result
    assert "function Cache:Set(key, value)" in result
    assert "self[key] = value" in result

def test_lua_generator_complex_conditions():
    """Test generating complex conditions"""
    generator = LuaGenerator()
    actions = [
        {
            'action': 'spirit_bomb',
            'type': 'spell',
            'conditions': [
                'soul_fragments >= 4',
                '!buff.metamorphosis.up',
                'target.time_to_die > 10'
            ]
        }
    ]
    context = {'metadata': {'name': 'Test'}}
    
    result = generator.generate(actions, context)
    
    assert "if Player.SoulFragments >= 4 and not Player:BuffUp(Spell.Metamorphosis) and Target.TimeToDie > 10 then" in result
    assert "if Spell.SpiritBomb:IsReady() then" in result
    assert "return Cast(Spell.SpiritBomb)" in result
