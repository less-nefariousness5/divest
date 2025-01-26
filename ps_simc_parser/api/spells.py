"""Spell conversion utilities."""

from dataclasses import dataclass


@dataclass
class SpellMapping:
    """Mapping for spell names and IDs"""
    simc_name: str
    ps_name: str
    spell_id: int


def convert_spell(spell_name: str) -> str:
    """Convert a SimC spell name to PS spell name."""
    if not spell_name:
        raise ValueError("Empty spell name")
        
    # Normalize spell name
    normalized_name = spell_name.lower().replace(' ', '_')
    
    # Look up in spell mappings
    if normalized_name in SPELL_MAPPINGS:
        return SPELL_MAPPINGS[normalized_name].ps_name
        
    raise ValueError(f"Unknown spell: {spell_name}")


# Define core mappings
SPELL_MAPPINGS = {
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
    'invoke_external_buff': SpellMapping('InvokeExternalBuff', 'InvokeExternalBuff', spell_id=0),
    
    # Demon Hunter spells
    'shear': SpellMapping('Shear', 'Shear', spell_id=203782),
    '/shear': SpellMapping('Shear', 'Shear', spell_id=203782),
    'fel_desolation': SpellMapping('FelDesolation', 'FelDesolation', spell_id=212084),
    '/fel_desolation': SpellMapping('FelDesolation', 'FelDesolation', spell_id=212084),
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
    'sigil_of_doom': SpellMapping('SigilOfDoom', 'SigilOfDoom', spell_id=202137),
    '/sigil_of_doom': SpellMapping('SigilOfDoom', 'SigilOfDoom', spell_id=202137),
    'throw_glaive': SpellMapping('ThrowGlaive', 'ThrowGlaive', spell_id=204157),
    '/throw_glaive': SpellMapping('ThrowGlaive', 'ThrowGlaive', spell_id=204157),
    'immolation_aura': SpellMapping('ImmolationAura', 'ImmolationAura', spell_id=258920),
    '/immolation_aura': SpellMapping('ImmolationAura', 'ImmolationAura', spell_id=258920),
    'soul_cleave': SpellMapping('SoulCleave', 'SoulCleave', spell_id=228477),
    '/soul_cleave': SpellMapping('SoulCleave', 'SoulCleave', spell_id=228477),
    'fracture': SpellMapping('Fracture', 'Fracture', spell_id=263642),
    '/fracture': SpellMapping('Fracture', 'Fracture', spell_id=263642),
    'felblade': SpellMapping('Felblade', 'Felblade', spell_id=232893),
    '/felblade': SpellMapping('Felblade', 'Felblade', spell_id=232893),
    'disrupt': SpellMapping('Disrupt', 'Disrupt', spell_id=183752),
    '/disrupt': SpellMapping('Disrupt', 'Disrupt', spell_id=183752),
    'arcane_torrent': SpellMapping('ArcaneTorrent', 'ArcaneTorrent', spell_id=202719),
    '/arcane_torrent': SpellMapping('ArcaneTorrent', 'ArcaneTorrent', spell_id=202719),
    'sigil_of_spite': SpellMapping('SigilOfSpite', 'SigilOfSpite', spell_id=202798),
    '/sigil_of_spite': SpellMapping('SigilOfSpite', 'SigilOfSpite', spell_id=202798),
    'vengeful_retreat': SpellMapping('VengefulRetreat', 'VengefulRetreat', spell_id=198793),
    '/vengeful_retreat': SpellMapping('VengefulRetreat', 'VengefulRetreat', spell_id=198793),
    'soul_carver': SpellMapping('SoulCarver', 'SoulCarver', spell_id=207407),
    '/soul_carver': SpellMapping('SoulCarver', 'SoulCarver', spell_id=207407),
    'spirit_burst': SpellMapping('SpiritBurst', 'SpiritBurst', spell_id=227225),
    '/spirit_burst': SpellMapping('SpiritBurst', 'SpiritBurst', spell_id=227225),
    'soul_sunder': SpellMapping('SoulSunder', 'SoulSunder', spell_id=227174),
    '/soul_sunder': SpellMapping('SoulSunder', 'SoulSunder', spell_id=227174),
    'bulk_extraction': SpellMapping('BulkExtraction', 'BulkExtraction', spell_id=320341),
    '/bulk_extraction': SpellMapping('BulkExtraction', 'BulkExtraction', spell_id=320341),
    'reavers_glaive': SpellMapping('ReaversGlaive', 'ReaversGlaive', spell_id=272794),
    '/reavers_glaive': SpellMapping('ReaversGlaive', 'ReaversGlaive', spell_id=272794),
    'the_hunt': SpellMapping('TheHunt', 'TheHunt', spell_id=370965),
    '/the_hunt': SpellMapping('TheHunt', 'TheHunt', spell_id=370965),
}