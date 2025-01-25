# Test user registration
POST http://localhost:8000/api/v1/auth/register
{
    "email": "test@example.com",
    "password": "Test@123456"
}
HTTP 201
[Asserts]
header "Content-Type" == "application/json"
jsonpath "$.email" == "test@example.com"
jsonpath "$.is_active" == true
jsonpath "$.id" matches /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/

# Test duplicate email registration (should fail)
POST http://localhost:8000/api/v1/auth/register
{
    "email": "test@example.com",
    "password": "Test@123456"
}
HTTP 400
[Asserts]
jsonpath "$.detail" == "User with this email already exists"

# Test login with correct credentials
POST http://localhost:8000/api/v1/auth/login
[FormParams]
username: test@example.com
password: Test@123456
HTTP 200
[Asserts]
header "Content-Type" == "application/json"
jsonpath "$.access_token" exists
jsonpath "$.token_type" == "bearer"
jsonpath "$.expires_in" exists
[Captures]
access_token: jsonpath "$.access_token"

# Test login with incorrect password
POST http://localhost:8000/api/v1/auth/login
[FormParams]
username: test@example.com
password: wrongpassword
HTTP 401
[Asserts]
jsonpath "$.detail" == "Invalid credentials"

# Test change password
POST http://localhost:8000/api/v1/auth/change-password
Authorization: Bearer {% raw %}{{access_token}}{% endraw %}
{
    "current_password": "Test@123456",
    "new_password": "NewTest@123456"
}
HTTP 204

# Test login with new password
POST http://localhost:8000/api/v1/auth/login
[FormParams]
username: test@example.com
password: NewTest@123456
HTTP 200
[Asserts]
jsonpath "$.access_token" exists

# Test change password with incorrect current password
POST http://localhost:8000/api/v1/auth/change-password
Authorization: Bearer {% raw %}{{access_token}}{% endraw %}
{
    "current_password": "wrongpassword",
    "new_password": "NewTest@123456"
}
HTTP 400
[Asserts]
jsonpath "$.detail" == "Current password is incorrect"

# Test change password without authentication
POST http://localhost:8000/api/v1/auth/change-password
{
    "current_password": "Test@123456",
    "new_password": "NewTest@123456"
}
HTTP 401
[Asserts]
jsonpath "$.detail" == "Not authenticated"
