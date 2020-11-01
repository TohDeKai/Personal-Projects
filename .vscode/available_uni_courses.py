# Importing essential modules
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader
from pathlib import Path
import pdfplumber
import pprint

# A-Level Grades Conversion to UAS
grade_to_uas = {"A": 20, "B": 17.5, "C": 15, "D": 12.5, "E": 10, "S": 5, "U": 0}

# Ask user to enter their A - Levels Score
print ("Please enter your A Level Score")
h2_1 = input('What is the grade of your first H2?').upper()
h2_2 = input('What is the grade of your second H2?').upper()
h2_3 = input('What is the grade of your third H2?').upper()
h1 = input('What is the grade of your H1?').upper()
gp = input('What is the grade of your General Paper?').upper()
pw = input('What is the grade of your Project Work?').upper()


# Calculating to UAS
try:
    h2_total = grade_to_uas[h2_1] + grade_to_uas[h2_2] + grade_to_uas[h2_3]
    h1_total = (grade_to_uas[gp] + grade_to_uas[pw] + grade_to_uas[h1])/2
    total_uas = h2_total + h1_total
    print (f'Your UAS is {total_uas}')
    print ('\n')
except KeyError:
    print ("Only letter grades are accepted. For example, \"A\" or \"B\"")

# Web - Scraping

#NUS

URL_NUS = 'http://www.nus.edu.sg/oam/undergraduate-programmes/indicative-grade-profile-(igp)'
page = requests.get(URL_NUS)

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='ContentPlaceHolder_contentPlaceholder_TC88F994D007_Col00')

igp_elems = results.find_all("tr", class_=False, id=False)

# Data starts from Index 3 : Faculty of Law, ends at Index 47

for i in igp_elems[3:48]:
    course_elem = i.find('td',  class_=False, id=False)
    igp_grades = i.find('div', class_=False, id=False)
    if igp_grades == None:
        continue
    uas_for_course = 0
    for i in igp_grades.text[:4]:
        if i == '/':
            continue
        uas_for_course += grade_to_uas[i]
    uas_for_course += grade_to_uas[igp_grades.text[4]]/2
    # Since GP and PW assumed to be C
    uas_for_course += 15
    if uas_for_course < total_uas:
        print ('NUS',",",course_elem.text,",",uas_for_course) 
        print ('\n')


#NTU
# URL_NTU = 'https://www3.ntu.edu.sg/oad2/website_files/IGP/NTU_IGP.pdf'


filename = Path('NTU_IGP.pdf')
url = 'https://www3.ntu.edu.sg/oad2/website_files/IGP/NTU_IGP.pdf'
response = requests.get(url)
filename.write_bytes(response.content)

pdf_path='NTU_IGP.pdf'
pdf = PdfFileReader(str(pdf_path))

with pdfplumber.open('NTU_IGP.pdf') as pdf:
    second_page = pdf.pages[1]
    third_page = pdf.pages[2]
    ntu_course_list = []
    for i in second_page.extract_table():
        if i[0] == None or i[0] == "":
            continue
        course_and_igp = []
        course_and_igp.append(i[0])
        course_and_igp.append(i[2])
        ntu_course_list.append(course_and_igp)
    for i in third_page.extract_table():
        if i[0] == None or i[0] == "":
            continue
        course_and_igp = []
        course_and_igp.append(i[0])
        course_and_igp.append(i[2])
        ntu_course_list.append(course_and_igp)

for i in ntu_course_list:
    coursename = i[0]
    uas_for_course = 0
    if i[1] == "":
        continue
    for char in i[1][:4]:
        if char == '/':
            continue
        uas_for_course += grade_to_uas[char]
    uas_for_course += grade_to_uas[i[1][4]]/2
    # Since GP and PW assumed to be C
    uas_for_course += 15
    if uas_for_course <= total_uas:
        print ('NTU',",",coursename,",",uas_for_course)
        print ('\n')