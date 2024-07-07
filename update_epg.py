import requests
from lxml import etree

# Fetch EPG data from your source (replace with actual source)
source_url = "http://example.com/tv-schedule"  # Update this URL
response = requests.get(source_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the EPG data (this will vary depending on your source format)
    # Here's a simplified example
    root = etree.Element("tv")

    # Example channel
    channel = etree.SubElement(root, "channel", id="channel1")
    display_name = etree.SubElement(channel, "display-name")
    display_name.text = "Channel 1"

    # Example program
    programme = etree.SubElement(root, "programme", start="20240701000000 +0000", stop="20240701010000 +0000", channel="channel1")
    title = etree.SubElement(programme, "title")
    title.text = "Program 1"
    desc = etree.SubElement(programme, "desc")
    desc.text = "Description of Program 1"

    # Add more programs as needed
    programme = etree.SubElement(root, "programme", start="20240701010000 +0000", stop="20240701020000 +0000", channel="channel1")
    title = etree.SubElement(programme, "title")
    title.text = "Program 2"
    desc = etree.SubElement(programme, "desc")
    desc.text = "Description of Program 2"

    # Write to file
    tree = etree.ElementTree(root)
    with open("epg.xml", "wb") as f:
        tree.write(f, pretty_print=True, xml_declaration=True, encoding="UTF-8")
else:
    print(f"Failed to fetch EPG data. Status code: {response.status_code}")
