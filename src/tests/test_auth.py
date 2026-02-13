async def test_register(client, db_session):
    """Регистрация нового пользователя"""
    response = await client.post("/api/v1/auth/register", data={
        "username": "new@example.com",
        "password": "new123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

async def test_login(client, test_user):
    """Логин существующего пользователя"""
    response = await client.post("/api/v1/auth/login", data={
        "username": "user@test.com",
        "password": "user123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

async def test_refresh(client, user_token_refresh):
    """Обновление access-токена"""
    response = await client.post("/api/v1/auth/refresh", json={
        "refresh_token": user_token_refresh
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

async def test_me(client, user_token_access):
    """Информация о текущем пользователе"""
    response = await client.get("/api/v1/users/me", headers={
        "Authorization": f"Bearer {user_token_access}"
        }  
    )
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert data["email"] == "user@test.com"