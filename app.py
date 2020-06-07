from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

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

'''

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(26), nullable=False)
    admissionNumber = db.Column(db.String(10), nullable=False)
    books = db.relationship('Book', backref='student', lazy=True)

    def __repr__(self):
        return 'Student({}, {})'.format(self.name, self.admissionNumber)
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(26), nullable=False)
    studentID = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

    def __repr__(self):
        return 'Book({}, {})'.format(self.name, self.author)

def getStatusResponseFrom(status):
    STATUS = 'status'
    return {STATUS: status}

def addEntryToDatabase(student):
    db.session.add(student)
    db.session.commit()


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        return TakeBook()
    elif request.method == 'GET':
        return SeeBook()


def SeeBook():
    admNumber = request.args.get('admNumber')
    if admNumber:
        student = Student.query.filter_by(admissionNumber=admNumber).first()
        if student:
            books = student.books
            listOfBooksBorrowed = []
            for book in books:
                newBook = {'name': book.name,'author': book.author}
                listOfBooksBorrowed.append(newBook)
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
        book=Book(name=bookName, author=authorName, studentID=student.id)
        addEntryToDatabase(book)
        return getStatusResponseFrom(200)
    return getStatusResponseFrom(400)
   


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)