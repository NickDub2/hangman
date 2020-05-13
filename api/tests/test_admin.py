"""Simple admin rendering tests"""


def test_account_admin(admin_client):
    response = admin_client.get("/admin/api/account/")
    assert response.status_code == 200
