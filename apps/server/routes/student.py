from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from apps.server.database import (
    add_student,
    delete_student,
    retrieve_student,
    retrieve_students,
    update_student
)

from apps.server.models.student import (
    ErrorResponseModel,
    ResponseModel,
    StudentSchema,
    UpdateStudentModel
)

router = APIRouter()

@router.get("/", response_description="Students retrieved")
async def get_students():
    try:
        students = await retrieve_students()
        
        if students:
            return ResponseModel(students, "Students data retrieved successfully")
        return ResponseModel(students, "Empty list returned")
    except Exception:
        return ErrorResponseModel(Exception, 500, "Student data not returned")

@router.post("/", response_description="Student data added into the database")
async def add_student_data(student: StudentSchema = Body(...)):
    try:
        student = jsonable_encoder(student)
        new_student = await add_student(student)
        return ResponseModel(new_student, "Student added successfully")
    except Exception:
        return ErrorResponseModel(Exception, 500, "Student not added")

@router.get("/{id}", response_description="Student data retrieved")
async def get_student_data(id):
    try:
        student = await retrieve_student(id)
        
        if student:
            return ResponseModel(student, "Student data rettrieved successfully")
        return ResponseModel("An error ocurred", 404, "Student does not exist")
    except Exception:
        return ErrorResponseModel(Exception, 500, "Student data not returned")

@router.put("/{id}")
async def update_student_data(id: str, req: UpdateStudentModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    
    student = await retrieve_student(id)
    
    try:
        if student:
            updated_student = await update_student(id, req)
            return ResponseModel(
                "Student with ID: {} name update is successful".format(id),
                "Student name updated successfully",
                )
        return ResponseModel("An error occurred", 404, "There was an error updating the student data.",)

    except Exception:
        return ErrorResponseModel(Exception, 500, "Student not updated")

@router.delete("/{id}", response_description="Student data deleted from the database")
async def delete_student_data(id: str):
    try:
        student = await retrieve_student(id)
        if student:
            deleted_student = await delete_student(id)
            
            if deleted_student:
                return ResponseModel("Student with ID: {} removed".format(id), "Student deleted successfully")
            return ErrorResponseModel("An error occurred", 404, "Student with id {0} doesn't exist".format(id))
        return ResponseModel("An error ocurred", 404, "Student does not exist")
    except Exception:
        return ErrorResponseModel(Exception, 500, "Student not deleted")
    