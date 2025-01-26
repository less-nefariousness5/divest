# Parser Implementation Issues

## 1. Generator Action Lists Handling
- **Issue**: Generator expects dictionary for action lists but receives list
- **Location**: `lua_gen/generator.py` in `_generate_action_lists` method
- **Error**: `'list' object has no attribute 'items'`
- **Status**: Needs Fix
- **Test Cases**: Multiple test failures in `test_performance.py` and `test_validation.py`

## 2. Template Parameter Mismatch
- **Issue**: `format_rotation` method signature mismatch between different versions
- **Location**: `lua_gen/templates.py`
- **Error**: Missing/undefined `action_lists` parameter
- **Status**: Needs Fix
- **Test Cases**: Affects all test cases using template rendering

## 3. Parser Variable Handling
- **Issue**: Incorrect handling of variable definitions in parser
- **Location**: `parser/__init__.py` in `parse_line` method
- **Error**: Variables not properly parsed when defined in action lists
- **Status**: Needs Fix
- **Test Cases**: Variable-related test failures

## 4. Condition Format Mismatch
- **Issue**: Conditions not properly formatted between parser and generator
- **Location**: Multiple files (`parser/__init__.py`, `lua_gen/generator.py`)
- **Error**: Condition string format inconsistency
- **Status**: Needs Fix
- **Test Cases**: Condition parsing test failures

## 5. Template Rendering Context
- **Issue**: Template render method not properly handling context dictionary
- **Location**: `lua_gen/templates.py` in `render` method
- **Error**: Missing or incorrect context values
- **Status**: Needs Fix
- **Test Cases**: Template rendering test failures

## 6. Lua Variable Assignment Syntax
- **Issue**: Variable assignments in generated Lua code have incorrect syntax
- **Location**: `lua_gen/generator.py` in `_generate_variable_action` method
- **Error**: LuaSyntaxError: ')' expected near '='
- **Status**: In Progress
- **Test Cases**: `test_lua_syntax` failing
- **Root Cause**: Variable assignments are being generated with incorrect parentheses placement

## Action Plan
1. Fix Generator Action Lists Handling
   - Update `_generate_action_lists` to handle both list and dict inputs
   - Add proper type conversion
   - Add validation for input format

2. Standardize Template Parameters
   - Align `format_rotation` method signatures
   - Update all calls to use consistent parameter format
   - Add proper default values

3. Fix Variable Parsing
   - Update `parse_line` to properly handle variable definitions
   - Add validation for variable parameters
   - Update variable scope handling

4. Standardize Condition Format
   - Define clear format for conditions
   - Update parser and generator to use consistent format
   - Add validation for condition syntax

5. Fix Template Context Handling
   - Update render method to properly handle all context values
   - Add validation for required context fields
   - Add proper default values for optional fields

6. Fix Lua Variable Assignment Syntax
   - Review how variable values are being converted to Lua syntax
   - Ensure proper parentheses placement in assignments
   - Update variable action generation to use correct Lua syntax
   - Add test cases for variable assignments
