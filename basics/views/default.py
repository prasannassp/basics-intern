from pyramid.response import Response
from pyramid.renderers import render 
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
import random
from ..models import Questions
from collections import Counter
from ..models import Students
from ..models import Professors
from ..models import Admin
import hashlib, binascii, os
import pdfkit 
import statistics 
from ..models import UpdateMark
import re
from ..models import Workspace
from ..models import adminlink
from ..models import Syllabus
import datetime
from sqlalchemy import and_
import transaction
import cgi, os
import cgitb; cgitb.enable()
from sqlalchemy.orm import Query
from sqlalchemy.sql import text as sa_text
from pyramid.session import SignedCookieSessionFactory

import os
import uuid
import shutil
from pyramid.response import Response 
'''
@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def my_view(request):
    return {}'''

@view_config(route_name='jex',renderer='../templates/jex.jinja2')
def jex(request):
	return {}
@view_config(route_name='index',renderer='../templates/index.jinja2')
def home_page(request):
	return {}
@view_config(route_name='uploadstu', renderer='../templates/admin-students.jinja2')
def uploadstu(request):
	if request.method == 'POST':
		data = request.get_array(field_name='file')
		return excel.make_response_from_array(data, 'csv')
	return Response(upload_form)


'''#!/usr/bin/python

	form = cgi.FieldStorage()
	# Get filename here.
	fileitem = form['filename']
	# Test if the file was uploaded
	if fileitem.filename:
 	  # strip leading path from file name to avoid
 	  # directory traversal attacks
 	  fn = os.path.basename(fileitem.filename)
 	  open('/tmp/' + fn, 'wb').write(fileitem.file.read())
 	  message = 'The file "' + fn + '" was uploaded successfully' 	
	else:
 	  message = 'No file was uploaded'
	return {}'''

@view_config(route_name='admin-link',renderer='../templates/admin-link.jinja2')
def admin_link_query(request):
	try:
		session = request.session	
		result = ''
		sec = ''
		sclid = session['adm_id']
		prof = ['']
		ref = ''
		arr = ''
		r = ''
		secs = ''
		item = []
		subs = ''
		arr = ''
		sub = ''
		subnm = ''
		secnm = ''
		classes = ''
		classname = ''
		n = ''
		d = ''
		allclass = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
		for j in allclass:
			d += j.classname.replace(" ","_") + ","
		#d += "All" + ","
		allsec = request.dbsession.query(Students.sec).distinct().filter(Students.schoolid == sclid)
		for j in allsec:
			sec += j.sec.replace(" ","_") + ","		
		#sec += "All" + ","
		allprof = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)	
		for i in allprof:
			sub += i.subject.replace(" ","_") + ","
		#sub += "All" + ","
		for i in allclass:
			classes += i.classname + ','
		classes = classes[:-1]
		classes = classes.split(",")
		for i in allprof:
			subs += i.subject + ','
		subs = subs[:-1]
		subs = subs.split(",")
		for i in allsec:
			secs += i.sec +','
		secs = secs[:-1]
		secs = secs.split(",")
		allclass = request.dbsession.query(Students)
		staffs = request.dbsession.query(Professors)
		for i in classes:
					for j in secs:
						for k in subs:
								result = staffs.filter(and_(Professors.subject == k.replace("_"," "),Professors.schoolid == sclid))
								try:	
									for l in result:
										r += l.name.replace(" ","_") + ','
									arr = i.replace(" ","_") + "," + j.replace(" ","_") + "," + k.replace(" ","_") +","+ r.replace(" ","_")
									r = ''
									arr = arr[:-1]
									arr = arr.split(",")
									item.append(arr)
								except DBAPIError:
									return Response(db_err_msg, content_type='text/plain', status=500)
		if request.POST.get('query'):
			classname = request.params['sel_class']
			secnm = request.params['sel_sec']
			subnm = request.params['sel_sub']
			for i in allclass:
				classes += i.classname + ','
			classes = classes[:-1]
			classes = classes.split(",")
			for i in allprof:
				subs += i.subject + ','
			subs = subs[:-1]
			subs = subs.split(",")
			for i in allsec:
				secs += i.sec +','
			secs = secs[:-1]
			secs = secs.split(",")
			allclass = request.dbsession.query(Students)
			staffs = request.dbsession.query(Professors)
			if classname == 'All' and secnm == 'All' and subnm == 'All': 
				for i in classes:
					for j in secs:
						for k in subs:
								result = staffs.filter(and_(Professors.subject == k.replace("_"," "),Professors.schoolid == sclid))
								try:	
									for l in result:
										r += l.name.replace(" ","_") + ','
									arr = i.replace(" ","_") + "," + j.replace(" ","_") + "," + k.replace(" ","_") +","+ r.replace(" ","_")
									r = ''
									arr = arr[:-1]
									arr = arr.split(",")
									item.append(arr)
								except DBAPIError:
									return Response(db_err_msg, content_type='text/plain', status=500)
			elif secnm == 'All' and subnm == 'All':
				for i in secs:
					for j in subs:
							result = staffs.filter(and_(Professors.subject == j.replace("_"," "),Professors.schoolid == sclid))
							try:
								for k in result:
									r +=k.name.replace(" ","_") + ','
								arr = classname.replace(" ","_") + "," + i.replace(" ","_") + "," + j.replace(" ","_") + "," + r.replace(" ","_") 				
								r = ''
								arr = arr[:-1]
								arr = arr.split(",")
								item.append(arr)
							except DBAPIError:
								return Response(db_err_msg, content_type='text/plain', status=500)
			elif classname == 'All' and secnm == 'All':
				for i in classes:
					for j in secs:
							result = staffs.filter(and_(Professors.subject == subnm.replace("_"," "),Professors.schoolid == sclid))
							try:	
								for k in result:
									r += k.name.replace(" ","_") + ','
								arr = i.replace(" ","_") + ',' + j.replace(" ","_") + ',' + subnm.replace(" ","_") + ',' + 	r.replace(" ","_") 			
								r = ''	
								arr = arr[:-1]
								arr = arr.split(",")
								item.append(arr)
							except DBAPIError:
								return Response(db_err_msg, content_type='text/plain', status=500)
			elif classname == 'All' and subnm == 'All':
				for i in classes:
					for j in subs:
							result = staffs.filter(and_(Professors.subject == j.replace("_"," "),Professors.schoolid == sclid))
							try:	
								for k in result:
									r += k.name.replace(" ","_") + ','
								arr = i.replace(" ","_") + ',' + secnm.replace(" ","_") + ',' + j.replace(" ","_") + ',' + r.replace(" ","_") 
								r = ''
								arr = arr[:-1]
								arr = arr.split(",")
								item.append(arr)
							except DBAPIError:
								return Response(db_err_msg, content_type='text/plain', status=500)
			elif classname == 'All':
				for i in classes:
						result = staffs.filter(and_(Professors.subject == subnm.replace("_"," "),Professors.schoolid == sclid))
						try:	
							for k in result:
								r += k.name.replace(" ","_") + ','
							arr = i.replace(" ","_") + ',' + secnm.replace(" ","_") + ',' + subnm.replace(" ","_") + ',' + r
							r = ''
							arr = arr[:-1]
							arr = arr.split(",")
							item.append(arr)
						except DBAPIError:
							return Response(db_err_msg, content_type='text/plain', status=500)
			elif secnm == 'All':
				for i in secs:
						result = staffs.filter(and_(Professors.subject == subnm.replace("_"," "),Professors.schoolid == sclid))
						try:
							for k in result:
								r += k.name.replace(" ","_") + ','
							arr = classname.replace(" ","_") + ',' + i.replace(" ","_") + ',' + subnm.replace(" ","_") + ',' + r
							r = ''
							arr = arr[:-1]
							arr = arr.split(",")
							item.append(arr)
						except DBAPIError:
							return Response(db_err_msg, content_type='text/plain', status=500)
			elif subnm == 'All':
				for i in subs:
						result = staffs.filter(and_(Professors.subject == i.replace("_"," "),Professors.schoolid == sclid))
						try:	
							for k in result:
								r += k.name.replace(" ","_") + ','
							arr = classname.replace(" ","_") + ',' + secnm.replace(" ","_") + ',' + i.replace(" ","_") + ',' + r
							r = ''
							arr = arr[:-1]
							arr = arr.split(",")
							item.append(arr)
						except DBAPIError:
							return Response(db_err_msg, content_type='text/plain', status=500)
			else:
					result = staffs.filter(and_(Professors.subject == subnm.replace("_"," "),Professors.schoolid == sclid))
					try:
						for j in result:
							r += j.name.replace(" ","_") + ','
						r = r[:-1]
						arr = classname.replace(" ","_") + ',' + secnm.replace(" ","_") + ',' + subnm.replace(" ","_") + ',' + r
						arr = arr.split(",")
						item.append(arr)
					except DBAPIError:
						return Response(db_err_msg, content_type='text/plain', status=500)
			return {'classname':classes,'sel_class':classname,'sel_sub':subnm,'sel_sec':secnm,'sub':subs,'sec':secs,'names':item,'iter':zip(item,range(len(item))),'result':prof,'classes':d,'sections':sec,'subjects':sub}
		elif request.POST.get('save'):
			stud = request.dbsession.query(adminlink).filter(adminlink.schoolid == sclid)
			Query.delete(stud)
			transaction.commit()
			arr = ''
			item = request.params['names']
			ref = item 
			item= item[:-1]
			item = item.split(',')
			n = len(item)
			for i in range(0,n,4):
				arr= item[i:i+4]
				obj = adminlink()
				obj.classname = arr[0].replace("_"," ")
				obj.section = arr[1].replace("_"," ")
				obj.subject =arr[2].replace("_"," ")
				obj.profid = arr[3].replace("_"," ")
				obj.schoolid = sclid
				request.dbsession.add(obj)	
			item = []
			ref = ref[:-1]
			ref = ref.split(',')
			for i in range(0,len(ref),4):
				item.append(ref[i:i+4])
			return {'classname':classes,'sel_class':classname,'err':'Data saved Successfully !','sel_sub':subnm,'sel_sec':secnm,'sub':subs,'sec':secs,'names':item,'iter':zip(item,range(len(item))),'result':prof,'classes':d,'sections':sec,'subjects':sub}		
		return {'classname':classes,'sel_class':classname,'sel_sub':subnm,'sel_sec':secnm,'sub':subs,'sec':secs,'names':item,'iter':zip(item,range(len(item))),'result':prof,'classes':d,'sections':sec,'subjects':sub}
	except KeyError:
		return Response(keyerr, content_type='text/plain', status=500)

