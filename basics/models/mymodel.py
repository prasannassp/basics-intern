from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    ForeignKey,
)
import datetime
from .meta import Base
from sqlalchemy.orm import relationship
'''class Question_paper(Base):
	__tablename__ = 'question_paper'
	id = Column(Integer, primary_key=True)
	subject = Column(Text)
	classname = Column(Text)
	section = Column(Text)
	testname = Column(Text)
	doe = Column(DateTime, default=datetime.datetime.utcnow)
	maxques = Column(Integer)
	duration = Column(Integer)
	papername = Column(Text)
	sections = Column(Integer)
	total = Column(Text)
	papernm = Column(Text)
	def __init__(self, subject, classname, testname, doe,devpi-server --status maxques, duration, noofsec, totalques,papernm):
		self.subject = subject
		self.classname = classname
		self.testname = testname
		self.doe = doe
		self.maxques = maxques
		self.duration = duration
		self.noofsec = noofsec
		self.total  = totalques
		self.papernm = papernm'''
	
class adminlink(Base):
	__tablename__ = 'link'
	id = Column(Integer, primary_key=True)
	classname = Column(Text)
	section = Column(Text)
	subject = Column(Text)
	profid = Column(Text)
	schoolid = Column(Integer)

'''class Sections(Base):
	__tablename__ = 'sections'
	id = Column(Integer, primary_key=True)
	numberofques = Column(Integer)
	type = Column(Integer)
	maxmark = Column(Integer)
	description = Column(Text)
	quesid = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'))
	ques = relationship('Questions', back_populates='sections')'''
	

class Questions(Base):
	__tablename__ = 'questions'
	id = Column(Integer, primary_key=True)
	questiondesc = Column(Text)
	subchapter = Column(Text)
	section = Column(Integer)
	papernm = Column(Text)
	qno = Column(Text)
	subject = Column(Text)
	classname = Column(Text)
	section = Column(Text)
	testname = Column(Text)
	doe = Column(Text)
	maxques = Column(Integer)
	duration = Column(Integer)
	sections = Column(Integer)
	total = Column(Text)
	schoolid = Column(Integer)
	profid = Column(Integer)
	mark = Column(Integer)
	def __init__(self, question, subchapter, section, papernm, qno, subject, classname, testname, doe, maxques, duration, noofsec, totalques, schoolid, profid, mark):
		self.questiondesc = question
		self.subchapter = subchapter
		self.section = section 
		self.papernm = papernm
		self.qno = qno
		self.subject = subject
		self.classname = classname
		self.testname = testname
		self.doe = doe
		self.maxques = maxques
		self.duration = duration
		self.sections = noofsec
		self.total  = totalques 
		self.schoolid =schoolid       
		self.profid = profid
		self.mark = mark

class Students(Base):
	__tablename__ = 'students'
	id = Column(Integer, primary_key=True)
	name = Column(Text)
	rollno = Column(Text)
	regno = Column(Text)
	classname = Column(Text)
	sec = Column(Text)
	subgrp = Column(Text)
	bday = Column(Text)
	bldgrp = Column(Text)
	gender = Column(Text)
	guardian = Column(Text)
	email = Column(Text)
	mobile = Column(Integer)
	income = Column(Integer)
	password = Column(Text)
	schoolid = Column(Integer)
	def __init__(self, name, rollno, regno, classname, sec, subgrp, bday ,bldgrp, gender, guardian, email, mobile, income, password, schoolid):
		self.name = name
		self.rollno = rollno
		self.regno = regno
		self.classname = classname
		self.sec = sec
		self.subgrp = subgrp
		self.bday = bday
		self.bldgrp = bldgrp
		self.gender = gender
		self.guardian = guardian
		self.email = email
		self.mobile = mobile
		self.income = income		
		self.password = password
		self.schoolid = schoolid

	def __json__(self, request):
		return{'name':self.name, 'rollno':self.rollno, 'regno':self.regno, 'classname':self.classname, 'sec':self.sec, 'subgrp':self.subgrp, 'bday':self.bday, 'bldgrp':self.bldgrp, 'gender':self.gender, 'guardian':self.guardian, 'email':self.email, 'mobile':self.mobile, 'income':self.income, 'password':self.password, 'schoolid':self.schoolid}

class Professors(Base):
	__tablename__ = 'professor'
	id = Column(Integer, primary_key=True)
	name = Column(Text)
	subject = Column(Text)
	empno = Column(Text)
	bday = Column(Text)
	bloodgrp = Column(Text)        	
	gender = Column(Text)
	email = Column(Text)
	mobile = Column(Integer)
	income = Column(Integer)
	password = Column(Text)
	schoolid = Column(Integer)
	def __init__(self, name, subject, empno, bday ,bloodgrp, gender, email, mobile, income, password, schoolid):
		self.name = name
		self.subject = subject
		self.empno = empno
		self.bday = bday
		self.bloodgrp = bloodgrp
		self.gender = gender
		self.email = email
		self.mobile = mobile
		self.income = income		
		self.password = password
		self.schoolid = schoolid
class Admin(Base):
	__tablename__ = 'admin'
	id = Column(Integer, primary_key=True)
	username = Column(Text)
	password = Column(Text)
	schoolname = Column(Text)
class Syllabus(Base):
	__tablename__ = 'syllabus'
	id = Column(Integer, primary_key=True)
	classname = Column(Text)
	subject = Column(Text)
	chapter = Column(Text)
	subchapter = Column(Text)
	schoolid = Column(Integer)
	subgroup = Column(Text)

class UpdateMark(Base):
	__tablename__ = 'updatemark'
	id = Column(Integer, primary_key=True)
	qno = Column(Text)
	studid = Column(Text)
	paperid = Column(Text)
	classname = Column(Text)
	subject = Column(Text)
	subchapter = Column(Text)
	mark = Column(Integer)
	schoolid = Column(Integer)
	profid = Column(Integer)


class Workspace(Base):
	__tablename__ = "workspace"
	id = Column(Integer, primary_key=True)
	name = Column(Text)
	stud = Column(Text)
	perc = Column(Text)
	cls = Column(Text)
	sec = Column(Text)
	sub = Column(Text)
	prof = Column(Text)
	stugen = Column(Text)
	profgen = Column(Text)
	income = Column(Text)
	schoolid = Column(Integer)

'''Sections.question_paper = relationship('Question_paper', order_by = Question_paper.id, back_populates='sec')
Professors.question_paper = relationship('Question_paper', order_by = Question_paper.id, back_populates='prof')'''
'''Questions.sections = relationship('Sections', order_by=Sections.id, back_populates='ques')'''
'''Admin.students = relationship('Students', order_by=Students.id, back_populates='school')
Admin.professor = relationship('Professors', order_by=Professors.id, back_populates='schools')'''



