import pytest


@pytest.mark.asyncio
async def test_create_comment(make_post_request):
    # add post
    data = {
        "text": "Post text.",
    }
    response = await make_post_request("posts", data=data)
    post_id = response.body["id"]
    # add comment to post
    data = {
        "post": post_id,
        "text": "fckn first one"
    }
    response = await make_post_request("posts/comments/", data=data)

    assert response.status == 200

    # add comment to post
    created_comment_id = response.body["id"]
    data = {
        "post": post_id,
        "comment": created_comment_id,
        "text": "child of first one"
    }
    response = await make_post_request("posts/comments/", data=data)

    assert response.status == 200


@pytest.mark.asyncio
async def test_update_comment(make_post_request, make_patch_request):
    # add post
    data = {
        "text": "Post text.",
    }
    response = await make_post_request("posts", data=data)
    post_id = response.body["id"]

    # add comment to post
    data = {
        "post": post_id,
        "text": "fckn first one"
    }
    response = await make_post_request("posts/comments/", data=data)
    comment_id = response.body["id"]

    # update comment
    data = {
        "post": post_id,
        "comment": comment_id,
        "text": "child of first one"
    }

    response = await make_patch_request(f"posts/comments/{comment_id}", data=data)

    assert response.status == 200


@pytest.mark.asyncio
async def test_get_comments(make_get_request, make_post_request):
    # add post
    data = {
        "text": "Post text.",
    }
    response = await make_post_request("posts", data=data)
    post_id = response.body["id"]

    # add comment to post
    data = {
        "post": post_id,
        "text": "fckn first one"
    }

    data = {
        "offset": 0,
        "limit": 10,
    }

    response = await make_get_request(f"posts/{post_id}/comments/", data=data)

    assert response.status == 200


@pytest.mark.asyncio
async def test_delete_comment(make_post_request, make_delete_request):
    # add post
    data = {
        "text": "Post text.",
    }
    response = await make_post_request("posts", data=data)
    post_id = response.body["id"]

    # add comment to post
    data = {
        "post": post_id,
        "text": "fckn first one"
    }
    response = await make_post_request("posts/comments/", data=data)
    comment_id = response.body["id"]

    response = await make_delete_request(f"posts/comments/{comment_id}")

    assert response.status == 200
