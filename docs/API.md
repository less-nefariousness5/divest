# PS SimC Parser API Documentation

## Overview

The PS SimC Parser is a tool for converting SimulationCraft (SimC) Action Priority Lists (APLs) into Priority Scripting (PS) Lua code. This document describes the API and features of the parser.

## Core Components

### Parser

The main parser class that orchestrates the conversion of SimC APLs to PS Lua code.

```python
from ps_simc_parser.parser import Parser

# Create parser for a specific specialization
parser = Parser('vengeance')

# Parse SimC content and generate Lua code
lua_code = parser.parse_file(simc_content)
```

### APLParser

Handles the parsing of SimC APL syntax into intermediate representations.

```python
from ps_simc_parser.parser.apl import APLParser

# Create APL parser
apl_parser = APLParser()

# Parse APL content with context
actions = apl_parser.parse(content, context)
```

### ActionParser

Converts APL actions into PS actions and generates Lua code.

```python
from ps_simc_parser.parser.actions import ActionParser

# Create action parser
action_parser = ActionParser()

# Parse APL action into PS action
ps_action = action_parser.parse(apl_action, context)

# Generate Lua code from PS actions
lua_code = action_parser.generate_lua(ps_actions)
```

## Supported Features

### Actions

The parser supports the following action types:

- Spell casts (e.g., `spell_name`)
- Variable operations (e.g., `variable,name=x,value=1`)
- Special actions:
  - `snapshot_stats`
  - `potion`
  - `flask`
  - `food`
  - `augmentation`
  - `use_item`
  - `pool_resource`
  - `call_action_list`
  - `run_action_list`
  - `wait`
  - `invoke_external_buff`

### Conditions

The parser supports various condition types:

- Buff/debuff conditions (e.g., `buff.x.up`, `debuff.x.remains`)
- Talent conditions (e.g., `talent.x`)
- Spell conditions (e.g., `spell.x.ready`)
- Cooldown conditions (e.g., `cooldown.x.remains`)
- Resource conditions (e.g., `fury>=40`)
- Target conditions (e.g., `target.time_to_die`)
- Special variables (e.g., `fight_remains`, `execute_time`)

### Variables

Variables can be:

- Set: `variable,name=x,value=1`
- Added: `variable,name=x,op=add,value=1`
- Subtracted: `variable,name=x,op=sub,value=1`
- Multiplied: `variable,name=x,op=mul,value=1`
- Divided: `variable,name=x,op=div,value=1`
- Minimized: `variable,name=x,op=min,value=1`
- Maximized: `variable,name=x,op=max,value=1`

### Operators

The parser supports standard SimC operators:

- Logical: `&&` (and), `||` (or), `!` (not)
- Comparison: `==`, `!=`, `>=`, `<=`, `>`, `<`
- Arithmetic: `+`, `-`, `*`, `/`

## Error Handling

The parser provides detailed error information:

- Line numbers for syntax errors
- Unknown spell warnings
- Unsatisfied dependency warnings
- Invalid operator warnings
- Circular reference detection

## Command Line Interface

The parser can be run from the command line:

```bash
ps-simc-parser parse --spec SPEC --input INPUT_FILE --output OUTPUT_FILE
```

Options:
- `--spec`: Specialization to parse for (required)
- `--input`: Input SimC APL file (required)
- `--output`: Output Lua file (required)

## Best Practices

1. Always specify the correct specialization when creating a parser
2. Handle unknown spells and unsatisfied dependencies appropriately
3. Use meaningful variable names
4. Keep conditions simple and readable
5. Use action lists to organize complex rotations

## Known Limitations

1. Some complex expressions may not be parsed correctly
2. Some advanced spell and buff references are not fully supported
3. Some advanced variable operations are not fully supported
4. Some advanced target references are not fully supported

## Future Enhancements

1. Support for more complex expressions
2. Support for more spell and buff references
3. Support for more variable operations
4. Support for more target references
5. Improved error handling and reporting
6. Performance optimizations for large APL files
