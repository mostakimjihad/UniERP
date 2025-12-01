# Performance Testing Guidelines

## Overview

Performance testing in UniERP focuses on ensuring the system performs optimally under various load conditions, identifying bottlenecks, and validating that performance meets business requirements. This includes load testing, stress testing, and performance monitoring.

## Testing Framework Setup

### Performance Test Base Classes

```python
from odoo.tests import common, tagged
import time
import psutil
import gc
from unittest.mock import patch

@common.tagged('performance')
@common.tagged('slow')
class TestPerformance(common.TransactionCase):
    """Base class for performance tests."""
    
    def setUp(self):
        super().setUp()
        # Setup performance monitoring
        self.start_time = None
        self.end_time = None
        self.memory_before = psutil.Process().memory_info().rss
        self.gc_before = gc.collect()
    
    def tearDown(self):
        super().tearDown()
        # Record performance metrics
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            memory_after = psutil.Process().memory_info().rss
            gc_after = gc.collect()
            
            self.record_performance_metric({
                'test_name': self._testMethodName,
                'duration': duration,
                'memory_before': self.memory_before,
                'memory_after': memory_after,
                'gc_before': self.gc_before,
                'gc_after': gc_after,
            })
    
    def start_timer(self):
        """Start performance timer."""
        self.start_time = time.time()
    
    def stop_timer(self):
        """Stop performance timer."""
        self.end_time = time.time()
    
    def record_performance_metric(self, metric):
        """Record performance metric for analysis."""
        self.env['performance.metric'].create(metric)
```

### Benchmarking Framework

```python
# addons/performance/tests/benchmark_base.py
from contextlib import contextmanager
import time
import statistics

class PerformanceBenchmark:
    """Framework for performance benchmarking."""
    
    def __init__(self, name, warmup_runs=3, measurement_runs=10):
        self.name = name
        self.warmup_runs = warmup_runs
        self.measurement_runs = measurement_runs
        self.results = []
    
    @contextmanager
    def measure(self):
        """Context manager for measuring performance."""
        gc.collect()  # Clean up before measurement
        start_time = time.perf_counter()
        start_memory = psutil.Process().memory_info().rss
        
        try:
            yield
        finally:
            end_time = time.perf_counter()
            end_memory = psutil.Process().memory_info().rss
            
            self.results.append({
                'duration': end_time - start_time,
                'memory_delta': end_memory - start_memory,
            })
    
    def run_benchmark(self, test_function, *args, **kwargs):
        """Run complete benchmark."""
        # Warmup runs
        for i in range(self.warmup_runs):
            with self.measure():
                test_function(*args, **kwargs)
        
        # Measurement runs
        for i in range(self.measurement_runs):
            with self.measure():
                test_function(*args, **kwargs)
        
        return self.get_statistics()
    
    def get_statistics(self):
        """Calculate statistics from results."""
        durations = [r['duration'] for r in self.results]
        memory_deltas = [r['memory_delta'] for r in self.results]
        
        return {
            'name': self.name,
            'duration': {
                'mean': statistics.mean(durations),
                'median': statistics.median(durations),
                'min': min(durations),
                'max': max(durations),
                'std': statistics.stdev(durations),
            },
            'memory': {
                'mean': statistics.mean(memory_deltas),
                'median': statistics.median(memory_deltas),
                'min': min(memory_deltas),
                'max': max(memory_deltas),
                'std': statistics.stdev(memory_deltas),
            },
        }
```

## Best Practices and Naming Conventions

### File Organization

```
addons/my_module/tests/
├── performance/
│   ├── __init__.py
│   ├── test_model_performance.py    # Model operation performance
│   ├── test_api_performance.py      # API endpoint performance
│   ├── test_database_performance.py  # Database query performance
│   ├── test_load_performance.py     # Load testing scenarios
│   └── benchmarks/
│       ├── __init__.py
│       ├── benchmark_operations.py   # Operation benchmarks
│       └── benchmark_data.py        # Data generation for benchmarks
```

