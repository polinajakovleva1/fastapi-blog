async def test_public_posts(client, test_post):
    """Список постов"""
    response = await client.get("/api/v1/posts")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "title" in data[0]
        assert "slug" in data[0]
        assert "content" in data[0]
        assert "author" in data[0]
        assert "category" in data[0]

async def test_public_post(client, test_post):
    """Пост по конкретному slug"""
    response = await client.get(f"/api/v1/posts/{test_post.slug}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_post.title
    assert data["slug"] == test_post.slug
    assert data["content"] == test_post.content
    assert data["author"]["email"] == "user@test.com"
    assert data["category"]["name"] == "Тестовая категория"

async def test_public_categories(client, test_category):
    """Список категорий"""
    response = await client.get("/api/v1/categories")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "name" in data[0]
        assert "slug" in data[0]

async def test_public_posts_from_category(client, test_category, test_post):
    """Список постов в конкретной категории"""
    response = await client.get(f"/api/v1/categories/{test_category.slug}/posts")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert data[0]["category"]["slug"] == test_category.slug
        assert data[0]["title"] == test_post.title