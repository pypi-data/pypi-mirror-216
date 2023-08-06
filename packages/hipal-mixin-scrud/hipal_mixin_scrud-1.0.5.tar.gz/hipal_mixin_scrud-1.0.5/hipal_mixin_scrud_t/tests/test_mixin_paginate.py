# lib
import json

# unittest
from unittest.mock import MagicMock
from unittest.mock import patch
import unittest

# fast api
from fastapi.testclient import TestClient
from fastapi import FastAPI

# sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# app
from tests.factory_test.person import PersonFactory
from tests.factory_test.person import PersonSchema
from tests.factory_test.person import PersonModel
from crud.mixin_list import ListModelMixin
from unittest.mock import MagicMock
from mixin import MixinCrud


class TestMixin(unittest.TestCase):
    
    def factory_list_to_dict(self, list_to_dict: list):
        return [{k:v for k ,v in item.__dict__.items() if k != '_sa_instance_state'} for item in list_to_dict]

    def factory_obj_to_dict(self, obj: object):
        return {k:v for k ,v in obj.__dict__.items() if k != '_sa_instance_state'}

    @patch('crud.mixin_list.ListModelMixin.paginate')
    def test_success_paginate(self, mocker):
        
        mock_db_session = Session()
        
        persons: list[PersonFactory] = PersonFactory.create_batch(10)
        
        obj =  {
            "pagination":{
                "offset": 0,
                "limit": 10,
                "total": 10,
                "total_pages": 1,
                "links": {
                    "first":'localhost',
                    "prev": 'localhost',
                    "next": 'localhost',
                    "last": 'localhost',
                },
            },
            "data": self.factory_list_to_dict(persons)
        }        
        
        mocker.return_value = obj

        list_model_mixin = ListModelMixin()
        result = list_model_mixin.paginate(
            db_session=mock_db_session,
            model=PersonModel,
            squema=PersonSchema,
            path='localhost',
        )

        assert result == obj

    def session(self):
        engine = create_engine(
            'postgresql://user:pass@db:5432/db',
        )
        Session = sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=False
        )
        
        db_session = Session()
        
        return db_session


    def mock_refresh(self, model):
        person_refresh: PersonFactory = PersonFactory.create(id=2)
        model.name_1 = person_refresh.name_1
        model.name_2 = person_refresh.name_2
        model.last_name_1 = person_refresh.last_name_1
        model.last_name_2 = person_refresh.last_name_2
        model.rh = person_refresh.rh


    def test_routes(self):
        
        mock_session = MagicMock()
        mock_session = self.session().create_session = MagicMock(return_value=mock_session)
        
        mock_model = MagicMock(spec=PersonModel)
        persons: list[PersonFactory] = PersonFactory.create_batch(10)
        person1: PersonFactory = PersonFactory.create(id=1)
        person2: PersonFactory = PersonFactory.create(id=2)
        
        mock_session.query.return_value.order_by.return_value.limit.return_value.offset.return_value.all.return_value = persons
        mock_session.query.return_value.filter.return_value.first.return_value = person1
        mock_session.refresh = self.mock_refresh

        url = 'api/v1/items'

        mixin_route = MixinCrud(
            schema=PersonSchema,
            db_session=mock_session,
            model=mock_model,
            prefix=url,
        )
        
        app = FastAPI(title='items')
        app.include_router(mixin_route)

        client = TestClient(app)

        item_url = f"{url}/1"

        actions = [
            ('get', url, {}),
            ('get', item_url, {}),
            ('post', url, self.factory_obj_to_dict(person2)),
            ('put', item_url, self.factory_obj_to_dict(person2)),
            ('delete', item_url, {}),
        ]
        
        success_codes = []

        for method, url, data in actions:

            request = client.request(
                method,
                url, 
                headers = {'Content-Type': 'application/json'},
                data=json.dumps(data)
            )
            status_code = request.status_code
            assert 200 <= status_code <= 226
            success_codes.append(status_code)
    
        assert len(success_codes) == len(actions)