### Naming Conventions

```python
# Performance test class names
class TestModelPerformance(common.TransactionCase):  # Test + Entity + Performance
class TestAPIPerformance(common.TransactionCase):  # Test + Entity + Performance
class TestDatabasePerformance(common.TransactionCase):  # Test + Entity + Performance

# Performance test method names
def test_create_1000_records_performance(self):  # test_action_quantity_performance
def test_search_with_filters_performance(self):  # test_operation_with_condition_performance
def test_batch_operations_performance(self):  # test_batch_operation_performance
def test_concurrent_users_performance(self):  # test_concurrent_scenario_performance
```

## Sample Test Cases and Code Examples

### Model Performance Testing

```python
# addons/base/tests/performance/test_model_performance.py
@common.tagged('performance')
@common.tagged('slow')
class TestModelPerformance(common.TransactionCase):
    """Test model operation performance."""
    
    def setUp(self):
        super().setUp()
        # Create test data
        self.partners = []
        for i in range(1000):
            self.partners.append(self.env['res.partner'].create({
                'name': f'Partner {i}',
                'email': f'partner{i}@test.com',
            }))
    
    def test_partner_search_performance(self):
        """Test partner search performance."""
        benchmark = PerformanceBenchmark('partner_search')
        
        def search_partners():
            return self.env['res.partner'].search([('name', 'ilike', 'Partner%')])
        
        # Run benchmark
        stats = benchmark.run_benchmark(search_partners)
        
        # Assert performance requirements
        self.assertLess(stats['duration']['mean'], 0.1)  # 100ms max
        self.assertLess(stats['memory']['mean'], 10 * 1024 * 1024)  # 10MB max
    
    def test_partner_create_performance(self):
        """Test partner creation performance."""
        benchmark = PerformanceBenchmark('partner_create')
        
        def create_partners():
            partners = []
            for i in range(100):
                partners.append({
                    'name': f'Batch Partner {i}',
                    'email': f'batch{i}@test.com',
                })
            return self.env['res.partner'].create(partners)
        
        # Run benchmark
        stats = benchmark.run_benchmark(create_partners)
        
        # Assert performance requirements
        self.assertLess(stats['duration']['mean'], 0.5)  # 500ms max
        self.assertLess(stats['memory']['mean'], 50 * 1024 * 1024)  # 50MB max
    
    def test_partner_write_performance(self):
        """Test partner write performance."""
        partner = self.partners[0]
        benchmark = PerformanceBenchmark('partner_write')
        
        def update_partners():
            return partner.write({
                'name': 'Updated Partner',
                'email': 'updated@test.com',
            })
        
        # Run benchmark
        stats = benchmark.run_benchmark(update_partners)
        
        # Assert performance requirements
        self.assertLess(stats['duration']['mean'], 0.05)  # 50ms max
        self.assertLess(stats['memory']['mean'], 5 * 1024 * 1024)  # 5MB max
```

### Database Performance Testing

