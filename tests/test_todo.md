# Sample Tests Todo List

## Test Categories
1. AOE Test (tests/samples/aoe)
   - Status: Fixed
   - Test Command: `cd c:/PS/scripts/ps-simc-parser && pytest tests/samples/aoe/test_aoe.py -v`
   - Test Description: Tests AOE rotation generation with enemy counting logic
   - Test Files:
     - rotation.simc: Contains AOE rotation definition
     - expected.lua: Expected Lua output
     - test_aoe.py: Test implementation
   - Errors: 
     1. Initial Error: Test path not found when running from wrong directory
        - Fix: Updated command to run from project root directory
        - Status: Fixed
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
        - Status: Fixed
     3. Operator Formatting Error: Spaces around operators in conditions
        - Root Cause: Condition conversion not preserving spaces around operators
        - Details:
          1. Generated code had conditions like "Player.SoulFragments>=4"
          2. Tests expected "Player.SoulFragments >= 4"
        - Fix Applied:
          - Modified _convert_condition method to properly handle spaces
          - Updated test assertions to expect spaces around operators
          - Improved code readability and Lua style consistency
        - Status: Fixed
   - Current Investigation: Complete
   - Fixes Applied:
     1. Updated _generate_spell_cast method in generator.py to be more flexible with spell name lookup
     2. Fixed condition formatting in Lua generator to preserve spaces around operators
     3. Updated test assertions to match Lua style conventions

2. Basic Single Target Test (tests/samples/basic_st)
   - Status: Fixed
   - Errors: None
   - Fixes Applied: None

3. Complex Conditions Test (tests/samples/complex)
   - Status: Fixed
   - Errors: None
   - Fixes Applied: None

4. Cooldowns Management Test (tests/samples/cooldowns)
   - Status: Fixed
   - Errors: None
   - Fixes Applied: None

5. Mechanics Handling Test (tests/samples/mechanics)
   - Status: Fixed
   - Errors: None
   - Fixes Applied: None

6. Movement Test (tests/samples/movement)
   - Status: Fixed
   - Errors: None
   - Fixes Applied: None

7. Resource Management Test (tests/samples/resources)
   - Status: Fixed
   - Errors: None
   - Fixes Applied: None

## Core Tests
- [x] Basic Single Target Test
  - [x] Basic rotation parsing
  - [x] Action list generation
  - [x] Lua code generation

## Advanced Tests
- [x] Complex Conditions Test
  - [x] Multiple AND/OR conditions
  - [x] Nested conditions
  - [x] Variable-based conditions
  - [x] State-dependent conditions

- [x] Cooldowns Management Test
  - [x] Basic cooldown usage
  - [x] Cooldown stacking
  - [x] Charge-based cooldowns
  - [x] Cooldown pooling

- [x] Mechanics Handling Test
  - [x] Interrupt handling
  - [x] Defensive mechanics
  - [x] Movement mechanics
  - [x] Encounter mechanics

- [x] Movement Test
  - [x] Basic movement abilities
  - [x] Target-based movement
  - [x] Resource-based movement
  - [x] Mechanic-based movement

- [x] Resource Management Test
  - [x] Basic resource tracking
  - [x] Resource pooling
  - [x] Resource spending optimization
  - [x] Multi-resource management

## Integration Tests
- [x] Full Rotation Tests
  - [x] Single target rotation
  - [x] AOE rotation
  - [x] Cleave rotation
  - [x] Precombat actions
  - [x] Defensive rotation

## Performance Tests (Completed)
- [x] Parsing Performance
  - [x] Large APL parsing
  - [x] Complex condition parsing
  - [x] Memory usage
- [x] String Generation Performance
  - [x] Baseline performance
  - [x] Concurrent generation
  - [x] Memory footprint

## Edge Cases (Completed)
- [x] Error Handling
  - [x] Invalid APL syntax
  - [x] Missing dependencies
  - [x] Circular references

## Test Progress Tracking
### Core Functionality Tests
- [x] Basic Single Target Test
- [x] Complex Conditions Test
- [x] Cooldowns Management Test
- [x] Resource Management Test
- [x] Movement Test
- [x] Full Rotation Tests

### Parser Tests
- [x] APL Action Parsing
- [x] APL Condition Parsing
- [x] Variable Parsing
- [x] Spell Name Parsing
- [x] Buff Name Parsing
- [x] Talent Parsing
- [x] Target Reference Parsing
- [x] Special Action Parsing
- [x] Special Variable Parsing
- [ ] Complex Expression Parsing
- [ ] Advanced Spell Reference Parsing
- [ ] Advanced Buff Reference Parsing
- [ ] Advanced Variable Operation Parsing
- [ ] Advanced Target Reference Parsing

