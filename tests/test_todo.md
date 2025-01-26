# Sample Tests Todo List

## Test Categories
1. AOE Test (tests/samples/aoe)
   - Status: Fix In Progress
   - Test Command: `cd c:/PS/scripts/ps-simc-parser && pytest tests/samples/aoe/test_aoe.py -v`
   - Test Description: Tests AOE rotation generation with enemy counting logic
   - Test Files:
     - rotation.simc: Contains AOE rotation definition
     - expected.lua: Expected Lua output
     - test_aoe.py: Test implementation
   - Errors: 
     1. Initial Error: Test path not found when running from wrong directory
        - Fix: Updated command to run from project root directory
        - Status: 
     2. Current Error: GeneratorError: Failed to generate action lists: 'spell'
        - Root Cause: Mismatch between parser output and generator expectations
        - Details:
          1. In generator.py, _generate_spell_cast expects action['spell']
          2. Parser is providing the spell name directly in action['name']
          3. This causes KeyError when trying to access action['spell']
        - Fix Being Applied:
          - Modified _generate_spell_cast to check both 'spell' and 'name' keys
          - Added error handling for missing spell names
          - Made spell name lookup more robust
        - Status: 
   - Current Investigation: Complete
   - Fixes Applied:
     1. Updated _generate_spell_cast method in generator.py to be more flexible with spell name lookup

2. Basic Single Target Test (tests/samples/basic_st)
   - Status: Not Run
   - Errors: None yet
   - Fixes Applied: None yet

3. Complex Conditions Test (tests/samples/complex)
   - Status: Not Run
   - Errors: None yet
   - Fixes Applied: None yet

4. Cooldowns Management Test (tests/samples/cooldowns)
   - Status: Not Run
   - Errors: None yet
   - Fixes Applied: None yet

5. Mechanics Handling Test (tests/samples/mechanics)
   - Status: Not Run
   - Errors: None yet
   - Fixes Applied: None yet

6. Movement Test (tests/samples/movement)
   - Status: Not Run
   - Errors: None yet
   - Fixes Applied: None yet

7. Resource Management Test (tests/samples/resources)
   - Status: Not Run
   - Errors: None yet
   - Fixes Applied: None yet

## Test Progress Tracking
- [ ] AOE Test Complete
- [ ] Basic Single Target Test Complete
- [ ] Complex Conditions Test Complete
- [ ] Cooldowns Management Test Complete
- [ ] Mechanics Handling Test Complete
- [ ] Movement Test Complete
- [ ] Resource Management Test Complete

## Notes
- Each test will be run sequentially
- Errors will be documented under each test's section
- Fixes will be tracked and documented
- No changes to previously fixed code without explicit permission

## Current Status
Applying fix to AOE Test:
1. Modified _generate_spell_cast method in generator.py
2. Made spell name lookup more flexible
3. Added better error handling
4. Waiting to run tests again after fix is applied

## Environment Setup Required
1. Must run tests from project root directory (c:/PS/scripts/ps-simc-parser)
2. Python environment must have pytest and other dev requirements installed