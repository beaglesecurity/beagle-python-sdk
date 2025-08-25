#!/usr/bin/env python3
"""
Basic usage example for the Beagle Python SDK.

This example demonstrates the fundamental operations you can perform
with the Beagle SDK including project management, application testing,
and result retrieval.
"""

import os
import time
from beagle_sdk import BeagleClient, BeagleAPIError


def main():
    # Initialize client with API key from environment variable
    api_key = os.getenv('BEAGLE_API_KEY')
    if not api_key:
        print("Please set BEAGLE_API_KEY environment variable")
        return
    
    client = BeagleClient(api_key=api_key)
    
    try:
        # 1. List all projects
        print("📁 Fetching all projects...")
        projects = client.projects.list()
        print(f"Found {len(projects.get('data', []))} projects")
        
        if not projects.get('data'):
            print("No projects found. Please create a project first.")
            return
        
        # Use the first project
        project = projects['data'][0]
        project_key = project['id']
        print(f"Using project: {project['name']} ({project_key})")
        
        # 2. List applications in the project
        print(f"\n🚀 Fetching applications for project {project['name']}...")
        applications = client.applications.list(project_key=project_key)
        
        if not applications.get('data'):
            print("No applications found in this project.")
            return
        
        # Use the first application
        app = applications['data'][0]
        app_token = app['application_token']
        print(f"Using application: {app['name']} ({app_token})")
        
        # 3. Get application details
        print(f"\n📋 Getting application details...")
        app_details = client.applications.get(app_token)
        print(f"Application URL: {app_details.get('url', 'N/A')}")
        print(f"Application Status: {app_details.get('status', 'N/A')}")
        
        # 4. Get application summary
        print(f"\n📊 Getting application summary...")
        summary = client.applications.get_summary(app_token)
        print(f"Total Vulnerabilities: {summary.get('total_vulnerabilities', 'N/A')}")
        print(f"Critical Issues: {summary.get('critical_count', 'N/A')}")
        print(f"High Issues: {summary.get('high_count', 'N/A')}")
        
        # 5. Start a security test
        print(f"\n🔍 Starting security test for {app['name']}...")
        test_config = {
            "scan_type": "quick",
            "description": "SDK example test"
        }
        
        test_result = client.testing.start(app_token, test_config)
        result_token = test_result.get('result_token')
        
        if result_token:
            print(f"Test started successfully. Result token: {result_token}")
            
            # 6. Monitor test status
            print("\n⏳ Monitoring test progress...")
            max_wait_time = 300  # 5 minutes
            wait_interval = 30   # 30 seconds
            elapsed_time = 0
            
            while elapsed_time < max_wait_time:
                status = client.testing.get_status(app_token, result_token)
                current_status = status.get('status', 'unknown')
                progress = status.get('progress', 0)
                
                print(f"Status: {current_status}, Progress: {progress}%")
                
                if current_status in ['completed', 'failed', 'stopped']:
                    break
                
                time.sleep(wait_interval)
                elapsed_time += wait_interval
            
            # 7. Get test results if completed
            if current_status == 'completed':
                print("\n📄 Retrieving test results...")
                results = client.results.get_json(app_token, result_token)
                
                vulnerabilities = results.get('vulnerabilities', [])
                print(f"Found {len(vulnerabilities)} vulnerabilities")
                
                # Show top 5 vulnerabilities
                for i, vuln in enumerate(vulnerabilities[:5], 1):
                    print(f"  {i}. {vuln.get('title', 'Unknown')} "
                          f"(Severity: {vuln.get('severity', 'N/A')})")
                
                # 8. Download PDF report
                print("\n📥 Downloading PDF report...")
                pdf_path = client.results.download_pdf(
                    app_token, 
                    result_token,
                    f"beagle_report_{app['name'].replace(' ', '_')}.pdf"
                )
                print(f"Report saved to: {pdf_path}")
            
            elif current_status == 'failed':
                print("❌ Test failed")
            elif elapsed_time >= max_wait_time:
                print("⏰ Test is still running after 5 minutes")
                
                # Stop the test
                print("🛑 Stopping the test...")
                client.testing.stop(app_token)
        else:
            print("❌ Failed to start test")
        
        # 9. Get running sessions
        print(f"\n🏃 Getting running test sessions...")
        running_sessions = client.testing.get_running_sessions()
        active_count = len(running_sessions.get('data', []))
        print(f"Active test sessions: {active_count}")
        
        print("\n✅ Example completed successfully!")
        
    except BeagleAPIError as e:
        print(f"❌ Beagle API Error: {e}")
        if hasattr(e, 'status_code'):
            print(f"Status Code: {e.status_code}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
