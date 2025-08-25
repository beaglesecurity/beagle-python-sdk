#!/usr/bin/env python3
"""
Project management example for the Beagle Python SDK.

This example demonstrates how to manage projects including:
- Creating and updating projects
- Managing project webhooks
- Retrieving project analytics and insights
"""

import os
from datetime import datetime
from beagle_sdk import BeagleClient, BeagleAPIError


def main():
    # Initialize client
    api_key = os.getenv('BEAGLE_API_KEY')
    if not api_key:
        print("Please set BEAGLE_API_KEY environment variable")
        return
    
    client = BeagleClient(api_key=api_key)
    
    try:
        # 1. Create a new project
        print("🆕 Creating a new project...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_data = {
            "name": f"SDK Example Project {timestamp}",
            "description": "Project created by Beagle Python SDK example",
            "tags": ["example", "sdk", "demo"]
        }
        
        new_project = client.projects.create(project_data)
        project_key = new_project.get('id') or new_project.get('project_key')
        
        print(f"✅ Project created: {new_project['name']}")
        print(f"   Project Key: {project_key}")
        
        # 2. Get project details
        print(f"\n📋 Getting project details...")
        project_details = client.projects.get(project_key)
        print(f"   Name: {project_details['name']}")
        print(f"   Status: {project_details.get('status', 'N/A')}")
        print(f"   Created: {project_details.get('created_at', 'N/A')}")
        
        # 3. Update project
        print(f"\n✏️  Updating project...")
        updated_data = project_data.copy()
        updated_data['description'] = "Updated description from SDK example"
        updated_data['project_key'] = project_key
        
        updated_project = client.projects.update(updated_data)
        print(f"✅ Project updated: {updated_project.get('description', 'N/A')}")
        
        # 4. Setup project webhook
        print(f"\n🎣 Setting up project webhook...")
        webhook_data = {
            "url": "https://webhook.site/unique-id-here",  # Replace with your webhook URL
            "events": ["test_completed", "vulnerability_found"],
            "active": True
        }
        
        try:
            webhook = client.projects.create_webhook(project_key, webhook_data)
            print(f"✅ Webhook created: {webhook.get('url', 'N/A')}")
            
            # Get webhook details
            webhook_details = client.projects.get_webhook(project_key)
            print(f"   Webhook Status: {webhook_details.get('active', 'N/A')}")
            print(f"   Events: {', '.join(webhook_details.get('events', []))}")
            
        except BeagleAPIError as e:
            print(f"⚠️  Webhook setup failed: {e}")
        
        # 5. Get project analytics
        print(f"\n📊 Getting project analytics...")
        
        try:
            # Get project summary
            summary = client.projects.get_summary(project_key)
            print(f"   Total Applications: {summary.get('total_applications', 0)}")
            print(f"   Total Tests: {summary.get('total_tests', 0)}")
            print(f"   Total Vulnerabilities: {summary.get('total_vulnerabilities', 0)}")
            
            # Get vulnerability count by criticality
            criticality_data = client.projects.get_open_count_by_criticality(project_key)
            if 'data' in criticality_data:
                print(f"   Critical: {criticality_data['data'].get('critical', 0)}")
                print(f"   High: {criticality_data['data'].get('high', 0)}")
                print(f"   Medium: {criticality_data['data'].get('medium', 0)}")
                print(f"   Low: {criticality_data['data'].get('low', 0)}")
            
            # Get project score
            score_data = client.projects.get_score("cvss", project_key)
            if 'score' in score_data:
                print(f"   CVSS Score: {score_data['score']}")
                
        except BeagleAPIError as e:
            print(f"ℹ️  Analytics not available yet (new project): {e}")
        
        # 6. Get all projects summary
        print(f"\n📈 Getting account-wide project analytics...")
        try:
            all_summaries = client.projects.get_all_summaries()
            total_projects = len(all_summaries.get('data', []))
            print(f"   Total Projects in Account: {total_projects}")
            
            # Get account-wide vulnerability trends
            trend_data = client.projects.get_vulnerability_count_trend(limit=10)
            if 'data' in trend_data and trend_data['data']:
                print(f"   Recent Vulnerability Trends Available: {len(trend_data['data'])} entries")
                
        except BeagleAPIError as e:
            print(f"ℹ️  Account analytics: {e}")
        
        # 7. Get project insights
        print(f"\n🔍 Getting project insights...")
        try:
            insights = client.projects.get_insight(project_key)
            if insights.get('recommendations'):
                print(f"   Recommendations: {len(insights['recommendations'])}")
            if insights.get('security_score'):
                print(f"   Security Score: {insights['security_score']}")
                
        except BeagleAPIError as e:
            print(f"ℹ️  Insights not available: {e}")
        
        # 8. List all projects with search
        print(f"\n🔍 Searching for projects...")
        search_results = client.projects.list(search="SDK Example")
        matching_projects = len(search_results.get('data', []))
        print(f"   Found {matching_projects} projects matching 'SDK Example'")
        
        # 9. Clean up - delete the project
        print(f"\n🗑️  Cleaning up - deleting project...")
        confirmation = input(f"Delete project '{new_project['name']}'? (y/N): ")
        
        if confirmation.lower() == 'y':
            try:
                # Delete webhook first if it exists
                client.projects.delete_webhook(project_key)
                print("   ✅ Webhook deleted")
            except BeagleAPIError:
                pass  # Webhook might not exist
            
            # Delete project
            client.projects.delete(project_key)
            print("   ✅ Project deleted")
        else:
            print(f"   ℹ️  Project kept: {project_key}")
        
        print("\n✅ Project management example completed!")
        
    except BeagleAPIError as e:
        print(f"❌ Beagle API Error: {e}")
        if hasattr(e, 'status_code'):
            print(f"Status Code: {e.status_code}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
