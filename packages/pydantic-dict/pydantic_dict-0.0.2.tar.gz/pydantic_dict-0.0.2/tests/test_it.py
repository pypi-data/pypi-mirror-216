# from pydantic_dict import BaseModelDict


# class User(BaseModelDict):
#     id: int
#     name: str = "Jane Doe"


# def test_it():
#     user = User(id=42)

#     user["session_id"] = "95607c42-250a-4913-9dfb-00eb6535e685"
#     assert user.session_id == "95607c42-250a-4913-9dfb-00eb6535e685"
#     assert user["session_id"] == "95607c42-250a-4913-9dfb-00eb6535e685"
#     user.pop("session_id")
#     assert "session_id" not in user

#     assert user.get("last_name", None) is None

#     user.update({"email": "jane.doe@email.com"})
#     print(user.json())
#     # >>> {"id": 42, "name": "Jane Doe", "email": "jane.doe@email.com"}

#     user.clear()  # field's are NOT removed. only non-field's are removed
#     print(user.json())
#     # >>> {"id": 42, "name": "Jane Doe"}

#     user.setdefault("last_active", "2023-01-01T19:56:10Z")
#     del user["last_active"]

from pydantic_dict import BaseModelDict, Unset
from typing import Optional

class User(BaseModelDict):
    id: int
    name: str = "Jane Doe"
    email: Optional[str] = Unset

import pytest
def test_it_2():
    user = User(id=42)

    assert "email" not in user
    with pytest.raises(KeyError):
        user["email"] # raises KeyError

    assert len(user) == 2
    assert set(user.keys()) == {"id", "name"}

    user.setdefault("email", f"{user.id}@service.com") # returns `42@service.com`
    assert "email" in user

