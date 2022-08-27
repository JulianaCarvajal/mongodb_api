import motor.motor_asyncio

from bson.objectid import ObjectId
from decouple import config

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.students

student_collection = database.get_collection("students_collection")

# Helper student function

def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "gpa": student["gpa"],
    }

# CRUD

# Recuperar todos los estudiantes de la db
# get => "/students"
async def retrieve_students():
    students = []
    async for student in student_collection.find():
        student.append(student_helper(student))
    return students

# Agregar un nuevo estudiante a la db
# post => "/students"
async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({'_id': student.insert_id})
    return student_helper(new_student)

# Recuperar un estudiante con un id especifico
# get => "/students/{id}"
async def retrieve_student(id: str) -> dict:
    student = await student_collection.find_one({'_id': ObjectId(id)})
    if student:
        return student_helper(student)

# Actualizar un estudiante con un id especifico
# put => "/students/{id}"
async def update_student(id: str, data: dict) -> dict:
    if len(data) < 1:
        return False
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        updated_student = await student_collection.update_one(
            {"_id": ObjectId(id)}, {'$Set': data}
        )
        if update_student:
            return True
        return False

# Eliminar un estudiante con un id especifico
# delete => "/students/{id}"
async def delete_student(id: str) -> dict:
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({'_id': ObjectId(id)})
        return True
