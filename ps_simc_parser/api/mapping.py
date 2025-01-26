"""
API mapping definitions for converting SimC concepts to PS API
"""
from typing import Dict, Optional, Any, List
from dataclasses import dataclass
import time
import logging
from datetime import datetime
import re
from .validator import is_valid_condition
from .resources import RESOURCE_MAPPINGS
from .spells import convert_spell, SpellMapping, SPELL_MAPPINGS

@dataclass
class SpellMapping:
    """Mapping for spell names and IDs"""
    simc_name: str
    ps_name: str
    spell_id: int

@dataclass
class ResourceMapping:
    """Mapping for resource types"""
    simc_name: str
    ps_getter: str

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

RESOURCE_MAPPINGS: Dict[str, ResourceMapping] = {
    'fury': ResourceMapping(
        simc_name='fury',
        ps_getter='Player.Fury'
    ),
    'energy': ResourceMapping(
        simc_name='energy',
        ps_getter='Player.Energy'
    ),
    'mana': ResourceMapping(
        simc_name='mana',
        ps_getter='Player.Mana'
    ),
    'soul_fragments': ResourceMapping(
        simc_name='soul_fragments',
        ps_getter='Player.SoulFragments'
    ),
}

# Conversion functions
def convert_spell(simc_spell: str) -> Optional[SpellMapping]:
    """Convert SimC spell name to PS spell"""
    # Remove leading slash if present
    if simc_spell.startswith('/'):
        simc_spell = simc_spell[1:]
    return SPELL_MAPPINGS.get(simc_spell.lower())

def convert_condition(condition: str) -> str:
    """Convert a SimC condition to PS condition."""
    if not condition:
        return 'true'
        
    # Handle negation
    if condition.startswith('!'):
        return f'not ({convert_condition(condition[1:])})'
        
    # Handle complex conditions with & and |
    if '&' in condition:
        parts = [convert_condition(c.strip()) for c in condition.split('&')]
        return f'({" and ".join(parts)})'
    if '|' in condition:
        parts = [convert_condition(c.strip()) for c in condition.split('|')]
        return f'({" or ".join(parts)})'
        
    # Handle hero_tree and talent conditions
    if condition.startswith('hero_tree.'):
        tree_name = condition[len('hero_tree.'):]
        return f'Player.HasHeroTreeNode("{tree_name}")'
    if condition.startswith('talent.'):
        talent_name = condition[len('talent.'):]
        return f'Player.HasTalent("{talent_name}")'
        
    # Handle other conditions
    if condition.startswith((
        'Variables.', 'Mechanics.', 'Position.', 'Player.',
        'buff.', 'debuff.', 'cooldown.', 'spell.', 'resource.'
    )):
        return condition
        
    # Handle special conditions
    if condition == 'not.in.position':
        return 'not Player.InPosition'
    if condition in ('true', 'false'):
        return condition.lower()
        
    # Handle numeric comparisons
    if any(op in condition for op in ('>', '<', '>=', '<=', '==', '!=')):
        return condition
        
    return condition

def convert_resource(resource: str) -> Optional[str]:
    """Convert SimC resource name to PS resource getter"""
    mapping = RESOURCE_MAPPINGS.get(resource.lower())
    return mapping.ps_getter if mapping else None

def convert_buff(buff: str) -> str:
    """Convert SimC buff name to PS buff check"""
    return f"Player.Buff({buff})"

def convert_target(target_expr: str) -> str:
    """Convert SimC target expression to PS target check"""
    if target_expr == 'target.health.pct':
        return 'Target.HealthPercent'
    if target_expr.startswith('spell_targets.'):
        return 'Enemies.Count'
    return f"-- TODO: Convert target expression: {target_expr}"

# Add validation and error handling
class MappingError(Exception):
    """Custom exception for mapping errors"""
    pass

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

# Add version info
API_VERSION = {
    'major': 1,
    'minor': 0,
    'patch': 0,
    'compatible_with': ['1.0.x'],
}

# Add validation rules
VALIDATION_RULES = {
    'spell': {
        'required_fields': ['id', 'name', 'type'],
        'optional_fields': ['range', 'gcd', 'cooldown', 'charges'],
        'field_types': {
            'id': int,
            'name': str,
            'type': str,
            'range': (int, float),
            'gcd': bool,
            'cooldown': (int, float),
        },
    },
    'resource': {
        'required_fields': ['max', 'initial'],
        'optional_fields': ['generates', 'spenders', 'modifiers'],
        'field_types': {
            'max': (int, float),
            'initial': (int, float),
        },
    },
}