@view_config(route_name='admin-professors',renderer='../templates/admin-professors.jinja2')
def admin_professors(request):
	try:
		session = request.session
		name = ''	
		subj = ''
		email = ''
		mobile = ''
		bday = ''
		income = ''
		password = ''
		leng = ''
		subs = ''
		bloodgrp = ''
		gender = ''
		sub = ''
		d = ''
		empno = ''
		sect = ''
		sclid = session['adm_id']
		def is_valid_email(email):
			if len(email) > 7:
				return bool(re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email))			
		cls = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
		#d += 'All' + ','
		for i in cls:
			d += i.classname + ','
		cls = request.dbsession.query(Students.sec).distinct().filter(Students.schoolid == sclid)
		#sect += 'All' + ','
		for i in cls:
			sect += i.sec + ','
		cls = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
		#sub += 'All' + ','
		for i in cls:
			sub += i.subject.replace(" ","_") + ','
			subs += i.subject + ','
		subs = subs[:-1]
		subs = subs.split(',')
		stud = request.dbsession.query(Professors).distinct(Professors.empno).filter(Professors.schoolid == sclid)
		try:
			arr = ""
			arr1 =[]
			for i in stud:
				arr += i.name + "," + i.subject + "," + i.empno + "," + i.bday + "," + i.bloodgrp + "," + i.gender + "," + i.email + "," + str(i.mobile) + "," + str(i.income) + "," + i.password + ","
			arr = arr[:-1]
			arr = arr.split(",")
			n = len(arr)
			k = []
			for x in range(0,n,10):
				k.append(arr[x:x+10])
			for i in stud:
				name += i.name.replace(" ","_") + ','
				subj += i.subject.replace(" ","_") + ','
				empno += i.empno.replace(" ","_") + ','
				bday += i.bday.replace(" ","_") + ','
				bloodgrp += i.bloodgrp.replace(" ","_") + ','
				gender += i.gender.replace(" ","_") + ','
				email += i.email.replace(" ","_") + ','
				mobile += str(i.mobile).replace(" ","_") +','
				income += str(i.income).replace(" ","_") +','
				password += i.password +','
			leng = len(name)
		except DBAPIError:
			return Response(db_err_msg, content_type='text/plain', status=500)
		if request.POST.get('savedata'):
			sclid = session['adm_id']
			stud = request.dbsession.query(Professors).filter(Professors.schoolid == sclid)
			Query.delete(stud)
			transaction.commit()
			k = ''
			arr =  ''
			sub = ''
			cls = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
			n = int(request.params['savedata'])
			for i in request.params['profdata']:
				k += i
			k = k.split(',')
			for i in cls:
				sub += i.subject.replace(" ","_") + ','
			#sub += 'All' + ','
			for x in range(0,n * 10,10):
				arr = k[x:x+11]
				val = is_valid_email(arr[6])
				if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', arr[9]):				
					if val is True:
						if arr[7].isdigit() and arr[8].isdigit():
							#try:								
								p = Professors(arr[0],arr[1],arr[2],arr[3],arr[4],arr[5],arr[6],arr[7],arr[8],arr[9],session['adm_id'])
								request.dbsession.add(p)
								transaction.commit()
						else:
							err = "mobile number and income must be a integer value!"
							return Response(render('../templates/admin-professors.jinja2',{'k':arr,'classes':d,'sections':sect,'subjects':sub,'err':err},request=request))								
					else:
						err = "Invalid email!"
						return Response(render('../templates/admin-professors.jinja2',{'k':arr,'classes':d,'sections':sect,'subjects':sub,'err':err},request=request))					
				else:
					err = "Password must be 8 characters long and contain a capital letter,small letter ,a number and a special character !"
					return Response(render('../templates/admin-professors.jinja2',{'k':arr,'classes':d,'sections':sect,'subjects':sub,'err':err},request=request))					
			s = request.dbsession.query(Professors).filter(Professors.schoolid == sclid)
			for i in s:
				name += i.name.replace(" ","_") + ','
				subj += i.subject.replace(" ","_") + ','
				empno += i.empno.replace(" ","_") + ','
				bday += i.bday.replace(" ","_") + ','
				bloodgrp += i.bloodgrp.replace(" ","_") + ','
				gender += i.gender.replace(" ","_") + ','
				email += i.email.replace(" ","_") + ','
				mobile += str(i.mobile).replace(" ","_") +','
				income += str(i.income).replace(" ","_") +','
				password += i.password +','
			leng = len(name)			
			return Response(render('../templates/admin-professors.jinja2',{'k':arr,'classes':d,'sections':sect,'subjects':sub,'err':"Data saved successfully !",'name':name,'sub':subj,'empno':empno,'bldgrp':bloodgrp,'gender':gender,'email':email,'subjects':sub,'mobile':mobile,'income':income,'password':password,'len':leng,'bday':bday},request=request))
		elif request.POST.get('search'):
			sear=request.params['search_name']
			sear='%'+sear+'%'
			r=request.dbsession.query(Professors).filter(Professors.name.ilike(sear)).all()
			name =''
			subj =''
			empno =''
			bday =''
			bloodgrp =''
			gender =''
			email =''
			mobile =''
			income =''
			password =''
			for i in r:
				name += i.name.replace(" ","_") + ','
				subj += i.subject.replace(" ","_") + ','
				empno += i.empno.replace(" ","_") + ','
				bday += i.bday.replace(" ","_") + ','
				bloodgrp += i.bloodgrp.replace(" ","_") + ','
				gender += i.gender.replace(" ","_") + ','
				email += i.email.replace(" ","_") + ','
				mobile += str(i.mobile).replace(" ","_") +','
				income += str(i.income).replace(" ","_") +','
				password += i.password +','
			leng = len(name)		
			if leng==0:
				return Response(render('../templates/admin-professors.jinja2',{'k':arr,'classes':d,'sections':sect,'subjects':sub,'err':"Data not Found!",'name':name,'sub':subj,'empno':empno,'bldgrp':bloodgrp,'gender':gender,'email':email,'subjects':sub,'mobile':mobile,'income':income,'password':password,'len':leng,'bday':bday},request=request))
			else:
				return Response(render('../templates/admin-professors.jinja2',{'k':arr,'classes':d,'sections':sect,'subjects':sub,'name':name,'sub':subj,'empno':empno,'bldgrp':bloodgrp,'gender':gender,'email':email,'subjects':sub,'mobile':mobile,'income':income,'password':password,'len':leng,'bday':bday},request=request))
		elif request.POST.get('save'):
			sclid = session['adm_id']
			empno = ''
			name = ''
			subj = ''
			bloodgrp = ''
			gender = ''
			gaurd = ''
			email = ''
			mobile = ''
			income = ''
			d = ''
			sect = ''
			sub = ''
			subs = ''
			password = ''
			leng = ''
			subgroup = ''
			stud = request.dbsession.query(Professors)
			subgroup = request.params['sel_sub']
			cls = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
			for i in cls:
				d += i.classname + ','
			#d += 'All' + ','
			cls = request.dbsession.query(Students.sec).distinct().filter(Students.schoolid == sclid)
			for i in cls:
				sect += i.sec + ','
			#sect += 'All' + ','
			cls = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
			for i in cls:
				sub += i.subject.replace(" ","_") + ','
				subs += i.subject + ','
			#sub += 'All' + ","			
			subs = subs[:-1]
			subs = subs.split(',')		
			if subgroup == 'All':
				d = ''
				sect = ''
				sub = ''
				subs = ''
				cls = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					d += i.classname + ','
				#d += 'All' + ','
				cls = request.dbsession.query(Students.sec).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					sect += i.sec + ','
				#sect += 'All' + ','
				cls = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
				#sub += 'All' + ','
				for i in cls:
					sub += i.subject.replace(" ","_") + ','
					subs += i.subject + ','
				
				subs = subs[:-1]
				subs = subs.split(',')
				for j in subs:
						result = stud.filter(and_(Professors.subject == j,Professors.schoolid == sclid))	
						try:
							for i in result:
								name += i.name.replace(" ","_") + ','
								subj += i.subject.replace(" ","_") + ','
								empno += i.empno.replace(" ","_") + ','
								bday += i.bday.replace(" ","_") + ','
								bloodgrp += i.bloodgrp.replace(" ","_") + ','
								gender += i.gender.replace(" ","_") + ','
								email += i.email.replace(" ","_") + ','
								mobile += str(i.mobile).replace(" ","_") +','
								income += str(i.income).replace(" ","_") +','
								password += i.password +','
						except DBAPIError:
							return Response(db_err_msg, content_type='text/plain', status=500)
				leng = len(name)
				return Response(render('../templates/admin-professors.jinja2',{'sel_sub':subgroup,'name':name,'subjects':sub,'sub':subj,'empno':empno,'bldgrp':bloodgrp,'gender':gender,'email':email,'mobile':mobile,'income':income,'password':password,'len':leng,'bday':bday},request=request))		
			else:
					d = ''
					sect = ''
					sub = ''
					subs = ''
					cls = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
					for i in cls:
						sub += i.subject.replace(" ","_") + ','
						subs += i.subject + ','
					#sub += 'All' + ","					
					subs = subs[:-1]
					subs = subs.split(',')					
					result = stud.filter(and_(Professors.subject == subgroup.replace("_"," "),Professors.schoolid == sclid))	
					try:
						for i in result:
							name += i.name.replace(" ","_") + ','
							subj += i.subject.replace(" ","_") + ','
							empno += i.empno.replace(" ","_") + ','
							bday += i.bday.replace(" ","_") + ','
							bloodgrp += i.bloodgrp.replace(" ","_") + ','
							gender += i.gender.replace(" ","_") + ','
							email += i.email.replace(" ","_") + ','
							mobile += str(i.mobile).replace(" ","_") +','
							income += str(i.income).replace(" ","_") +','
							password += i.password +','
						leng = len(name)
						return Response(render('../templates/admin-professors.jinja2',{'sel_sub':subgroup,'name':name,'subjects':sub,'sub':subj,'bldgrp':bloodgrp,'gender':gender,'email':email,'mobile':mobile,'income':income,'password':password,'len':leng,'bday':bday},request=request))		
					except DBAPIError:
						return Response(db_err_msg, content_type='text/plain', status=500)
			return Response(render('../templates/admin-professors.jinja2',{'sel_sub':subgroup,'name':name,'subjects':sub,'sub':subj,'empno':empno,'bldgrp':bloodgrp,'gender':gender,'email':email,'bday':bday,'mobile':mobile,'income':income,'password':password,'len':leng},request=request))		
		return {'name':name,'sub':subj,'empno':empno,'bldgrp':bloodgrp,'gender':gender,'email':email,'subjects':sub,'mobile':mobile,'income':income,'password':password,'len':leng,'bday':bday}
	except KeyError:
		return Response(keyerr, content_type='text/plain', status=500)
@view_config(route_name='admin-snapshot',renderer='../templates/admin-snapshot.jinja2')
def admin_snapshot(request):
		session = request.session
		stu = ''
		stugen = ''
		income = ''
		cls = ''
		sec = ''
		tot = 0
		totstr = ''
		sub = ''
		sclid = session['adm_id']
		meanm = ''
		sampnm = ''
		b = 0
		stud = ''
		sec = ''
		ag = ''
		sub= ''
		prof = ''
		stugen = ''
		profgen = ''
		income = ''
		perc = ''
		stud2 = ''
		sec2 = ''
		avg = 0
		cls2 = ''
		sub2 = ''
		prof2 = ''
		def get_first_mode(a):
			c = Counter(a)  
			mode_count = max(c.values())
			mode = {key for key, count in c.items() if count == mode_count}
			first_mode = next(x for x in a if x in mode)
			return first_mode
		stugen2 = ''
		profgen2 = ''
		income2 = ''
		item = []
		n = ''
		res = ''
		arr = ''
		wsnm = ''
		finaltot = 0
		finalavg = 0
		ws = ''
		workspc = request.dbsession.query(Workspace)
		workspc = workspc.filter(Workspace.schoolid == sclid)
		for i in workspc:
			ws += i.name + ","
		studs = request.dbsession.query(Students).filter(Students.schoolid == sclid)	
		links = request.dbsession.query(adminlink)
		profs = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
		staffs = request.dbsession.query(Professors)
		for i in studs:
			stu += i.name.replace(" ","_") + ','
			stugen += i.gender.replace(" ","_") + ','
			income += str(i.income).replace(" ","_") + ','
			cls += i.classname.replace(" ","_") + ','
			sec += i.sec.replace(" ","_") + ','
			for j in profs:
				sub += j.subject.replace(" ","_") + ','
				result = links.filter(and_(adminlink.classname == i.classname.replace("_"," "),adminlink.section == i.sec.replace("_"," "),adminlink.subject == j.subject.replace("_"," ")))
				result2 = links.filter(and_(adminlink.classname == i.classname.replace("_"," "),adminlink.section == i.sec.replace("_"," "),adminlink.subject == j.subject.replace("_"," "))).first()
				if result2 is not None:
					for k in result:
						res = staffs.filter(Professors.name == k.profid)
						for z in res:
							gen = z.gender
							upd = request.dbsession.query(UpdateMark).filter(and_(UpdateMark.subject == j.subject.replace("_"," "),UpdateMark.schoolid == sclid,UpdateMark.studid == i.id))
							cnt = request.dbsession.query(Questions.papernm).distinct().filter(and_(Questions.subject == j.subject.replace("_"," "),Questions.schoolid == sclid,Questions.classname == i.classname.replace("_"," "))).count()
							if cnt != 0:
									for u in upd:
										tot += u.mark
										totstr += str(int(u.mark)) + ","
									totstr = totstr[:-1]
									totstr = totstr.split(",")
									avg += float(tot/cnt)
									ag = float(tot/cnt)
									rnk = list(map(int,totstr))
									if meanm == 'Average':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + str(tot).replace(" ","_") + ',' + str(ag).replace(" ","_") + ','
										finaltot += tot
										finalavg += avg								
									elif meanm == 'Median':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + str(tot).replace(" ","_") + ',' + str(statistics.median(rnk)).replace(" ","_") + ','
										finaltot += tot
										finalavg += avg								
									elif meanm == 'Mode':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + str(tot).replace(" ","_") + ',' + str(get_first_mode(totstr)).replace(" ","_") + ','
										finaltot += tot
										finalavg += avg							
									elif meanm == 'Percentile':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + str(tot).replace(" ","_") + ',' + str(tot/100).replace(" ","_") + ','
										finaltot += tot
										finalavg += avg
									totstr = ''
							else:
									if meanm == 'Average':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + "0" + ',' + "0" + ','
										finaltot += tot
										finalavg += avg								
									elif meanm == 'Median':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + "0" + ',' + "0" + ','
										finaltot += tot
										finalavg += avg								
									elif meanm == 'Mode':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + "0" + ',' + "0" + ','
										finaltot += tot
										finalavg += avg							
									elif meanm == 'Percentile':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + "0" + ',' + "0" + ','
										finaltot += tot
										finalavg += avg
									totstr = ''
				else:
					return Response(render('../templates/admin-snapshot.jinja2',{'err':"No data found!",'sel_ws':wsnm,'ws':ws,'sel_mea':meanm,'sel_samp':sampnm,'stud':stud,'perc':perc,'cls':cls,'sec':sec,'sub':sub,'prof':prof,'studgen':stugen,'profgen':profgen,'len':len(item),'final_average':finalavg,'item':zip(item,range(len(item))),'final_total':finaltot},request=request))					
		arr = arr[:-1]
		arr = arr.split(',')
		n =len(arr)
		for x in range(0,n,10):
			item.append(arr[x:x+10])
		if request.POST.get("submit"):
				ws = ''
				sub = ''
				workspc = request.dbsession.query(Workspace)
				workspc = workspc.filter(Workspace.schoolid == sclid)
				for i in workspc:
					ws += i.name + ","
				stud = request.params['sel_stud']
				per= request.params['sel_perc']
				cls = request.params['sel_cls']
				sec = request.params['sel_sec']
				sub = request.params['sel_sub']
				prof = request.params['sel_prof']
				studgen = request.params['sel_stud_gen']
				profgen = request.params['sel_prof_gen']
				income = request.params['sel_income']
				snaps  = Workspace()
				snaps.name = "workspace"+ str(random.randint(1,21)*5)
				snaps.stud = stud
				snaps.perc = per
				snaps.cls = cls
				snaps.sub = sub
				snaps.sec = sec
				snaps.prof = prof
				snaps.stugen = studgen
				snaps.profgen = profgen
				snaps.income = income
				snaps.schoolid = sclid
				request.dbsession.add(snaps)
				return {'sel_ws':wsnm,'ws':ws,'sel_mea':meanm,'sel_samp':sampnm,'stud':stud,'perc':perc,'cls':cls,'sec':sec,'sub':sub,'prof':prof,'studgen':studgen,'profgen':profgen,'err':"workspace saved !",'len':len(item),'final_average':finalavg,'item':zip(item,range(len(item))),'final_total':finaltot}
		elif request.POST.get('save'):
			ws = ''
			sub = ''
			workspc = request.dbsession.query(Workspace)
			workspc = workspc.filter(Workspace.schoolid == sclid)
			for i in workspc:
				ws += i.name + ","
			wsnm = request.params['sel_ws']
			meanm = request.params['sel_mea']
			totstr = ''
			sampnm = request.params['sel_samp']
			workspc = request.dbsession.query(Workspace)
			res = workspc.filter(and_(Workspace.name == wsnm,Workspace.schoolid == sclid))
			for i in res:
				stud = i.stud
				perc = i.perc
				cls = i.cls
				sec = i.sec
				sub = i.sub
				prof = i.prof
				stugen = i.stugen
				profgen = i.profgen
				income = i.income
			if sampnm == 'Board':
				arr = ''
				totstr = ''
				ws = ''
				workspc = request.dbsession.query(Workspace)
				workspc = workspc.filter(Workspace.schoolid == sclid)
				for i in workspc:
					ws += i.name + ","
				studs = request.dbsession.query(Students).filter(Students.schoolid == sclid)	
				links = request.dbsession.query(adminlink)
				profs = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
				staffs = request.dbsession.query(Professors)
				for i in studs:
					stud2 += str(i.id).replace(" ","_") + ','
					stugen2 += i.gender.replace(" ","_") + ','
					income2 += str(i.income).replace(" ","_") + ','
					cls2 += i.classname.replace(" ","_") + ','
					sec2 += i.sec.replace(" ","_") + ','
					for j in profs:
						sub2 += j.subject + ','
						result = links.filter(and_(adminlink.classname == i.classname,adminlink.section == i.sec,adminlink.subject == j.subject))
						for k in result:
							res = staffs.filter(Professors.name == k.profid)
							for z in res:
								gen = z.gender
								upd = request.dbsession.query(UpdateMark).filter(and_(UpdateMark.subject == j.subject,UpdateMark.schoolid == sclid,UpdateMark.studid == i.id))
								cnt = request.dbsession.query(Questions.papernm).distinct().filter(and_(Questions.subject == j.subject,Questions.schoolid == sclid,Questions.classname == i.classname)).count()
								if cnt != 0:
									for u in upd:
										tot += u.mark
										totstr += str(int(u.mark)) + ","
									totstr = totstr[:-1]
									totstr = totstr.split(",")
									avg += float(tot/cnt)
									ag = float(tot/cnt)
									rnk = list(map(int,totstr))
									if meanm == 'Average':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + str(tot).replace(" ","_") + ',' + str(ag).replace(" ","_") + ','
										finaltot += tot
										finalavg += avg								
									elif meanm == 'Median':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + str(tot).replace(" ","_") + ',' + str(statistics.median(rnk)).replace(" ","_") + ','
										finaltot += tot
										finalavg += avg								
									elif meanm == 'Mode':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + str(tot).replace(" ","_") + ',' + str(get_first_mode(totstr)).replace(" ","_") + ','
										finaltot += tot
										finalavg += avg							
									elif meanm == 'Percentile':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + str(tot).replace(" ","_") + ',' + str(tot/100).replace(" ","_") + ','
										finaltot += tot
										finalavg += avg
									totstr = ''
								else:
									if meanm == 'Average':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + "0" + ',' + "0" + ','						
									elif meanm == 'Median':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + "0" + ',' + "0" + ','							
									elif meanm == 'Mode':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + "0" + ',' + "0" + ','						
									elif meanm == 'Percentile':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + "0" + ',' + "0" + ','
									totstr = ''
				arr = arr[:-1]
				arr = arr.split(',')
				n =len(arr)
				for x in range(0,n,10):
					item.append(arr[x:x+10])
				#return {'sel_ws':wsnm,'ws':ws,'sel_mea':meanm,'sel_samp':sampnm,'stud':stud,'perc':perc,'cls':cls,'sec':sec,'sub':sub,'prof':prof,'studgen':stugen,'profgen':profgen,'item':zip(item,range(len(item))),'len':len(item),'final_total':finaltot,'final_average':finalavg,'itms':arr}								
			elif sampnm == 'School':
				arr = ''
				ws = ''
				workspc = request.dbsession.query(Workspace)
				workspc = workspc.filter(Workspace.schoolid == sclid)
				for i in workspc:
					ws += i.name + ","
				totstr = ''
				studs = request.dbsession.query(Students).filter(Students.schoolid == sclid)	
				links = request.dbsession.query(adminlink)
				profs = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
				staffs = request.dbsession.query(Professors)
				for i in studs:
					stud2 += i.name.replace(" ","_") + ','
					stugen2 += i.gender.replace(" ","_") + ','
					income2 += str(i.income).replace(" ","_") + ','
					cls2 += i.classname.replace(" ","_") + ','
					sec2 += i.sec.replace(" ","_") + ','
					for j in profs:
						sub2 += j.subject + ','
						result = links.filter(and_(adminlink.classname == i.classname,adminlink.section == i.sec,adminlink.subject == j.subject))
						for k in result:
							res = staffs.filter(Professors.name == k.profid)
							for z in res:
								gen = z.gender
								upd = request.dbsession.query(UpdateMark).filter(and_(UpdateMark.subject == j.subject,UpdateMark.schoolid == sclid,UpdateMark.studid == i.id))
								cnt = request.dbsession.query(Questions.papernm).distinct().filter(and_(Questions.subject == j.subject,Questions.schoolid == sclid,Questions.classname == i.classname)).count()
								for u in upd:
									tot += u.mark
									totstr += str(int(u.mark)) + ","
								totstr = totstr[:-1]
								totstr =totstr.split(",")
								if cnt != 0:
									avg += float(tot/cnt)
									rnk = list(map(int,totstr))
									if meanm == 'Average':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + str(tot).replace(" ","_") + ',' + str(tot/cnt).replace(" ","_") + ','
										finaltot += tot
										finalavg += avg								
									elif meanm == 'Median':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_")+ ',' + z.gender.replace(" ","_") + ',' + str(tot).replace(" ","_") + ',' + str(statistics.median(rnk)).replace(" ","_") + ','
										finaltot += tot
										finalavg += avg								
									elif meanm == 'Mode':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_")+ ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + str(tot).replace(" ","_") + ',' + str(get_first_mode(totstr)).replace(" ","_")  + ','
										finaltot += tot
										finalavg += avg							
									elif meanm == 'Percentile':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + str(tot).replace(" ","_") + ',' + str(tot/100).replace(" ","_") + ','
										finaltot += tot
										finalavg += avg
									totstr = ''
								else:
									if meanm == 'Average':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + "0" + ',' + "0" + ','							
									elif meanm == 'Median':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + "0" + ',' + "0" + ','								
									elif meanm == 'Mode':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + "0" + ',' + "0"  + ','						
									elif meanm == 'Percentile':
										arr += i.name.replace(" ","_") + ',' + i.gender.replace(" ","_") + ',' + str(i.income).replace(" ","_") + ',' + i.classname.replace(" ","_") + ',' + i.sec.replace(" ","_") + ',' + j.subject.replace(" ","_") + ',' + k.profid.replace(" ","_") + ',' + z.gender.replace(" ","_") + ',' + "0" + ',' + "0" + ','
									totstr = ''
				arr = arr[:-1]
				arr = arr.split(',')
				n =len(arr)
				for x in range(0,n,10):
					item.append(arr[x:x+10])
				#return {'sel_ws':wsnm,'ws':ws,'sel_mea':meanm,'sel_samp':sampnm,'stud':stud,'perc':perc,'cls':cls,'sec':sec,'sub':sub,'prof':prof,'studgen':stugen,'profgen':profgen,'item':zip(item,range(len(item))),'len':len(item),'final_total':finaltot,'final_average':finalavg,'itms':arr}							
			return {'sel_ws':wsnm,'ws':ws,'sel_mea':meanm,'sel_samp':sampnm,'stud':stud,'perc':perc,'cls':cls,'sec':sec,'sub':sub,'prof':prof,'studgen':stugen,'profgen':profgen,'item':zip(item,range(len(item))),'len':len(item),'final_total':finaltot,'final_average':finalavg,'itms':arr}						
		return {'sel_ws':wsnm,'ws':ws,'sel_mea':meanm,'sel_samp':sampnm,'stud':'Yes','cls':'Yes','sec':'Yes','sub':'Yes','prof':'Yes','studgen':'Yes','profgen':'Yes','item':zip(item,range(len(item))),'len':len(item),'final_average':finalavg,'final_total':finaltot,'itms':arr}
