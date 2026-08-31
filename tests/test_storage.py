import os
import pytest
from storage.json_storage import JSONStorage

def test_json_storage_crud(tmp_path):
    file_path = os.path.join(tmp_path, "test_data.json")
    storage = JSONStorage(file_path)

    # Read empty
    assert storage.read_all() == []

    # Append
    item1 = {'id': '1', 'name': 'Item 1'}
    storage.append_one(item1)
    assert len(storage.read_all()) == 1

    # Update
    storage.update_one('1', {'name': 'Updated Item 1'})
    updated = storage.read_all()[0]
    assert updated['name'] == 'Updated Item 1'

    # Delete
    deleted = storage.delete_one('1')
    assert deleted is True
    assert len(storage.read_all()) == 0
