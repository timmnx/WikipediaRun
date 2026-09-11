import sys

import webview
import time

debug : bool = "-d" in sys.argv

start = 'https://fr.wikipedia.org/wiki/Cookie_(informatique)'
start_html = f'''
    <html>
    <body style="background-color:Tomato;">
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
# mid   = 'https://fr.wikipedia.org/wiki/Kaamelott'
mid_html = f'''
    <html>
    <body style="background-color:Gold;">
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
# end   = 'https://fr.wikipedia.org/wiki/OCaml'

def str_list(l : list[str]) -> str:
    res = ""
    space = "&nbsp; &nbsp; &nbsp;"
    for e in l:
        res += "<br>"+ space + "->" + e.removeprefix("https://fr.wikipedia.org/wiki/") + space
        # res += str(e) + " -> "
    return res

def time_to_str(t : float) -> str:
    m : int = int(t) // 60
    s : int = int(t) % 60
    c : int = int(t*100) % 100
    if debug: print("time_to_str", t, "->", m,":",s,":",c)
    return (f"{m} minutes {s} secondes et {c} centièmes")

def end_html(path, t, team):
    html = f'''
        <html>
        <body style="background-color:LightGreen;">
            <div style="display: grid; place-items: center; height:100%; width:100%">
                <h1> Bravo, vous avez fini ! </h1>
                <h2> Équipe "{team}" : {time_to_str(t)} ! </h2>

                <div style="background-color: white; border-radius:1em; outset: 3em">
                    <p> {path} <p>
                </div>
            </div>
        </body>
        </html>
    '''
    # html = start_html
    return html


urls : list[str|None]= [None]
timer = None
urls_not_None = []

def main(window):
    global timer, urls_not_None
    if debug: print("here1")
    while window.get_current_url() is None:
        pass
    if debug: print("here2")
    run = True
    timer_on = time.time()
    while run:
        current_url = window.get_current_url()
        if current_url is None:
            raise ValueError("None url... should not be possible!")
        if current_url != urls[-1]: #if current url is different from the last saved
            if current_url == mid:
                if debug: print("mid:", current_url)
                window.load_html(mid_html)
            elif current_url == end:
                if debug: print("end:", current_url)
                urls.append(str(current_url))
                run = False
            else:
                if debug: print("oth:", current_url)
                urls.append(str(current_url))
    timer_off = time.time()
    timer = timer_off - timer_on
    urls_not_None = [url for url in urls if (url is not None and not url.startswith('file://'))]
    window.destroy()


if __name__ == '__main__':
    team = input("Joueurs de l'équipe : ")
    window = webview.create_window('Wikipedia Run', html=start_html, frameless=True, fullscreen=False, focus=False)
    webview.start(main, window)
    if debug: print("hello world")
    path = str_list(urls_not_None)
    window = webview.create_window('Wikipedia Run', html=end_html(path, timer, team), frameless=False, fullscreen=False)
    webview.start()
