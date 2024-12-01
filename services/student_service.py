from bson import ObjectId
from models import StudentCreate, StudentUpdate
from db import DatabaseConnection 

class StudentService:
    @staticmethod
    async def create_student(student: StudentCreate):
        student_dict = student.model_dump()
        db = DatabaseConnection.db
        result = await db.students.insert_one(student_dict)
        return str(result.inserted_id)

    @staticmethod
    async def get_students(country: str = None, age: int = None):
        query_filter = {}
        if country:
            query_filter["address.country"] = country
        if age:
            query_filter["age"] = {"$gte": age}

        db = DatabaseConnection.db
        students_cursor = db.students.find(query_filter)
        students_list = await students_cursor.to_list(length=1000)
        return students_list

    @staticmethod
    async def get_student_by_id(student_id: str):
        try:
            object_id = ObjectId(student_id)
        except Exception:
            raise ValueError("Invalid student ID format")
        
        db = DatabaseConnection.db
        student = await db.students.find_one({"_id": object_id})
        if not student:
            return None
        return student

    @staticmethod
    async def update_student(student_id: str, update_data: StudentUpdate):
        try:
            object_id = ObjectId(student_id)
        except Exception:
            raise ValueError("Invalid student ID format")
        
        update_dict = {k: v for k, v in update_data.model_dump(exclude_unset=True).items()}
        if not update_dict:
            return False

        db = DatabaseConnection.db
        result = await db.students.update_one({"_id": object_id}, {"$set": update_dict})
        return result.modified_count > 0

    @staticmethod
    async def delete_student(student_id: str):
        try:
            object_id = ObjectId(student_id)
        except Exception:
            raise ValueError("Invalid student ID format")
        
        db = DatabaseConnection.db
        result = await db.students.delete_one({"_id": object_id})
        return result.deleted_count > 0
