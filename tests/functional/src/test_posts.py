import pytest


@pytest.mark.asyncio
async def test_create_post(make_post_request):
    data = {
        "id": 1,
        "text": "Post text.",
    }
    response = await make_post_request("posts", data=data)

    assert response.status == 200


@pytest.mark.asyncio
async def test_update_post(make_patch_request):

    post_id = 1

    data = {
        "id": 1,
        "text": "New post text.",
    }

    response = await make_patch_request(f"posts/{post_id}", data=data)

    assert response.status == 200


@pytest.mark.asyncio
async def test_get_posts(make_get_request):
    data = {
        "offset": 0,
        "limit": 10,
    }

    response = await make_get_request("posts", data=data)

    assert response.status == 200


@pytest.mark.asyncio
async def test_delete_posts(make_delete_request):

    post_id = 1

    response = await make_delete_request(f"posts/{post_id}")

    assert response.status == 200