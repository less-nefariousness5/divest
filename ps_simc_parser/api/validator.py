"""Validator for SimC conditions."""

from .resources import RESOURCE_MAPPINGS
from .spells import convert_spell, SPELL_MAPPINGS


def is_valid_spell(spell_name: str) -> bool:
    """Check if a spell name is valid."""
    if not spell_name:
        return False
        
    try:
        # Normalize spell name by converting to lowercase and replacing spaces/underscores
        normalized_name = spell_name.lower().replace(' ', '_')
        
        # Handle variables
        if normalized_name == 'variable':
            return True
            
        # Check in SPELL_MAPPINGS
        if normalized_name in SPELL_MAPPINGS:
            return True
            
        # Handle consumables and utility actions
        if normalized_name in [
            'flask', 'augmentation', 'food', 'snapshot_stats', 'potion',
            'use_item', 'auto_attack', 'wait', 'call_action_list', 'run_action_list'
        ]:
            return True
            
        # Try to convert the spell name
        convert_spell(normalized_name)
        return True
    except ValueError:
        return False


def is_valid_condition(condition: str) -> bool:
    """Check if a condition is valid."""
    if not condition:
        return False

    # Handle negation
    if condition.startswith('!'):
        return is_valid_condition(condition[1:])

    # Handle complex conditions with & and |
    if '&' in condition:
        return all(is_valid_condition(c.strip()) for c in condition.split('&'))
    if '|' in condition:
        return all(is_valid_condition(c.strip()) for c in condition.split('|'))

    # Handle namespaces
    if condition.startswith((
        'Variables.', 'Mechanics.', 'Position.', 'Player.',
        'hero_tree.', 'talent.', 'buff.', 'debuff.',
        'cooldown.', 'spell.', 'resource.'
    )):
        return True

    # Handle special conditions
    if condition in ('not.in.position', 'true', 'false'):
        return True

    # Handle numeric comparisons
    if any(op in condition for op in ('>', '<', '>=', '<=', '==', '!=')):
        return True

    return False


def _check_numeric_comparison(comparison: str) -> bool:
    """Helper function to check numeric comparisons."""
    if not comparison:
        return False
        
    for op in ['>=', '<=', '>', '<', '=']:
        if op in comparison:
            try:
                value = float(comparison.split(op)[1].strip())
                return True
            except (ValueError, IndexError):
                return False
                
    return False