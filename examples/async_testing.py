#!/usr/bin/env python3
"""
Asynchronous testing example for the Beagle Python SDK.

This example demonstrates how to manage multiple security tests
concurrently and monitor their progress efficiently.
"""

import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from beagle_sdk import BeagleClient, BeagleAPIError


def monitor_test(client, app_token, result_token, app_name, max_wait=600):
    """
    Monitor a single test until completion.
    
    Args:
        client: BeagleClient instance
        app_token: Application token
        result_token: Test result token
        app_name: Application name for logging
        max_wait: Maximum wait time in seconds
        
    Returns:
        dict: Test results or None if failed/timeout
    """
    print(f"🔍 Monitoring test for {app_name}...")
    
    start_time = time.time()
    wait_interval = 30  # Check every 30 seconds
    
    while (time.time() - start_time) < max_wait:
        try:
            status = client.testing.get_status(app_token, result_token)
            current_status = status.get('status', 'unknown')
            progress = status.get('progress', 0)
            
            print(f"📊 {app_name}: {current_status} ({progress}%)")
            
            if current_status == 'completed':
                # Get test results
                results = client.results.get_json(app_token, result_token)
                vulnerabilities = results.get('vulnerabilities', [])
                
                print(f"✅ {app_name}: Test completed - {len(vulnerabilities)} vulnerabilities found")
                
                return {
                    'app_name': app_name,
                    'app_token': app_token,
                    'result_token': result_token,
                    'status': 'completed',
                    'vulnerabilities': vulnerabilities,
                    'results': results
                }
                
            elif current_status in ['failed', 'stopped']:
                print(f"❌ {app_name}: Test {current_status}")
                return {
                    'app_name': app_name,
                    'app_token': app_token,
                    'result_token': result_token,
                    'status': current_status,
                    'vulnerabilities': [],
                    'results': None
                }
            
            # Wait before next check
            time.sleep(wait_interval)
            
        except BeagleAPIError as e:
            print(f"⚠️  {app_name}: Error checking status - {e}")
            time.sleep(wait_interval)
    
    # Timeout reached
    print(f"⏰ {app_name}: Test timeout after {max_wait} seconds")
    
    try:
        # Try to stop the test
        client.testing.stop(app_token)
        print(f"🛑 {app_name}: Test stopped due to timeout")
    except BeagleAPIError:
        pass
    
    return {
        'app_name': app_name,
        'app_token': app_token,
        'result_token': result_token,
        'status': 'timeout',
        'vulnerabilities': [],
        'results': None
    }


def start_test_for_app(client, app, test_config):
    """
    Start a test for a single application.
    
    Args:
        client: BeagleClient instance
        app: Application data
        test_config: Test configuration
        
    Returns:
        dict: Test start result or None if failed
    """
    app_name = app['name']
    app_token = app['application_token']
    
    try:
        print(f"🚀 Starting test for {app_name}...")
        test_result = client.testing.start(app_token, test_config)
        result_token = test_result.get('result_token')
        
        if result_token:
            print(f"✅ {app_name}: Test started - Result token: {result_token}")
            return {
                'app': app,
                'app_token': app_token,
                'result_token': result_token,
                'app_name': app_name
            }
        else:
            print(f"❌ {app_name}: Failed to start test")
            return None
            
    except BeagleAPIError as e:
        print(f"❌ {app_name}: Error starting test - {e}")
        return None


