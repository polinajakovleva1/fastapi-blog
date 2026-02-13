async def test_admin_get_users(client, admin_headers, test_user, admin_user):
    """Admin видит всех пользователей"""
    response = await client.get("/api/v1/admin/users", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    emails = [u["email"] for u in data]
    assert "user@test.com" in emails
    assert "admin@test.com" in emails

async def test_user_cannot_get_users(client, auth_headers, test_user, admin_user):
    """User не видит всех пользователей"""
    response = await client.get("/api/v1/admin/users", headers=auth_headers)
    assert response.status_code == 403

async def test_admin_change_role(client, admin_headers, test_user):
    """Admin может сменить роль"""
    response = await client.patch(f"/api/v1/admin/users/{test_user.id}/role", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["role"] == "ADMIN"

    response = await client.patch(f"/api/v1/admin/users/{test_user.id}/role", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["role"] == "USER"

async def test_user_cannot_change_role(client, auth_headers, test_user):
    """User не может менять роли"""
    response = await client.patch(f"/api/v1/admin/users/{test_user.id}/role", headers=auth_headers)
    assert response.status_code == 403

async def test_admin_create_category(client, admin_headers):
    """Admin может создать категорию"""
    response = await client.post("/api/v1/admin/categories", 
                                 json={"name": "Новая категория"},
                                 headers=admin_headers
                                )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Новая категория"
    assert "slug" in data

async def test_user_cannot_create_category(client, auth_headers):
    """User не может создать категорию"""
    response = await client.post("/api/v1/admin/categories", json={"name": "Хакнутая категория"}, 
                                 headers=auth_headers
                                )
    assert response.status_code == 403

async def test_admin_update_category(client, admin_headers, test_category):
    """Admin может обновить категорию"""
    response = await client.patch(f"/api/v1/admin/categories/{test_category.id}", 
                                  json={"name": "Обновленная категория"}, 
                                  headers=admin_headers
                                  )
    assert response.status_code == 200
    assert response.json()["name"] == "Обновленная категория"

async def test_user_cannot_update_category(client, auth_headers, test_category):
    """User не может обновить категорию"""
    response = await client.patch(f"/api/v1/admin/categories/{test_category.id}", 
                                  json={"name": "Обновленная категория"}, 
                                  headers=auth_headers
                                  )
    assert response.status_code == 403

async def test_admin_delete_category(client, admin_headers, test_category):
    """Admin может удалить категорию"""
    response = await client.delete(f"/api/v1/admin/categories/{test_category.id}", 
                                   headers=admin_headers
                                   )
    assert response.status_code == 200

    get_response = await client.get(f"/api/v1/admin/categories/{test_category.id}", 
                                    headers=admin_headers
                                    )
    assert get_response.status_code == 404

async def test_user_cannot_delete_category(client, auth_headers, test_category):
    """User не может удалить категорию"""
    response = await client.delete(f"/api/v1/admin/categories/{test_category.id}", 
                                   headers=auth_headers
                                   )
    assert response.status_code == 403

async def test_admin_create_post(client, admin_headers, test_category, test_user):
    """Admin может создать пост"""
    response = await client.post("/api/v1/admin/posts", 
                                 json={
                                     "title": "Новый пост",
                                     "content": "Содержание",
                                     "content_html": "<p>Содержание</p>",
                                     "category_id": test_category.id,
                                     "author_id": test_user.id
                                 },
                                 headers=admin_headers
                                )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Новый пост"
    assert "slug" in data
    assert data["category_id"] == test_category.id
    assert data["author_id"] == test_user.id

async def test_user_cannot_create_post(client, auth_headers, test_category, test_user):
    """User не может создать пост"""
    response = await client.post("/api/v1/admin/posts", 
                                 json={
                                     "title": "Новый пост",
                                     "content": "Содержание",
                                     "content_html": "<p>Содержание</p>",
                                     "category_id": test_category.id,
                                     "author_id": test_user.id
                                 },
                                 headers=auth_headers
                                )
    assert response.status_code == 403

async def test_admin_update_post(client, admin_headers, test_post):
    """Admin может обновить пост"""
    response = await client.patch(f"/api/v1/admin/posts/{test_post.id}", 
                                  json={"title": "Обновленный пост"},
                                  headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Обновленный пост"

async def test_user_cannot_update_post(client, auth_headers, test_post):
    """User не может обновить пост"""
    response = await client.patch(f"/api/v1/admin/posts/{test_post.id}",
                                  json={"title": "Обновленный пост"},
                                  headers=auth_headers)
    assert response.status_code == 403

async def test_admin_delete_post(client, admin_headers, test_post):
    """Admin может удалить пост"""
    response = await client.delete(f"/api/v1/admin/posts/{test_post.id}",
                                   headers=admin_headers)
    assert response.status_code == 200
    
    get_response = await client.get(f"/api/v1/admin/posts/{test_post.id}",
                                    headers=admin_headers)
    assert get_response.status_code == 404

async def test_user_cannot_create_post(client, auth_headers, test_category, test_user):
    """User не может создать пост"""
    response = await client.post("/api/v1/admin/posts",
                                 json={
                                     "title": "Хакнутый пост",
                                     "content": "Хак",
                                     "category_id": test_category.id,
                                     "author_id": test_user.id
                                 },
                                 headers=auth_headers)
    assert response.status_code == 403