from bs4 import BeautifulSoup
import requests
import csv

csv_file = open('zoomit2.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Category','Title', 'Abstract', 'Paragraphs', 'Link'])


for page in range(5):
    # Space
    if page == 0:
        source = requests.get('https://www.zoomit.ir/space/').text
    else:
        source = requests.get(f'https://www.zoomit.ir/space/page/{page}').text
    soup = BeautifulSoup(source, 'lxml')
    for article in soup.find_all('div', class_='col-md-8 col-sm-8 col-xs-8 item-list-text'):
        title_raw = article.find('a', class_="catlist__post-title")
        title = title_raw.text
        abstract = article.find('p', class_='hidden-xs hidden-sm').text
        pgh_link = 'https://www.zoomit.ir/space/' + str(title_raw).split('/')[4]
        pgh_source = requests.get(pgh_link).text
        pgh_soup = BeautifulSoup(pgh_source, 'lxml')
        try:
            paragraphs = pgh_soup.find('div', id="bodyContainer").text
        except:
            pass

        category = 'space'
        title = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in title)
        abstract = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in abstract)
        paragraphs = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in paragraphs)

        csv_writer.writerow([category, title, abstract, paragraphs, pgh_link])


    # health-medical
    if page == 0:
        source = requests.get('https://www.zoomit.ir/health-medical/').text
    else:
        source = requests.get(f'https://www.zoomit.ir/health-medical/page/{page}').text
    soup = BeautifulSoup(source, 'lxml')
    for article in soup.find_all('div', class_='col-md-8 col-sm-8 col-xs-8 item-list-text'):
        title_raw = article.find('a', class_="catlist__post-title")
        title = title_raw.text
        abstract = article.find('p', class_='hidden-xs hidden-sm').text
        pgh_link = 'https://www.zoomit.ir/health-medical/' + str(title_raw).split('/')[4]
        pgh_source = requests.get(pgh_link).text
        pgh_soup = BeautifulSoup(pgh_source, 'lxml')
        try:
            paragraphs = pgh_soup.find('div', id="bodyContainer").text
        except:
            pass

        category = 'health-medical'
        title = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in title)
        abstract = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in abstract)
        paragraphs = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in paragraphs)

        csv_writer.writerow([category, title, abstract, paragraphs, pgh_link])


    # fundamental-science
    if page == 0:
        source = requests.get('https://www.zoomit.ir/fundamental-science/').text
    else:
        source = requests.get(f'https://www.zoomit.ir/fundamental-science/page/{page}').text
    soup = BeautifulSoup(source, 'lxml')
    for article in soup.find_all('div', class_='col-md-8 col-sm-8 col-xs-8 item-list-text'):
        title_raw = article.find('a', class_="catlist__post-title")
        title = title_raw.text
        abstract = article.find('p', class_='hidden-xs hidden-sm').text
        pgh_link = 'https://www.zoomit.ir/fundamental-science/' + str(title_raw).split('/')[4]
        pgh_source = requests.get(pgh_link).text
        pgh_soup = BeautifulSoup(pgh_source, 'lxml')
        try:
            paragraphs = pgh_soup.find('div', id="bodyContainer").text
        except:
            pass

        category = 'fundamental-science'
        title = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in title)
        abstract = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in abstract)
        paragraphs = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in paragraphs)

        csv_writer.writerow([category, title, abstract, paragraphs, pgh_link])


    # energy-environment
    if page == 0:
        source = requests.get('https://www.zoomit.ir/energy-environment/').text
    else:
        source = requests.get(f'https://www.zoomit.ir/energy-environment/page/{page}').text
    soup = BeautifulSoup(source, 'lxml')
    for article in soup.find_all('div', class_='col-md-8 col-sm-8 col-xs-8 item-list-text'):
        title_raw = article.find('a', class_="catlist__post-title")
        title = title_raw.text
        abstract = article.find('p', class_='hidden-xs hidden-sm').text
        pgh_link = 'https://www.zoomit.ir/energy-environment/' + str(title_raw).split('/')[4]
        pgh_source = requests.get(pgh_link).text
        pgh_soup = BeautifulSoup(pgh_source, 'lxml')
        try:
            paragraphs = pgh_soup.find('div', id="bodyContainer").text
        except:
            pass

        category = 'energy-environment'
        title = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in title)
        abstract = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in abstract)
        paragraphs = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in paragraphs)

        csv_writer.writerow([category, title, abstract, paragraphs, pgh_link])
csv_file.close()