```python
# addons/base/tests/performance/test_database_performance.py
@common.tagged('performance')
@common.tagged('slow')
class TestDatabasePerformance(common.TransactionCase):
    """Test database operation performance."""
    
    def setUp(self):
        super().setUp()
        # Create test data
        self.test_records = []
        for i in range(10000):
            self.test_records.append(self.env['res.partner'].create({
                'name': f'Perf Test {i}',
                'email': f'perftest{i}@test.com',
            }))
    
    def test_query_optimization(self):
        """Test query optimization."""
        # Test unoptimized query
        benchmark = PerformanceBenchmark('unoptimized_query')
        
        def unoptimized_search():
            return self.env.cr.execute("""
                SELECT id, name, email 
                FROM res_partner 
                WHERE name LIKE %s
                ORDER BY name
            """, ('%Test%',))
        
        unoptimized_stats = benchmark.run_benchmark(unoptimized_search)
        
        # Test optimized query
        benchmark_opt = PerformanceBenchmark('optimized_query')
        
        def optimized_search():
            return self.env.cr.execute("""
                SELECT id, name, email 
                FROM res_partner 
                WHERE name ILIKE %s
                ORDER BY name
                LIMIT 1000
            """, ('%Test%',))
        
        optimized_stats = benchmark_opt.run_benchmark(optimized_search)
        
        # Optimized query should be faster
        self.assertLess(
            optimized_stats['duration']['mean'],
            unoptimized_stats['duration']['mean'] * 0.5  # At least 2x faster
        )
    
    def test_index_usage(self):
        """Test index usage performance."""
        # Test without index
        benchmark = PerformanceBenchmark('search_without_index')
        
        def search_without_index():
            return self.env.cr.execute("""
                SELECT id FROM res_partner 
                WHERE email = %s
            """, ('test@example.com',))
        
        without_index_stats = benchmark.run_benchmark(search_without_index)
        
        # Create index
        self.env.cr.execute("""
            CREATE INDEX CONCURRENTLY IF NOT EXISTS 
            idx_res_partner_email 
            ON res_partner(email)
        """)
        
        # Test with index
        benchmark_with_index = PerformanceBenchmark('search_with_index')
        
        def search_with_index():
            return self.env.cr.execute("""
                SELECT id FROM res_partner 
                WHERE email = %s
            """, ('test@example.com',))
        
        with_index_stats = benchmark_with_index.run_benchmark(search_with_index)
        
        # Indexed query should be faster
        self.assertLess(
            with_index_stats['duration']['mean'],
            without_index_stats['duration']['mean'] * 0.1  # At least 10x faster
        )
    
    def test_batch_operations(self):
        """Test batch operation performance."""
        benchmark_single = PerformanceBenchmark('single_operations')
        
        def single_operations():
            for record in self.test_records[:100]:
                record.write({'name': record.name + '_updated'})
        
        single_stats = benchmark_single.run_benchmark(single_operations)
        
        benchmark_batch = PerformanceBenchmark('batch_operations')
        
        def batch_operations():
            records = self.test_records[:100]
            return self.env['res.partner'].browse([r.id for r in records]).write({
                'name': self.env.cr.mogrify(
                    r.name + '_updated', 
                    records, 
                    'name'
                )
            })
        
        batch_stats = benchmark_batch.run_benchmark(batch_operations)
        
        # Batch operations should be faster
        self.assertLess(
            batch_stats['duration']['mean'],
            single_stats['duration']['mean'] * 0.2  # At least 5x faster
        )
```

### API Performance Testing

