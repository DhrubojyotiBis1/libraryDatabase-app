from libraryDatabase import db

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