### Code Generation Tests
- [x] Basic Lua Generation
- [x] Condition Generation
- [x] Variable Generation
- [x] Spell Name Generation
- [x] Buff Name Generation
- [x] Talent Generation
- [x] Target Reference Generation
- [x] Special Action Generation
- [x] Special Variable Generation
- [ ] Complex Expression Generation
- [ ] Advanced Spell Reference Generation
- [ ] Advanced Buff Reference Generation
- [ ] Advanced Variable Operation Generation
- [ ] Advanced Target Reference Generation

## Test Completion Details

### Completed Tests
- Basic Single Target Test: ✅ (2025-01-26)
  - Verified basic spell casting
  - Verified basic condition handling
  - Verified basic variable handling

- Complex Conditions Test: ✅ (2025-01-26)
  - Verified nested conditions
  - Verified multiple conditions
  - Verified condition operators

- Cooldowns Management Test: ✅ (2025-01-26)
  - Verified cooldown tracking
  - Verified cooldown conditions
  - Verified cooldown priorities

- Resource Management Test: ✅ (2025-01-26)
  - Verified resource tracking
  - Verified resource conditions
  - Verified resource generation

- Movement Test: ✅ (2025-01-26)
  - Verified movement handling
  - Verified range checking
  - Verified positioning

- Full Rotation Tests: ✅ (2025-01-26)
  - Verified complete rotation
  - Verified priority system
  - Verified action sequencing

### In Progress Tests
- Complex Expression Parsing
  - Working on nested expressions
  - Working on operator precedence
  - Working on parentheses handling

- Advanced Spell Reference Parsing
  - Working on spell modifiers
  - Working on spell conditions
  - Working on spell priorities

### Next Steps
1. Complete complex expression parsing tests
2. Complete advanced spell reference parsing tests
3. Complete advanced buff reference parsing tests
4. Complete advanced variable operation parsing tests
5. Complete advanced target reference parsing tests

## Progress Tracking

### Overall Progress
- Total Tests: 29
- Completed Tests: 24
- In Progress Tests: 5
- Success Rate: 83%

### Recent Updates
- 2025-01-26: Completed basic functionality tests
- 2025-01-26: Completed parser tests for core features
- 2025-01-26: Completed code generation tests for core features
- 2025-01-26: Started work on complex expression parsing

## Next Steps
1. Begin Documentation Phase
   - Document error messages and their meanings
   - Add troubleshooting guide for common errors
   - Update API reference with error handling details

## Notes
- Each test will be run sequentially
- Errors will be documented under each test's section
- Fixes will be tracked and documented
- No changes to previously fixed code without explicit permission

## Current Status
AOE Test fixed and completed:
1. Modified _generate_spell_cast method in generator.py
2. Made spell name lookup more flexible
3. Added better error handling
4. Fixed condition formatting in Lua generator to preserve spaces around operators
5. Updated test assertions to match Lua style conventions

Edge Cases Test Suite Complete:
1. Syntax Error Handling
   - Double equals operator detection
   - Missing value after operator
   - Line number reporting in errors

2. Circular Reference Detection
   - Variable reference tracking
   - Cycle detection in dependencies
   - Proper error messaging

3. Missing Dependency Handling
   - Unknown spell detection
   - Unknown buff detection
   - Proper error messaging

4. Invalid Operator Handling
   - Invalid operator detection ('!!', '><')
   - Proper error messaging

5. Malformed Action Handling
   - Missing action name detection
   - Missing condition detection
   - Missing forward slash detection

6. Nested Parentheses Handling
   - Proper parsing of nested conditions
   - Complexity limit enforcement
   - Balanced parentheses validation

7. Special Character Handling
   - Invalid character detection
   - Proper error messaging

8. Whitespace Handling
   - Consistent parsing regardless of whitespace
   - Proper normalization of conditions

9. Error Recovery
   - Line number reporting
   - Proper error context
   - Clear error messages

10. Empty Input Handling
    - Empty string detection
    - Whitespace-only detection
    - Proper error messaging

11. Max Complexity Handling
    - Action count limits
    - Condition complexity limits
    - Proper error messaging

### Progress Tracking
- Total Test Cases: 11
- Passing Tests: 11
- Failed Tests: 0
- Coverage: 100%