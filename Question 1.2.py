from bs4 import BeautifulSoup
import urllib.request

seed_url = 'https://www.europarl.europa.eu/news/en/press-room'
maxNumUrl = 10

urls = [f'{seed_url}?page={i}' for i in range(1, 15)]
seen = []
opened = []
press_releases = []

print("Starting with urls=" + str(urls))

while len(urls) > 0 and len(press_releases) < maxNumUrl:
    try:
        curr_url = urls.pop(0)
        print("num. of URLs in stack: %d " % len(urls))
        print("Trying to access= " + curr_url)
        req = urllib.request.Request(curr_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= " + curr_url)
        print(ex)
        continue

    soup = BeautifulSoup(webpage, 'html.parser')
    tags = soup.find_all('a', href=True)
    links = [urllib.parse.urljoin(seed_url, tag['href']) for tag in tags if urllib.parse.urljoin(seed_url, tag['href']) not in seen]

    for link in links:
        if len(press_releases) == maxNumUrl:
            break 
        try:
            with urllib.request.urlopen(link) as response_link:
                soup_link = BeautifulSoup(response_link, 'html.parser')
                text_content = soup_link.get_text()
                if 'crisis' in text_content and 'Plenary session' in text_content:
                    press_releases.append(link)
                    break
        except Exception as ex:
            print("Unable to access= " + link)
            print(ex)

    seen.extend(links)

for index, press_release in enumerate(press_releases):
    try:
        with urllib.request.urlopen(press_release) as press_response:
            with open(f'2_{index + 1}.txt', 'w', encoding='utf-8') as file:
                file.write(press_response.read().decode('utf-8'))
    except Exception as ex:
        print("Unable to access= " + press_release)
        print(ex)

print("num. of URLs seen = %d, and scanned = %d" % (len(seen), len(opened)))
print("List of seen URLs:")
for seen_url in seen:
    print(seen_url)






