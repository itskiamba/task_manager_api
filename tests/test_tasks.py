from tests.conftest import make_user


def test_task_crud(client, auth):
    r = client.post("/api/v1/tasks", json={"title": "Learn FastAPI"}, headers=auth)
    assert r.status_code == 201
    task = r.json()
    assert task["status"] == "todo"

    r = client.patch(f"/api/v1/tasks/{task['id']}", json={"status": "done"}, headers=auth)
    assert r.status_code == 200
    assert r.json()["status"] == "done"
    assert r.json()["title"] == "Learn FastAPI"  # untouched fields stay the same

    assert client.get(f"/api/v1/tasks/{task['id']}", headers=auth).status_code == 200
    assert client.delete(f"/api/v1/tasks/{task['id']}", headers=auth).status_code == 204
    assert client.get(f"/api/v1/tasks/{task['id']}", headers=auth).status_code == 404


def test_list_filter_and_pagination(client, auth):
    for i in range(3):
        client.post("/api/v1/tasks", json={"title": f"t{i}"}, headers=auth)
    client.post("/api/v1/tasks", json={"title": "done one", "status": "done"}, headers=auth)

    assert len(client.get("/api/v1/tasks", headers=auth).json()) == 4
    assert len(client.get("/api/v1/tasks?status=done", headers=auth).json()) == 1
    assert len(client.get("/api/v1/tasks?limit=2", headers=auth).json()) == 2


def test_users_cannot_see_each_others_tasks(client, auth):
    task = client.post("/api/v1/tasks", json={"title": "secret"}, headers=auth).json()

    other = make_user(client, email="eve@example.com")

    assert client.get(f"/api/v1/tasks/{task['id']}", headers=other).status_code == 404
    assert client.get("/api/v1/tasks", headers=other).json() == []


def test_cannot_update_or_delete_someone_elses_task(client, auth):
    task = client.post("/api/v1/tasks", json={"title": "mine"}, headers=auth).json()
    other = make_user(client, email="eve@example.com")
    url = f"/api/v1/tasks/{task['id']}"

    assert client.patch(url, json={"title": "hacked"}, headers=other).status_code == 404
    assert client.delete(url, headers=other).status_code == 404
    assert client.get(url, headers=auth).json()["title"] == "mine"  # unchanged


def test_tasks_require_login(client):
    assert client.get("/api/v1/tasks").status_code == 401


def test_empty_title_rejected(client, auth):
    r = client.post("/api/v1/tasks", json={"title": ""}, headers=auth)
    assert r.status_code == 422


def test_patch_with_null_title_rejected(client, auth):
    task = client.post("/api/v1/tasks", json={"title": "keep me"}, headers=auth).json()
    r = client.patch(f"/api/v1/tasks/{task['id']}", json={"title": None}, headers=auth)
    assert r.status_code == 422