@view_config(route_name='admin-students',renderer='../templates/admin-students.jinja2')
def admin_students(request):
	try:
		session = request.session
		d = ''	
		sec = ''	
		sect = ''
		sub = ''
		name = ''
		subs = ''
		classes = ''
		rollno = ''
		regno = ''
		classname = ''	
		secs = ''
		subgrp =''
		bldgrp = ''
		gender = ''
		bday = ''
		guardian = ''
		email = ''
		mobile = ''
		income = ''
		password = ''
		leng = ''
		sclid = session['adm_id']
		def is_valid_email(email):
			if len(email) > 7:
				return bool(re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email))
		cls = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
		for i in cls:
			d += i.classname.replace(" ","_") + ','
		#d += 'All' + ","
		for i in cls:
			classes += i.classname.replace(" ","_") + ','
		classes = classes[:-1]
		classes = classes.split(',')
		cls = request.dbsession.query(Students.sec).distinct().filter(Students.schoolid == sclid)
		for i in cls:
			sect += i.sec.replace(" ","_") + ','	
		#sect += 'All' + ","
		for i in cls:
			secs += i.sec.replace(" ","_") +','
		secs = secs[:-1]
		secs = secs.split(',')
		cls = request.dbsession.query(Students.subgrp).distinct().filter(Students.schoolid == sclid)
		for i in cls:
			sub += i.subgrp.replace(" ","_") + ','
		#sub += 'All' + ","
		for i in cls:
			subs += i.subgrp.replace(" ","_") +','
		subs = subs[:-1]
		subs = subs.split(',')
		stud = request.dbsession.query(Students).filter(Students.schoolid == sclid) 
		try:
			arr = ""
			arr1 =[]
			for i in stud:
				arr += i.name + "," + i.rollno + "," + i.regno + "," + i.classname + "," + i.bday + "," + i.sec + "," + i.subgrp + "," + i.bldgrp + "," + i.gender + "," + i.guardian + "," + i.email + "," + str(i.mobile) + "," + str(i.income) + "," + i.password 
			arr = arr[:-1]
			arr = arr.split(",")
			n = len(arr)
			k = []
			for x in range(0,n,10):
				k.append(arr[x:x+10])
			for i in stud:
				name += i.name.replace(" ","_") + ','
				rollno += i.rollno.replace(" ","_") + ','
				regno += i.regno.replace(" ","_") + ','
				classname += i.classname.replace(" ","_") + ','
				bday += i.bday.replace(" ","_") + ','
				sec += i.sec.replace(" ","_") + ','
				subgrp += i.subgrp.replace(" ","_") + ','
				bldgrp += i.bldgrp.replace(" ","_") + ','
				gender += i.gender.replace(" ","_") + ','
				guardian += i.guardian.replace(" ","_") + ','
				email += i.email.replace(" ","_") + ','
				mobile += str(i.mobile).replace(" ","_") +','
				income += str(i.income).replace(" ","_") +','
				password += i.password +','
			'''arr=[]
			for i in stud:
				arr += i.name + "," + i.rollno + "," + i.regno + "," + i.classname + "," + i.bday + "," + i.sec + "," + i.subgrp + "," + i.bldgrp + "," + i.gender + "," + i.guardian + "," + i.email + "," + str(i.mobile) + "," + str(i.income) + "," + i.password 
				arr = arr[:-1]
				#arr = arr.split(",")
			n = len(arr)
			k = []
			for x in range(0,n,10):
				k.append(arr[x:x+10])
			for i in stud:
				name += i.name.replace(" ","_") + ','
				rollno += i.rollno.replace(" ","_") + ','
				regno += i.regno.replace(" ","_") + ','
				classname += i.classname.replace(" ","_") + ','
				bday  += i.bday.replace(" ","_") + ','
				sec += i.sec.replace(" ","_") + ','
				subgrp += i.subgrp.replace(" ","_") + ','
				bloodgrp += i.bldgrp.replace(" ","_") + ','
				gender += i.gender.replace(" ","_") + ','
				gaurd += i.guardian.replace(" ","_") + ','
				email += i.email.replace(" ","_") + ','
				mobile += str(i.mobile).replace(" ","_") +','
				income += str(i.income).replace(" ","_") +','
				password += i.password +','  '''
		except DBAPIError:
			return Response(db_err_msg, content_type='text/plain', status=500)
		if request.POST.get('savedata'):
			k = ''
			sclid = session['adm_id']
			arr =  ''
			stud = request.dbsession.query(Students).filter(Students.schoolid == sclid)
			Query.delete(stud)
			transaction.commit()
			n = int(request.params['savedata'])
			for i in request.params['profdata']:
				k += i
			k = k.split(",")
			for x in range(0,n * 14,14):
				arr = k[x:x+14]
				val = is_valid_email(arr[10])
				if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', arr[13]):			
					if val is True:
						if arr[11].isdigit() and arr[12].isdigit():
							#try:
								p = Students(arr[0],arr[1],arr[2],arr[3],arr[4],arr[5],arr[6],arr[7],arr[8],arr[9],arr[10],arr[11],arr[12],arr[13],sclid)
								request.dbsession.add(p)
								transaction.commit()
						else:
							err = "mobile number and income must be an integer !"
							return Response(render('../templates/admin-students.jinja2',{'k':arr,'classes':d,'sections':sect,'subjects':sub,'err':err},request=request))							
					else:
						err = "Invalid email !"
						return Response(render('../templates/admin-students.jinja2',{'k':arr,'classes':d,'sections':sect,'subjects':sub,'err':err},request=request))
				else:
					err = "Password must be 8 characters long and contain a capital letter,small letter ,a number and a special character !"
					return Response(render('../templates/admin-students.jinja2',{'k':arr,'classes':d,'sections':sect,'subjects':sub,'err':err},request=request))					
			s = request.dbsession.query(Students).filter(Students.schoolid == sclid)
			for i in s:
				name += i.name.replace(" ","_") + ','
				rollno += i.rollno.replace(" ","_") + ','
				regno += i.regno.replace(" ","_") + ','
				classname += i.classname.replace(" ","_") + ','
				bday  += i.bday.replace(" ","_") + ','
				sec += i.sec.replace(" ","_") + ','
				subgrp += i.subgrp.replace(" ","_") + ','
				bldgrp += i.bldgrp.replace(" ","_") + ','
				gender += i.gender.replace(" ","_") + ','
				guardian += i.guardian.replace(" ","_") + ','
				email += i.email.replace(" ","_") + ','
				mobile += str(i.mobile).replace(" ","_") +','
				income += str(i.income).replace(" ","_") +','
				password += i.password +','
			name1 = name[:-1];
			name1 = name.split(',');
			leng = len(name1);				
			return Response(render('../templates/admin-students.jinja2',{'k':arr,'classes':d,'sections':sect,'bday':bday,'subjects':sub,'err':"Data saved sucessfully !",'name':name,'classes':d,'sections':sect,'subjects':sub,'rollno':rollno,'regno':regno,'classname':classname,'sec':sec,'subgrp':subgrp,'bldgrp':bldgrp,'gender':gender,'gaurd':guardian,'email':email,'mobile':mobile,'income':income,'password':password,'len':leng,'sel_class':"All",'sel_sub':'All','sel_sec':'All'},request=request))
		elif request.POST.get('search'):
			sear=request.params['search_name']
			sear='%'+sear+'%'
			r=request.dbsession.query(Students).filter(Students.name.ilike(sear)).all()
			name=''
			rollno=''
			regno =''
			classname =''
			bday  =''
			sec =''
			subgrp =''
			bldgrp =''
			gender =''
			guardian =''
			email =''
			mobile =''
			income =''
			password =''
			for i in r:
				name += i.name.replace(" ","_") + ','
				rollno += i.rollno.replace(" ","_") + ','
				regno += i.regno.replace(" ","_") + ','
				classname += i.classname.replace(" ","_") + ','
				bday  += i.bday.replace(" ","_") + ','
				sec += i.sec.replace(" ","_") + ','
				subgrp += i.subgrp.replace(" ","_") + ','
				bldgrp += i.bldgrp.replace(" ","_") + ','
				gender += i.gender.replace(" ","_") + ','
				guardian += i.guardian.replace(" ","_") + ','
				email += i.email.replace(" ","_") + ','
				mobile += str(i.mobile).replace(" ","_") +','
				income += str(i.income).replace(" ","_") +','
				password += i.password +','
			name1 = name[:-1];
			name1 = name.split(',');
			leng = len(name);
			if leng==0:
				return Response(render('../templates/admin-students.jinja2',{'k':arr,'classes':d,'sections':sect,'bday':bday,'subjects':sub,'err':"Data not Found!",'name':name,'classes':d,'sections':sect,'subjects':sub,'rollno':rollno,'regno':regno,'classname':classname,'sec':sec,'subgrp':subgrp,'bldgrp':bldgrp,'gender':gender,'gaurd':guardian,'email':email,'mobile':mobile,'income':income,'password':password,'len':leng,'sel_class':"All",'sel_sub':'All','sel_sec':'All'},request=request))
			else:
				return Response(render('../templates/admin-students.jinja2',{'k':arr,'classes':d,'sections':sect,'bday':bday,'subjects':sub,'name':name,'classes':d,'sections':sect,'subjects':sub,'rollno':rollno,'regno':regno,'classname':classname,'sec':sec,'subgrp':subgrp,'bldgrp':bldgrp,'gender':gender,'gaurd':guardian,'email':email,'mobile':mobile,'income':income,'password':password,'len':leng,'sel_class':"All",'sel_sub':'All','sel_sec':'All'},request=request))
		elif request.POST.get('save'):
			sec = ''
			sclid = session['adm_id']
			sub = ''
			name = ''
			rollno = ''
			regno = ''
			d = ''
			sect = ''
			classname = ''	
			subgrp =''
			bldgrp = ''
			gender = ''
			guardian = ''
			email = ''
			mobile = ''
			income = ''
			password = ''
			leng = ''
			cname = ''
			bday = ''
			secnm = ''
			subgroup = ''
			classes = ''
			secs = ''
			subs = ''
			cls = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
			for i in cls:
				d += i.classname.replace(" ","_") + ','
			#d += 'All' + ","
			for i in cls:
				classes += i.classname.replace(" ","_") + ','
			classes = classes[:-1]
			classes = classes.split(",")
			cls = request.dbsession.query(Students.sec).distinct().filter(Students.schoolid == sclid)
			for i in cls:
				sect += i.sec.replace(" ","_") + ','
			#sect += 'All' + ","			
			for i in cls:
				secs += i.sec.replace(" ","_") +','
			secs = secs[:-1]
			secs = secs.split(",")
			cls = request.dbsession.query(Students.subgrp).distinct().filter(Students.schoolid == sclid)
			for i in cls:
				sub += i.subgrp.replace(" ","_") + ','
			#sub += 'All' + ","
			for i in cls:
				subs += i.subgrp.replace(" ","_") +','
			subs = subs[:-1]
			subs = subs.split(",")		
			subgroup = request.params['sel_sub']
			cname = request.params['sel_class']
			secnm = request.params['sel_sec']
			stud = request.dbsession.query(Students)	
			if secnm == 'All' and subgroup == 'All' and cname == 'All':
				classes = ''
				name = ''
				secs = ''
				subs = ''
				d = ''
				sclid = session['adm_id']
				sect = ''
				sub = ''
				cls = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					d += i.classname.replace(" ","_") + ','
				#d += 'All' + ","
				for i in cls:
					classes += i.classname.replace(" ","_") + ','
				classes = classes[:-1]
				classes = classes.split(",")
				cls = request.dbsession.query(Students.sec).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					sect += i.sec.replace(" ","_") + ','
				#sect += 'All' + ","				
				for i in cls:
					secs += i.sec.replace(" ","_") +','
				secs = secs[:-1]
				secs = secs.split(",")
				cls = request.dbsession.query(Students.subgrp).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					sub += i.subgrp.replace(" ","_") + ','
				#sub += 'All' + ","
				for i in cls:
					subs += i.subgrp.replace(" ","_") +','
				subs = subs[:-1]
				subs = subs.split(",")						
				result = request.dbsession.query(Students).filter(Students.schoolid == sclid)	
				for i in result:
						name += i.name.replace(" ","_") + ','
						rollno += i.rollno.replace(" ","_") + ','
						regno += i.regno.replace(" ","_") + ','
						classname += i.classname.replace(" ","_") + ','
						sec += i.sec.replace(" ","_") + ','
						subgrp += i.subgrp.replace(" ","_") + ','
						bldgrp += i.bldgrp.replace(" ","_") + ','
						bday += i.bday.replace(" ","_") + ','
						gender += i.gender.replace(" ","_") + ','
						guardian += i.guardian.replace(" ","_") + ','
						email += i.email.replace(" ","_") + ','
						mobile += str(i.mobile).replace(" ","_") +','
						income += str(i.income).replace(" ","_") +','
						password += i.password +','
				leng = len(name)
				return Response(render('../templates/admin-students.jinja2',{'sel_class':cname,'sel_sub':subgroup,'sel_sec':secnm,'name':name,'classes':d,'sections':sect,'subjects':sub,'rollno':rollno,'regno':regno,'classname':classname,'sec':sec,'subgrp':subgrp,'bldgrp':bldgrp,'gender':gender,'gaurd':guardian,'email':email,'mobile':mobile,'income':income,'password':password,'len':leng,'bday':bday},request=request))		
			elif secnm == 'All' and subgroup == 'All' and cname != 'All':
				stud = request.dbsession.query(Students)
				for k in secs:
					for j in subs:
						result = stud.filter(and_(Students.subgrp == j.replace("_",""),Students.sec == k,Students.classname == cname,Students.schoolid == sclid)).all()
						try:
							for i in result:
								name += i.name.replace(" ","_") + ','
								rollno += i.rollno.replace(" ","_") + ','
								regno += i.regno.replace(" ","_") + ','
								classname += i.classname.replace(" ","_") + ','
								sec += i.sec.replace(" ","_") + ','
								bday += i.bday.replace(" ","_") + ','
								print('subgrp before space',subgrp)
								subgrp += i.subgrp.replace(" ","_") + ','
								print('subgrp after space',subgrp)
								bldgrp += i.bldgrp.replace(" ","_") + ','
								gender += i.gender.replace(" ","_") + ','
								guardian += i.guardian.replace(" ","_") + ','
								email += i.email.replace(" ","_") + ','
								mobile += str(i.mobile).replace(" ","_") +','
								income += str(i.income).replace(" ","_") +','
								password += i.password +','
						except DBAPIError:
							return Response(db_err_msg, content_type='text/plain', status=500)
				leng = len(name)
				return Response(render('../templates/admin-students.jinja2',{'sel_class':cname,'sel_sub':subgroup,'sel_sec':secnm,'name':name,'classes':d,'sections':sect,'subjects':sub,'rollno':rollno,'regno':regno,'classname':classname,'sec':sec,'subgrp':subgrp,'bldgrp':bldgrp,'gender':gender,'gaurd':guardian,'email':email,'mobile':mobile,'income':income,'password':password,'len':leng,'bday':bday},request=request))							
			elif secnm != 'All' and subgroup == 'All' and cname == 'All':
				classes = ''
				secs = ''
				subs = ''
				d = ''
				sclid = session['adm_id']
				subgroup = request.params['sel_sub']
				cname = request.params['sel_class']
				secnm = request.params['sel_sec']
				sect = ''
				sub = ''				
				cls = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					d += i.classname.replace(" ","_") + ','
				#d += 'All' + ","
				for i in cls:
					classes += i.classname.replace(" ","_") + ','
				classes = classes[:-1]
				classes = classes.split(",")
				cls = request.dbsession.query(Students.sec).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					sect += i.sec + ','
				#sect += 'All' + ","			
				for i in cls:
					secs += i.sec +','
				secs = secs[:-1]
				secs = secs.split(",")
				cls = request.dbsession.query(Students.subgrp).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					sub += i.subgrp.replace(" ","_") + ','
				#sub += 'All' + ","				
				for i in cls:
					subs += i.subgrp.replace(" ","_") +','
				subs = subs[:-1]
				subs = subs.split(",")
				for m in classes:
					for j in subs:
							result = stud.filter(and_(Students.subgrp == j,Students.sec == secnm,Students.classname == m,Students.schoolid == sclid))	
							try:
								for i in result:
									name += i.name.replace(" ","_") + ','
									rollno += i.rollno.replace(" ","_") + ','
									bday += i.bday.replace(" ","_") + ','
									regno += i.regno.replace(" ","_") + ','
									classname += i.classname.replace(" ","_") + ','
									sec += i.sec.replace(" ","_") + ','
									subgrp += i.subgrp.replace(" ","_") + ','
									bldgrp += i.bldgrp.replace(" ","_") + ','
									gender += i.gender.replace(" ","_") + ','
									guardian += i.guardian.replace(" ","_") + ','
									email += i.email.replace(" ","_") + ','
									mobile += str(i.mobile).replace(" ","_") +','
									income += str(i.income).replace(" ","_") +','
									password += i.password +','
							except DBAPIError:
								return Response(db_err_msg, content_type='text/plain', status=500)
				leng = len(name)			
				return Response(render('../templates/admin-students.jinja2',{'sel_class':cname,'sel_sub':subgroup,'sel_sec':secnm,'name':name,'classes':d,'sections':sect,'subjects':sub,'rollno':rollno,'regno':regno,'classname':classname,'sec':sec,'subgrp':subgrp,'bldgrp':bldgrp,'gender':gender,'gaurd':guardian,'email':email,'mobile':mobile,'income':income,'password':password,'len':leng,'bday':bday},request=request))		
			elif secnm == 'All' and subgroup != 'All' and cname == 'All':
				stud = request.dbsession.query(Students)
				classes = ''
				secs = ''
				sclid = session['adm_id']
				subs = ''
				d = ''
				sect = ''
				subgroup = request.params['sel_sub']
				cname = request.params['sel_class']
				secnm = request.params['sel_sec']
				sub = ''				
				cls = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					d += i.classname.replace(" ","_") + ','
				#d += 'All' + ","				
				for i in cls:
					classes += i.classname.replace(" ","_") + ','
				classes = classes[:-1]
				classes = classes.split(",")
				cls = request.dbsession.query(Students.sec).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					sect += i.sec.replace(" ","_") + ','
				#sect += 'All' + ","				
				for i in cls:
					secs += i.sec.replace(" ","_") +','
				secs = secs[:-1]
				secs = secs.split(",")
				cls = request.dbsession.query(Students.subgrp).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					sub += i.subgrp.replace(" ","_") + ','
				#sub += 'All' + ","				
				for i in cls:
					subs += i.subgrp.replace(" ","_") +','
				subs = subs[:-1]
				subs = subs.split(",")
				for m in classes:
					for j in secs:
							result = stud.filter(and_(Students.subgrp == subgroup.replace("_"," "),Students.sec == j.replace("_"," "),Students.classname == m.replace("_"," "),Students.schoolid == sclid))	
							try:
								for i in result:
									name += i.name.replace(" ","_") + ','
									rollno += i.rollno.replace(" ","_") + ','
									regno += i.regno.replace(" ","_") + ','
									classname += i.classname.replace(" ","_") + ','
									sec += i.sec.replace(" ","_") + ','
									bday += i.bday.replace(" ","_") + ','
									subgrp += i.subgrp.replace(" ","_") + ','
									bldgrp += i.bldgrp.replace(" ","_") + ','
									gender += i.gender.replace(" ","_") + ','
									guardian += i.guardian.replace(" ","_") + ','
									email += i.email.replace(" ","_") + ','
									mobile += str(i.mobile).replace(" ","_") +','
									income += str(i.income).replace(" ","_") +','
									password += i.password +','
							except DBAPIError:
								return Response(db_err_msg, content_type='text/plain', status=500)
				leng = len(name)
				return Response(render('../templates/admin-students.jinja2',{'sel_class':cname,'sel_sub':subgroup,'sel_sec':secnm,'name':name,'classes':d,'sections':sect,'bday':bday,'subjects':sub,'rollno':rollno,'regno':regno,'classname':classname,'sec':sec,'subgrp':subgrp,'bldgrp':bldgrp,'gender':gender,'gaurd':guardian,'email':email,'mobile':mobile,'income':income,'password':password,'len':leng},request=request))		
			elif secnm == 'All' and subgroup != 'All' and cname != 'All':
				classes = ''
				secs = ''
				subs = ''
				d = ''
				sect = ''
				sub = ''
				sclid = session['adm_id']
				subgroup = request.params['sel_sub']
				cname = request.params['sel_class']
				secnm = request.params['sel_sec']				
				cls = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					d += i.classname.replace(" ","_") + ','
				#d += 'All' + ","
				for i in cls:
					classes += i.classname.replace(" ","_") + ','
				classes = classes[:-1]
				classes = classes.split(",")
				cls = request.dbsession.query(Students.sec).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					sect += i.sec.replace(" ","_") + ','
				#sect += 'All' + ","
				for i in cls:
					secs += i.sec.replace(" ","_") +','
				secs = secs[:-1]
				secs = secs.split(",")
				cls = request.dbsession.query(Students.subgrp).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					sub += i.subgrp.replace(" ","_") + ','
				#sub += 'All' + ","
				for i in cls:
					subs += i.subgrp.replace(" ","_") +','
				subs = subs[:-1]
				subs = subs.split(",")
				for j in secs:
							result = stud.filter(and_(Students.subgrp == subgroup.replace("_"," "),Students.sec == j.replace("_"," "),Students.classname == cname.replace("_"," "),Students.schoolid == sclid))	
							try:
								for i in result:
									name += i.name.replace(" ","_") + ','
									rollno += i.rollno.replace(" ","_") + ','
									regno += i.regno.replace(" ","_") + ','
									bday += i.bday.replace(" ","_") + ','
									classname += i.classname.replace(" ","_") + ','
									sec += i.sec.replace(" ","_") + ','
									subgrp += i.subgrp.replace(" ","_") + ','
									bldgrp += i.bldgrp.replace(" ","_") + ','
									gender += i.gender.replace(" ","_") + ','
									guardian += i.guardian.replace(" ","_") + ','
									email += i.email.replace(" ","_") + ','
									mobile += str(i.mobile).replace(" ","_") +','
									income += str(i.income).replace(" ","_") +','
									password += i.password +','
							except DBAPIError:
								return Response(db_err_msg, content_type='text/plain', status=500)
				leng = len(name)			
				return Response(render('../templates/admin-students.jinja2',{'sel_class':cname,'sel_sub':subgroup,'bday':bday,'sel_sec':secnm,'name':name,'classes':d,'sections':sect,'subjects':sub,'rollno':rollno,'regno':regno,'classname':classname,'sec':sec,'subgrp':subgrp,'bldgrp':bldgrp,'gender':gender,'gaurd':guardian,'email':email,'mobile':mobile,'income':income,'password':password,'len':leng},request=request))		
			elif secnm != 'All' and subgroup != 'All' and cname == 'All':
				classes = ''
				secs = ''
				subs = ''
				d = ''
				sclid = session['adm_id']
				subgroup = request.params['sel_sub']
				cname = request.params['sel_class']
				secnm = request.params['sel_sec']
				sect = ''
				sub = ''				
				cls = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					d += i.classname.replace(" ","_") + ','
				#d += 'All' + ","
				for i in cls:
					classes += i.classname.replace(" ","_") + ','
				classes = classes[:-1]
				classes = classes.split(",")
				cls = request.dbsession.query(Students.sec).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					sect += i.sec + ','
				#sect += 'All' + ","
				for i in cls:
					secs += i.sec +','
				secs = secs[:-1]
				secs = secs.split(",")
				cls = request.dbsession.query(Students.subgrp).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					sub += i.subgrp.replace(" ","_") + ','
				#sub += 'All' + ","
				for i in cls:
					subs += i.subgrp.replace(" ","_") +','
				subs = subs[:-1]
				subs = subs.split(",")
				for m in classes:
							result = stud.filter(and_(Students.subgrp == subgroup.replace("_"," "),Students.sec == secnm.replace("_"," "),Students.classname == m.replace("_"," "),Students.schoolid == sclid))	
							try:
								for i in result:
									name += i.name.replace(" ","_") + ','
									rollno += i.rollno.replace(" ","_") + ','
									regno += i.regno.replace(" ","_") + ','
									classname += i.classname.replace(" ","_") + ','
									sec += i.sec.replace(" ","_") + ','
									bday += i.bday.replace(" ","_") + ','
									subgrp += i.subgrp.replace(" ","_") + ','
									bldgrp += i.bldgrp.replace(" ","_") + ','
									gender += i.gender.replace(" ","_") + ','
									guardian += i.guardian.replace(" ","_") + ','
									email += i.email.replace(" ","_") + ','
									mobile += str(i.mobile).replace(" ","_") +','
									income += str(i.income).replace(" ","_") +','
									password += i.password +','
							except DBAPIError:
								return Response(db_err_msg, content_type='text/plain', status=500)
				leng = len(name)
				return Response(render('../templates/admin-students.jinja2',{'sel_class':cname,'bday':bday,'sel_sub':subgroup,'sel_sec':secnm,'name':name,'classes':d,'sections':sect,'subjects':sub,'rollno':rollno,'regno':regno,'classname':classname,'sec':sec,'subgrp':subgrp,'bldgrp':bldgrp,'gender':gender,'gaurd':guardian,'email':email,'mobile':mobile,'income':income,'password':password,'len':leng},request=request))		
			elif secnm != 'All' and subgroup == 'All' and cname != 'All':
				classes = ''
				secs = ''
				subs = ''
				sclid = session['adm_id']
				d = ''
				sect = ''
				subgroup = request.params['sel_sub']
				cname = request.params['sel_class']
				secnm = request.params['sel_sec']
				sub = ''				
				cls = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					d += i.classname.replace(" ","_") + ','
				#d += 'All' + ","
				for i in cls:
					classes += i.classname.replace(" ","_") + ','
				classes = classes[:-1]
				classes = classes.split(",")
				cls = request.dbsession.query(Students.sec).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					sect += i.sec.replace(" ","_") + ','
				#sect += 'All' + ","
				for i in cls:
					secs += i.sec.replace(" ","_") +','
				secs = secs[:-1]
				secs = secs.split(",")
				cls = request.dbsession.query(Students.subgrp).distinct().filter(Students.schoolid == sclid)
				for i in cls:
					sub += i.subgrp.replace(" ","_") + ','
				#sub += 'All' + ","
				for i in cls:
					subs += i.subgrp.replace(" ","_") +','
				subs = subs[:-1]
				subs = subs.split(",")
				for j in subs:
							result = stud.filter(and_(Students.subgrp == j.replace("_"," "),Students.sec == secnm.replace("_"," "),Students.classname == cname.replace("_"," "),Students.schoolid == sclid))	
							try:
								for i in result:
									name += i.name.replace(" ","_") + ','
									rollno += i.rollno.replace(" ","_") + ','
									regno += i.regno.replace(" ","_") + ','
									classname += i.classname.replace(" ","_") + ','
									sec += i.sec.replace(" ","_") + ','
									bday += i.bday.replace(" ","_") + ','
									subgrp += i.subgrp.replace(" ","_") + ','
									bldgrp += i.bldgrp.replace(" ","_") + ','
									gender += i.gender.replace(" ","_") + ','
									guardian += i.guardian.replace(" ","_") + ','
									email += i.email.replace(" ","_") + ','
									mobile += str(i.mobile).replace(" ","_") +','
									income += str(i.income).replace(" ","_") +','
									password += i.password +','
							except DBAPIError:
								return Response(db_err_msg, content_type='text/plain', status=500)
				leng = len(name)
				return Response(render('../templates/admin-students.jinja2',{'sel_class':cname,'sel_sub':subgroup,'bday':bday,'sel_sec':secnm,'name':name,'classes':d,'sections':sect,'subjects':sub,'rollno':rollno,'regno':regno,'classname':classname,'sec':sec,'subgrp':subgrp,'bldgrp':bldgrp,'gender':gender,'gaurd':guardian,'email':email,'mobile':mobile,'income':income,'password':password,'len':leng},request=request))		
			else:
				stud = request.dbsession.query(Students);
				sclid = session['adm_id']
				subgroup = request.params['sel_sub']
				cname = request.params['sel_class']
				secnm = request.params['sel_sec']
				result = stud.filter(and_(Students.subgrp == subgroup.replace("_"," "),Students.sec == secnm.replace("_"," "),Students.classname == cname.replace("_"," "),Students.schoolid == sclid))	
				try:
					for i in result:
						name += i.name.replace(" ","_") + ','
						rollno += i.rollno.replace(" ","_") + ','
						regno += i.regno.replace(" ","_") + ','
						classname += i.classname.replace(" ","_") + ','
						sec += i.sec.replace(" ","_") + ','
						subgrp += i.subgrp.replace(" ","_") + ','
						bldgrp += i.bldgrp.replace(" ","_") + ','
						gender += i.gender.replace(" ","_") + ','
						guardian += i.guardian.replace(" ","_") + ','
						email += i.email.replace(" ","_") + ','
						mobile += str(i.mobile).replace(" ","_") +','
						bday += i.bday.replace(" ","_") + ','
						income += str(i.income).replace(" ","_") +','
						password += i.password +','
				except DBAPIError:
					return Response(db_err_msg, content_type='text/plain', status=500)
				leng = len(name)
				return Response(render('../templates/admin-students.jinja2',{'sel_class':cname,'bday':bday,'sel_sub':subgroup,'sel_sec':secnm,'name':name,'classes':d,'sections':sect,'subjects':sub,'rollno':rollno,'regno':regno,'classname':classname,'sec':sec,'subgrp':subgrp,'bldgrp':bldgrp,'gender':gender,'gaurd':guardian,'email':email,'mobile':mobile,'income':income,'password':password,'len':leng},request=request))		
			return Response(render('../templates/admin-students.jinja2',{'sel_class':cname,'bday':bday,'sel_sub':subgroup,'sel_sec':secnm,'name':name,'classes':d,'sections':sect,'subjects':sub,'rollno':rollno,'regno':regno,'classname':classname,'sec':sec,'subgrp':subgrp,'bldgrp':bldgrp,'gender':gender,'gaurd':guardian,'email':email,'mobile':mobile,'income':income,'password':password,'len':leng},request=request))		
		return {'name':name,'classes':d,'sections':sect,'subjects':sub,'rollno':rollno,'bday':bday,'regno':regno,'classname':classname,'sec':sec,'subgrp':subgrp,'bldgrp':bldgrp,'gender':gender,'gaurd':guardian,'email':email,'mobile':mobile,'income':income,'password':password,'len':leng}
	except KeyError:
		return Response(keyerr, content_type='text/plain', status=500)