# Add caching
class MappingCache:
    """Cache for frequently used mappings"""
    def __init__(self):
        self._spell_cache = {}
        self._resource_cache = {}
        self._expression_cache = {}
        
    def get_spell(self, name: str) -> Optional[Dict]:
        return self._spell_cache.get(name)
        
    def set_spell(self, name: str, data: Dict):
        self._spell_cache[name] = data

# Add performance hints
PERFORMANCE_HINTS = {
    'cache_spell_lookups': True,
    'cache_resource_checks': True,
    'batch_condition_checks': True,
    'optimize_expressions': True,
}

# Add migration helpers
def validate_api_compatibility(required_version: str) -> bool:
    """Check if current API version is compatible"""
    pass

def migrate_mapping(old_version: str, new_version: str, mapping_data: Dict) -> Dict:
    """Migrate mapping data between API versions"""
    pass

def validate_mapping_data(mapping_type: str, data: Dict) -> bool:
    """Validate mapping data against rules"""
    pass

@dataclass
class OperationMetric:
    """Metric for a single operation"""
    start_time: float
    end_time: float = 0.0
    success: bool = True
    error: Optional[str] = None

class APILogger:
    """Logger for API operations"""
    def __init__(self, level=logging.INFO):
        self.level = level
        self.logger = logging.getLogger('ps_simc_parser')
        self.setup_logger()
        
    def setup_logger(self):
        """Setup logging configuration"""
        self.logger.setLevel(self.level)
        
        # File handler
        fh = logging.FileHandler('ps_simc_parser.log')
        fh.setLevel(self.level)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    
    def log(self, level: int, message: str, context: Dict = None):
        """Log a message with optional context"""
        if level <= self.level:
            log_msg = message
            if context:
                log_msg += f" Context: {context}"
            
            if level == logging.ERROR:
                self.logger.error(log_msg)
            elif level == logging.WARNING:
                self.logger.warning(log_msg)
            elif level == logging.INFO:
                self.logger.info(log_msg)
            elif level == logging.DEBUG:
                self.logger.debug(log_msg)
            elif level == logging.TRACE:
                self.logger.debug(f"TRACE: {log_msg}")
                
    def debug(self, message: str, context: Dict = None):
        self.log(logging.DEBUG, message, context)
        
    def info(self, message: str, context: Dict = None):
        self.log(logging.INFO, message, context)
        
    def warn(self, message: str, context: Dict = None):
        self.log(logging.WARNING, message, context)
        
    def error(self, message: str, context: Dict = None):
        self.log(logging.ERROR, message, context)
        
    def trace(self, message: str, context: Dict = None):
        self.log(logging.TRACE, message, context)

