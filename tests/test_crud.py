from app import crud, database, models


def test_to_base36():
    assert crud.to_base36(0) == "0"
    assert crud.to_base36(35) == "Z"
    assert crud.to_base36(36) == "10"
    assert crud.to_base36(123456) != ""


def test_create_and_visit_counts():
    original = "https://example.com/test"
    url = crud.create_short_url(original)
    assert url is not None
    assert url.original_url == original
    assert url.short_code is not None

    code = url.short_code
    assert crud.get_visit_count(code) == 0
    crud.increment_visit_count(code)
    assert crud.get_visit_count(code) == 1

    fetched = crud.get_url_by_code(code)
    assert fetched is not None
    assert fetched.original_url == original


def test_generate_keys_updates_counter():
    with database.SessionLocal() as db:
        ctr = db.query(models.Counter).filter(models.Counter.id == 1).first()
        before = ctr.value

    res = crud.generate_keys()
    assert res["generated"] == 1000
    assert res["start"] == before
    assert res["end"] == before + 1000

    with database.SessionLocal() as db:
        count = db.query(models.Key).count()
        assert count >= 1000
