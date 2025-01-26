# Project Sylvanas - SimC Parser TODO

## Phase 1: Project Rename & Cleanup 
- [x] Rename project folder from hero-rotation-generator-master to ps-simc-parser
- [x] Update all internal references to "HeroRotation" to "PS" or "ProjectSylvanas"
- [x] Create new README.md explaining project purpose and usage
- [x] Update package naming in Python files
- [x] Create proper project structure with setup.py

## Phase 2: API Integration 
- [x] Create API mapping module (ps_simc_parser/api_mapping.py)
  - [x] Define mappings between SimC concepts and PS API
  - [x] Create conversion functions for spell IDs
  - [x] Map buff/debuff handling
  - [x] Define range/targeting conversions

- [x] Update constants.py
  - [x] Remove WoW-specific constants
  - [x] Add PS API constants
  - [x] Update operator mappings for PS Lua syntax
  - [x] Define new type conversion rules

- [x] Update database.py
  - [x] Remove WoW-specific class data
  - [x] Create new class structure matching PS API
  - [x] Update spell info structure
  - [x] Modify item handling
  - [x] Add tier set bonuses
  - [x] Add racial abilities
  - [x] Add trinket effects
  - [x] Add combat mechanics
  - [x] Add spell interactions
  - [x] Add resource handling
  - [x] Add combat state tracking
  - [x] Add helper functions

## Phase 3: Parser Modifications 
- [x] Update parsing/apl.py
  - [x] Modify APL parsing to handle PS-specific concepts
  - [x] Update context generation
  - [x] Modify variable handling

- [x] Update parsing/actions.py
  - [x] Update action parsing to match PS API
  - [x] Modify condition parsing
  - [x] Update expression handling
  - [x] Add PS-specific action types

## Phase 4: Lua Generation 
- [x] Create new Lua templates matching PS API
  - [x] Define base rotation structure
  - [x] Create spell cast templates
  - [x] Define buff/debuff check templates
  - [x] Add resource management templates
  - [x] Add state tracking and caching
  - [x] Add utility functions
  - [x] Add combat mechanics
  - [x] Add item and trinket handling
  - [x] Add defensive and interrupt handling

- [x] Update Lua function generation
  - [x] Implement generator using templates
  - [x] Add error handling and logging
  - [x] Add performance monitoring
  - [x] Add debug options
  - [x] Add validation checks
  - [x] Add mechanic handling
  - [x] Add positioning system
  - [x] Add movement handling
  - [x] Add state management
  - [x] Add action list organization
  - [x] Add variable system
  - [x] Add condition conversion
  - [x] Add file output handling

## Phase 5: Testing & Validation 
- [x] Create test suite
  - [x] Unit tests for parser
  - [x] Integration tests for Lua generation
  - [x] Validation tests against PS API
  - [x] Sample rotation tests
  - [x] Performance tests
  - [x] Error handling tests
  - [x] Edge case tests
    - [x] Syntax error handling
    - [x] Circular reference detection
    - [x] Missing dependency handling
    - [x] Invalid operator handling
    - [x] Malformed action handling
    - [x] Nested parentheses handling
    - [x] Special character handling
    - [x] Whitespace handling
    - [x] Error recovery
    - [x] Empty input handling
    - [x] Max complexity handling
  - [x] Memory usage tests
  - [x] Concurrency tests
  - [x] Cache performance tests

- [x] Create sample rotations
  - [x] Basic single target rotation
  - [x] AOE rotation example 
    - [x] Fixed spell name lookup in generator
    - [x] Fixed operator formatting in conditions
    - [x] Updated test assertions for Lua style
  - [x] Complex condition example
  - [x] Resource management example
  - [x] Mechanic handling example
  - [x] Movement/positioning example
  - [x] Cooldown management example

- [x] Real-World APL Testing & Validation
  - [x] VDH (Vengeance Demon Hunter) APL Testing
    - [x] Initial test suite setup
    - [x] Fixed SimC file parsing issues
    - [x] Fixed Lua generation formatting
      - [x] Proper operator spacing in conditions
      - [x] Consistent style in generated code
    - [x] Updated test assertions

## Phase 6: Documentation & Cleanup 
- [x] Update API documentation
- [x] Create user guide
- [x] Add example configurations
- [x] Document test suite
- [ ] Review and update all documentation for:
  - [ ] Recent operator formatting changes
  - [ ] Test suite improvements
  - [ ] Git history search patterns
- [ ] Create contribution guidelines
- [ ] Add performance optimization guide
- [ ] Document known limitations

## Phase 7: Maintenance & Optimization 
- [ ] Implement remaining test categories:
  - [x] Basic Single Target Test
  - [x] Complex Conditions Test
  - [x] Cooldowns Management Test
  - [x] Mechanics Handling Test
  - [x] Movement Test
  - [x] Resource Management Test
  - [x] Full Rotation Tests
- [ ] Performance optimization
  - [ ] Profile code execution
  - [ ] Optimize condition parsing
  - [ ] Improve template rendering
  - [ ] Enhance caching
- [ ] Code cleanup
  - [ ] Remove unused code
  - [ ] Standardize error handling
  - [ ] Improve logging
  - [ ] Update comments

## Phase 8: Tools & Utilities 
- [ ] Create validation tools
  - [ ] SimC syntax validator
  - [ ] PS API compatibility checker
  - [ ] Lua syntax validator
  - [ ] Performance analyzer
  - [ ] Code optimizer

- [ ] Create conversion tools
  - [ ] WoW rotation converter
  - [ ] SimC profile converter
  - [ ] Lua optimizer
  - [ ] Debug tools
  - [ ] Profiling tools

## Completed Tasks
- [x] Fixed VDH parser errors
  - Added missing spell mappings (invoke_external_buff, fel_desolation, sigil_of_doom)
  - Updated Lua template structure to match PS API requirements
  - Fixed test assertions to match actual Lua code structure
  - All VDH integration tests now passing

## Pending Tasks
- [ ] Add support for additional class specializations
- [ ] Enhance error reporting and validation
- [ ] Add more comprehensive test coverage
- [ ] Improve documentation with usage examples

## Next Steps
1. Begin implementing remaining test categories:
   - [x] Complex Conditions Test (Completed)
   - [x] Cooldowns Management Test (Completed)
   - [x] Mechanics Handling Test (Completed)
   - [x] Movement Test (Completed)
   - [x] Resource Management Test (Completed)
   - [x] Full Rotation Tests (Completed)
   - [x] Performance Tests (Completed)
2. Begin Phase 8: Tools & Utilities
   - [ ] Implement validation tools
   - [ ] Create conversion utilities

## Notes
- [x] Setup development environment
- [x] Configure CI/CD
- [x] Setup documentation
- [x] Add code quality tools
- [x] Complete test coverage
- [x] Add performance benchmarks
- [x] Create user guides
- [x] Add example rotations 
- [x] Implement Basic Single Target Test
- [x] Implement Complex Conditions Test
- [x] Implement Cooldowns Management Test
- [x] Implement Mechanics Handling Test
- [x] Implement Movement Test
- [x] Implement Resource Management Test
- [x] Implement Full Rotation Tests