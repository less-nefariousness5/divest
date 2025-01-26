## Lua Syntax Error - Variable Assignment
**Issue**: LuaSyntaxError: ')' expected near '=' in generated Lua code
**Location**: Variable assignments in generated code
**Current Status**: In Progress

### Root Cause:
The variable assignment code was generating invalid Lua syntax due to:
1. Incorrect handling of conditions
2. Missing proper if-statement wrapping
3. Improper value conversion handling
4. Incorrect spell mapping integration

### Attempted Fixes:

1. **Direct Value Assignment** [Failed]
```python
# In _generate_variable_action:
return f"Variables._values['{name}'] = {value}"
```
Result: Caused Lua syntax error - direct table access not working

2. **Using Variables:Set Method** [Failed]
```python
# In _generate_variable_action:
return f"Variables:Set('{name}', {value})"
```
Result: Still getting syntax error - possibly due to value conversion

3. **Parentheses Around Value** [Failed]
```python
# In _generate_variable_action:
return f"Variables._values['{name}'] = ({value})"
```
Result: Syntax error persists - parentheses didn't help

4. **Converting Value to Lua Condition** [Failed]
```python
# In _generate_variable_action:
value = convert_condition(action['value'])
return f"Variables:Set('{name}', {value})"
```
Result: Still getting syntax error - conversion might be incorrect

5. **Converting value to Lua condition with parentheses** [Failed]
```python
value = convert_condition(action['value'])
Variables:Set('{name}', ({value}))
```
Result: Syntax errors persist - parentheses and conversion combination didn't resolve the issue

6. **Fixed Variables table definition** [Failed]
```lua
local Variables = {
    _values = {},
}

function Variables:Set(name, value)
    self._values[name] = value
end

function Variables:Get(name, default)
    return self._values[name] or default
end
```
Result: Table definition correct but value conversion still causing issues

7. **SpellMapping Integration** [Fixed]
```python
# Fixed SpellMapping object handling in _generate_spell_cast
ps_spell = convert_spell(spell_name)
if not ps_spell:
    raise GeneratorError(f"Could not convert spell: {spell_name}")

# Extract spell info from SpellMapping object
simc_name = ps_spell.simc_name
ps_name = ps_spell.ps_name
spell_id = ps_spell.spell_id
```
Result: Fixed the AttributeError by properly accessing SpellMapping object attributes

8. **Proper Variable Assignment Structure** [In Progress]
```python
def _generate_variable_action(self, action: Dict[str, Any]) -> str:
    name = action['name']
    value = self._convert_value(action['value'])
    
    # Format the variable assignment with Cache:Set
    assignment = f"Cache:Set('{name}', {value})"
    
    # If there are conditions, wrap in if statement
    if conditions:
        condition_str = ' and '.join(self._convert_conditions(conditions))
        return f"if {condition_str} then\n    {assignment}\nend"
    
    return assignment

def _convert_value(self, value: str) -> str:
    if 'health.pct' in value:
        op = re.search(r'[<>=]+', value).group()
        threshold = re.search(r'\d+', value).group()
        return f"Player:HealthPercent() {op} {threshold}"
    elif 'buff.' in value:
        buff_name = value.split('.')[1].split('.')[0]
        if value.startswith('!'):
            return f"not Player:Buff('{buff_name}')"
        return f"Player:Buff('{buff_name}')"
    # ... handle other value types
```
Result: Improved value conversion but still encountering syntax errors

### Current Status:
- Fixed SpellMapping integration
- Improved condition handling
- Added proper if-statement wrapping for conditional assignments
- Still working on resolving Lua syntax errors in variable assignments

### Verification:
The following test cases are failing:
1. Basic variable assignments - Syntax error near '='
2. Conditional variable assignments - Missing operator
3. Complex condition expressions - Invalid syntax
4. Resource-based conditions - Incorrect method calls
5. Buff/debuff conditions - Invalid syntax for negation

### Next Steps:
1. Fix variable assignment syntax by ensuring proper operator usage
2. Update condition conversion to use correct Lua syntax for comparisons
3. Implement proper resource method calls
4. Add comprehensive test cases for each condition type
5. Consider adding validation for generated Lua code before execution
6. Add error recovery mechanisms for syntax errors
7. Improve error messages to better identify syntax issues
8. Consider adding a Lua syntax validator 