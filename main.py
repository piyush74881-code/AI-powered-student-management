from fastapi import FastAPI,HTTPException
from typing import List,Optional
from models import Student,Feedback
from database import students
from nlp_utils import analyze_sentiment,smart_search

app=FastAPI(
    title="AI powered student Restfull api",
    version="1.0.0"
)
@app.get('/')
def home():
    return {
        "message":"api is running successfully"
    }

@app.post('/students',response_model=Student)
def create_student(student:Student): #student =request body(JSON)
    students.append(student)
    return student

@app.get('/students',response_model=List[Student])
def get_students():
    return students

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):

    if student_id < 0 or student_id >= len(students):
        raise HTTPException(status_code=404, detail="Student not found")

    return students[student_id]

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_student: Student):

    if student_id < 0 or student_id >= len(students):
        raise HTTPException(status_code=404, detail="Student not found")

    students[student_id] = updated_student
    return updated_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    if student_id < 0 or student_id >= len(students):
        raise HTTPException(status_code=404, detail="Student not found")

    deleted_student = students.pop(student_id)

    return {
        "message": "Student deleted successfully",
        "data": deleted_student
    }


@app.post("/analyze-feedback")
def analyze_feedback(feedback: Feedback):
    result = analyze_sentiment(feedback.text)
    return {
        "text": feedback.text,
        "analysis": result
    }

#smart search

@app.get("/search")
def search_students(query: str):
    results = smart_search(students, query)

    if not results:
        raise HTTPException(status_code=404, detail="No matching students found")

    return {"count": len(results), "students": results}