@view_config(route_name='admin-students-json', renderer='json')
def admin_students_json(request):
	name = request.dbsession.query(Students.name).all()
	return {'name':name}


@view_config(route_name='admin-create',renderer='../templates/admin-create.jinja2')
def admin_create(request):
	try:
		if request.POST.get('submit'):
			schoolname = request.params['schoolname']
			username = request.params['username']
			password = request.params['password']
			adm = request.dbsession.query(Admin)
			for i in adm:
				if i.username == username:
					return Response(render('../templates/admin-create.jinja2',{'exist_err':'User already exists !'},request=request))
				for i in adm:
					if i.schoolname == schoolname:
						return Response(render('../templates/admin-create.jinja2',{'exist_err':'School name already exists !'},request=request))
			if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
				admin = Admin()
				admin.username = username
				admin.password = password
				admin.schoolname = schoolname
				request.dbsession.add(admin)
				return Response(render('../templates/index-sign-in.jinja2',{},request=request))
			else:
				return Response(render('../templates/admin-create.jinja2',{'exist_err':'Password must be 8 characters long and contain a uppercase,lowercase,special character,and a number !'},request=request))
		else:  
			return {}		
	except KeyError:
		return Response(keyerr, content_typesignin='text/plain', status=500)
@view_config(route_name='index-get-started',renderer='../templates/index-get-started.jinja2')
def index_get_started(request):
        return {}