```python
# addons/web/tests/performance/test_api_performance.py
@common.tagged('performance')
@common.tagged('slow')
class TestAPIPerformance(common.TransactionCase):
    """Test API endpoint performance."""
    
    def setUp(self):
        super().setUp()
        # Create test data
        self.partners = []
        for i in range(1000):
            self.partners.append(self.env['res.partner'].create({
                'name': f'API Test {i}',
                'email': f'apitest{i}@test.com',
            }))
    
    def test_list_api_performance(self):
        """Test list API performance."""
        benchmark = PerformanceBenchmark('api_list')
        
        def call_list_api():
            return self.url_open(
                '/api/partner',
                query={'limit': 100},
                headers={'Content-Type': 'application/json'}
            )
        
        # Run benchmark
        stats = benchmark.run_benchmark(call_list_api)
        
        # Assert API performance requirements
        self.assertLess(stats['duration']['mean'], 0.2)  # 200ms max
        self.assertEqual(stats['status_code'], 200)
    
    def test_search_api_performance(self):
        """Test search API performance."""
        benchmark = PerformanceBenchmark('api_search')
        
        def call_search_api():
            return self.url_open(
                '/api/partner/search',
                data=json.dumps({
                    'domain': [('name', 'ilike', 'API Test%')],
                    'limit': 50,
                }),
                headers={'Content-Type': 'application/json'}
            )
        
        # Run benchmark
        stats = benchmark.run_benchmark(call_search_api)
        
        # Assert API performance requirements
        self.assertLess(stats['duration']['mean'], 0.3)  # 300ms max
        self.assertEqual(stats['status_code'], 200)
    
    def test_concurrent_api_calls(self):
        """Test API performance under concurrent load."""
        import threading
        import queue
        
        results = queue.Queue()
        
        def api_worker():
            try:
                response = self.url_open('/api/partner', query={'limit': 10})
                results.put(response.status_code)
            except Exception as e:
                results.put(f'Error: {e}')
        
        # Create concurrent workers
        threads = []
        start_time = time.time()
        
        for i in range(10):  # 10 concurrent requests
            thread = threading.Thread(target=api_worker)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Analyze results
        success_count = 0
        error_count = 0
        
        while not results.empty():
            result = results.get()
            if result == 200:
                success_count += 1
            else:
                error_count += 1
        
        # Assert concurrent performance
        self.assertLess(total_time, 5.0)  # All requests within 5 seconds
        self.assertEqual(success_count, 10)  # All requests successful
        self.assertEqual(error_count, 0)  # No errors
```

### Load Testing

```python
# addons/performance/tests/test_load_performance.py
@common.tagged('performance')
@common.tagged('slow')
class TestLoadPerformance(common.TransactionCase):
    """Test system performance under load."""
    
    def test_concurrent_user_simulation(self):
        """Test system with multiple concurrent users."""
        import threading
        import time
        
        results = []
        
        def simulate_user(user_id):
            """Simulate user operations."""
            start_time = time.time()
            
            # Simulate user login and navigation
            self.authenticate('user%s@test.com' % user_id, 'password123')
            
            # Simulate browsing products
            self.url_open('/web/shop')
            self.url_open('/web/shop/category/1')
            self.url_open('/web/shop/product/1')
            
            # Simulate adding to cart
            self.url_open('/web/shop/cart/add', data={
                'product_id': 1,
                'quantity': 2
            })
            
            end_time = time.time()
            results.append({
                'user_id': user_id,
                'duration': end_time - start_time,
                'success': True
            })
        
        # Create concurrent user simulations
        threads = []
        start_time = time.time()
        
        for i in range(50):  # 50 concurrent users
            thread = threading.Thread(target=simulate_user, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Analyze load test results
        successful_users = [r for r in results if r['success']]
        failed_users = [r for r in results if not r['success']]
        
        # Assert load performance requirements
        self.assertLess(total_time, 60.0)  # Complete within 1 minute
        self.assertGreater(len(successful_users), 45)  # At least 90% success
        self.assertLess(len(failed_users), 5)  # Less than 10% failure
    
    def test_memory_usage_under_load(self):
        """Test memory usage under load."""
        import psutil
        import gc
        
        # Get initial memory
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        
        # Create large dataset
        records = []
        for i in range(10000):
            records.append({
                'name': f'Memory Test {i}',
                'description': 'x' * 100,  # 100 chars description
            })
        
        self.env['test.model'].create(records)
        
        # Get peak memory
        peak_memory = process.memory_info().rss
        memory_increase = peak_memory - initial_memory
        
        # Assert memory requirements
        self.assertLess(memory_increase, 500 * 1024 * 1024)  # Less than 500MB increase
        
        # Clean up
        gc.collect()
```

## Test Data Management Strategies

### Performance Test Data Generation

