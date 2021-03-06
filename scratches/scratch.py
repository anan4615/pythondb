import cx_Oracle
import csv

import string

dsn_tns = cx_Oracle.makedsn('edb-test.int.colorado.edu', '1521', 'edtest')
#TODO
conn = cx_Oracle.connect(user='', password='', dsn=dsn_tns)
c = conn.cursor()

f = csv.reader(open('datatypes.csv','r'))
for row in f:
    sep = ", "
    activitytype = sep.join(row)
    #TODO
    term = 20207
    print(activitytype)
    print("-------------")

######Pick a course based on actvity type in sis_course
    c.execute("select COURSE, SECTION, TERM from dirsvcs.sis_course where TERM ='%s' and ACTIVITY_TYPE ='%s'" % (term, activitytype))
    ans = c.fetchall()
    for row in  ans:
    #print(row)
        course=row[0]
        section=row[1]
        term=row[2]
##########check if the course is in canvas LMS table and if yes get the course_sourced_id---
        c.execute("select course_sourced_id from LMSMANAGER.LMS_COURSES where COURSE ='%s' and SECTION ='%s' and TERM ='%s'" % (course, section, term))

        lms = c.fetchone()
    #print(lms)
        if (lms is None):
          print("Success: course/section/term is not in canvas LMS table"+ " "+ course+ " "+ section+ " "+term + " " + activitytype)
          ############################check if the selected course has an combined section
          c.execute("select CLASS_NBR from dirsvcs.sis_course where COURSE ='%s' and SECTION ='%s' and TERM ='%s'" % (course, section, term))
          clsnbr =c.fetchone()
          #print(clsnbr)
          strm= 2207
          #TODO
          c.execute("SELECT a.class_nbr FROM dirsvcs.isis_section_combined a INNER JOIN dirsvcs.isis_section_combined b ON a.combined_section_id = b.combined_section_id AND a.strm = b.strm AND a.session_code = b.session_code WHERE b.class_nbr = '%s' AND b.strm = '2207'" % (clsnbr))
          #c.execute("select CLASS_NBR from dirsvcs.isis_section_combined where STRM ='%s' and CLASS_NBR ='%s'" % (strm, clsnbr))
          combined_sec=c.fetchall()
          rows_affected = c.rowcount
          if (len(combined_sec) == 0):
              print("No this class is not a combined section and is therefore a single-section course. Check in Canvas to see if this course  has been created" )

          else:
              print("%%%%%%%%%%%%%%%%%%%%%%%combined section" + " " + str(rows_affected))
              c.execute("SELECT a.class_nbr FROM dirsvcs.isis_section_combined a INNER JOIN dirsvcs.isis_section_combined b ON a.combined_section_id = b.combined_section_id AND a.strm = b.strm AND a.session_code = b.session_code WHERE b.class_nbr = '%s' AND b.strm = '2207' order by a.class_nbr asc" % (clsnbr))
              classnumber_asc= c.fetchone()

              c.execute("select course, section from dirsvcs.sis_course where CLASS_NBR='%s' and term='20207'" % (classnumber_asc))
              chkparent=c.fetchall()

              for row in chkparent:
                  coursep=row[0]
                  sectionp=row[1]
                  c.execute("select course_sourced_id from LMSMANAGER.LMS_COURSES where COURSE ='%s' and SECTION ='%s' and TERM ='%s'" % (coursep, sectionp, term))
                  parent_sec = c.fetchall()

                  if (len(parent_sec) == 0):
                      print("################################This parent course needs to be created and is not in canvas" +" " +coursep +" "+ section)
                  else:
                      print("$$$$$$$$$$$$$$$parent course exists make sure to add subsequent sections to this course" +" "+coursep +" "+section + " "+str(classnumber_asc))


        else:
          print("**********course is in canvas LMS table"+ " "+ course+ " "+ section+ " "+term +" "+activitytype )













