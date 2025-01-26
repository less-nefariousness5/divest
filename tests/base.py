"""
Base test class for PS SimC Parser tests
"""
import unittest
import json
from pathlib import Path
from ps_simc_parser.parser import Parser
from ps_simc_parser.utils.lua import LuaGenerator
import lupa
from ps_simc_parser.api.mapping import logger, monitor
from typing import Any, Dict
import os
from ps_simc_parser.parser.parser import ParserContext

class PSTestCase(unittest.TestCase):
    """Base test class with common test functionality"""
    
    def setUp(self):
        """Set up test case with parser, generator, and default context"""
        self.parser = Parser()
        self.generator = LuaGenerator()
        self.lua = lupa.LuaRuntime()
        self.test_dir = Path(__file__).parent
        self.fixtures_dir = self.test_dir / 'fixtures'
        self.output_dir = self.test_dir / 'output'
        self.output_dir.mkdir(exist_ok=True)
        
        # Reset performance monitor
        monitor.reset_metrics()
        
        self.default_context = {
            'name': 'Test Rotation',
            'class': 'demonhunter',
            'spec': 'vengeance',
            'role': 'tank',
            'level': 70
        }
        
    def tearDown(self):
        """Clean up after test"""
        # Clean output directory
        for file in self.output_dir.glob('*'):
            file.unlink()
            
    def load_fixture(self, name: str) -> Dict:
        """Load test fixture file"""
        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', f'{name}')
        with open(fixture_path, 'r') as f:
            content = f.read()
            
            # If it's a SimC file, parse it with the parser
            if name.endswith('.simc'):
                return self.parser.parse(content)
            
            # Try JSON parsing
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                # If not JSON, return raw content
                return content
                
    def save_output(self, name: str, content: str) -> Path:
        """Save test output to file"""
        path = self.output_dir / name
        path.write_text(content)
        return path
        
    def assertLuaValid(self, lua_code: str):
        """Assert that Lua code is syntactically valid"""
        try:
            # Create mock PS table with required functions
            mock_lua = """
                -- Create mock PS table
                PS = {
                    Spell = setmetatable({}, {
                        __index = function(t, k)
                            return {
                                IsReady = function() return true end
                            }
                        end
                    }),
                    Player = {
                        Target = {
                            Exists = function() return true end,
                            IsDead = function() return false end,
                            GUID = function() return "target-guid" end
                        },
                        Enemies = {
                            Count = function() return 3 end
                        },
                        SoulFragments = 4,
                        Fury = 80,
                        IncomingDamage = function(self, time) return 50000 end,
                        IsCasting = function() return false end,
                        IsChanneling = function() return false end,
                        IsMoving = function() return false end
                    }
                }

                -- Create mock Combat table
                Combat = {
                    GetTime = function() return 0 end,
                    Exists = function() return true end
                }

                -- Create mock Cast function
                function Cast(spell)
                    return true
                end

                -- Create mock chunk environment
                local env = {
                    PS = PS,
                    Combat = Combat,
                    Cast = Cast
                }

                -- Return the environment for the chunk
                return env
            """

            # Execute mock setup and get environment
            env = self.lua.execute(mock_lua)

            # Load the code as a module using require()
            setup = f"""
                -- Save the code to a temporary string
                local code = [=[
                    {lua_code}
                ]=]
                
                -- Create a loader function that returns our code
                package.preload['rotation'] = function()
                    local chunk = assert(load(code))
                    return chunk(PS)  -- Pass PS as the module parameter
                end
                
                -- Load the module and verify it
                local rotation = require('rotation')
                assert(type(rotation) == 'table', 'Rotation must be a table')
                assert(type(rotation.Execute) == 'function', 'Rotation must have Execute function')
                return rotation
            """
            
            # Execute the chunk to get the rotation
            rotation = self.lua.execute(setup)
            
            # Basic validation in Python
            self.assertIsNotNone(rotation)
        except Exception as e:
            self.fail(f"Lua code is invalid: {e}\nCode:\n{lua_code}")
        
    def assertMetricsValid(self):
        """Assert that performance metrics are valid"""
        metrics = monitor.get_metrics()
        self.assertGreater(metrics['total_operations'], 0)
        self.assertGreater(metrics['successful_operations'], 0)
        self.assertLess(metrics['failed_operations'], 1)

    def get_test_file(self, filename):
        """Get path to test file relative to test case"""
        return Path(__file__).parent / filename 