def main():
    # Initialize client
    api_key = os.getenv('BEAGLE_API_KEY')
    if not api_key:
        print("Please set BEAGLE_API_KEY environment variable")
        return
    
    client = BeagleClient(api_key=api_key)
    
    try:
        # 1. Get applications to test
        print("📱 Finding applications to test...")
        applications = client.applications.list(count=50)
        
        if not applications.get('data'):
            print("No applications found")
            return
        
        # Filter applications that are testable (you might want to add more criteria)
        testable_apps = [
            app for app in applications['data'] 
            if app.get('status') == 'active' and app.get('url')
        ][:5]  # Limit to 5 applications for this example
        
        if not testable_apps:
            print("No testable applications found")
            return
        
        print(f"Found {len(testable_apps)} applications to test:")
        for app in testable_apps:
            print(f"  - {app['name']} ({app['url']})")
        
        # 2. Configure test settings
        test_config = {
            "scan_type": "quick",
            "description": "Concurrent testing via SDK",
            "max_duration": 1800  # 30 minutes max per test
        }
        
        print(f"\n🔧 Test Configuration:")
        print(f"  - Scan Type: {test_config['scan_type']}")
        print(f"  - Max Duration: {test_config['max_duration']} seconds")
        
        # 3. Start tests concurrently
        print(f"\n🚀 Starting {len(testable_apps)} tests concurrently...")
        
        started_tests = []
        
        # Use ThreadPoolExecutor to start tests in parallel
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all test start tasks
            future_to_app = {
                executor.submit(start_test_for_app, client, app, test_config): app
                for app in testable_apps
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_app):
                result = future.result()
                if result:
                    started_tests.append(result)
        
        if not started_tests:
            print("❌ No tests were started successfully")
            return
        
        print(f"✅ Successfully started {len(started_tests)} tests")
        
        # 4. Monitor all tests concurrently
        print(f"\n⏳ Monitoring {len(started_tests)} tests...")
        
        completed_tests = []
        
        # Use ThreadPoolExecutor to monitor tests in parallel
        with ThreadPoolExecutor(max_workers=len(started_tests)) as executor:
            # Submit all monitoring tasks
            future_to_test = {
                executor.submit(
                    monitor_test, 
                    client, 
                    test['app_token'], 
                    test['result_token'], 
                    test['app_name'],
                    600  # 10 minute timeout per test
                ): test
                for test in started_tests
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_test):
                result = future.result()
                if result:
                    completed_tests.append(result)
        
        # 5. Generate summary report
        print(f"\n📊 Test Summary Report")
        print("=" * 50)
        
        total_vulnerabilities = 0
        completed_count = 0
        failed_count = 0
        timeout_count = 0
        
        for test in completed_tests:
            status = test['status']
            vuln_count = len(test['vulnerabilities'])
            
            print(f"\n🏷️  {test['app_name']}")
            print(f"   Status: {status}")
            print(f"   Vulnerabilities: {vuln_count}")
            
            if status == 'completed':
                completed_count += 1
                total_vulnerabilities += vuln_count
                
                # Show top vulnerabilities
                if vuln_count > 0:
                    top_vulns = test['vulnerabilities'][:3]
                    print("   Top vulnerabilities:")
                    for i, vuln in enumerate(top_vulns, 1):
                        severity = vuln.get('severity', 'Unknown')
                        title = vuln.get('title', 'Unknown')[:50]
                        print(f"     {i}. [{severity}] {title}")
                        
            elif status == 'failed':
                failed_count += 1
            elif status == 'timeout':
                timeout_count += 1
        
        # Overall statistics
        print(f"\n📈 Overall Statistics:")
        print(f"   Total Tests: {len(completed_tests)}")
        print(f"   Completed: {completed_count}")
        print(f"   Failed: {failed_count}")
        print(f"   Timeout: {timeout_count}")
        print(f"   Total Vulnerabilities: {total_vulnerabilities}")
        
        if completed_count > 0:
            avg_vulns = total_vulnerabilities / completed_count
            print(f"   Average Vulnerabilities per App: {avg_vulns:.1f}")
        
        # 6. Download reports for completed tests
        if completed_count > 0:
            print(f"\n📥 Downloading reports for completed tests...")
            
            for test in completed_tests:
                if test['status'] == 'completed':
                    try:
                        app_name_clean = test['app_name'].replace(' ', '_').replace('/', '_')
                        pdf_path = client.results.download_pdf(
                            test['app_token'],
                            test['result_token'],
                            f"report_{app_name_clean}_{test['result_token'][:8]}.pdf"
                        )
                        print(f"   ✅ {test['app_name']}: {pdf_path}")
                    except BeagleAPIError as e:
                        print(f"   ❌ {test['app_name']}: Failed to download - {e}")
        
        print("\n✅ Asynchronous testing example completed!")
        
    except BeagleAPIError as e:
        print(f"❌ Beagle API Error: {e}")
        if hasattr(e, 'status_code'):
            print(f"Status Code: {e.status_code}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
