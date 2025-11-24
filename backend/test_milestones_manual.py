"""
Manual test script for milestone functionality.
Run this after starting the backend server to verify the milestone API endpoints.
"""

import requests
import json
from datetime import date, timedelta

BASE_URL = "http://localhost:8000/api"

def test_milestones():
    """Test milestone CRUD operations"""
    
    print("=" * 60)
    print("Testing Milestone API")
    print("=" * 60)
    
    # First, create a test project (assuming projects API exists)
    print("\n1. Creating test project...")
    project_data = {
        "code": "TEST2025-M001",
        "requirement_code": "R202511240001",
        "name": "里程碑測試專案",
        "status": "active"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/projects/", json=project_data)
        if response.status_code == 201:
            project = response.json()
            project_id = project["id"]
            print(f"✓ Project created: ID={project_id}, Name={project['name']}")
        else:
            print(f"✗ Failed to create project: {response.status_code}")
            print(response.text)
            return
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend server. Make sure it's running on http://localhost:8000")
        return
    
    # Test 1: Create milestone
    print("\n2. Creating milestone...")
    milestone_data = {
        "name": "需求啟動",
        "start_date": str(date.today()),
        "end_date": str(date.today() + timedelta(days=3)),
        "description": "專案需求啟動階段",
        "display_order": 1
    }
    
    response = requests.post(f"{BASE_URL}/projects/{project_id}/milestones/", json=milestone_data)
    if response.status_code == 201:
        milestone = response.json()
        milestone_id = milestone["id"]
        print(f"✓ Milestone created: ID={milestone_id}, Name={milestone['name']}")
    else:
        print(f"✗ Failed to create milestone: {response.status_code}")
        print(response.text)
        return
    
    # Test 2: Get project milestones
    print("\n3. Getting project milestones...")
    response = requests.get(f"{BASE_URL}/projects/{project_id}/milestones/")
    if response.status_code == 200:
        milestones = response.json()
        print(f"✓ Retrieved {len(milestones)} milestone(s)")
        for m in milestones:
            print(f"  - {m['name']}: {m['start_date']} ~ {m['end_date']}")
    else:
        print(f"✗ Failed to get milestones: {response.status_code}")
    
    # Test 3: Get single milestone
    print("\n4. Getting single milestone...")
    response = requests.get(f"{BASE_URL}/milestones/{milestone_id}")
    if response.status_code == 200:
        milestone = response.json()
        print(f"✓ Retrieved milestone: {milestone['name']}")
    else:
        print(f"✗ Failed to get milestone: {response.status_code}")
    
    # Test 4: Update milestone
    print("\n5. Updating milestone...")
    update_data = {
        "name": "需求啟動（已更新）",
        "description": "更新後的說明"
    }
    response = requests.patch(f"{BASE_URL}/milestones/{milestone_id}", json=update_data)
    if response.status_code == 200:
        milestone = response.json()
        print(f"✓ Milestone updated: {milestone['name']}")
    else:
        print(f"✗ Failed to update milestone: {response.status_code}")
        print(response.text)
    
    # Test 5: Create another milestone
    print("\n6. Creating second milestone...")
    milestone_data2 = {
        "name": "系統分析 SA",
        "start_date": str(date.today() + timedelta(days=4)),
        "end_date": str(date.today() + timedelta(days=13)),
        "description": "系統分析階段",
        "display_order": 2
    }
    response = requests.post(f"{BASE_URL}/projects/{project_id}/milestones/", json=milestone_data2)
    if response.status_code == 201:
        milestone2 = response.json()
        milestone2_id = milestone2["id"]
        print(f"✓ Second milestone created: ID={milestone2_id}, Name={milestone2['name']}")
    else:
        print(f"✗ Failed to create second milestone: {response.status_code}")
    
    # Test 6: Get all milestones again
    print("\n7. Getting all project milestones...")
    response = requests.get(f"{BASE_URL}/projects/{project_id}/milestones/")
    if response.status_code == 200:
        milestones = response.json()
        print(f"✓ Retrieved {len(milestones)} milestone(s)")
        for m in milestones:
            print(f"  - {m['name']}: {m['start_date']} ~ {m['end_date']}")
    else:
        print(f"✗ Failed to get milestones: {response.status_code}")
    
    # Test 7: Delete milestone
    print("\n8. Deleting first milestone...")
    response = requests.delete(f"{BASE_URL}/milestones/{milestone_id}")
    if response.status_code == 204:
        print(f"✓ Milestone deleted")
    else:
        print(f"✗ Failed to delete milestone: {response.status_code}")
    
    # Verify deletion
    print("\n9. Verifying deletion...")
    response = requests.get(f"{BASE_URL}/projects/{project_id}/milestones/")
    if response.status_code == 200:
        milestones = response.json()
        print(f"✓ Now {len(milestones)} milestone(s) remain")
        for m in milestones:
            print(f"  - {m['name']}: {m['start_date']} ~ {m['end_date']}")
    
    # Cleanup: Delete test project
    print("\n10. Cleaning up test project...")
    response = requests.delete(f"{BASE_URL}/projects/{project_id}")
    if response.status_code == 204:
        print(f"✓ Test project deleted")
    else:
        print(f"  (Project cleanup skipped or failed)")
    
    print("\n" + "=" * 60)
    print("Milestone API Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_milestones()

