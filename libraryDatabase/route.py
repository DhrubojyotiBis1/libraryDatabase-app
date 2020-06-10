from flask import request
from libraryDatabase import db, app
from libraryDatabase.models import Student, Book

'''
Argument list:

Post request:
stdName -> student
admNumber -> admission number
book -> Name of the book
author -> author of the book


HTTP STATUS CODE
400 -> bad request 
404 -> data not found
405 -> method not allowed

'''

def getStatusResponseFrom(status):
    STATUS = 'status'
    return {STATUS: status}

def addEntryToDatabase(student):
    db.session.add(student)
    db.session.commit()

def DeleteEntryFromDatabase(entry):
    db.session.delete(entry)
    db.session.commit()


@app.route('/', methods=['POST', 'GET', 'PUT'])
def Home():
    if request.method == 'POST':
        return TakeBook()
    elif request.method == 'GET':
        return SeeBook()
    elif request.method == 'PUT':
        return SumbitBook()
    return getStatusResponseFrom(405)


@app.route('/database')
def GetAll():
    students = Student.query.all()
    if students:
        database = []
        for student in students:
            studentDict = {'name': student.name, 'admNumber': student.admissionNumber}
            books = student.books
            listOfBooksBorrowed = []
            for book in books:
                bookDict = {'name': book.name,'author': book.author}
                listOfBooksBorrowed.append(bookDict)
            studentDict['Books'] = listOfBooksBorrowed
            database.append(studentDict)
        databaseDict = {'database': database}
        return databaseDict
    return getStatusResponseFrom(404)


def SumbitBook():
    admNumber = request.args.get('admNumber')
    bookName = request.args.get('book')
    authorName = request.args.get('author')
    if admNumber and bookName and authorName:
        student = Student.query.filter_by(admissionNumber=admNumber).first()
        if student:
            books = student.books
            for book in books:
                if bookName == book.name and authorName == book.author:
                    DeleteEntryFromDatabase(book)
                    books = student.books
                    if not books:
                        DeleteEntryFromDatabase(student)
                    return getStatusResponseFrom(200)
        return getStatusResponseFrom(404)
    return getStatusResponseFrom(400)

def SeeBook():
    admNumber = request.args.get('admNumber')
    if admNumber:
        student = Student.query.filter_by(admissionNumber=admNumber).first()
        if student:
            books = student.books
            listOfBooksBorrowed = []
            for book in books:
                bookDict = {'name': book.name,'author': book.author}
                listOfBooksBorrowed.append(bookDict)
            response = {'Books': listOfBooksBorrowed}
            return response
        return getStatusResponseFrom(404)
    return getStatusResponseFrom(400)


def TakeBook():
    studentName = request.args.get('stdName')
    admNumber = request.args.get('admNumber')
    bookName = request.args.get('book')
    authorName = request.args.get('author')
    if studentName and admNumber and bookName and authorName:
        student = Student.query.filter_by(admissionNumber=admNumber).first()
        if not student:
            student = Student(name=studentName, admissionNumber=admNumber)
            addEntryToDatabase(student)
        if studentName == student.name:
            book=Book(name=bookName, author=authorName, studentID=student.id)
            addEntryToDatabase(book)
            return getStatusResponseFrom(200)
    return getStatusResponseFrom(400)