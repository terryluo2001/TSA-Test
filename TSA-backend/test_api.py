"""
Simple test script to demonstrate the To-Do List API functionality.
Make sure the Flask server is running before executing this script.
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def print_response(title, response):
    """Pretty print API responses"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_api():
    """Test all API endpoints"""

    print("Starting API Tests...")
    print(f"Base URL: {BASE_URL}")

    # Test 1: Get root endpoint
    response = requests.get(f"{BASE_URL}/")
    print_response("Test 1: Root Endpoint", response)

    # Test 2: Get all tasks (initially empty)
    response = requests.get(f"{BASE_URL}/tasks")
    print_response("Test 2: Get All Tasks (Empty)", response)

    # Test 3: Create first task
    task1 = {
        "title": "Buy groceries",
        "description": "Milk, eggs, bread, and vegetables",
        "status": "pending"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=task1)
    print_response("Test 3: Create First Task", response)
    task1_id = response.json()["data"]["id"]

    # Test 4: Create second task
    task2 = {
        "title": "Finish homework",
        "description": "Math and science assignments"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=task2)
    print_response("Test 4: Create Second Task (Default Status)", response)
    task2_id = response.json()["data"]["id"]

    # Test 5: Create third task
    task3 = {
        "title": "Go to gym",
        "description": "Cardio and strength training",
        "status": "in_progress"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=task3)
    print_response("Test 5: Create Third Task", response)

    # Test 6: Get all tasks (now with data)
    response = requests.get(f"{BASE_URL}/tasks")
    print_response("Test 6: Get All Tasks (With Data)", response)

    # Test 7: Update task status
    update_data = {"status": "completed"}
    response = requests.put(f"{BASE_URL}/tasks/{task1_id}", json=update_data)
    print_response("Test 7: Update Task Status to Completed", response)

    # Test 8: Update multiple fields
    update_data = {
        "title": "Complete all homework assignments",
        "description": "Math, science, and history",
        "status": "in_progress"
    }
    response = requests.put(f"{BASE_URL}/tasks/{task2_id}", json=update_data)
    print_response("Test 8: Update Multiple Fields", response)

    # Test 9: Get statistics
    response = requests.get(f"{BASE_URL}/tasks/stats")
    print_response("Test 9: Get Task Statistics", response)

    # Test 10: Delete a task
    response = requests.delete(f"{BASE_URL}/tasks/{task1_id}")
    print_response("Test 10: Delete Task", response)

    # Test 11: Get all tasks after deletion
    response = requests.get(f"{BASE_URL}/tasks")
    print_response("Test 11: Get All Tasks After Deletion", response)

    # Test 12: Try to get non-existent task (error handling)
    response = requests.put(f"{BASE_URL}/tasks/999", json={"status": "completed"})
    print_response("Test 12: Update Non-Existent Task (Error)", response)

    # Test 13: Try to create task without title (validation)
    invalid_task = {"description": "No title provided"}
    response = requests.post(f"{BASE_URL}/tasks", json=invalid_task)
    print_response("Test 13: Create Task Without Title (Validation Error)", response)

    # Test 14: Try to create task with invalid status
    invalid_task = {
        "title": "Invalid status task",
        "status": "not_a_valid_status"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=invalid_task)
    print_response("Test 14: Create Task With Invalid Status", response)

    # Test 15: Final statistics
    response = requests.get(f"{BASE_URL}/tasks/stats")
    print_response("Test 15: Final Statistics", response)

    print(f"\n{'='*60}")
    print("All tests completed!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
        print("Make sure the Flask server is running on http://localhost:5000")
        print("Run: python app.py")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
