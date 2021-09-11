import pytest


@pytest.mark.asyncio
async def test_get_posts(make_get_request):
    response = make_get_request("posts")

    assert response.status == 200
