"""Spell conversion utilities."""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class SpellMapping:
    """Mapping for spell names and IDs"""
    simc_name: str
    ps_name: str
    spell_id: int


# Define spell mappings
SPELL_MAPPINGS: Dict[str, SpellMapping] = {
    # Consumables and utility actions
    'flask': SpellMapping('Flask', 'UseFlask', spell_id=0),
    'augmentation': SpellMapping('Augmentation', 'UseAugmentation', spell_id=0),
    'food': SpellMapping('Food', 'UseFood', spell_id=0),
    'snapshot_stats': SpellMapping('SnapshotStats', 'SnapshotStats', spell_id=0),
    'potion': SpellMapping('Potion', 'UsePotion', spell_id=0),
    'use_item': SpellMapping('UseItem', 'UseItem', spell_id=0),
    'auto_attack': SpellMapping('AutoAttack', 'AutoAttack', spell_id=0),
    'wait': SpellMapping('Wait', 'Wait', spell_id=0),
    'call_action_list': SpellMapping('CallActionList', 'CallActionList', spell_id=0),
    'run_action_list': SpellMapping('RunActionList', 'RunActionList', spell_id=0),
    
    # Demon Hunter spells
    'spirit_bomb': SpellMapping('SpiritBomb', 'SpiritBomb', spell_id=247454),
    '/spirit_bomb': SpellMapping('SpiritBomb', 'SpiritBomb', spell_id=247454),
    'fel_devastation': SpellMapping('FelDevastation', 'FelDevastation', spell_id=212084),
    '/fel_devastation': SpellMapping('FelDevastation', 'FelDevastation', spell_id=212084),
    'metamorphosis': SpellMapping('Metamorphosis', 'Metamorphosis', spell_id=187827),
    '/metamorphosis': SpellMapping('Metamorphosis', 'Metamorphosis', spell_id=187827),
    'demon_spikes': SpellMapping('DemonSpikes', 'DemonSpikes', spell_id=203720),
    '/demon_spikes': SpellMapping('DemonSpikes', 'DemonSpikes', spell_id=203720),
    'fiery_brand': SpellMapping('FieryBrand', 'FieryBrand', spell_id=204021),
    '/fiery_brand': SpellMapping('FieryBrand', 'FieryBrand', spell_id=204021),
    'infernal_strike': SpellMapping('InfernalStrike', 'InfernalStrike', spell_id=189110),
    '/infernal_strike': SpellMapping('InfernalStrike', 'InfernalStrike', spell_id=189110),
    'sigil_of_flame': SpellMapping('SigilOfFlame', 'SigilOfFlame', spell_id=204596),
    '/sigil_of_flame': SpellMapping('SigilOfFlame', 'SigilOfFlame', spell_id=204596),
    'throw_glaive': SpellMapping('ThrowGlaive', 'ThrowGlaive', spell_id=204157),
    '/throw_glaive': SpellMapping('ThrowGlaive', 'ThrowGlaive', spell_id=204157),
    'immolation_aura': SpellMapping('ImmolationAura', 'ImmolationAura', spell_id=258920),
    '/immolation_aura': SpellMapping('ImmolationAura', 'ImmolationAura', spell_id=258920),
    'soul_cleave': SpellMapping('SoulCleave', 'SoulCleave', spell_id=228477),
    '/soul_cleave': SpellMapping('SoulCleave', 'SoulCleave', spell_id=228477),
    'fracture': SpellMapping('Fracture', 'Fracture', spell_id=263642),
    '/fracture': SpellMapping('Fracture', 'Fracture', spell_id=263642),
    'shear': SpellMapping('Shear', 'Shear', spell_id=203782),
    '/shear': SpellMapping('Shear', 'Shear', spell_id=203782),
    'felblade': SpellMapping('Felblade', 'Felblade', spell_id=232893),
    '/felblade': SpellMapping('Felblade', 'Felblade', spell_id=232893),
    'empower_wards': SpellMapping('EmpowerWards', 'EmpowerWards', spell_id=218256),
    '/empower_wards': SpellMapping('EmpowerWards', 'EmpowerWards', spell_id=218256),
    
    # Mage spells (keeping these for reference)
    'fireball': SpellMapping('Fireball', 'Fireball', spell_id=133),
    'frostbolt': SpellMapping('Frostbolt', 'Frostbolt', spell_id=116),
    'arcane_blast': SpellMapping('ArcaneBlast', 'ArcaneBlast', spell_id=30451),
}


def convert_spell(simc_spell: str) -> Optional[SpellMapping]:
    """Convert SimC spell name to PS spell"""
    # Remove leading slash if present
    if simc_spell.startswith('/'):
        simc_spell = simc_spell[1:]
    return SPELL_MAPPINGS.get(simc_spell.lower())


class Spells:
    """Class to provide access to spell mappings"""
    def __init__(self):
        pass

    def __getattr__(self, name: str) -> str:
        """Get spell name by attribute access"""
        # Convert camelCase to snake_case for lookup
        lookup_name = ''.join(['_' + c.lower() if c.isupper() else c.lower() for c in name]).lstrip('_')
        mapping = SPELL_MAPPINGS.get(lookup_name)
        if mapping is None:
            raise AttributeError(f"Unknown spell: {name}")
        return mapping.ps_name