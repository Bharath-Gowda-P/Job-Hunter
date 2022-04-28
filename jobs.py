from ast import Div
from asyncore import write
from urllib import response
from webbrowser import get
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv


def get_url(position, location):
    template = 'https://in.indeed.com/jobs?q={}&l={}'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    url = template.format(position, location)
    return url 


def get_record(card):
    title = card.span.get('title')
    company = card.find('span', class_='companyName').text
    location = card.find('div', class_ = 'companyLocation').text
    summary = card.find('div', class_ = 'job-snippet').text.strip()
    post_date = card.find('span', class_ = 'date').text
    try:
        salary = card.find('div', 'attribute_snippet').text
    except AttributeError:
        salary = 'Salary Not Mentioned'
    more_info = 'https://www.indeed.com' + card.get('href')

    record = (title, company, location, summary, post_date, salary, more_info)

    return record


def main():
    records = []
    position = input("Enter the Position for Job: ")
    location = input("Enter the location for the Job: ")
    url = get_url(position, location)

    while True:
        i = 0
        result = requests.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')
        cards = soup.find_all('a', class_='tapItem')
        for card in cards:
            record = get_record(card)
            records.append(record)
            print(records[i])
            print('')
            i= i+1
        try:
            url = "https://www.indeed.com/" + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break

        with open('results.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Company', 'Location', 'Summary', 'Posted On', 'Salary', 'More Info'])
            writer.writerows(records)
        

            
main()