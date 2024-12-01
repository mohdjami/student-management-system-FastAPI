from fastapi import FastAPI, Query, HTTPException, Path
from fastapi.responses import JSONResponse

from models import (
    StudentCreate, 
    StudentUpdate,
    StudentResponse, 
    StudentDetailResponse,
    StudentListResponse, 
    StudentIdResponse
)
from db import DatabaseConnection
from services.student_service import StudentService

app = FastAPI(
    title="Student Management System",
    description="API for managing student records",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    await DatabaseConnection.connect_mongodb()

@app.on_event("shutdown")
async def shutdown_event():
    await DatabaseConnection.close_mongodb()

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Student Management System API"}

@app.post("/students", response_model=StudentIdResponse, status_code=201, tags=["Students"])
async def create_student(student: StudentCreate):
    student_id = await StudentService.create_student(student)
    return StudentIdResponse(id=student_id)

@app.get("/students", response_model=StudentListResponse, tags=["Students"])
async def list_students(country: str = Query(None), age: int = Query(None)):
    students = await StudentService.get_students(country, age)
    students_response = [StudentResponse(name=student['name'], age=student['age']) for student in students]
    return StudentListResponse(data=students_response)

@app.get("/students/{student_id}", response_model=StudentDetailResponse, tags=["Students"])
async def get_student(student_id: str = Path(...)):
    try:
        student = await StudentService.get_student_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return StudentDetailResponse(
        name=student['name'],
        age=student['age'],
        address=student['address']
    )

@app.patch("/students/{student_id}", status_code=204, tags=["Students"])
async def update_student(student_data: StudentUpdate, student_id: str = Path(...)):
    try:
        updated = await StudentService.update_student(student_id, student_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Student not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return None

@app.delete("/students/{student_id}", status_code=200, tags=["Students"])
async def delete_student(student_id: str = Path(...)):
    try:
        deleted = await StudentService.delete_student(student_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Student not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {}


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )
