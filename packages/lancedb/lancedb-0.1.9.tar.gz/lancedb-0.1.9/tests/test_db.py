#  Copyright 2023 LanceDB Developers
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pandas as pd
import pytest

import lancedb


def test_basic(tmp_path):
    db = lancedb.connect(tmp_path)

    assert db.uri == str(tmp_path)
    assert db.table_names() == []

    table = db.create_table(
        "test",
        data=[
            {"vector": [3.1, 4.1], "item": "foo", "price": 10.0},
            {"vector": [5.9, 26.5], "item": "bar", "price": 20.0},
        ],
    )
    rs = table.search([100, 100]).limit(1).to_df()
    assert len(rs) == 1
    assert rs["item"].iloc[0] == "bar"

    rs = table.search([100, 100]).where("price < 15").limit(2).to_df()
    assert len(rs) == 1
    assert rs["item"].iloc[0] == "foo"

    assert db.table_names() == ["test"]
    assert "test" in db
    assert len(db) == 1

    assert db.open_table("test").name == db["test"].name


def test_ingest_pd(tmp_path):
    db = lancedb.connect(tmp_path)

    assert db.uri == str(tmp_path)
    assert db.table_names() == []

    data = pd.DataFrame(
        {
            "vector": [[3.1, 4.1], [5.9, 26.5]],
            "item": ["foo", "bar"],
            "price": [10.0, 20.0],
        }
    )
    table = db.create_table("test", data=data)
    rs = table.search([100, 100]).limit(1).to_df()
    assert len(rs) == 1
    assert rs["item"].iloc[0] == "bar"

    rs = table.search([100, 100]).where("price < 15").limit(2).to_df()
    assert len(rs) == 1
    assert rs["item"].iloc[0] == "foo"

    assert db.table_names() == ["test"]
    assert "test" in db
    assert len(db) == 1

    assert db.open_table("test").name == db["test"].name


def test_create_mode(tmp_path):
    db = lancedb.connect(tmp_path)
    data = pd.DataFrame(
        {
            "vector": [[3.1, 4.1], [5.9, 26.5]],
            "item": ["foo", "bar"],
            "price": [10.0, 20.0],
        }
    )
    db.create_table("test", data=data)

    with pytest.raises(Exception):
        db.create_table("test", data=data)

    new_data = pd.DataFrame(
        {
            "vector": [[3.1, 4.1], [5.9, 26.5]],
            "item": ["fizz", "buzz"],
            "price": [10.0, 20.0],
        }
    )
    tbl = db.create_table("test", data=new_data, mode="overwrite")
    assert tbl.to_pandas().item.tolist() == ["fizz", "buzz"]


def test_delete_table(tmp_path):
    db = lancedb.connect(tmp_path)
    data = pd.DataFrame(
        {
            "vector": [[3.1, 4.1], [5.9, 26.5]],
            "item": ["foo", "bar"],
            "price": [10.0, 20.0],
        }
    )
    db.create_table("test", data=data)

    with pytest.raises(Exception):
        db.create_table("test", data=data)

    assert db.table_names() == ["test"]

    db.drop_table("test")
    assert db.table_names() == []

    db.create_table("test", data=data)
    assert db.table_names() == ["test"]
