from selenium import webdriver
from selenium.webdriver.common.by import By
from functions import log
import time


coursesByFaculty = open('coursesByFaculty.txt', 'w')
coursesByCareer = open('coursesByCareer.txt', 'w')
allCourses = {}
allCoursesCareer = {}


# Opens a Browser on the courses page
coursesPage = "https://registro.usach.cl/index.php?ct=horario"
driver = webdriver.Firefox()
driver.get(coursesPage)

# CODE LOOKS GROSS DUE TO XPATH STRINGS
# Gets the number of entries in the faculties form
faculties = driver.find_elements(By.XPATH, '/html/body/div/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[2]/form/select/*')

# Goes through every faculty on the page
for faculty in range(2, len(faculties)):
    driver.find_element(By.XPATH, f'//*[@id="id_facultad"]/option[{faculty}]').click()
    facultyCode =  driver.find_element(By.XPATH, f'//*[@id="id_facultad"]/option[{faculty}]').text.split(' ', 2)
    allCourses[facultyCode[0]] = {'name': facultyCode[2], 'courses': {}}
    allCoursesCareer[facultyCode[0]] = {'name': facultyCode[2], 'careers': {}}
    time.sleep(10)
    careers = driver.find_elements(By.XPATH, '/html/body/div/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[2]/form/div/select/*')
    # Goes through every career at the faculty
    for career in range(2, len(careers)):
        driver.find_element(By.XPATH, f'/html/body/div/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[2]/form/div/select/option[{career}]').click()
        careerCode = driver.find_element(By.XPATH, f'/html/body/div/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[2]/form/div/select/option[{career}]').text.split(' ', 2)
        # Goes through the first x periods
        for period in range(2, 7):
            driver.find_element(By.XPATH, f'/html/body/div/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[2]/form/center/h6/select/option[{period}]').click()
            driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[2]/form/center/button').click()
            handles = driver.window_handles
            driver.switch_to.window(handles[1])

            # Waits until the page has loaded
            while True:
                try:
                    time.sleep(0.5)
                    page = driver.find_element(By.XPATH, '/html/body/center/table[1]/tbody/tr[2]/td/table/tbody/tr/td/strong').text
                    break
                except:
                    pass
            
            # Checks if the page has data
            if page == 'PLANIFICACIÓN HORARIA':
                periodText = driver.find_element(By.XPATH, '/html/body/center/table[1]/tbody/tr[1]/td/table/tbody/tr[2]/td[3]').text.split('\n')[3].split()
                if len(periodText) != 1:
                    foundCourses = []
                    nTables = driver.find_elements(By.XPATH, '/html/body/center/*')
                    for table in range(1, (len(nTables) // 3) + 1):
                        nCourses = driver.find_elements(By.XPATH, f'/html/body/center/table[{table}]/tbody/tr[3]/td/table/tbody/tr[2]/td/font/table/tbody/*')
                        for course in range(2, len(nCourses) + 1):

                            # Takes all the rows that have CODE and CAREER (Rows with less than 3 childs are teachers)
                            row = driver.find_elements(By.XPATH, f'/html/body/center/table[{table}]/tbody/tr[3]/td/table/tbody/tr[2]/td/font/table/tbody/tr[{course}]/*')
                            if len(row) >= 3:
                                code = driver.find_element(By.XPATH, f'/html/body/center/table[{table}]/tbody/tr[3]/td/table/tbody/tr[2]/td/font/table/tbody/tr[{course}]/td[2]/strong/font').text
                                className = driver.find_element(By.XPATH, f'/html/body/center/table[{table}]/tbody/tr[3]/td/table/tbody/tr[2]/td/font/table/tbody/tr[{course}]/td[5]/strong/font').text
                                foundCourses.append(f"{code}: {className}")
                                allCourses[facultyCode[0]]['courses'][code] = className
                                allCoursesCareer[facultyCode[0]]['careers'][careerCode[0]] = {'name': careerCode[2], 'courses': {}}
                                allCoursesCareer[facultyCode[0]]['careers'][careerCode[0]]['courses'][code] = className
                                log(2, foundCourses)
                else:
                    log(1)

            else:
                log(0)

            driver.close()
            driver.switch_to.window(handles[0])
            

            time.sleep(0.5)

        driver.find_element(By.XPATH, f'/html/body/div/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[2]/form/div/select/option[{career}]').click()
    driver.find_element(By.XPATH, f'//*[@id="id_facultad"]/option[{faculty}]').click()
    coursesByFaculty.write(str(allCourses))
    coursesByCareer.write(str(allCoursesCareer))
