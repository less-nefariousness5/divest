# Project Sylvanas SimC Parser API Documentation

## Overview

This document describes the API for converting SimulationCraft (SimC) APL to Project Sylvanas Lua code.

## Core Components

### Parser

The main parser class that handles conversion of SimC files to PS Lua:

```python
from ps_simc_parser import Parser

parser = Parser()
parser.parse_file("input.simc", "output.lua")
```

### API Mapping

The API mapping module provides conversion between SimC concepts and PS API:

- Spell mappings
- Resource handling
- Buff/debuff tracking
- Targeting and range checks

```python
from ps_simc_parser.api.mapping import convert_spell, convert_condition

# Convert a SimC spell name to PS spell
spell = convert_spell("spirit_bomb")  # Returns SpellMapping object

# Convert a SimC condition to PS condition
condition = convert_condition("soul_fragments>=4")  # Returns "soul_fragments >= 4"
```

### Spells

The Spells class provides dynamic access to spell mappings:

```python
from ps_simc_parser.api.spells import Spells

# Access spells using attribute syntax
spells = Spells()
spell_name = spells.SpiritBomb  # Returns "SpiritBomb"
```

### Condition Conversion

The parser converts SimC conditions to PS Lua syntax:

- Logical operators: `&&` -> `and`, `||` -> `or`
- Comparison operators: `==`, `!=`, `>=`, `<=`, `>`, `<` (same as SimC)
- Negation: `!` is preserved for compatibility
- Resources: `soul_fragments`, `fury`, etc. are mapped to PS getters
- Buffs/Debuffs: `buff.X.up`, `debuff.Y.up` syntax is preserved

Example:
```python
# SimC condition:
"soul_fragments>=4&&!buff.metamorphosis.up"

# Converted to PS Lua:
"soul_fragments >= 4 and !buff.metamorphosis.up"
```

## SimC to PS Mappings

### Actions
- `cast` -> `Cast()`
- `use_item` -> `UseItem()`
- `variable` -> Local variables
- `run_action_list` -> Function calls

### Conditions
- `target.health.pct` -> `Target.HealthPercent`
- `spell_targets` -> `Enemies.Count`
- `buff.X.up` -> `Player.Buff(X).Exists`
- `cooldown.X.ready` -> `Spell(X).IsReady`

### Resources
- `fury` -> `Player.Fury`
- `energy` -> `Player.Energy`
- `mana` -> `Player.Mana`

## Usage Examples

### Basic Rotation
```lua
-- Generated from SimC:
-- actions=immolation_aura
-- actions+=/fel_devastation,if=fury>50

function Rotation()
    if Spell.ImmolationAura:IsReady() then
        return Cast(Spell.ImmolationAura)
    end
    
    if Spell.FelDevastation:IsReady() and Player.Fury > 50 then
        return Cast(Spell.FelDevastation)
    end
end
```

## Error Handling

The parser provides detailed error messages for:
- Invalid SimC syntax
- Unsupported actions
- Missing mappings
- API compatibility issues

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on:
- Adding new mappings
- Improving parser functionality
- Adding support for new SimC features
