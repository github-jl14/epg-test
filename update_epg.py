import urllib.request
from inscriptis import get_text
from bs4 import BeautifulSoup
from lxml import etree
import datetime
import logging

# Function to fetch and parse the TV schedule using urllib and inscriptis
def fetch_tv_schedule(url):
    html = urllib.request.urlopen(url).read().decode('utf-8')
    text = get_text(html)

    # Parse the plain text using BeautifulSoup
    soup = BeautifulSoup(text, 'html.parser')
    
    # This part depends on the actual structure of the website
    # Example assumes each program is contained in a <div class="program">
    programs = soup.find_all('div', class_='program')

    schedule = []
    for program in programs:
        title = program.find('h2').text
        desc = program.find('p').text
        start_time_str = program.find('time', class_='start')['datetime']
        end_time_str = program.find('time', class_='end')['datetime']

import urllib.request
from inscriptis import get_text
from bs4 import BeautifulSoup
from lxml import etree
import datetime
import logging

# Function to fetch and parse the TV schedule using urllib and inscriptis
def fetch_tv_schedule(url):
    try:
        html = urllib.request.urlopen(url).read().decode('utf-8')
        text = get_text(html)

        # Parse the plain text using BeautifulSoup
        soup = BeautifulSoup(text, 'html.parser')
        
        # This part depends on the actual structure of the website
        # Example assumes each program is contained in a <div class='program'>
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
    except Exception as e:
        logging.error(f"Error fetching TV schedule: {e}")
        return None

# Function to update the EPG XML file
def update_epg(schedule, output_file):
    try:
        # Parse the existing EPG XML file
        tree = etree.parse(output_file)
        root = tree.getroot()

        # Locate the channel element
        channel = root.find(".//channel[@id='channel1']")
        if channel is None:
            # If the channel does not exist, create it
            channel = etree.SubElement(root, "channel", id="channel1")
            display_name = etree.SubElement(channel, "display-name")
            display_name.text = "Channel 1"

        # Add new programs to the EPG
        for program in schedule:
            start = program['start'].strftime("%Y%m%d%H%M%S %z")
            end = program['end'].strftime("%Y%m%d%H%M%S %z")
            programme = etree.SubElement(root, "programme", start=start, stop=end, channel="channel1")
            
            title = etree.SubElement(programme, "title")
            title.text = program['title']
            
            desc = etree.SubElement(programme, "desc")
            desc.text = program['desc']

        # Write the updated EPG back to the file
        tree.write(output_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")

        logging.info("EPG updated successfully.")
    except Exception as e:
        logging.error(f"Error updating EPG: {e}")

# Main update process
def update_epg_process(url, output_file):
    try:
        logging.info("Starting EPG update process")
        # Fetch the TV schedule
        schedule = fetch_tv_schedule(url)

        if schedule:
            # Update the EPG file
            update_epg(schedule, output_file)
        else:
            logging.error("Failed to fetch TV schedule.")
        logging.info("EPG update process completed successfully")
    except Exception as e:
        logging.error(f"Failed to update EPG: {e}")
        raise

if __name__ == "__main__":
    # URL of the TV schedule page (example)
    tv_schedule_url = "https://www.tv5.com.ph/schedule"
    output_file = "epg.xml"

    logging.basicConfig(level=logging.INFO)
    update_epg_process(tv_schedule_url, output_file)
