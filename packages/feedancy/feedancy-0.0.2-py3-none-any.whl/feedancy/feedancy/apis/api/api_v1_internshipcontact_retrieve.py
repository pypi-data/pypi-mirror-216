from __future__ import annotations

import datetime
import pydantic
import typing

from pydantic import BaseModel

from feedancy.lib.base import BaseApi
from feedancy.lib.request import ApiRequest
from feedancy.lib import json
class InternshipContact(BaseModel):
    contact: int 
    id: int 
    internship: int 

def make_request(self: BaseApi,


) -> InternshipContact:
    

    
    body = None
    

    m = ApiRequest(
        method="GET",
        path="/api/v1/internshipcontact/".format(
            
        ),
        content_type=None,
        body=body,
        headers=self._only_provided({
        }),
        query_params=self._only_provided({
        }),
        cookies=self._only_provided({
        }),
    )
    return self.make_request({
    
        "200": {
            
                "application/json": InternshipContact,
            
        },
    
    }, m)