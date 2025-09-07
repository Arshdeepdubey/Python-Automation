import pytest
import requests
import allure
from jsonpath_ng import jsonpath, parse

@allure.feature('API Tests')
class TestAPI:
    
    @allure.story('Get User Data')
    def test_get_user(self):
        """Test to verify user retrieval from a sample API"""
        response = requests.get('https://jsonplaceholder.typicode.com/users/1')
        assert response.status_code == 200
        
        # Extract and verify user data
        user_data = response.json()
        assert user_data['name'] is not None
        assert user_data['email'] is not None
        
        # Use JSONPath to verify nested data
        company_name_expr = parse('$.company.name')
        company_name = company_name_expr.find(user_data)[0].value
        assert company_name is not None
        
    @allure.story('Create User')
    def test_create_user(self):
        """Test to verify user creation"""
        payload = {
            'name': 'Test User',
            'email': 'test@example.com',
            'username': 'testuser'
        }
        
        response = requests.post('https://jsonplaceholder.typicode.com/users', json=payload)
        assert response.status_code == 201
        
        created_user = response.json()
        assert created_user['name'] == payload['name']
        assert created_user['email'] == payload['email']