@view_config(route_name='index-sign-in',renderer='../templates/index-sign-in.jinja2')
def index_sign_in(request):
	try:
		if request.POST.get('signin'):
			stud = request.dbsession.query(Students)
			prof = request.dbsession.query(Professors)
			admin = request.dbsession.query(Admin)
			x = request.params['username']
			z = request.params['password']
			y = request.params['schoolname']
			for n in stud:
				if n.email == x and n.password == z :
					session = request.session
					session['username'] = x
					session['type'] = "student"
					session['stud_id'] = n.id
					return Response(render('../templates/student-chapters.jinja2',{},request=request))
			for n in prof:
				if n.email == x and n.password == z:
					session = request.session
					session['username'] = x
					session["type"] = "professor"
					session['prof_id'] = n.id
					avg = 0
					profid = session['prof_id']
					ans = request.dbsession.query(Professors).filter(Professors.id  == profid)
					for i in ans:
						sclid = i.schoolid 
					mark = request.dbsession.query(UpdateMark)
					sec = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
					s = ''
					for i in sec:
						s += i.classname.replace(' ','_') + ","
					sub = ''
					subject = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
					for i in subject:
						sub += i.subject.replace(' ','_') + ","
					return Response(render('../templates/professor-chapters.jinja2',{'classes':s,'subjects':sub},request=request))
			for n in admin:
				if n.username == x and n.schoolname == y and n.password == z:
					session = request.session
					session['username'] = x
					session["type"] = "admin"
					session['adm_id'] = n.id
					return Response(render('../templates/admin-snapshot.jinja2',{'session':session},request=request))
			return Response(render('../templates/index-sign-in.jinja2',{'error':'Username or password is incorrect !'},request=request))
		else:
			return {} 
	except KeyError:
		return Response(keyerr, content_type='text/plain', status=500)

@view_config(route_name='professor-chapters',renderer='../templates/professor-chapters.jinja2')
def professor_chapters(request):
	try:
		session = request.session
		clsnm = ''
		subchap = ''
		subnm = ''
		classes = ''
		subs = ''
		arr = ''
		item = []
		marks = []
		s = ''
		sclid = ''
		c = ''
		total = ''
		m = ''
		err = ''
		tot = []
		r = ''
		sc = ''
		finaltot = 0
		finalavg = 0
		def get_first_mode(a):
			c = Counter(a)  
			mode_count = max(c.values())
			mode = {key for key, count in c.items() if count == mode_count}
			first_mode = next(x for x in a if x in mode)
			return first_mode
		avg = 0
		profid = session['prof_id']
		ans = request.dbsession.query(Professors).filter(Professors.id  == profid)
		for i in ans:
			sclid = i.schoolid 
		mark = request.dbsession.query(UpdateMark)
		sec = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
		for i in sec:
			s += i.classname.replace(' ','_') + ","
		sub = ''
		subject = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
		for i in subject:
			sub += i.subject.replace(' ','_') + ","
		if request.POST.get('save'):
			subchap = ''
			chapters = ['']
			m = 0
			total = 0
			mark = request.dbsession.query(UpdateMark)
			syll = request.dbsession.query(Syllabus)
			clsnm = request.params['sel_class']	
			subnm = request.params['sel_sub']
			sampnm = request.params['sel_samp']
			meanm = request.params['sel_mea']
			if subnm == 'All':
				for j in subs:
					subchaps = []
					tot = 0
					cnt = 0
					arr = ''
					r = ''
					stu = []
					item = []
					mark = request.dbsession.query(UpdateMark)
					if sampnm == 'Board':
						result = mark.filter(and_(UpdateMark.classname == clsnm,UpdateMark.subject == j))
						r = mark.filter(and_(UpdateMark.classname == clsnm,UpdateMark.subject == j)).first()
						if r is None:
							err = "No data found !"
						else:
							for i in result:
								if i.subchapter in subchaps:
									pass
								else:
									subchaps.append(i.subchapter)
							for k in subchaps:
								r = mark.filter(UpdateMark.subchapter == k)
								check = mark.filter(UpdateMark.subchapter == k).first()
								if check is None:
									pass
								else:
									for y in r:
										tot += y.mark
										median  += str(y.mark) + ","
										if y.studnm in stu :
											pass
										else:
											stu.append(y.studnm)
									median = median[:-1]
									median = median.split(",")
									cnt = len(stu)
									avg = tot/cnt
									rnk = list(map(int,median))
									if meanm == 'Average':
										arr = k + "," + str(tot) + "," + str(tot/cnt) + ","
										finaltot += tot
										finalavg += avg
									elif meanm == 'Median':
										arr = k + "," + str(tot) + "," + str(statistics.median(rnk)) + ","
										finaltot += tot
										finalavg += avg
									elif meanm == 'Mode':
										arr = k + "," + str(tot) + "," + str(get_first_mode(median)) + ","
										finaltot += tot
										finalavg += avg
									elif meanm == 'Percentile':
										arr = k + "," + str(tot) + "," + str(tot/100) + ","
										finaltot += tot
										finalavg += avg
									arr = arr[:-1]
									arr = arr.split(",")
									item.append(arr)
									tot = 0
					elif sampnm == 'School':
							result = mark.filter(and_(UpdateMark.classname == clsnm,UpdateMark.subject == j,UpdateMark.schoolid == sclid))
							r = mark.filter(and_(UpdateMark.classname == clsnm,UpdateMark.subject == j)).first()
							if r is None:
								err = "No data found !"							
							else:
								for i in result:
									if i.subchapter in subchaps:
										pass
									else:
										subchaps.append(i.subchapter)
								for k in subchaps:
									r = mark.filter(UpdateMark.subchapter == k)
									for y in r:
										tot += y.mark
										median  += str(y.mark) + ","
										if(y.studnm in stu):
											pass
										else:
											stu.append(y.studnm)
									median = median[:-1]
									median = median.split(",")
									cnt = len(stu)
									avg = tot/cnt
									if meanm == 'Average':
										arr = k + "," + str(tot) + "," + str(tot/cnt) + ","
										finaltot += tot
										finalavg += avg
									elif meanm == 'Median':
										arr = k + "," + str(tot) + "," + statistics.median(median) + ","
										finaltot += tot
										finalavg += avg
									elif meanm == 'Mode':
										arr = k + "," + str(tot) + "," + statistics.mode(median) + ","
										finaltot += tot
										finalavg += avg
									elif meanm == 'Percentile':
										arr = k + "," + str(tot) + "," + tot/100 + ","
										finaltot += tot
										finalavg += avg
									arr = arr[:-1]
									arr = arr.split(",")
									item.append(arr)
									tot = 0						
				return {'classes':s,'subjects':sub,'sel_class':clsnm,'res':item,'sel_sub':subnm,'sel_samp':sampnm,'sel_mea':meanm,'err':err}
			elif clsnm == 'All':
				for j in classes:
					subchaps = []
					tot = 0
					cnt = 0
					arr = ''
					r = ''
					stu = []
					item = []
					mark = request.dbsession.query(UpdateMark)
					if sampnm == 'Board':
						result = mark.filter(and_(UpdateMark.classname == j,UpdateMark.subject == subnm))
						r = mark.filter(and_(UpdateMark.classname == clsnm,UpdateMark.subject == j)).first()
						if r is None:
							err = "No data found !"
						else:
							for i in result:
								if i.subchapter in subchaps :
									pass
								else:
									subchaps.append(i.subchapter)
							for k in subchaps:
								r = mark.filter(UpdateMark.subchapter == k)
								try:
									for y in r:
										tot += y.mark
										if(y.studnm in stu):
											pass
										else:
											stu.append(y.studnm)
									cnt = len(stu)
									avg = tot/cnt
									arr = k + "," + str(tot) + "," + str(tot/cnt) + ","
									finaltot += tot
									finalavg += avg
									arr = arr[:-1]
									arr = arr.split(",")
									item.append(arr)
									tot = 0
								except DBAPIError:
									return Response(db_err_msg, content_type='text/plain', status=500)
					elif sampnm == 'School':
						result = mark.filter(and_(UpdateMark.classname == j,UpdateMark.subject == subnm,UpdateMark.schoolid == sclid))
						r = mark.filter(and_(UpdateMark.classname == clsnm,UpdateMark.subject == j)).first()
						if r is None:
							err = "No data found !"
						else:
							for i in result:
								if i.subchapter in subchaps :
									pass
								else:
									subchaps.append(i.subchapter)
							for k in subchaps:
								r = mark.filter(UpdateMark.subchapter == k)
								try:
									for y in r:
										tot += y.mark
										if(y.studnm in stu):
											pass
										else:
											stu.append(y.studnm)
									cnt = len(stu)
									avg = tot/cnt
									arr = k + "," + str(tot) + "," + str(tot/cnt) + ","
									finaltot += tot
									finalavg += avg
									arr = arr[:-1]
									arr = arr.split(",")
									item.append(arr)
									tot = 0
								except DBAPIError:
									return Response(db_err_msg, content_type='text/plain', status=500)										
				return {'classes':s,'subjects':sub,'sel_class':clsnm,'res':item,'sel_sub':subnm,'sel_samp':sampnm,'sel_mea':meanm,'err':err}
			elif subnm == 'All' and clsnm == 'All':
				for i in classes:
					for j in subs:
						subchaps = []
						tot = 0
						cnt = 0
						arr = ''
						r = ''
						stu = []
						item = []
						mark = request.dbsession.query(UpdateMark)
						if sampnm == 'Board':
							result = mark.filter(and_(UpdateMark.classname == i,UpdateMark.subject == j))
							r = mark.filter(and_(UpdateMark.classname == clsnm,UpdateMark.subject == j)).first()
							if r is None:
								err = "No data found !"
							else:							
								for i in result:
									if i.subchapter in subchaps:
										pass
									else:
										subchaps.append(i.subchapter)
								for k in subchaps:
									r = mark.filter(UpdateMark.subchapter == k)
									try:
										for y in r:
											tot += y.mark
											if(y.studnm in stu):
												pass
											else:
												stu.append(y.studnm)
										cnt = len(stu)
										avg = tot/cnt
										arr = k + "," + str(tot) + "," + str(tot/cnt) + ","
										finaltot += tot
										finalavg += avg
										arr = arr[:-1]
										arr = arr.split(",")
										item.append(arr)
										tot = 0
									except DBAPIError:
										return Response(db_err_msg, content_type='text/plain', status=500)
						elif sampnm == 'School':
							result = mark.filter(and_(UpdateMark.classname == j,UpdateMark.subject == subnm,UpdateMark.schoolid == sclid))
							r = mark.filter(and_(UpdateMark.classname == clsnm,UpdateMark.subject == subnm,UpdateMark.schoolid == sclid)).first()
							if r is None:
								err = "No data found !"
							else:
								for i in result:
									if i.subchapter in subchaps :
										pass
									else:
										subchaps.append(i.subchapter)
								for k in subchaps:
									r = mark.filter(UpdateMark.subchapter == k)
									try:
										for y in r:
											tot += y.mark
											if(y.studnm in stu):
												pass
											else:
												stu.append(y.studnm)
										cnt = len(stu)
										avg = tot/cnt
										arr = k + "," + str(tot) + "," + str(tot/cnt) + ","
										finaltot += tot
										finalavg += avg
										arr = arr[:-1]
										arr = arr.split(",")
										item.append(arr)
										tot = 0
									except DBAPIError:
										return Response(db_err_msg, content_type='text/plain', status=500)
				return {'classes':s,'subjects':sub,'sel_class':clsnm,'res':item,'sel_sub':subnm,'sel_samp':sampnm,'sel_mea':meanm,'err':err}
			else:	
				subchaps = []
				tot = 0
				cnt = 0
				arr = ''
				r = ''
				stu = []
				item = []
				mark = request.dbsession.query(UpdateMark)
				if sampnm == 'Board':
					result = mark.filter(and_(UpdateMark.classname == clsnm,UpdateMark.subject == subnm))
					r = mark.filter(and_(UpdateMark.classname == clsnm,UpdateMark.subject == subnm)).first()
					if r is None:
						err = "No data found !"				
					else:
						for i in result:
							if i.subchapter in subchaps:
								pass
							else:
								subchaps.append(i.subchapter)
						for k in subchaps:
							r = mark.filter(UpdateMark.subchapter == k)
							try:
								for y in r:
									tot += y.mark
									if(y.studid in stu):
										pass
									else:
										stu.append(y.studid)
								cnt = len(stu)
								avg = tot/cnt
								arr = k + "," + str(tot) + "," + str(tot/cnt) + ","
								finaltot += tot
								finalavg += avg
								arr = arr[:-1]
								arr = arr.split(",")
								item.append(arr)
								tot = 0
							except DBAPIError:
								return Response(db_err_msg, content_type='text/plain', status=500)
				elif sampnm == 'School':
					result = mark.filter(and_(UpdateMark.classname == clsnm,UpdateMark.subject == subnm,UpdateMark.schoolid == sclid))
					r = mark.filter(and_(UpdateMark.classname == clsnm,UpdateMark.subject == subnm,UpdateMark.schoolid == sclid)).first()
					if r is None:
						err = "No data found !"				
					else:
						for i in result:
							if i.subchapter in subchaps:
								pass
							else:
								subchaps.append(i.subchapter)
						for k in subchaps:
							r = mark.filter(UpdateMark.subchapter == k)
							try:
								for y in r:
									tot += y.mark
									if(y.studid in stu):
										pass
									else:
										stu.append(y.studid)
								cnt = len(stu)
								avg= tot/cnt
								arr = k + "," + str(tot) + "," + str(tot/cnt) + ","
								finaltot += tot
								finalavg += avg
								arr = arr[:-1]
								arr = arr.split(",")
								item.append(arr)
								tot = 0
							except DBAPIError:
								return Response(db_err_msg, content_type='text/plain', status=500)					
				return {'classes':s,'subjects':sub,'sel_class':clsnm,'res':item,'sel_sub':subnm,'sel_samp':sampnm,'sel_mea':meanm,'err':err}				
			return {'classes':s,'subjects':sub,'sel_class':clsnm,'res':item,'sel_sub':subnm,'sel_samp':sampnm,'sel_mea':meanm,'err':err}
		return {'classes':s,'subjects':sub}
	except KeyError:
		return Response(keyerr, content_type='text/plain', status=500)
