# REST API Design Guidelines

Designing an effective REST API requires adherence to a set of principles that promote consistency, scalability, and usability. The following guidelines outline industry best practices for designing high-quality REST APIs.

---

## 1. Use Appropriate HTTP Methods

Each operation should use the correct HTTP method to indicate its purpose:

| HTTP Method | Purpose                          |
|-------------|----------------------------------|
| `GET`       | Retrieve a resource or collection|
| `POST`      | Create a new resource            |
| `PUT`       | Replace an existing resource     |
| `PATCH`     | Partially update a resource      |
| `DELETE`    | Remove a resource                |

---

## 2. Use Nouns for Endpoints, Not Verbs

Endpoints should represent resources (nouns), while the HTTP methods define the actions. This improves readability and aligns with REST principles.

**Examples:**

- Preferred: `/users`, `/orders/123`
- Avoid: `/getUsers`, `/createUser`

---

## 3. Use Plural Nouns for Resource Names

Maintain consistency by using plural form for all resources.

**Examples:**

- Correct: `/products`, `/orders`
- Incorrect: `/product`, `/order`

---

## 4. API Versioning

APIs should be versioned to avoid breaking existing clients when introducing changes.

**Recommended Format:**

```
/api/v1/users
```

---

## 5. Use Proper HTTP Status Codes

Use standard HTTP status codes to indicate the result of the API operations.

| Status Code | Description                    |
|-------------|--------------------------------|
| 200         | OK                             |
| 201         | Created                        |
| 204         | No Content                     |
| 400         | Bad Request                    |
| 401         | Unauthorized                   |
| 404         | Not Found                      |
| 500         | Internal Server Error          |

---

## 6. Use JSON for Request and Response Bodies

JSON is the most widely adopted format for REST APIs due to its simplicity and compatibility.

**Example:**

```json
{
  "username": "john_doe",
  "email": "john@example.com"
}
```

---

## 7. Implement Filtering, Sorting, and Pagination

Support common query parameters to enhance usability and performance for large datasets.

**Example:**

```
GET /products?category=electronics&sort=price&order=asc&page=2&limit=10
```

---

## 8. Avoid Exposing Sensitive Data in URLs

Sensitive data such as passwords or tokens should not be passed in the URL, as they may be logged or cached. Use the request body instead.

**Incorrect:**

```
GET /login?username=user&password=pass
```

**Correct:**

```
POST /login
{
  "username": "user",
  "password": "pass"
}
```

---

## 9. Handle Errors Gracefully

Return structured and meaningful error responses to assist in client-side debugging.

**Example:**

```json
{
  "status": 404,
  "error": "User not found"
}
```

---

## 10. Design Clean and Intuitive URLs

Keep URLs simple and descriptive. Avoid deeply nested resource paths.

**Examples:**

- Preferred: `/users/123`
- Avoid: `/users/123/orders/456/items/789`

---

![](https://i.imgur.com/xaqv0cP.png)

## Additional Recommendations

- Use lowercase letters in URLs.
- Avoid using file extensions (e.g., `.json`, `.xml`) in URLs.
- Include descriptive response messages along with status codes.
- Use consistent naming conventions across all endpoints.
- Provide OpenAPI (Swagger) documentation for clarity and testing.

---

These practices help in building APIs that are easy to understand, consume, and maintain. Following them ensures better developer experience and seamless integration across systems.