class PerformanceMonitor:
    """Monitor performance metrics"""
    def __init__(self):
        self.metrics: Dict[str, List[OperationMetric]] = {
            'spell_lookups': [],
            'cache_operations': [],
            'parse_operations': [],
            'conversion_operations': [],
            'validation_operations': [],
            'lua_generation': []  # Add lua_generation metric
        }
        self.current_operations: Dict[str, OperationMetric] = {}
        
    def start_operation(self, operation: str, context: Dict = None):
        """Start timing an operation"""
        self.current_operations[operation] = OperationMetric(
            start_time=time.time()
        )
        
    def end_operation(self, operation: str, success: bool = True, error: str = None):
        """End timing and record metrics"""
        if operation in self.current_operations:
            metric = self.current_operations[operation]
            metric.end_time = time.time()
            metric.success = success
            metric.error = error
            
            if operation not in self.metrics:
                self.metrics[operation] = []
                
            self.metrics[operation].append(metric)
            del self.current_operations[operation]
            
    def get_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get performance metrics summary"""
        summary = {}
        for op, metrics in self.metrics.items():
            if not metrics:
                continue
                
            total_time = sum(m.end_time - m.start_time for m in metrics)
            avg_time = total_time / len(metrics)
            success_rate = sum(1 for m in metrics if m.success) / len(metrics)
            
            summary[op] = {
                'count': len(metrics),
                'total_time': total_time,
                'avg_time': avg_time,
                'success_rate': success_rate,
                'errors': [m.error for m in metrics if m.error]
            }
            
        return summary
        
    def reset_metrics(self):
        """Reset all metrics"""
        for op in self.metrics:
            self.metrics[op] = []
        self.current_operations = {}

class DataValidator:
    """Validates SimC data against PS API"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def is_valid_spell(self, spell_name: str) -> bool:
        """Check if spell exists in mappings"""
        return spell_name.lower() in SPELL_MAPPINGS
        
    def is_valid_resource(self, resource: str) -> bool:
        """Check if resource exists in mappings"""
        # Handle resource.attribute format
        if '.' in resource:
            resource = resource.split('.')[0]
        return resource.lower() in RESOURCE_MAPPINGS
        
    def is_valid_condition(self, condition: str) -> bool:
        """Check if condition is valid"""
        # Empty conditions are not valid
        if not condition:
            return False
            
        # Variable references are always valid
        if condition.startswith('variable.'):
            return True
            
        # Resource checks
        if '>' in condition or '<' in condition:
            resource = condition.split('>')[0].split('<')[0].strip()
            return self.is_valid_resource(resource)
            
        # Buff checks
        if condition.endswith('.up'):
            return True
            
        # Cooldown checks
        if condition.startswith('cooldown.') and condition.endswith('.ready'):
            spell_name = condition[9:-6]
            return self.is_valid_spell(spell_name)
            
        # Target checks
        if condition.startswith('target.'):
            return True
            
        # Position checks
        if condition.startswith('position.'):
            return True
            
        # Mechanic checks
        if condition.startswith('mechanic.'):
            return True
            
        # Default to invalid
        return False

class ErrorRecovery:
    """Handle and recover from errors"""
    def __init__(self, logger: APILogger):
        self.logger = logger
        self.error_count = 0
        self.recovery_attempts = {}
        
    def handle_error(self, error: Exception, context: Dict = None) -> None:
        """Handle a generic error"""
        self.error_count += 1
        self.logger.error(str(error), context or {})
        
    def handle_missing_spell(self, spell_name: str) -> Dict:
        """Handle missing spell mapping"""
        self.error_count += 1
        self.logger.warn(f"Missing spell: {spell_name}", {'recovery': 'using default template'})
        
        # Return a safe default template
        return {
            'id': 0,
            'name': spell_name,
            'type': 'spell',
            'gcd': True,
        }
        
    def handle_invalid_mapping(self, mapping_data: Dict) -> Dict:
        """Handle invalid mapping data"""
        self.error_count += 1
        self.logger.warn("Invalid mapping", {'data': mapping_data})
        
        # Try to salvage what we can
        cleaned_data = {
            k: v for k, v in mapping_data.items()
            if k in VALIDATION_RULES['spell']['required_fields']
        }
        
        return cleaned_data

class APICompatibilityChecker:
    """Check API compatibility"""
    def __init__(self, logger: APILogger):
        self.logger = logger
        
    def check_version(self, required: str) -> bool:
        """Check if current API version is compatible with required version"""
        try:
            major, minor, patch = map(int, required.split('.'))
            current = f"{API_VERSION['major']}.{API_VERSION['minor']}.{API_VERSION['patch']}"
            
            # Major version must match
            if major != API_VERSION['major']:
                self.logger.error(f"Incompatible major version: required {major}, current {API_VERSION['major']}")
                return False
                
            # Minor version must be less than or equal
            if minor > API_VERSION['minor']:
                self.logger.error(f"Incompatible minor version: required {minor}, current {API_VERSION['minor']}")
                return False
                
            self.logger.info(f"API version check passed: required {required}, current {current}")
            return True
            
        except ValueError:
            self.logger.error(f"Invalid version format: {required}")
            return False
            
    def _is_compatible(self, current: str, required: str) -> bool:
        """Check if versions are compatible"""
        current_parts = list(map(int, current.split('.')))
        required_parts = list(map(int, required.split('.')))
        
        # Compare versions
        for i in range(min(len(current_parts), len(required_parts))):
            if current_parts[i] < required_parts[i]:
                return False
            elif current_parts[i] > required_parts[i]:
                return True
        return True

# Initialize global instances
logger = APILogger()
monitor = PerformanceMonitor()
validator = DataValidator()
recovery = ErrorRecovery(logger)
compatibility = APICompatibilityChecker(logger)
