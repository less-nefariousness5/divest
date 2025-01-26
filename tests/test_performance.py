"""
Performance tests for PS SimC Parser
"""
import time
import cProfile
import pstats
import io
from .base import PSTestCase
import psutil
import os
import concurrent.futures
import gc
import json
from memory_profiler import profile
from ps_simc_parser.utils.lua import LuaGenerator

class TestPerformance(PSTestCase):
    """Test parser and generator performance"""
    
    def setUp(self):
        super().setUp()
        self.profiler = cProfile.Profile()
        self.process = psutil.Process(os.getpid())
        
        # Large APL template with complex conditions
        self.large_apl = """
# Large APL Template
actions=auto_attack

# Complex conditions section
actions+=/variable,name=complex_var1,value=target.health.pct<=20&(buff.avenging_wrath.up|buff.crusade.up)&holy_power>=3
actions+=/variable,name=complex_var2,value=cooldown.blade_of_justice.remains<=gcd*2&holy_power<=3&(buff.avenging_wrath.up|buff.crusade.up)
actions+=/variable,name=complex_var3,value=target.time_to_die<=8&holy_power>=3|target.time_to_die<=12&holy_power>=4

# Resource tracking section
actions+=/variable,name=resource_var1,value=holy_power.deficit>=2&(cooldown.blade_of_justice.remains>=gcd*2|cooldown.divine_toll.remains>=gcd*2)
actions+=/variable,name=resource_var2,value=holy_power>=3&buff.divine_purpose.up&buff.divine_purpose.remains<gcd*2

# Generated section (100 similar actions)
""" + '\n'.join([f'actions+=/spell_{i},if=holy_power>={i%5}&buff.avenging_wrath.remains>={i%10}' for i in range(100)])

    def test_parser_performance(self):
        """Test parser performance with large APL"""
        # Enable profiling
        self.profiler.enable()
        
        start_time = time.time()
        result = self.parser.parse(self.large_apl)
        parse_time = time.time() - start_time
        
        self.profiler.disable()
        
        # Get profiling stats
        s = io.StringIO()
        ps = pstats.Stats(self.profiler, stream=s).sort_stats('cumulative')
        ps.print_stats()
        
        # Performance assertions
        self.assertLess(parse_time, 1.0, "Parsing took too long")
        self.assertGreater(len(result.action_lists['default']), 100, "Not all actions were parsed")
        
        # Log performance metrics
        with open('performance_metrics.json', 'a') as f:
            metrics = {
                'timestamp': time.time(),
                'parse_time': parse_time,
                'action_count': len(result.action_lists['default']),
                'profile': s.getvalue()
            }
            json.dump(metrics, f)
            f.write('\n')

    @profile
    def test_memory_usage(self):
        """Test memory usage during parsing and generation"""
        # Force garbage collection
        gc.collect()
        
        # Get initial memory state
        initial_memory = self.process.memory_info().rss
        
        # Parse large APL
        result = self.parser.parse(self.large_apl)
        parse_memory = self.process.memory_info().rss - initial_memory
        
        # Generate Lua code
        generator = LuaGenerator()
        lua_code = []
        for action in result.action_lists['default']:
            lua_code.append(generator.get_indent() + str(action))
        total_memory = self.process.memory_info().rss - initial_memory
        
        # Memory assertions
        self.assertLess(parse_memory, 25 * 1024 * 1024, "Parsing used too much memory")
        self.assertLess(total_memory, 50 * 1024 * 1024, "Total memory usage too high")
        
        # Log memory metrics
        with open('memory_metrics.json', 'a') as f:
            metrics = {
                'timestamp': time.time(),
                'parse_memory_mb': parse_memory / (1024 * 1024),
                'total_memory_mb': total_memory / (1024 * 1024),
                'action_count': len(result.action_lists['default'])
            }
            json.dump(metrics, f)
            f.write('\n')

    def test_string_generation_performance(self):
        """Test string generation performance"""
        # Parse complex APL
        result = self.parser.parse(self.large_apl)
        actions = result.action_lists['default']
        
        # First generation (cold run)
        start_time = time.time()
        generator = LuaGenerator()
        for _ in range(100):
            lua_code = []
            for action in actions:
                lua_code.append(generator.get_indent() + str(action))
        cold_time = time.time() - start_time
        
        # Second generation (warm run)
        start_time = time.time()
        for _ in range(100):
            lua_code = []
            for action in actions:
                lua_code.append(generator.get_indent() + str(action))
        warm_time = time.time() - start_time
        
        # Performance assertions - warm run should be within reasonable range
        # Allow some variance since timing can be affected by system load
        self.assertLess(abs(warm_time - cold_time), cold_time * 0.5, 
                       "String generation performance varies too much between runs")
        
        # Log performance metrics
        with open('string_generation_metrics.json', 'a') as f:
            metrics = {
                'timestamp': time.time(),
                'cold_time': cold_time,
                'warm_time': warm_time,
                'action_count': len(actions),
                'iterations': 100
            }
            json.dump(metrics, f)
            f.write('\n')

    def test_concurrent_generation(self):
        """Test concurrent generation performance and scaling"""
        result = self.parser.parse(self.large_apl)
        actions = result.action_lists['default']
        
        def generate_lua():
            generator = LuaGenerator()
            lua_code = []
            for action in actions:
                lua_code.append(generator.get_indent() + str(action))
            return '\n'.join(lua_code)
        
        # Test with different numbers of workers
        for num_workers in [2, 4, 8]:
            start_time = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                futures = []
                for _ in range(num_workers):
                    futures.append(
                        executor.submit(generate_lua)
                    )
                
                # All generations should complete within timeout
                timeout = 5 * (num_workers / 4)  # Scale timeout with workers
                done, _ = concurrent.futures.wait(futures, timeout=timeout)
                
                # Performance assertions
                self.assertEqual(len(done), num_workers, f"Not all workers completed with {num_workers} workers")
                
                # Calculate throughput
                total_time = time.time() - start_time
                throughput = num_workers / total_time
                
                # Log concurrency metrics
                with open('concurrency_metrics.json', 'a') as f:
                    metrics = {
                        'timestamp': time.time(),
                        'num_workers': num_workers,
                        'total_time': total_time,
                        'throughput': throughput,
                        'completed_tasks': len(done)
                    }
                    json.dump(metrics, f)
                    f.write('\n')

if __name__ == '__main__':
    unittest.main()