```python
# addons/performance/tests/data_generators.py
import random
import string
from faker import Faker

class PerformanceDataGenerator:
    """Generate realistic test data for performance tests."""
    
    def __init__(self):
        self.fake = Faker()
    
    def generate_partners(self, count):
        """Generate realistic partner data."""
        partners = []
        for i in range(count):
            partners.append({
                'name': self.fake.company(),
                'email': self.fake.email(),
                'phone': self.fake.phone_number(),
                'street': self.fake.street_address(),
                'city': self.fake.city(),
                'country_id': self._get_random_country(),
                'is_company': random.choice([True, False]),
            })
        return partners
    
    def generate_products(self, count):
        """Generate realistic product data."""
        products = []
        for i in range(count):
            products.append({
                'name': self.fake.catch_phrase(),
                'description': self.fake.text(max_nb_chars=200),
                'list_price': round(random.uniform(10, 1000), 2),
                'cost': round(random.uniform(5, 500), 2),
                'type': random.choice(['product', 'service']),
                'categ_id': self._get_random_category(),
            })
        return products
    
    def generate_sales_orders(self, count, lines_per_order=5):
        """Generate realistic sales order data."""
        orders = []
        for i in range(count):
            order_lines = []
            for j in range(lines_per_order):
                order_lines.append({
                    'product_id': self._get_random_product(),
                    'quantity': random.randint(1, 10),
                    'price_unit': round(random.uniform(10, 500), 2),
                })
            
            orders.append({
                'partner_id': self._get_random_partner(),
                'order_line': order_lines,
                'date_order': self.fake.date_between(
                    start_date='-30d',
                    end_date='today'
                ),
            })
        return orders
```

### Performance Metrics Collection

```python
# addons/performance/tests/metrics_collector.py
import time
import psutil
import json
from datetime import datetime

class PerformanceMetricsCollector:
    """Collect and analyze performance metrics."""
    
    def __init__(self):
        self.metrics = []
        self.start_time = None
    
    def start_collection(self):
        """Start metrics collection."""
        self.start_time = time.time()
    
    def record_metric(self, name, value, unit='ms'):
        """Record a performance metric."""
        metric = {
            'timestamp': datetime.now().isoformat(),
            'name': name,
            'value': value,
            'unit': unit,
            'memory_usage': psutil.Process().memory_info().rss,
            'cpu_percent': psutil.cpu_percent(),
        }
        self.metrics.append(metric)
    
    def get_summary(self):
        """Get performance summary."""
        if not self.metrics:
            return {}
        
        # Group metrics by name
        grouped_metrics = {}
        for metric in self.metrics:
            name = metric['name']
            if name not in grouped_metrics:
                grouped_metrics[name] = []
            grouped_metrics[name].append(metric)
        
        # Calculate statistics
        summary = {}
        for name, metrics in grouped_metrics.items():
            values = [m['value'] for m in metrics]
            summary[name] = {
                'count': len(values),
                'mean': sum(values) / len(values),
                'min': min(values),
                'max': max(values),
                'total': sum(values),
            }
        
        return summary
    
    def export_metrics(self, filename):
        """Export metrics to file."""
        summary = self.get_summary()
        
        with open(filename, 'w') as f:
            json.dump({
                'test_run': {
                    'start_time': self.start_time,
                    'end_time': time.time(),
                    'duration': time.time() - self.start_time,
                },
                'metrics': self.metrics,
                'summary': summary,
            }, f, indent=2)
```

## Coverage Requirements and Reporting

### Performance Coverage Targets

| Performance Area | Minimum Coverage | Target Coverage |
|-----------------|------------------|-----------------|
| Model Operations | 80% | 95% |
| Database Queries | 85% | 98% |
| API Endpoints | 90% | 100% |
| Concurrent Users | 75% | 90% |
| Memory Usage | 80% | 95% |
| Load Scenarios | 70% | 85% |

### Performance Benchmarks

