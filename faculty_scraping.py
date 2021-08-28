# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def crawling():
    """ This function simulates a crawling look. """

    global faculty_url
    print("Started crawling...")
    print("Please wait while until the crawling session finishes:")
    base_url = 'https://www.marmara.edu.tr/'
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(base_url)

    faculty_finder = browser.find_element_by_xpath('//*[@id="menuzord-right"]/ul/li[2]/a/span[1]')
    faculty_finder.click()

    faculty_finder = browser.find_element_by_xpath('//*[@id="menuzord-right"]/ul/li[2]/div/div/div[1]/a[1]')
    faculty_finder.click()
    faculty_url = base_url + 'akademik/fakulteler'
    browser.get(faculty_url)
    

def faculties_tag():
    """ This function is used to parse html context of the url page, and access 
        the required informations on it."""
    global href_links
    href_links = list()

    source = requests.get(faculty_url).text
    soup = BeautifulSoup(source, 'html.parser')
    print("Faculties that Marmara University has are as follows:\n")
    for faculty in soup.find_all('div', class_='panel-title'):
        for p_tag in faculty.find_all('b'):
            faculties = p_tag.text
            print(faculties)
            print('')


    div_tags = soup.find('div', class_='panel-collapse')
    faculties = div_tags.find_next('ul')

    for faculty in faculties:
        print(faculty.string, end='')
    print('\n')

    class_link = soup.find('div', class_='panel-collapse')
    links = class_link.find_next('ul')
    with open('links.txt', 'w') as link_file:
        for link in links.find_all('a'):
            href_links.append(link.get('href'))
            link_file.write(link.get('href') + '\n')


def read_txt_file():
    global links
    with open('links.txt', 'r') as links_file:
        lines = links_file.readlines()
        links = list()
        for line in lines:
            links.append(line.strip('\n'))


def get_context_atf():
    """ This function gets the links from the text file 'links.txt' and uses the links to get 
        the necessary information about the departments from those links. """
        
    read_txt_file()
    
    faculty_url = links[0]
    source = requests.get(faculty_url).text
    soup = BeautifulSoup(source, 'html.parser')

    menu_elements = soup.find('ul', class_='menuzord-menu dark menuzord-right menuzord-indented scrollable')
    list_elements = menu_elements.find_all('ul', class_='dropdown')
    atf_departments = list()

    for departments in list_elements:
        for department in departments.find_all('a'):
            atf_departments.append(department.text)


    # Remove unnecessary context information in the atf_departments list.
    k = 0
    for _ in atf_departments:
        if not k >= 21 and not k < 30:
            atf_departments.remove(atf_departments[k])
        k += 1


    # Print the deparments in the Faculty, and create an absolute list.
    ataturk_faculty = list()
    print("Departments under Atatürk Education Faculty:\n")
    for i in range(len(atf_departments)):
        if 21 <= i < 30:
            print(atf_departments[i])
            ataturk_faculty.append(atf_departments[i])
    print()

def get_context_dentistry():
    """This function returns the string information for the Faculty of Dentistry. """
    return "Faculty of Denstistry doesn't include any other departments\n"


def get_context_pharmacy():
    """This function prints the departments under the faculty of pharmacy. """
    read_txt_file()
    faculty_url = links[2]
    source = requests.get(faculty_url).text
    soup = BeautifulSoup(source, 'html.parser')

    menu_elements = soup.find('ul', class_='menuzord-menu dark menuzord-right menuzord-indented scrollable')
    list_elements = menu_elements.find_all('ul', class_='dropdown')
    eczacılık_departments = list()


    # Create a list containing items in the faculty of pharmcy website
    for departments in list_elements:
        for department in departments.find_all('a'):
            eczacılık_departments.append(department.text)


    # Print the necessary items from the list of the Faculty of Pharmacy.
    print("Departments under the Faculty of Pharmacy")
    for i in range(len(eczacılık_departments)):
        if 57 <= i < 90:
            print(eczacılık_departments[i])


if __name__ == '__main__':
    crawling()
    if crawling:
        faculties_tag()
        get_context_atf()
        print(get_context_dentistry())
        get_context_pharmacy()
