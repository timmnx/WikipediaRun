import sys
import webview
# from webview.dom import DOMEventHandler
import time
import requests
from bs4 import BeautifulSoup

team = "Tim et Raph"

start = 'https://fr.wikipedia.org/wiki/Cookie_(informatique)'
start_html = f'''
    <html>
    <body style="background-color:red;">
        <div style="display: grid; place-items: center; height:100%; width:100%">
            <form action="{start}">
                <input type="submit" value="Commencer" style="
                    font-size:5em; border-radius:1em"/>
            </form>
        </div>
    </body>
    </html>
'''
mid   = 'https://fr.wikipedia.org/wiki/Europe'
mid_html = f'''
    <html>
    <body style="background-color:orange;">
        <div style="display: grid; place-items: center; height:100%; width:100%">
            <h1> Echangez </h1>
            <form action="{mid}">
                <input type="submit" value="Continuer" style="
                    font-size:5em; border-radius:1em"/>
            </form>
        </div>
    </body>
    </html>
'''
end   = 'https://fr.wikipedia.org/wiki/Territorialisme'
end_html = '''
    <html>
    <body style="background-color:green;">
        <div style="display: grid; place-items: center; height:100%; width:100%">
            <h1> Bravo, vous avez fini ! </h1>
            <h2> Envoie automatique des résultats et fin du jeu. </h2>
        </div>
    </body>
    </html>
'''

urls = [None]
path = ""

def filter_url(url):
    try:
        if url == None:
            return False
        elif url.startswith('file://'):
            return False
        else:
            return True
    except:
        print(url, url.type)
        return True

def str_list(l):
    res = ""
    for e in l:
        res += str(e).removeprefix("https://fr.wikipedia.org/wiki/") + " -> "
        # res += str(e) + " -> "
    return res

def send(path, t):
    # --- Step 1: URL of your Framaform ---
    form_url = "https://framaforms.org/wikipediarun-1757120534"

    # --- Step 2: Start a session ---
    session = requests.Session()

    # --- Step 3: GET the form page ---
    response = session.get(form_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # --- Step 4: Collect all hidden fields (e.g., CSRF tokens) ---
    data = {}
    for hidden in soup.find_all("input", type="hidden"):
        name = hidden.get("name")
        value = hidden.get("value", "")
        if name:
            data[name] = value

    # --- Step 5: Detect all questions automatically ---
    questions = []
    for input_tag in soup.find_all(["input", "textarea", "select"]):
        name = input_tag.get("name")
        if not name or name in data:
            continue  # skip hidden or already collected
        label = input_tag.get("placeholder") or input_tag.get("title") or name
        questions.append((label, name))

    # --- Step 6: Ask user for each answer ---
    for label, name in questions:
        # answer = input(f"{label}: ")
        data[name] = f"{team} : {path}{t}s"

    # --- Step 7: Submit the form ---
    post_url = form_url  # usually the same URL
    response = session.post(post_url, data=data)

    # --- Step 8: Confirm submission ---
    if response.status_code == 200:
        print("Form submitted successfully!")
    else:
        print("Failed to submit form. Status code:", response.status_code)
    print(path)


def aux(window):
    run = True
    timer_on = time.time()
    while run:
        current_url = window.get_current_url()
        if current_url != urls[-1]: #if current url is different of the last saved
            if current_url == mid:
                window.load_html(mid_html)
            elif current_url == end:
                urls.append(str(current_url))
                window.load_html(end_html)
                run = False
            else:
                urls.append(str(current_url))
    timer_off = time.time()
    path = str_list(filter(filter_url, urls))
    time.sleep(5)
    send(path, timer_off - timer_on)
    window.destroy()

window = webview.create_window('Wikipedia Run', html=start_html, frameless=True, fullscreen=False, focus=False)
webview.start(aux, window)