```python
# Performance benchmark definitions
PERFORMANCE_BENCHMARKS = {
    'database_query': {
        'simple_select': 0.01,  # 10ms
        'complex_join': 0.1,   # 100ms
        'aggregation': 0.2,     # 200ms
    },
    'api_response': {
        'simple_get': 0.05,     # 50ms
        'search_query': 0.1,     # 100ms
        'complex_post': 0.2,    # 200ms
    },
    'model_operation': {
        'create': 0.05,          # 50ms
        'write': 0.02,           # 20ms
        'read': 0.01,            # 10ms
        'unlink': 0.03,          # 30ms
    },
    'memory_usage': {
        'small_operation': 10 * 1024 * 1024,    # 10MB
        'medium_operation': 50 * 1024 * 1024,   # 50MB
        'large_operation': 100 * 1024 * 1024,   # 100MB
    },
    'concurrent_users': {
        'response_time': 2.0,     # 2 seconds
        'success_rate': 0.95,      # 95%
        'error_rate': 0.05,         # 5%
    },
}
```

## Running Performance Tests

### Command Line

```bash
# Run all performance tests
./unierp-bin -d test_db --test-enable --test-tags "+performance" --stop-after-init

# Run specific performance tests
./unierp-bin -d test_db --test-enable --test-tags "+performance,+database" --stop-after-init

# Run with performance monitoring
./unierp-bin -d test_db --test-enable --test-tags "+performance" --stop-after-init --log-level=debug

# Run with memory profiling
python3 -m cProfile -o profile.stats addons/my_module/tests/performance/test_model_performance.py
python3 -m pstats profile.stats
```

### Load Testing Tools

```bash
# Using Apache Bench (ab)
ab -n 1000 -c 10 -t 60 http://localhost:8069/web/shop

# Using Siege
siege -c 50 -r 10 -t 30S http://localhost:8069/api/partner

# Using Locust
locust -f performance_tests/locustfile.py --host=http://localhost:8069 --users=100 --spawn-rate=10 --run-time=60s

# Using JMeter
jmeter -n -t performance_tests.jmx -l results.jtl -Jusers=50 -Jrampup=10
```

## Common Pitfalls and Solutions

### Performance Test Isolation

```python
# Problem: Tests interfere with each other
def test_a_heavy_operation(self):
    # Heavy operation affects subsequent tests
    self.env['test.model'].create([{'name': f'Heavy {i}'} for i in range(10000)])

def test_b_light_operation(self):
    # Test B is slow due to Test A
    start = time.time()
    self.env['test.model'].create({'name': 'Light Operation'})
    duration = time.time() - start
    self.assertLess(duration, 0.1)  # Fails!

# Solution: Use proper cleanup
def tearDown(self):
    super().tearDown()
    # Clean up heavy data
    self.env['test.model'].search([('name', 'like', 'Heavy%')]).unlink()
```

### Measurement Accuracy

```python
# Problem: Inaccurate timing measurements
def test_operation_performance(self):
    start = time.time()  # Wall time, affected by system load
    self.env['test.model'].create({'name': 'Test'})
    end = time.time()
    duration = end - start

# Solution: Use perf_counter for accurate timing
def test_operation_performance(self):
    start = time.perf_counter()  # High-resolution timer
    self.env['test.model'].create({'name': 'Test'})
    end = time.perf_counter()
    duration = end - start
```

### Data Volume Issues

```python
# Problem: Tests use unrealistic data volumes
def test_with_unrealistic_data(self):
    # Creating 1 million records is unrealistic for most scenarios
    records = [{'name': f'Record {i}'} for i in range(1000000)]
    self.env['test.model'].create(records)

# Solution: Use realistic data volumes
def test_with_realistic_data(self):
    # Create realistic dataset (e.g., 1000 records)
    records = [{'name': f'Record {i}'} for i in range(1000)]
    self.env['test.model'].create(records)
```

---

*For specific testing methodologies, see: [Unit Testing](../unit-testing/README.md), [Integration Testing](../integration-testing/README.md), [Functional Testing](../functional-testing/README.md), [Security Testing](../security-testing/README.md)*