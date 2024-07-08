import requests
from bs4 import BeautifulSoup
from lxml import etree
import datetime

# Function to fetch and parse the TV schedule
def fetch_tv_schedule(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch TV schedule. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    # This part depends on the actual structure of the website
    # Example assumes each program is contained in a <div class="program">
    programs = soup.find_all('div', class_='program')

    schedule = []
    for program in programs:
        title = program.find('h2').text
        desc = program.find('p').text
        start_time_str = program.find('time', class_='start')['datetime']
        end_time_str = program.find('time', class_='end')['datetime']

        start_time = datetime.datetime.fromisoformat(start_time_str)
        end_time = datetime.datetime.fromisoformat(end_time_str)

        schedule.append({
            'title': title,
            'desc': desc,
            'start': start_time,
            'end': end_time
        })

    return schedule

# Function to update the EPG XML file
def update_epg(schedule, output_file):
    root = etree.Element("tv")

    # Example channel
    channel = etree.SubElement(root, "channel", id="channel1")
    display_name = etree.SubElement(channel, "display-name")
    display_name.text = "Channel 1"

    for program in schedule:
        start = program['start'].strftime("%Y%m%d%H%M%S %z")
        end = program['end'].strftime("%Y%m%d%H%M%S %z")
        programme = etree.SubElement(root, "programme", start=start, stop=end, channel="channel1")
        
        title = etree.SubElement(programme, "title")
        title.text = program['title']
        
        desc = etree.SubElement(programme, "desc")
        desc.text = program['desc']

    tree = etree.ElementTree(root)
    with open(output_file, "wb") as f:
        tree.write(f, pretty_print=True, xml_declaration=True, encoding="UTF-8")

# URL of the TV schedule page (example)
tv_schedule_url = "https://www.tv5.com.ph/schedule"

# Fetch the TV schedule
schedule = fetch_tv_schedule(tv_schedule_url)

if schedule:
    # Update the EPG file
    update_epg(schedule, "epg.xml")
    print("EPG updated successfully.")
else:
    print("Failed to update EPG.")
