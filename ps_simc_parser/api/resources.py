"""Resource mappings for PS SimC Parser"""

RESOURCE_MAPPINGS = {
    'fury': {
        'getter': 'Player.Fury',
        'max': 120,
        'min': 0,
        'type': 'primary'
    },
    'soul_fragments': {
        'getter': 'Player.SoulFragments',
        'max': 5,
        'min': 0,
        'type': 'secondary'
    },
    'health': {
        'getter': 'Player.Health',
        'max': 100,
        'min': 0,
        'type': 'vital'
    }
} 