import requests
import time
from bs4 import BeautifulSoup
from langdetect import detect
from collections import deque
import json
from random import randint


# scrape followerwonk.com for nurse information
def id_sprider(mints, maxts, max_pages):
    # starting from page 1
    page = 1
    # Store common(English based, no error) profile data
    common_file = 'profile' + mints + '-' + maxts + 'v3.json'
    # Store common(English based, no error) profile data
    uncommon_file = 'uncommonProfile' + mints + '-' + maxts + 'v3.json'

    comment = 'First_page of Tweets from ' + mints + ' to ' + maxts
    profile = []
    uncommon_profile = []
    print(comment)
    while page <= max_pages:
        # request the page source code
        url = 'https://followerwonk.com/bio/?q=nurse&q_type=all&stctmin=' + mints + '&stctmax=' + maxts + '&s=fl&p='\
              + str(page)
        source_code = requests.get(url)
        plain_text = source_code.text

        # parse the source code with BeautifulSoup
        soup = BeautifulSoup(plain_text, "html.parser")

        # find useful information
        for link1 in soup.findAll('tbody', {'class': "stripable_doublerow"}):
            # extract ID and name
            ID = link1.findAll('span', {'class': "person_scrn"})[0].string
            sname = link1.findAll('a', {'target': "_new"})[0].string

            # extract the numbers: tweets number, following number, followers number, sa number
            userinfo = deque([])
            for link4 in link1.findAll('td', {'class': "a_r num"}):
                if link4.string:
                    userinfo.append(link4.string)
                else:
                    for link5 in link4.findAll('div', {'class': "sa_score"}):
                        userinfo.append(int(link5.string.replace(',', '')))
            try:
                tweets = userinfo.popleft()
                following = userinfo.popleft()
                followers = userinfo.popleft()
                sa = userinfo.popleft()
            except Exception:
                pass

            # extract bios
            for link6 in link1.findAll('div', {'class': "person_bio"}):
                content = ""
                for string in link6.strings:
                    content = content + string
            try:
                if content == str() or detect(content) == 'en':
                    profile.append({'screen_name': ID, 'username': sname, 'tweets': tweets,
                                    'following': following, 'followers': followers, 'SA': sa, 'bio': content})

            except Exception:
                uncommon_profile.append({'screen_name': ID, 'username': sname, 'tweets': tweets,
                                        'following': following, 'followers': followers, 'SA': sa, 'bio': content})
        # print some information
        print('We are at page ' + str(page) + ' of Tweets from ' + str(mints) + ' to ' + str(maxts) + '\n')
        page += 1
        # delay a random number between pages
        time.sleep(randint(5, 30))

# normal profiles output
    f1out = open(common_file, 'w')
    json.dump(profile, f1out, indent=4)
    f1out.close()

# abnormal profiles output
    f2out = open(uncommon_file, 'w')
    json.dump(uncommon_profile, f2out, indent=4)
    f2out.close()


def main():

    id_sprider('100', '200', 483)
    time.sleep(randint(1200, 3600))

    id_sprider('200', '300', 289)
    time.sleep(randint(1200, 3600))

    id_sprider('300', '1000', 862)
    time.sleep(randint(1200, 3600))

    id_sprider('1000', '3000', 787)
    time.sleep(randint(1200, 3600))

    id_sprider('3000', '10000', 686)
    time.sleep(randint(1200, 3600))

    id_sprider('10000', '0', 340)


if __name__ == "__main__":
    main()