@view_config(route_name='professor-create',renderer='../templates/professor-create.jinja2')
def professor_create(request):
		s = ' ' + ","
		q = ' ' + ","
		session = request.session
		items = []
		classes = ''
		sub =' ' +","
		subs= ''
		res = ''
		secs =''
		selcls = ''
		s = ' ' + ","
		selsub = ''
		subname = ''
		que = request.dbsession.query(Questions)
		syl = request.dbsession.query(Syllabus)
		profid = session['prof_id']
		ans = request.dbsession.query(Professors).filter(Professors.id  == profid)
		for i in ans:
			sclid = i.schoolid 		
		studs = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid  == sclid)
		print("///////////////////////\n//classname///////////////////////////\n")
		for i in studs:
			s += i.classname.replace(" ","_") + ","
			print(i)
		studs = request.dbsession.query(Students.sec).distinct().filter(Students.schoolid == sclid)
		for i in studs:
			q += i.sec.replace(" ","_") + ","
		staffs = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
		for i in staffs:
			sub += i.subject.replace(" ","_") + ","
		studs = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)		
		for i in studs:
			classes += i.classname + ','
		classes = classes[:-1]
		classes = classes.split(",")
		staffs = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
		for i in staffs:
			subs += i.subject + ','
		subs = subs[:-1]
		subs = subs.split(",")
		studs = request.dbsession.query(Students.sec).distinct().filter(Students.schoolid == sclid)		
		for i in studs:
			secs += i.sec +','
		secs = secs[:-1]
		secs = secs.split(",")	
		if request.POST.get('save'):
			selcls = ''
			selsub = ''
			selsec = ''
			selcls = request.params['sel_class'].replace("_"," ")
			selsub = request.params['sel_sub'].replace("_"," ")
			selsec = request.params['sel_sec'].replace("_"," ")
			result = syl.filter(and_(Syllabus.classname == selcls,Syllabus.subject == selsub,Syllabus.schoolid == sclid))
			try:
				for k in result:
					res += k.subchapter.replace(" ","_") + ','
				qno = ''
				total = ''
				return {'sel_class':selcls.replace(" ","_"),'sel_sub':selsub.replace(" ","_"),'sel_sec':selsec.replace(" ","_"),'classes':s,'subjects':sub,'sections':q,'res':res}
			except DBAPIError:
				return Response(db_err_msg, content_type='text/plain', status=500)		
		elif request.POST.get('savedata'):
			total = ''
			totques = 0
			err = ''
			noofsecs = ''
			subnm = request.params['sel_sub']
			cls = request.params['sel_class']
			sec = request.params['sel_sec']
			test = request.params['testname']
			date = request.params['testdate']
			maxque = request.params['maxque']
			duration = request.params['duration']
			noofsec = request.params['noofsec']
			papername = test + '-' + cls +'-' + subnm
			noofsec = int(noofsec)
			for i in range(noofsec):
				qid = 'questions'+str(i+1)
				noofques = request.params[qid]
				noofques = int(noofques)
				totques += noofques
				total += str(noofques) + ','
				for j in range(noofques):
					quesid = 'ques'+str(str(i+1) + str(j+1))
					desc = request.params[quesid]
					qno = str(i +1)+'.'+str(j +1)
					optid = 'linksc'+str(i+1)+str(j+1)
					mrkid = 'marks'+str(i+1)+str(j+1)
					opt = request.params[optid]
					mrk = request.params[mrkid]
					try:
						if mrk.isdigit() and maxque.isdigit() and duration.isdigit():
							p = Questions(desc,opt,i+1,papername,qno,subnm,cls,test,date,maxque,duration,noofsec,total,sclid,profid,int(mrk))
							request.dbsession.add(p)
							transaction.commit() 
							total = total[:-1]
						else:
							err= "No of sec,marks,Max ques,duration must be integer !"
							return {'nos':noofsec,'total':total,'classes':s,'subjects':sub,'sections':q,'err':err}
					except ValueError:						
							err = "Invalid date value .Date must be in dd/mm/yy format!"
							return {'nos':noofsec,'total':total,'classes':s,'subjects':sub,'sections':q,'err':err}
			return {'nos':noofsec,'total':total,'classes':s,'subjects':sub,'sections':q,'err':'Question paper created !'}
		return {'classes':s,'subjects':sub,'sections':q,'res':res}
@view_config(route_name='professor-drive',renderer='../templates/professor-drive.jinja2')
def professor_drive(request):
	try:
		s = ' ' + ","
		session = request.session
		sub = ' ' + ","
		testname = []
		item=[]
		subnm = ''
		cls = ''
		arr=''
		profid = session['prof_id']
		ans = request.dbsession.query(Professors).filter(Professors.id  == profid)
		for i in ans:
			sclid = i.schoolid 		
		studs = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
		for i in studs:
			s += i.classname + ","
		staffs = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
		for i in staffs:
			sub += i.subject + ","
		if request.POST.get('save'):	
			subnm = request.params['sel_sub']
			cls = request.params['sel_class']
			if subnm == 'All':
				pass
			else:
				#arr = ''
				#item = []
				qp = request.dbsession.query(Questions.papernm).distinct()
				query = request.dbsession.query(Questions).filter(and_(Questions.classname == cls,Questions.subject == subnm,Questions.schoolid == sclid,Questions.profid == profid))
				for i in qp:
					res = request.dbsession.query(Questions).filter(and_(Questions.classname == cls,Questions.subject == subnm,Questions.schoolid == sclid,Questions.profid == profid,Questions.papernm == i.papernm)).first()
					if res is None:
						res = "no element"
					else:
							arr = res.testname + "," + res.doe + "," + res.subject + "," + str(res.maxques) + "," + str(res.duration) + ","
							arr = arr[:-1]
							arr = arr.split(",")
							item.append(arr)
				return {'classes':s,'subjects':sub,'res':zip(item,query),'sel_sub':subnm,'sel_class':cls,'qp':qp}
		return {'classes':s,'subjects':sub,'sel_sub':subnm,'sel_class':cls}
	except KeyError:
		return Response(keyerr, content_type='text/plain', status=500)
