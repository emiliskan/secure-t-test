import pytest


@pytest.mark.asyncio
async def test_create_post(auth_header, make_post_request):
    data = {
        "text": "Post text.",
    }
    response = await make_post_request("posts", data=data, headers=auth_header)

    assert response.status == 200


@pytest.mark.asyncio
async def test_update_post(auth_header, make_post_request, make_patch_request):

    data = {
        "text": "Post text.",
    }
    response = await make_post_request("posts", data=data, headers=auth_header)
    post_id = response.body["id"]

    data = {
        "text": "New post text.",
    }

    response = await make_patch_request(f"posts/{post_id}", data=data, headers=auth_header)

    assert response.status == 200


@pytest.mark.asyncio
async def test_get_posts(auth_header, make_get_request):
    data = {
        "offset": 0,
        "limit": 10,
    }

    response = await make_get_request("posts", data=data, headers=auth_header)

    assert response.status == 200


@pytest.mark.asyncio
async def test_delete_posts(auth_header, make_post_request, make_delete_request):

    data = {
        "text": "Post text.",
    }
    response = await make_post_request("posts", data=data, headers=auth_header)
    post_id = response.body["id"]

    response = await make_delete_request(f"posts/{post_id}")

    assert response.status == 200
