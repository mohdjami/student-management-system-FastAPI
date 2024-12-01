from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class Address(BaseModel):
    city: str
    country: str

class StudentCreate(BaseModel):
    name: str
    age: int
    address: Address

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[Address] = None

class StudentResponse(BaseModel):
    name: str
    age: int
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class StudentDetailResponse(StudentResponse):
    address: Address
    pass

class StudentIdResponse(BaseModel):
    id: str

class StudentListResponse(BaseModel):
    data: List[StudentResponse]

class StudentQueryParams:
    def __init__(self, country: Optional[str] = None, age: Optional[int] = None):
        self.country = country
        self.age = age

    def get_query_filter(self) -> Dict[str, Any]:
        query_filter = {}
        
        if self.country:
            query_filter['address.country'] = self.country
        
        if self.age is not None:
            query_filter['age'] = {'$gte': self.age}
        
        return query_filter