@view_config(route_name='professor-questions',renderer='../templates/professor-questions.jinja2')
def professor_questions(request):
	try:
		clsnm = ''
		subchap = ''
		subnm = ''
		classes = ''
		avg = 0
		cnt = 0
		mrk = 0
		subs = ''
		arr = ''
		item = []
		s = ''
		err = ''
		final_tot = 0
		final_avg = 0
		c = ''
		q = ''
		mea = ''
		syll = ''
		qps = ''
		qql=''
		sc = ''
		subjects = []
		session = request.session
		profid = session['prof_id']
		qlist=request.dbsession.query(Questions).all()
		for i in qlist:
			qql += i.questiondesc.replace(' ','_') + ","
		print("start--------=-=-=-=-=-=-=--=-==--=-=-=-=---------------------------")
		print(qql)
		print("stop--------=-=-=-=-=-=-=--=-==--=-=-=-=---------------------------")
		ans = request.dbsession.query(Professors).filter(Professors.id  == profid)
		for i in ans:
			sclid = i.schoolid 
		sec = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
		for i in sec:
			s += i.classname.replace(' ','_') + ","
		sub = ''
		subject = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
		for j in subject:
			sub += j.subject.replace(' ','_') + ","
		ques = request.dbsession.query(Questions.papernm).distinct().filter(Questions.schoolid == sclid)
		for i in ques:
			qps += i.papernm + ","
		
		for i in sec:
			classes += i.classname + ','
		classes = classes[:-1]
		classes = classes.split(",")
		for i in subject:
			subs += i.subject + ','
		subs = subs[:-1]
		subs = subs.split(",")
		if request.POST.get('save'):	
			qps = ''
			clsnm = request.params['sel_class']	
			subnm = request.params['sel_sub']
			quesnm = request.params['sel_ques']
			mea = request.params['sel_mea']
			questions = request.dbsession.query(Questions.papernm).distinct().filter(Questions.schoolid==sclid)
			for i in questions:
				qps += i.papernm + ','
			if subnm == 'All':
				q = request.dbsession.query(Questions)
				mark = request.dbsession.query(UpdateMark)
				for j in subs:
					res = q.filter(and_(Questions.classname == clsnm,Questions.subject == j,Questions.schoolid == sclid,Questions.papernm == quesnm))
					m = mark.filter(and_(UpdateMark.classname == clsnm,UpdateMark.subject == j,UpdateMark.schoolid == sclid,UpdateMark.paperid == quesnm))
					for i in res:
							r = m.filter(UpdateMark.qno == i.qno)
							cnt = r.count()
							if cnt != 0:
								for l in r:
									mrk += l.mark
								avg = mrk/cnt
								arr = i.subchapter.replace(" ","_") + ',' + i.qno.replace(" ","_") + ',' + i.questiondesc.replace(" ","_") + ',' + str(mrk).replace(" ","_") + ',' + str(i.mark).replace(" ","_") + "," + str(mrk/cnt).replace(" ","_") + ","
								final_tot += mrk
								final_avg += avg
								arr = arr[:-1]
								arr = arr.split(",")
								item.append(arr)	
								mrk = 0	
							else:
								err ="No data found !"	
				return {'qql':qql,'classes':s,'subjects':sub,'res':item,'sel_class':clsnm,'sel_sub':subnm,'sel_mea':mea,'err':err,'ques':qps,'sel_ques':quesnm}
			elif clsnm == 'All':
				qps = ''
				ques = request.dbsession.query(Questions.papernm).distinct().filter(Questions.schoolid == sclid)
				for i in ques:
					qps += i.papernm + ","
				q = request.dbsession.query(Questions)
				mark = request.dbsession.query(UpdateMark)
				for i in classes:
					res = q.filter(and_(Questions.classname == i,Questions.subject == subnm,Questions.schoolid == sclid,Questions.papernm == quesnm))
					m = mark.filter(and_(UpdateMark.classname == i,UpdateMark.subject == subnm,UpdateMark.schoolid == sclid,UpdateMark.paperid == quesnm))
					for i in res:
							r = m.filter(UpdateMark.qno == i.qno)
							cnt = r.count()
							if cnt != 0:
								for l in r:
									mrk += l.mark
								arr = i.subchapter.replace(" ","_") + ',' + i.qno.replace(" ","_") + ',' + i.questiondesc.replace(" ","_") + ',' + str(mrk).replace(" ","_") + ',' + str(i.mark).replace(" ","_") + "," + str(mrk/cnt).replace(" ","_") + ","
								final_tot += mrk
								final_avg += avg								
								arr = arr[:-1]
								arr = arr.split(",")
								item.append(arr)	
								mrk = 0	
							else:
								err = "No data found !"	
				return {'qql':qql,'classes':s,'subjects':sub,'res':subchap,'sel_class':clsnm,'sel_sub':subnm,'sel_mea':mea,'err':err,'ques':qps,'sel_ques':quesnm}
			elif subnm == 'All' and clsnm == 'All':
				qps = ''
				ques = request.dbsession.query(Questions.papernm).distinct().filter(Questions.schoolid == sclid)
				for i in ques:
					qps += i.papernm + ","
				q = request.dbsession.query(Questions)
				mark = request.dbsession.query(UpdateMark)
				for i in classes:
					for j in subs:
						res = q.filter(and_(Questions.classname == i,Questions.subject == j,Questions.schoolid == sclid,Questions.papernm == quesnm))
						m = mark.filter(and_(UpdateMark.classname == i,UpdateMark.subject == j,UpdateMark.schoolid == sclid,UpdateMark.paperid == quesnm))
						for i in res:
								r = m.filter(UpdateMark.qno == i.qno)
								cnt = r.count()
								if cnt != 0:
									for l in r:
										mrk += l.mark
									arr = i.subchapter.replace(" ","_") + ',' + i.qno.replace(" ","_") + ',' + i.questiondesc.replace(" ","_") + ',' + str(mrk).replace(" ","_") + ','  + str(i.mark).replace(" ","_") + "," + str(mrk/cnt).replace(" ","_") + ","
									final_tot += mrk
									final_avg += avg									
									arr = arr[:-1]
									arr = arr.split(",")
									item.append(arr)	
									mrk = 0	
								else:
									err = "No data found !"	
				return {'qql':qql,'classes':s,'subjects':sub,'res':item,'sel_class':clsnm,'sel_sub':subnm,'sel_mea':mea,'err':err,'ques':qps,'sel_ques':quesnm}
			else:
				qps = ''
				ques = request.dbsession.query(Questions.papernm).distinct().filter(Questions.schoolid == sclid)
				for i in ques:
					qps += i.papernm + ","
				q = request.dbsession.query(Questions)
				mark = request.dbsession.query(UpdateMark)
				chap = ''
				chaps= []
				subchap = ''
				item = []
				final_tot = 0
				final_avg = 0
				r = ''
				mrk = 0
				res = q.filter(and_(Questions.classname == clsnm,Questions.subject == subnm,Questions.schoolid == sclid))
				m = mark.filter(and_(UpdateMark.classname == clsnm,UpdateMark.subject == subnm,UpdateMark.schoolid == sclid))
				for i in res:
						r = m.filter(UpdateMark.qno == i.qno)
						cnt = r.count()
						if cnt != 0:
							for l in r:
								mrk += l.mark
							arr = i.subchapter.replace(" ","_") + ',' + i.qno.replace(" ","_") + ',' + i.questiondesc.replace(" ","_") + ',' + str(mrk).replace(" ","_") + ','  + str(i.mark).replace(" ","_") + ","+ str(mrk/cnt).replace(" ","_") + ","
							final_tot += mrk
							final_avg += avg							
							arr = arr[:-1]
							arr = arr.split(",")
							item.append(arr)	
							mrk = 0	
						else:
							err = "No data found !"
				return {'qql':qql,'classes':s,'ques':qps,'subjects':sub,'res':item,'sel_class':clsnm,'sel_sub':subnm,'sel_mea':mea,'err':err,'finaltot':final_tot,'finalavg':final_avg,'sel_ques':quesnm}
		return {'qql': qql,'classes':s,'subjects':sub,'res':item,'ques':qps}

	except KeyError:
		return Response(keyerr, content_type='text/plain', status=500)
@view_config(route_name='professor-update',renderer ='../templates/professor-update.jinja2')
def professor_update(request):
	try:
		clsnm = ''
		subchap = ''
		subnm = ''
		classes = ''
		subs = ''
		qtype = ''
		arr = ''
		item = ['']
		s = ' '+","
		c = ''
		sc = ''
		sc = ''
		q = ' '+","
		sub = ' '+","
		t = ''
		stu = ''
		session = request.session
		profid = session['prof_id']
		ans = request.dbsession.query(Professors).filter(Professors.id  == profid)
		for i in ans:
			sclid = i.schoolid 
		que = request.dbsession.query(Questions.papernm).distinct().filter(Questions.schoolid == sclid)
		studs = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
		for i in studs:
			s += i.classname + ","
		staffs = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid== sclid)
		for i in staffs:
			sub += i.subject + ","
		for i in que:
			q += i.papernm + ","
		if request.POST.get('save'):
			profid = session['prof_id']
			ans = request.dbsession.query(Professors).filter(Professors.id  == profid)
			for i in ans:
				sclid = i.schoolid 
			que = request.dbsession.query(Questions)
			sec = request.dbsession.query(Students)
			clsnm = request.params['sel_class']
			subnm = request.params['sel_sub']
			qtype = request.params['sel_qtype']
			syll = request.dbsession.query(Syllabus)
			result = que.filter(and_(Questions.classname == clsnm,Questions.subject == subnm,Questions.papernm == qtype,Questions.schoolid == sclid,Questions.profid == profid))
			result2 = que.filter(and_(Questions.classname == clsnm,Questions.subject == subnm,Questions.papernm == qtype,Questions.schoolid == sclid,Questions.profid == profid)).first()			
			if result2 is not None:
				for p in result:
					t += p.qno + ','
				result = sec.filter(and_(Students.classname == clsnm,Students.schoolid == sclid))
				for k in result:
					stu += k.rollno + ','
				return Response(render('../templates/professor-update.jinja2',{'sel_class':clsnm,'sel_sub':subnm,'sel_qtype':qtype,'classes':s,'subjects':sub,'qtype':q,'qno':t,'studnm':stu},request=request))
			else:
				err = "No data found !"
		elif request.POST.get('savedata'):	
			profid = session['prof_id']
			ans = request.dbsession.query(Professors).filter(Professors.id  == profid)
			for i in ans:
				sclid = i.schoolid 			
			qtype = request.params['sel_qtype2']			
			upd = request.dbsession.query(UpdateMark).filter(and_(UpdateMark.schoolid ==sclid,UpdateMark.profid == profid,UpdateMark.paperid == qtype))
			Query.delete(upd)
			transaction.commit()
			stu = request.dbsession.query(Students)
			que = request.dbsession.query(Questions)
			result = ''
			k = ''
			col = ''
			t2 = ''
			reg2 = ''
			reg = ''
			sc = ''
			t = ''
			arr = ''
			res = ''
			cls = ''
			n = int(request.params['savedata'])
			data = request.params['profdata']
			clsnm = request.params['sel_class2']
			subnm = request.params['sel_sub2']
			qtype = request.params['sel_qtype2']
			qresult = que.filter(and_(Questions.classname ==  clsnm,Questions.subject == subnm,Questions.papernm == qtype,Questions.schoolid == sclid,Questions.profid == profid))
			result = stu.filter(and_(Students.classname == clsnm,Students.schoolid == sclid))
			data = data[:-1]
			data = data.split(",")
			for j in result:
				reg += j.rollno + ','
				reg2 += j.rollno + ','
			reg = reg[:-1]
			reg = reg.split(",")
			qnm = qtype
			res = que.filter(and_(Questions.papernm == qnm,Questions.schoolid == sclid,Questions.profid == profid))
			for i in res:
				col = i.maxques
			for o in qresult:
				sc += o.subchapter + ','
				t += o.qno + ','
				t2 += o.qno + ','
				cls += o.classname + ',' 
			sc = sc[:-1]
			sc = sc.split(",")
			t = t[:-1]
			t = t.split(",")
			cls = cls[:-1]
			cls = cls.split(",")
			count = 0
			for l in range(len(reg)): 
				for m in range(col):
					if data[count].isdigit():
							updmrk = UpdateMark()
							updmrk.mark = data[count]
							updmrk.qno = t[m]
							updmrk.subchapter = sc[m]
							updmrk.paperid = qnm 
							updmrk.studid = reg[l]
							updmrk.classname = clsnm
							updmrk.subject = subnm
							updmrk.schoolid = sclid
							updmrk.profid = profid
							request.dbsession.add(updmrk)
							count = count + 1
					else:
						err = "mark must be an integer !"
						return Response(render('../templates/professor-update.jinja2',{'err':err,'sel_class':clsnm,'sel_sub':subnm,'sel_qtype':qtype,'classes':s,'subjects':sub,'qtype':q,'qno':t2,'studnm':reg2},request=request))
			return Response(render('../templates/professor-update.jinja2',{'err':"Data saved successfully !",'sel_class':clsnm,'sel_sub':subnm,'sel_qtype':qtype,'classes':s,'subjects':sub,'qtype':q,'qno':t2,'studnm':reg2},request=request))
		return {'sel_class':clsnm,'sel_sub':subnm,'sel_qtype':qtype,'classes':s,'subjects':sub,'qtype':q,'qno':t,'studnm':stu}
	except KeyError:
		return Response(keyerr, content_type='text/plain', status=500)
@view_config(route_name='student-chapters',renderer='../templates/student-chapters.jinja2')
def student_chapters(request):
	try:
		subnm = ''
		def get_first_mode(a):
			c = Counter(a)  
			mode_count = max(c.values())
			mode = {key for key, count in c.items() if count == mode_count}
			first_mode = next(x for x in a if x in mode)
			return first_mode
		subs = ''
		sub= ''
		tot = 0
		meanm = ''
		arr = ''
		med = ''
		item = []
		subchaps = []
		sampnm = ''
		session = request.session
		err = ''
		avg= 0
		final_total = 0
		final_average = 0 
		studid = session['stud_id']
		def get_first_mode(a):
			c = Counter(a)  
			mode_count = max(c.values())
			mode = {key for key, count in c.items() if count == mode_count}
			first_mode = next(x for x in a if x in mode)
			return first_mode
		ans = request.dbsession.query(Students).filter(Students.id  == studid)
		for i in ans:
			sclid = i.schoolid 
			regno = i.regno 		
		subject = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
		for i in subject:
			sub += i.subject + ","
		for i in subject:
			subs += i.subject + ','
		subs = subs[:-1]
		subs = subs.split(",")	
		if request.POST.get('save'):	
			subnm = request.params['sel_sub']
			meanm = request.params['sel_mea']
			sampnm = request.params['sel_samp']
			mark = request.dbsession.query(UpdateMark)
			if sampnm == 'Board': 	
				res = mark.filter(and_(UpdateMark.subject == subnm))
				res2 = mark.filter(and_(UpdateMark.subject == subnm)).first()
				if res2 is None:
					err = "No data found !"
				else:
					for i in res:
						if i.subchapter in subchaps:
							pass
						else:
							subchaps.append(i.subchapter)
					for k in subchaps:
						r = mark.filter(and_(UpdateMark.subchapter == k,UpdateMark.schoolid == sclid,UpdateMark.studid == regno))
						for y in r:
							tot += y.mark
							med += str(y.mark) + ","
						med = med[:-1]
						med = med.split(",")
						cnt = r.count()
						avg = tot/cnt
						rnk = list(map(int,med))
						if meanm == 'Average':
							arr = k + "," + str(tot) + "," + str(tot/cnt) + ","
							final_total += tot
							final_average += avg
						elif meanm == 'Median':
							arr = k + "," + str(tot) + "," + str(statistics.median(rnk)) + ","
							final_total += tot
							final_average += avg
						elif meanm == 'Mode':
							arr = k + "," + str(tot) + "," + str(get_first_mode(med)) + ","
							final_total += tot
							final_average += avg
						elif meanm == 'Percentile':
							arr = k + "," + str(tot) + "," + str(tot/100) + ","
							final_total += tot
							final_average += avg
						arr = arr[:-1]
						arr = arr.split(",")
						item.append(arr)
						tot = 0 
			elif sampnm == 'School':
				res = mark.filter(and_(UpdateMark.subject == subnm,UpdateMark.schoolid == sclid))
				res2 = mark.filter(and_(UpdateMark.subject == subnm,UpdateMark.schoolid == sclid)).first()
				if res2 is None:
					err = "No data found !"
				else:
					for i in res:
						if i.subchapter in subchaps:
							pass
						else:
							subchaps.append(i.subchapter)
					for k in subchaps:
						r = mark.filter(and_(UpdateMark.subchapter == k,UpdateMark.schoolid == sclid,UpdateMark.studid == regno))
						for y in r:
							tot += y.mark
							med += str(y.mark) + ","
						med = med[:-1]
						med = med.split(",")
						cnt = r.count()
						avg = tot/cnt
						rnk = list(map(int, med))
						if meanm == 'Average':
							arr = k + "," + str(tot) + "," + str(tot/cnt) + ","
							final_total += tot
							final_average += avg
						elif meanm == 'Median':
							arr = k + "," + str(tot) + "," + str(statistics.median(rnk)) + ","
							final_total += tot
							final_average += avg
						elif meanm == 'Mode':
							arr = k + "," + str(tot) + "," + str(get_first_mode(rnk)) + ","
							final_total += tot
							final_average += avg
						elif meanm == 'Percentile':
							arr = k + "," + str(tot) + "," + str(tot/100) + ","
							final_total += tot
							final_average += avg
						arr = arr[:-1]
						arr = arr.split(",")
						item.append(arr)
						tot = 0 	
			return {'subjects':sub,'res':item,'sel_sub':subnm,'sel_mea':meanm,'finaltot':final_total,'finalavg':final_average,'sel_samp':sampnm}
		return {'subjects':sub,'res':item,'sel_sub':subnm,'sel_mea':meanm,'sel_samp':sampnm,'err':err}
	except KeyError:
		return Response(keyerr, content_type='text/plain', status=500)		
