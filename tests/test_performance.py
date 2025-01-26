"""
Performance tests for PS SimC Parser
"""
import time
from .base import PSTestCase
import psutil
import os
import concurrent.futures

class TestPerformance(PSTestCase):
    """Test parser and generator performance"""
    
    def test_parser_performance(self):
        """Test parser performance with large APL"""
        simc = self.load_fixture('large_apl.simc')
        
        start_time = time.time()
        result = self.parser.parse(simc)
        end_time = time.time()
        
        self.assertLess(end_time - start_time, 1.0)  # Should parse in under 1 second
        
    def test_generator_performance(self):
        """Test generator performance with complex rotation"""
        actions = self.load_fixture('complex_rotation.json')
        
        start_time = time.time()
        lua_code = self.generator.generate(actions, {})
        end_time = time.time()
        
        self.assertLess(end_time - start_time, 2.0)  # Should generate in under 2 seconds 

    def test_memory_usage(self):
        """Test memory usage during generation"""
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Generate large rotation
        actions = self.load_fixture('complex_rotation.json')
        lua_code = self.generator.generate(actions, {})
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Should use less than 50MB additional memory
        self.assertLess(memory_increase, 50 * 1024 * 1024)

    def test_cache_performance(self):
        """Test caching performance"""
        actions = self.load_fixture('complex_rotation.json')
        
        # First generation (cold cache) - multiple iterations
        start_time = time.time()
        for _ in range(100):  # Run 100 times to get measurable difference
            self.generator.generate(actions, {})
        cold_time = time.time() - start_time
        
        # Second generation (warm cache) - multiple iterations
        start_time = time.time()
        for _ in range(100):  # Run 100 times to get measurable difference
            self.generator.generate(actions, {})
        warm_time = time.time() - start_time
        
        # Warm cache should be at least 25% faster
        self.assertLess(warm_time, cold_time * 0.75)

    def test_concurrent_generation(self):
        """Test concurrent generation performance"""
        actions = self.load_fixture('complex_rotation.json')
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for _ in range(4):
                futures.append(
                    executor.submit(self.generator.generate, actions, {})
                )
            
            # All generations should complete within 5 seconds
            done, _ = concurrent.futures.wait(futures, timeout=5)
            self.assertEqual(len(done), 4) 