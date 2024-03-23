from bs4 import BeautifulSoup

def get_schedules_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    # Find all <li> elements within the <ul> with class "schedules"
    schedule_elements = soup.select('ul.schedules li')
    schedules_list = []
    
    for schedule in schedule_elements:
        days = []
        times = ""
        room = schedule.find_all("div")[-1].get_text(strip=True)

        if room == "Online Class":
            days = ["X"]
            times = "00:00-00:00AM"
        else:
            days = [d for d in schedule.get_text().split()[0] if d.isalpha()]
            times = schedule.get_text().split()[1]


        schedules_list.append({
            'days': days,
            'times': times,
            'room': room
        })

    return schedules_list

# html_content = '\n\t\t\t\t\t\t\t<ul class="schedules"><li>MWF 12:45-04:15PM  <div>(04/22/2024 - 07/24/2024)</div><div>&nbsp;</div><div>Austin 125 Auto Lab</div></li><li>R 10:45-11:15PM  <div>(04/22/2024 - 07/24/2024)</div><div>&nbsp;</div><div>STC 104</div></li></ul>\n                            \n\t\t\t\t\t\t'
html_content = '\n\t\t\t\t\t\t\t<ul class="schedules"><li>00:00-00:00AM  <div>(04/22/2024 - 07/24/2024)</div><div>&nbsp;</div><div>Online Class</div></li></ul>\n                            \n\t\t\t\t\t\t'
print(get_schedules_text(html_content)) # Output: MWF 12:45-04:15PM Austin 125 Auto Lab