@view_config(route_name='student-questions',renderer='../templates/student-questions.jinja2')
def student_questions(request):
		clsnm = ''
		subchap = ''
		subnm = ''
		session = request.session
		subs = ''
		arr = ''
		marks = []
		mrk = 0
		tot = 0
		item = []
		s = ''
		med = ''
		qtype = ''
		c = ''
		meanm = ''
		def get_first_mode(a):
			c = Counter(a)  
			mode_count = max(c.values())
			mode = {key for key, count in c.items() if count == mode_count}
			first_mode = next(x for x in a if x in mode)
			return first_mode
		sc = ''
		final_total = 0
		final_avg = 0
		ques = ''
		avg = 0
		studid = session['stud_id']
		ans = request.dbsession.query(Students).filter(Students.id  == studid)
		for i in ans:
			sclid = i.schoolid
			regno = i.regno 		 
		sec = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
		for i in sec:
			s += i.classname + ","
		sub = ''
		subject = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
		for i in subject:
			sub += i.subject + ","
		for i in subject:
			subs += i.subject + ','
		subs = subs[:-1]
		subs = subs.split(",")
		questions = request.dbsession.query(Questions.papernm).distinct().filter(Questions.schoolid == sclid)
		for i in questions:
			ques += i.papernm + ","
		q = request.dbsession.query(Questions)
		if request.POST.get('save'):	
				subnm = request.params['sel_sub']
				qtype = request.params['sel_ques']
				meanm = request.params['sel_mea']
				mark = request.dbsession.query(UpdateMark)
				res = q.filter(and_(Questions.papernm == qtype,Questions.subject == subnm,Questions.schoolid == sclid))
				m = mark.filter(and_(UpdateMark.paperid == qtype,UpdateMark.subject == subnm,UpdateMark.schoolid == sclid))
				res2 = q.filter(and_(Questions.papernm == qtype,Questions.subject == subnm,Questions.schoolid == sclid)).first()
				if res2 is None:
					err = "No data found !"
				else:
					for i in res:
							r = m.filter(and_(UpdateMark.qno == i.qno,UpdateMark.studid == regno))
							cnt = r.count()
							for l in r:
								mrk += l.mark
								med += str(l.mark) + ","
							med = med[:-1]
							med = med.split(",")
							avg = mrk/cnt
							if meanm == 'Average':
								arr = i.subchapter.replace(" ","_") + ',' + i.qno.replace(" ","_") + ',' + i.questiondesc.replace(" ","_") + ',' + str(mrk).replace(" ","_") + ',' + str(i.mark).replace(" ","_") + "," + str(mrk/cnt).replace(" ","_")+ ","
								final_total += mrk
								final_avg += avg
							elif meanm == 'Mode':
								arr = i.subchapter.replace(" ","_") + ',' + i.qno.replace(" ","_") + ',' + i.questiondesc.replace(" ","_") + ',' + str(mrk).replace(" ","_") + ',' + str(i.mark).replace(" ","_") + "," + str(get_first_mode(med)).replace(" ","_")  + ","
								final_total += mrk
								final_avg += avg
							elif meanm == 'Median':
								rnk = list(map(int, med))
								arr = i.subchapter.replace(" ","_") + ',' + i.qno.replace(" ","_") + ',' + i.questiondesc.replace(" ","_") + ',' + str(mrk).replace(" ","_") + ',' + str(i.mark).replace(" ","_") + "," + str(statistics.median(rnk)).replace(" ","_")  + ","
								final_total += mrk
								final_avg += avg	
							elif meanm == 'Percentile':
								arr = i.subchapter.replace(" ","_") + ',' + i.qno.replace(" ","_") + ',' + i.questiondesc.replace(" ","_") + ',' + str(mrk).replace(" ","_") + ',' + str(i.mark).replace(" ","_") + "," + str(mrk/100).replace(" ","_")  + ","
								final_total += mrk
								final_avg += avg
							arr = arr[:-1]
							arr = arr.split(",")
							item.append(arr)	
							mrk = 0	
							med = ''
				return {'subjects':sub,'res':item,'sel_sub':subnm,'sel_ques':qtype,'qtype':ques,'sel_mea':meanm,'finaltot':final_total,'finalavg':final_avg}			
		return {'subjects':sub,'res':item,'sel_sub':subnm,'qtype':ques,'sel_mea':meanm,'sel_ques':qtype}
@view_config(route_name='admin-syllabus',renderer='../templates/admin-syllabus.jinja2')
def admin_syllabus(request):
		s = ''
		subgroup = ''
		sub = ''
		classnm = ''
		subgrp = ''
		subnm = ''
		chapter = ''
		subchapter = ''
		d = ''
		classes = ''
		subs = ''
		session = request.session
		sclid = session['adm_id']
		studs = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
		for i in studs:
			d += i.classname.replace(" ","_") + ","
		#d += 'All' + ','
		for i in studs:
			classes += i.classname.replace(" ","_") + ','
		classes = classes[:-1]
		classes = classes.split(",")
		staffs = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
		for i in staffs:
			sub += i.subject.replace(" ","_") + ","
		#sub += 'All' + ','
		for i in staffs:
			subs += i.subject.replace(" ","_") + ','
		subs = subs[:-1]
		subs = subs.split(",")
		stud = request.dbsession.query(Syllabus).filter(Syllabus.schoolid == sclid)
		for i in stud:
			classnm += i.classname.replace(" ","_") + ','
			subgrp += i.subgroup.replace(" ","_") + ',' 
			subnm += i.subject.replace(" ","_") + ','
			chapter += i.chapter.replace(" ","_")+ ','
			subchapter += i.subchapter.replace(" ","_") + ','
		leng = len(classnm)
		if request.POST.get('savedata'):
			classes = ''
			subs = ''
			sub = ''
			subgroup = ''
			studs = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
			for i in studs:
				classes += i.classname.replace(" ","_") + ','
			classes = classes[:-1]
			classes = classes.split(",")
			staffs = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
			for i in staffs:
				subs += i.subject.replace(" ","_") + ','
			subs = subs[:-1]
			subs = subs.split(",")	
			staffs = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
			for i in staffs:
				sub += i.subject.replace(" ","_") + ","	
			#sub += 'All' + ","
			syl = request.dbsession.query(Syllabus).filter(Syllabus.schoolid == sclid)
			Query.delete(syl)
			transaction.commit()
			k = ''
			arr = ''
			n = int(request.params['savedata'])
			for i in request.params['profdata']:
				k += i
			k = k.split(",")
			for x in range(0,n * 5,5):
				arr = k[x:x+6]
				p = Syllabus()
				p.classname = arr[0].replace("_"," ")
				p.subgroup = arr[1].replace("_"," ")
				p.subject = arr[2].replace("_"," ")
				p.chapter = arr[3].replace("_"," ")
				p.subchapter = arr[4].replace("_"," ")
				p.schoolid = sclid
				request.dbsession.add(p)
			sy = request.dbsession.query(Syllabus).filter(Syllabus.schoolid == sclid)
			for i in sy:
				classnm += i.classname.replace(" ","_")+','
				subgrp += i.subgroup.replace(" ","_")+','
				subnm += i.subject.replace(" ","_")+','
				chapter += i.chapter.replace(" ","_") + ','
				subchapter += i.subchapter.replace(" ","_") + ','
			return Response(render('../templates/admin-syllabus.jinja2',{'k':arr,'classes':d,'subjects':sub,'classname':classnm,'subgroup':subgrp,'subject':subnm,'chapter':chapter,'subchapter':subchapter,'leng':leng,'err':"Data saved successfully !"},request=request))
		elif request.POST.get('search'):
			sear=request.params['search_name']
			sear='%'+sear+'%'
			r=request.dbsession.query(Syllabus).filter(Syllabus.chapter.ilike(sear)).all()
			classnm =''
			subgrp =''
			subnm =''
			chapter =''
			subchapter =''
			for i in r:
				classnm += i.classname.replace(" ","_")+','
				subgrp += i.subgroup.replace(" ","_")+','
				subnm += i.subject.replace(" ","_")+','
				chapter += i.chapter.replace(" ","_") + ','
				subchapter += i.subchapter.replace(" ","_") + ','
			leng = len(chapter)		
			if leng==0:
				return Response(render('../templates/admin-syllabus.jinja2',{'classes':d,'subjects':sub,'classname':classnm,'subgroup':subgrp,'subject':subnm,'chapter':chapter,'subchapter':subchapter,'leng':leng,'err':"Data not Found!"},request=request))
			else:
				return Response(render('../templates/admin-syllabus.jinja2',{'classes':d,'subjects':sub,'classname':classnm,'subgroup':subgrp,'subject':subnm,'chapter':chapter,'subchapter':subchapter,'leng':leng},request=request))
		elif request.POST.get('save'):
			classes = ''
			subs = ''
			subgrp = ''
			sub = ''
			subgroup = ''
			staffs = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
			for i in staffs:
				sub += i.subject.replace(" ","_") + ","
			#sub += 'All' + ","
			studs = request.dbsession.query(Students.classname).distinct().filter(Students.schoolid == sclid)
			for i in studs:
				classes += i.classname.replace(" ","_") + ','
			classes = classes[:-1]
			classes = classes.split(",")
			staffs = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
			for i in staffs:
				subs += i.subject.replace(" ","_") + ','
			subs = subs[:-1]
			subs = subs.split(",")			
			stud = request.dbsession.query(Syllabus).filter(Syllabus.schoolid == sclid)
			subgroup = request.params['sel_sub']
			cname = request.params['sel_class']		
			if subgroup == 'All' and cname == 'All':
				stud = request.dbsession.query(Syllabus)
				classnm = ''
				subnm = ''
				chapter = ''
				sub = ''
				staffs = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
				for i in staffs:
					sub += i.subject.replace(" ","_") + ","
				#sub += 'All' + ','
				subchapter = ''
				for m in classes:
					for j in subs:
							result = stud.filter(and_(Syllabus.subject == j,Syllabus.classname == m,Syllabus.schoolid == sclid))	
							for i in result:
								classnm += i.classname.replace(" ","_")+','
								subgrp += i.subgroup.replace(" ","_")+','
								subnm += i.subject.replace(" ","_")+','
								chapter += i.chapter.replace(" ","_") + ','
								subchapter += i.subchapter.replace(" ","_") + ','
				leng = len(classnm)
				return Response(render('../templates/admin-syllabus.jinja2',{'classes':d,'subjects':sub,'classname':classnm,'subgroup':subgrp,'subject':subnm,'chapter':chapter,'subchapter':subchapter,'leng':leng,'sel_class':cname,'sel_sub':subgroup},request=request))			
			elif subgroup == 'All':
				stud = request.dbsession.query(Syllabus)			
				classnm = ''
				sub = ''
				subgrp = ''
				staffs = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
				for i in staffs:
					sub += i.subject.replace(" ","_") + ","		
				#sub += 'All' + ','		
				subnm = ''
				chapter = ''
				subchapter = ''
				for j in subs:
					result = stud.filter(and_(Syllabus.subject == j,Syllabus.classname == cname.replace("_"," "),Syllabus.schoolid == sclid))	
					for i in result:
							classnm += i.classname.replace(" ","_") +','
							subgrp += i.subgroup.replace(" ","_")+','							
							subnm += i.subject.replace(" ","_") + ','
							chapter += i.chapter.replace(" ","_") + ','
							subchapter += i.subchapter.replace(" ","_") + ','
				leng = len(classnm)
				return Response(render('../templates/admin-syllabus.jinja2',{'classes':d,'subjects':sub,'classname':classnm,'subgroup':subgrp,'subject':subnm,'chapter':chapter,'subchapter':subchapter,'leng':leng,'sel_class':cname,'sel_sub':subgroup},request=request))			
			elif cname == 'All':
				stud = request.dbsession.query(Syllabus)			
				classnm = ''
				subnm = ''
				sub = ''
				subgrp = ''
				staffs = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
				for i in staffs:
					sub += i.subject.replace(" ","_") + ","	
				#sub += 'All' + ','		
				chapter = ''
				subchapter = ''
				for m in classes:
					result = stud.filter(and_(Syllabus.subject == subgroup.replace("_"," "),Syllabus.classname == m,Syllabus.schoolid == sclid))	
					for i in result:
							classnm += i.classname.replace(" ","_") + ','
							subgrp += i.subgroup.replace(" ","_")+','							
							subnm += i.subject.replace(" ","_") + ','
							chapter += i.chapter.replace(" ","_") + ','
							subchapter += i.subchapter.replace(" ","_") + ','
				leng = len(classnm)
				return Response(render('../templates/admin-syllabus.jinja2',{'classes':d,'subjects':sub,'classname':classnm,'subgroup':subgrp,'subject':subnm,'chapter':chapter,'subchapter':subchapter,'sel_class':cname,'sel_sub':subgroup},request=request))			
			else:
				stud = request.dbsession.query(Syllabus)
				result = stud.filter(and_(Syllabus.subject == subgroup.replace("_"," "),Syllabus.classname == cname.replace("_"," "),Syllabus.schoolid == sclid))	
				classnm = ''
				sub = ''
				staffs = request.dbsession.query(Professors.subject).distinct().filter(Professors.schoolid == sclid)
				for i in staffs:
					sub += i.subject.replace(" ","_") + ","	
				#sub += 'All' + ','			
				subnm = ''
				chapter = ''
				subchapter = ''				
				for i in result:
								classnm += i.classname.replace(" ","_") + ','
								subgrp += i.subgroup.replace(" ","_")+','								
								subnm += i.subject.replace(" ","_") + ','
								chapter += i.chapter.replace(" ","_") + ','
								subchapter += i.subchapter.replace(" ","_") + ','
				leng = len(classnm)
				return Response(render('../templates/admin-syllabus.jinja2',{'classes':d,'subjects':sub,'classname':classnm,'subgroup':subgrp,'subject':subnm,'chapter':chapter,'subchapter':subchapter,'sel_class':cname,'sel_sub':subgroup},request=request))			
		return Response(render('../templates/admin-syllabus.jinja2',{'classes':d,'subjects':sub,'classname':classnm,'subgroup':subgrp,'subject':subnm,'chapter':chapter,'subchapter':subchapter},request=request))			
@view_config(route_name="logout")
def logout(request):
	request.session.invalidate()
	return Response(render('../templates/index-sign-in.jinja2',{},request=request))


@view_config(route_name="opentest",renderer="../templates/opentest.jinja2")
def opentest(request):
	session = request.session
	profid = session['prof_id']
	ans = request.dbsession.query(Professors).filter(Professors.id  == profid)
	for i in ans:
		sclid = i.schoolid 
	desc = ''
	test_id = request.params['open_test_id']
	qp = request.dbsession.query(Questions).filter(and_(Questions.schoolid == sclid,Questions.testname == test_id,Questions.profid == profid))
	for i in qp:
		desc += i.questiondesc + ","
	desc = desc[:-1]
	desc = desc.split(",")
	return {'questions':desc}
@view_config(route_name="downloadtest",renderer="../templates/downloadtest.jinja2")
def dowtnloadest(request):
	session = request.session
	profid = session['prof_id']
	ans = request.dbsession.query(Professors).filter(Professors.id  == profid)
	for i in ans:
		sclid = i.schoolid 
	desc = ''
	test_id = request.params['dwnd_test_id']
	qp = request.dbsession.query(Questions).filter(and_(Questions.schoolid == sclid,Questions.testname == test_id,Questions.profid == profid))
	for i in qp:
		desc += i.questiondesc + "\n"
	pdfkit.from_string(desc,'question_paper.pdf') 
	return {}

@view_config(route_name="forgotpassword",renderer="../templates/forgotpass.jinja2")
def forgotpass(request):
	return {}

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_basics_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

