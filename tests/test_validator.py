"""Test validator functionality."""

import unittest
from ps_simc_parser.api.validator import is_valid_spell, is_valid_condition
from ps_simc_parser.api.spells import SPELL_MAPPINGS

class TestValidator(unittest.TestCase):
    """Test validator functions."""
    
    def setUp(self):
        print("\nSetting up test...")
    
    def test_valid_spells(self):
        """Test valid spell validation."""
        print("\nTesting valid spells...")
        # Test a known spell from SPELL_MAPPINGS
        first_spell = next(iter(SPELL_MAPPINGS))
        print(f"Testing spell: {first_spell}")
        self.assertTrue(is_valid_spell(first_spell))
        
        # Test with spaces and underscores
        print("Testing spell variations...")
        self.assertTrue(is_valid_spell("immolation_aura"))
        self.assertTrue(is_valid_spell("immolation aura"))
        self.assertTrue(is_valid_spell("IMMOLATION_AURA"))
        
    def test_invalid_spells(self):
        """Test invalid spell validation."""
        print("\nTesting invalid spells...")
        self.assertFalse(is_valid_spell(""))
        self.assertFalse(is_valid_spell("nonexistent_spell"))
        self.assertFalse(is_valid_spell("!@#$"))
        
    def test_empty_condition(self):
        """Test empty condition validation."""
        print("\nTesting empty conditions...")
        self.assertFalse(is_valid_condition(""))
        self.assertFalse(is_valid_condition(None))
        
    def test_negated_conditions(self):
        """Test negated condition validation."""
        print("\nTesting negated conditions...")
        self.assertTrue(is_valid_condition("!buff.metamorphosis.up"))
        self.assertTrue(is_valid_condition("!cooldown.fel_devastation.ready"))
        
    def test_namespace_conditions(self):
        """Test namespace condition validation."""
        print("\nTesting namespace conditions...")
        namespaces = [
            "Variables.use_fiery_brand",
            "Mechanics.is_moving",
            "Position.distance",
            "Player.health_percent"
        ]
        for condition in namespaces:
            print(f"Testing namespace: {condition}")
            self.assertTrue(is_valid_condition(condition))
            
    def test_special_conditions(self):
        """Test special condition validation."""
        print("\nTesting special conditions...")
        self.assertTrue(is_valid_condition("not.in.position"))
        
    def test_buff_conditions(self):
        """Test buff condition validation."""
        print("\nTesting buff conditions...")
        self.assertTrue(is_valid_condition("buff.metamorphosis.up"))
        self.assertTrue(is_valid_condition("buff.demon_spikes.up"))
        
    def test_cooldown_conditions(self):
        """Test cooldown condition validation."""
        print("\nTesting cooldown conditions...")
        self.assertTrue(is_valid_condition("cooldown.fel_devastation.ready"))
        self.assertTrue(is_valid_condition("cooldown.fiery_brand.ready"))
        
    def test_variable_conditions(self):
        """Test variable condition validation."""
        print("\nTesting variable conditions...")
        self.assertTrue(is_valid_condition("variable.brand_for_next_pack"))
        self.assertTrue(is_valid_condition("variable.use_defensive"))
        
    def test_target_conditions(self):
        """Test target condition validation."""
        print("\nTesting target conditions...")
        conditions = [
            "target.distance",
            "target.time_to_die",
            "target.health.pct<20",
            "target.distance<=8"
        ]
        for condition in conditions:
            print(f"Testing target condition: {condition}")
            self.assertTrue(is_valid_condition(condition))
            
    def test_position_conditions(self):
        """Test position condition validation."""
        print("\nTesting position conditions...")
        self.assertTrue(is_valid_condition("position.safe_location_available"))
        
    def test_mechanic_conditions(self):
        """Test mechanic condition validation."""
        print("\nTesting mechanic conditions...")
        self.assertTrue(is_valid_condition("mechanic.immunity_required"))
        
    def test_active_enemies(self):
        """Test active enemies condition validation."""
        print("\nTesting active enemies conditions...")
        conditions = [
            "active_enemies>2",
            "active_enemies>=3",
            "active_enemies>1.5"
        ]
        for condition in conditions:
            print(f"Testing active enemies condition: {condition}")
            self.assertTrue(is_valid_condition(condition))
            
        # Invalid conditions
        print("Testing invalid active enemies conditions...")
        self.assertFalse(is_valid_condition("active_enemies>invalid"))
        
    def test_incoming_damage(self):
        """Test incoming damage condition validation."""
        print("\nTesting incoming damage conditions...")
        conditions = [
            "incoming_damage_5s>100000",
            "incoming_damage_10s>=50000",
            "incoming_damage_3s<75000"
        ]
        for condition in conditions:
            print(f"Testing incoming damage condition: {condition}")
            self.assertTrue(is_valid_condition(condition))
            
        # Invalid conditions
        print("Testing invalid incoming damage conditions...")
        invalid_conditions = [
            "incoming_damage_invalid>100000",  # Invalid time window
            "incoming_damage_5>100000",  # Missing 's' suffix
            "incoming_damage_5s100000",  # Missing operator
            "incoming_damage_5s>invalid"  # Invalid value
        ]
        for condition in invalid_conditions:
            print(f"Testing invalid incoming damage condition: {condition}")
            self.assertFalse(is_valid_condition(condition))
            
    def test_resource_conditions(self):
        """Test resource condition validation."""
        print("\nTesting resource conditions...")
        resources = [
            "fury>50",
            "soul_fragments>=3",
            "health<=20",
            "fury.deficit<30"
        ]
        for condition in resources:
            print(f"Testing resource condition: {condition}")
            self.assertTrue(is_valid_condition(condition))
            
    def test_complex_conditions(self):
        """Test complex condition validation."""
        print("\nTesting complex conditions...")
        conditions = [
            "buff.metamorphosis.up&active_enemies>=2",
            "fury>=50&soul_fragments>=3",
            "!buff.demon_spikes.up&health<=40",
            "target.health.pct<=20|player.buff.metamorphosis.up"
        ]
        for condition in conditions:
            print(f"Testing complex condition: {condition}")
            self.assertTrue(is_valid_condition(condition))
