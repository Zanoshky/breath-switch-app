#!/usr/bin/env python3
"""Builds the guide pages in docs/ from the bodies below. Run after any edit and commit docs/. Fails on any dash.

The look is the Zanoshky Standard, the same as breathswitch.zanoski.com: docs/tokens.css is a copy of the house
tokens (never edit it here), docs/style.css the guide's own parts. Both are inlined into every page so no
stylesheet holds up the first paint. Every screenshot in docs/img is a real capture of the app."""
import re
from pathlib import Path

D = Path(__file__).parent / "docs"
REPO = "https://github.com/Zanoshky/breath-switch-app"
PLAY = "https://play.google.com/store/apps/details?id=com.zanoshky.breathswitch"
SITE = "https://breathswitch.zanoski.com"
MAIL = "support@zanoski.com"
NAV = [("index.html", "Home"), ("guide.html", "Guide"), ("faq.html", "Questions"), ("report.html", "Report a bug")]

CSS = "\n".join((D / f).read_text() for f in ("tokens.css", "style.css"))
CSS = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S)
CSS = re.sub(r"\s*\n\s*", "\n", CSS).strip()


def shot(img, alt, name, line, lazy=True):
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high"'
    stem = img.rsplit(".", 1)[0]
    # The jpg stays for the README on GitHub; pages pick a small webp, about half the bytes.
    src = f'srcset="img/{stem}-300.webp 300w, img/{stem}-540.webp 540w" sizes="(min-width: 840px) 260px, 45vw"'
    return (f'<figure><img src="img/{img}" {src} alt="{alt}" width="540" height="1200" {load}>'
            f'<figcaption>{name}<span>{line}</span></figcaption></figure>')


def tv(img, alt, name, line):
    stem = img.rsplit(".", 1)[0]
    src = f'srcset="img/{stem}-480.webp 480w, img/{stem}-960.webp 960w" sizes="(min-width: 1140px) 540px, (min-width: 640px) 48vw, 100vw"'
    return (f'<li><figure class="tv"><img src="img/{img}" {src} alt="{alt}" width="960" height="540" loading="lazy" decoding="async">'
            f'<figcaption>{name}<span>{line}</span></figcaption></figure></li>')


def page(name, title, desc, body):
    for bad in ("\u2014", "\u2013", " - "):
        if bad in body:
            raise SystemExit(f"{name}: dash {bad!r} in copy")
    nav = "".join(f'<a class="hide-s" href="{h}"{" aria-current=\"page\"" if h == name else ""}>{t}</a>' for h, t in NAV)
    foot = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == name else ""}>{t}</a>' for h, t in
                   [(SITE, "Home"), ("index.html", "User guide"), ("faq.html", "Questions"), ("report.html", "Report a bug"),
                    (f"{SITE}/privacy", "Privacy"), (f"{SITE}/terms", "Terms")])
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · Breath Switch user guide</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#f6f7f9" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
<meta property="og:title" content="{title} · Breath Switch user guide">
<meta property="og:description" content="{desc}">
<link rel="icon" href="img/icon.svg" type="image/svg+xml">
<link rel="preload" href="fonts/jetbrains-mono-bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/inter-regular.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="bar">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="img/icon.svg" alt="" width="34" height="34"><span>Breath Switch</span></a>
    <nav aria-label="Guide pages">{nav}<a class="key" href="{PLAY}">Get the app</a></nav>
  </div>
</header>
<main id="main" class="page">
  <div class="wrap">
{body}
  </div>
</main>
<footer>
  <div class="wrap">
    <span>Breath Switch by <a href="https://zanoski.com">Marko Zanoski</a></span>
    <nav aria-label="Footer">{foot}</nav>
    <p class="lic">Guide text and images are shared under CC BY 4.0. The Breath Switch app itself is proprietary.</p>
  </div>
</footer>
</body>
</html>
"""
    (D / name).write_text(html)
    print(name)


HOME_ALT = "Breath Switch Home in Dark: Good evening, How do you want to feel?, the planet of light with its teal left half lit, LEFT BREATHE and RIGHT CLOSED, the 2, 5 and 10 min lengths, and the Calm, Focus, Balance and Sleep tiles, with Home, Sessions, Science and Settings in the bar."
SESSION_ALT = "A Moon Breath session in Dark: the planet with its amber right half lit, LEFT CLOSED and RIGHT BREATHE, the Music, Voice, Vibrate and Bubble chips, the count ring at 1 beside Breathe out, Switch. Close the left. Breathe out through the right., and the back a breath, pause and finish keys."
SESSIONS_ALT = "Sessions in Dark, grouped by Calm, Focus and Balance: Left Side Calm, Moon Breath, Right Side Wake Up, Sun Breath, Focus Reset, Alternate Nostril and Alternate With Pause, each with its length and counts, and On the home tile under the tile sessions."
TECH_ALT = "The Left Side Calm page in Dark: Slow, even breaths in and out through the left side only, In 5 and Out 5, the planet, the Length picker with 2, 5, 10 and 15 min, and a Start key."
DONE_ALT = "The done screen in Dark: Session complete, Well done., Every slow breath counts. Notice how you feel right now., 1 minute today, then the card A little ritual, Shall I remind you tomorrow? with Morning, Midday and Evening."
SCIENCE_ALT = "The science in Light, page 1 of 7: The nasal cycle, Your nose takes turns, with crossing teal and amber waves over a day."
ONB_ALT = "Step 2 of 3 in Light: the planet with LEFT OPEN and RIGHT CLOSED, Press one side shut with your thumb, and the note Like a mirror. The picture faces you, so its left is your left."
SETTINGS_ALT = "Settings in Dark: Look, then Sessions with Sound, voice and touch and Breath pace, Reminders with Daily reminder and Workday, Home screen with Add the widget, and App."
SOUND_ALT = "Sound, voice and touch in Dark: calm music, soft tones and the voice guide switched on, her or him for the voice, the touch switches, and With the music off with Tanpura drone chosen."
WORKDAY_ALT = "The Workday page in Dark: Calm check ins in work hours, work hours 9:00 AM to 5:00 PM, Deep focus call each work day at 1:00 PM, and the work days Mon to Sun as check boxes."
PRIVACY_ALT = "Privacy in Dark: red ban chips No ads, No tracking, No analytics, No crash reports, No error reports, No account, No AI and No internet, then Notifications, Run at startup and Vibration with why, and Internet, location, camera, microphone, contacts and health data denied by design."

page("index.html", "Home", "The user guide for Breath Switch, nostril breathing for calm, focus and sleep on Android phones, tablets and TVs.", f"""
    <p class="lbl">User guide</p>
    <h1>Breath Switch</h1>
    <p class="lede">Breathing exercises through one nostril or both in turn. Close one side and breathe through the other: the <span class="left">left</span> for calm, the <span class="right">right</span> for focus, both in turn to find the middle, and a slow wind down for sleep. Pay once, no ads, no account, fully offline. On phones, tablets, Android TV and Google TV.</p>
    <div class="keys">
      <a class="key filled" href="guide.html">Read the guide</a>
      <a class="key tonal" href="report.html">Report a bug or ask for a feature</a>
    </div>
    <ul class="shots">
      <li>{shot("home.jpg", HOME_ALT, "Home", "How do you want to feel?", lazy=False)}</li>
      <li>{shot("session.jpg", SESSION_ALT, "A session", "Which side to close, every breath.")}</li>
      <li>{shot("sessions.jpg", SESSIONS_ALT, "Sessions", "Eight, from 2 to 15 minutes.")}</li>
      <li>{shot("settings.jpg", SETTINGS_ALT, "Settings", "The last item in the bar.")}</li>
    </ul>
    <ul class="tvshots">
      {tv("tv-home.jpg", "Breath Switch Home on a TV with the side rail on the left: A quiet night, minutes today and days in a row, the planet, the Length row with 5 min chosen and the Calm tile in focus.", "On a TV", "Calm is in focus: press OK.")}
      {tv("tv-session.jpg", "A Left Side Calm session on a TV: the planet on the left with its teal half lit, Breathe in with the count ring at 4, the pause key in focus and the hint OK pauses, Back ends the session.", "A session on a TV", "OK pauses, Back ends.")}
    </ul>
""")

page("guide.html", "Guide", "How to use Breath Switch: the moods, the sessions, the planet of light, Science, Settings, the widget, reminders and Android TV.", f"""
    <p class="lbl">Guide</p>
    <h1>How Breath Switch works</h1>

    <div class="with-shot">
      <div class="doc">
        <h2>Close one side</h2>
        <p>The first time, three short steps show you how. Sit up and lift your right hand (any hand is fine if that one is busy). Press one side of your nose shut with your thumb, softly, just enough to close it. Then breathe slowly through the open side, never forcing it.</p>
        <p>The picture is like a mirror: it faces you, so its left is your left and its right is your right. <span class="left">Teal is always left</span> and <span class="right">amber is always right</span>, in every look. To see the steps again, open More (the three dots at the top) and pick How to close one side.</p>
      </div>
      {shot("onboarding.jpg", ONB_ALT, "How to close one side", "Three short steps, the first time.")}
    </div>

    <div class="with-shot">
      <div class="doc">
        <h2>Home</h2>
        <p>Home asks how you want to feel. Pick a length, 2, 5 or 10 minutes, then tap a tile and the session starts.</p>
        <dl class="rows plate">
          <div><dt>Calm</dt><dd>Close right, breathe left.</dd></div>
          <div><dt>Focus</dt><dd>Close left, breathe right.</dd></div>
          <div><dt>Balance</dt><dd>Switch sides each breath.</dd></div>
          <div><dt>Sleep</dt><dd>Close right, breathe left as it dims.</dd></div>
        </dl>
        <p style="margin-top:16px">Above the tiles you see your minutes today and the days in a row.</p>

        <h2>Four sections in the bar</h2>
        <p>The bar at the foot of the screen has Home, Sessions, Science and Settings. Tap one to go there, or tap the one you are on to go back to its top. The three dots at the top right open More: How to close one side and Add the widget.</p>
      </div>
      {shot("home.jpg", HOME_ALT, "Home", "A length, then a mood.")}
    </div>

    <div class="with-shot">
      <div class="doc">
        <h2>A session</h2>
        <p>The planet of light shows what to do. The open half lights up and air spirals into it as you breathe in and out of it as you breathe out; the closed half goes dark. Beside it, LEFT and RIGHT each carry a chip: BREATHE, HOLD, OPEN or CLOSED. The words always say the action, like Close the right. Breathe in through the left., and the count ring shows the seconds.</p>
        <dl class="rows plate">
          <div><dt>Pause and play</dt><dd>The big round key in the middle. While paused the planet keeps turning softly, and the count waits where you left it.</dd></div>
          <div><dt>Back a breath</dt><dd>The key on the left.</dd></div>
          <div><dt>Finish now</dt><dd>The tick on the right.</dd></div>
          <div><dt>The chips</dt><dd>Under the session's name: Music, Voice, Vibrate and Bubble, each a tap away, even mid session. Bubble swaps the planet for a simple bubble that grows and shrinks with your breath.</dd></div>
        </dl>
        <p style="margin-top:16px">The screen stays on while a session runs. At the end you let your hand rest and breathe through both sides.</p>
      </div>
      {shot("session.jpg", SESSION_ALT, "A session", "The open side glows.")}
    </div>

    <div class="with-shot">
      <div class="doc">
        <h2>Sessions</h2>
        <p>Eight guided sessions, grouped by mood, from 2 to 15 minutes. At the written pace each one runs at 5 to 6 breaths a minute, the slow rate used in breathing research. Pauses are short, used in one session only, and never held after the breath out.</p>
        <dl class="rows plate">
          <div><dt>Calm</dt><dd>Left Side Calm and Moon Breath.</dd></div>
          <div><dt>Focus</dt><dd>Right Side Wake Up, Sun Breath and Focus Reset.</dd></div>
          <div><dt>Balance</dt><dd>Alternate Nostril and Alternate With Pause.</dd></div>
          <div><dt>Sleep</dt><dd>Sleep Wind Down, with a long breath out.</dd></div>
        </dl>
        <p style="margin-top:16px">Tap a session to open its page: the pattern, the counts, a length from 2 to 15 minutes, Start, the steps, a Go gently note, what studies found, and the references. Use on the Calm tile (or Focus, Balance, Sleep) puts it on its Home tile.</p>
      </div>
      {shot("technique.jpg", TECH_ALT, "A session page", "Pattern, length and Start.")}
    </div>

    <div class="with-shot">
      <div class="doc">
        <h2>Well done</h2>
        <p>At the end you see your minutes today and the days in a row. Back home or Breathe again. On a phone, Breath Switch may ask once: Shall I remind you tomorrow? Pick a time and tap Yes, remind me, or Not now. After two Not now it never asks again.</p>

        <h2>Science</h2>
        <p>The science in seven short pages, each with a chart and the paper behind it, among them the nasal cycle, six breaths a minute, blood pressure, one session, left and right, and the honest limits. Turn them with Previous and Next, or swipe. Most nostril breathing studies are small, and results vary from person to person.</p>
      </div>
      {shot("done.jpg", DONE_ALT, "Well done", "And a gentle reminder, if you like.")}
    </div>

    <div class="with-shot">
      <div class="doc">
        <h2>The widget</h2>
        <p>Start Calm or Focus from your home screen with one tap; widen it for Balance and Sleep. It starts the Home tile's session at the Home length. Add it from Settings, Home screen, Add the widget, or from More.</p>

        <h2>Reminders</h2>
        <p>Every reminder is off until you turn it on. The daily reminder is one gentle note a day at your time, and none on days you have already breathed with Breath Switch. Workday adds two calm check ins at easy moments in your work hours, none right after a session, and a call to deep focus at your time, only on the days you pick. On Android 13 and newer, Android asks for notifications when you turn one on.</p>
      </div>
      {shot("workday.jpg", WORKDAY_ALT, "Workday", "Check ins and a focus call.")}
    </div>

    <div class="with-shot">
      <div class="doc">
        <h2>Settings</h2>
        <p>Settings is the last item in the bar: cards of rows, each saying what is set now. A row opens its own small page; Back takes you to the hub.</p>
        <dl class="rows plate">
          <div><dt>Look</dt><dd>Follow the phone (Light by day, Dark at night), Light, Dark, or Black, true black for OLED. And Just a bubble to follow, no planet.</dd></div>
          <div><dt>Sound, voice and touch</dt><dd>Calm music under the session, soft tones as the breath turns, and the voice guide; her voice (warm and a little playful) or his (deep and steady); a light tap on each change and a hum that rises and falls with your breath; and with the music off, a Tanpura drone, Ocean waves, Night crickets or Silence.</dd></div>
          <div><dt>Breath pace</dt><dd>A little quicker, As written, Slower or Slowest.</dd></div>
          <div><dt>Daily reminder and Workday</dt><dd>Each off until you turn it on, with its times and days.</dd></div>
          <div><dt>Home screen</dt><dd>Add the widget.</dd></div>
          <div><dt>Privacy</dt><dd>The promises as red ban chips, the three permissions and why, where your practice is kept, and the privacy policy in full.</dd></div>
          <div><dt>Help and feedback</dt><dd>This guide, the report page and the privacy policy.</dd></div>
          <div><dt>About</dt><dd>The version, and the credits for the sounds, the music, the voice and the type. Your minutes, streak and settings stay on this phone.</dd></div>
        </dl>
      </div>
      {shot("sound.jpg", SOUND_ALT, "Sound, voice and touch", "Music, a voice, a hum.")}
    </div>

    <div class="doc">
      <h2>On Android TV and Google TV</h2>
      <p>Breath Switch runs on Android TV and Google TV too: pick a session with the remote, pause with OK, end with Back, and scan links with your phone.</p>
      <dl class="rows plate">
        <div><dt>The side rail</dt><dd>Home, Sessions, Science and Settings sit in a rail on the left instead of the bar.</dd></div>
        <div><dt>Calm in focus</dt><dd>Home opens on the tile of your last mood, Calm at first, so OK starts it. A blue ring shows where you are.</dd></div>
        <div><dt>A session on the remote</dt><dd>OK pauses and plays, Back ends the session. The remote's play and pause keys work too.</dd></div>
        <div><dt>Open on your phone</dt><dd>A TV has no browser, so links (this guide, the report page, the privacy policy) open a QR code in a sheet from the right. Point your phone's camera at it to open the page there.</dd></div>
        <div><dt>Not on a TV</dt><dd>Vibration, reminders, Workday, the widget and More. Dark is where a TV starts; Follow the phone reads Follow the TV.</dd></div>
      </dl>
    </div>
    <ul class="tvshots">
      {tv("tv-home.jpg", "Breath Switch Home on a TV with the side rail on the left: A quiet night, minutes today and days in a row, the planet, the Length row with 5 min chosen and the Calm tile in focus.", "Home on a TV", "Calm is in focus.")}
      {tv("tv-session.jpg", "A Left Side Calm session on a TV: the planet on the left with its teal half lit, Breathe in with the count ring at 4, the pause key in focus and the hint OK pauses, Back ends the session.", "A session", "OK pauses, Back ends.")}
      {tv("tv-sessions.jpg", "Sessions on a TV in two columns of Calm, Focus, Balance and Sleep plates, with Left Side Calm in focus and the home tile sessions marked.", "Sessions", "Pick one with the remote.")}
      {tv("tv-settings.jpg", "Settings on a TV: Look in focus, Sound and voice, Breath pace, About, Privacy, and Help and feedback.", "Settings", "No reminders or touch on a TV.")}
    </ul>

    <div class="with-shot">
      <div class="doc">
        <h2>Privacy</h2>
        <p>No ads, no tracking, no analytics, no crash reports, no account, no AI and no internet. Breath Switch does not even ask for internet access, so Android does not let it reach the network. It asks for three things: notifications, only for the reminders you turn on; running at startup, to set your reminders again after a restart; and vibration, for the tap and the hum. Your choices, today's minutes and your streak stay in the app's own storage on your phone. See the <a href="{SITE}/privacy">privacy policy</a>.</p>

        <h2>Accessibility</h2>
        <p>TalkBack says every part of the breath with its action, like Close the right. Breathe in through the left., and the voice guide stays quiet while TalkBack runs. Every choice is a real switch, check box or radio button. Touch targets are at least 48 dp, words keep a 7 to 1 contrast, text grows with your phone's font size, and with Android's animations off the moving parts keep still.</p>

        <h2>Breathe safely</h2>
        <p>Breathe gently and never force air through a blocked nose. If you feel dizzy or light headed, stop and breathe normally. Skip the right side sessions and the pauses if you have high blood pressure or a heart condition, or if you are pregnant. Never practise while driving or in water. Breath Switch is a relaxation and wellbeing app, not a medical device; it does not diagnose, treat, cure, or prevent any medical condition.</p>
      </div>
      {shot("privacy.jpg", PRIVACY_ALT, "Privacy", "Every promise and permission.")}
    </div>
""")

page("faq.html", "Questions", "Answers to common questions about Breath Switch, and what to try when something does not work.", f"""
    <div class="doc">
    <p class="lbl">Questions</p>
    <h1>Questions and fixes</h1>

    <h2>My nose is blocked</h2>
    <p>Never force air through a blocked side. Breathe slowly through both sides instead; the slow pace is a good part of the point.</p>

    <h2>Which side do I close?</h2>
    <p>The picture is a mirror: its left is your left. <span class="left">Teal is always left</span>, <span class="right">amber is always right</span>, and the words always say it: Close the right. Breathe in through the left.</p>

    <h2>I hear no sound</h2>
    <p>Calm music, the soft tones and the voice guide each have their own switch in Settings, Sound, voice and touch, and the Music and Voice chips switch them mid session. With the music off, the sound under the session can be Silence. The voice guide stays quiet while TalkBack runs.</p>

    <h2>It feels too fast</h2>
    <p>Pick Slower or Slowest in Settings, Breath pace. Stop and breathe normally if you feel dizzy or short of breath.</p>

    <h2>The screen turns off</h2>
    <p>Breath Switch keeps the screen on while a session runs. When you pause or finish, the phone may turn it off as usual.</p>

    <h2>My reminder does not come</h2>
    <p>Reminders are off until you turn them on. If Android's notifications for Breath Switch are off, the switch stays off and Settings says so: turn them on in your phone settings. There is no reminder on days you have already breathed with Breath Switch, and it may come a few minutes after your time. It is set again after a restart or an update.</p>

    <h2>What is the bubble?</h2>
    <p>A simpler picture to follow: one bubble that grows and shrinks with your breath, in place of the planet. Tap Bubble in a session, or turn on Just a bubble to follow in Settings, Look. It needs no permission.</p>

    <h2>How do I add the widget?</h2>
    <p>Settings, Home screen, Add the widget, or More, Add the widget. Or touch and hold your home screen, pick Widgets, then Breath Switch.</p>

    <h2>Does it need the internet?</h2>
    <p>No. It works anywhere, fully offline, and cannot connect at all.</p>

    <h2>Will my streak move to a new phone?</h2>
    <p>Only through Android's own backup, if you use it. Android may then copy your settings to your own Google account; we never see that copy.</p>

    <h2>Where are reminders on my TV?</h2>
    <p>Not there, on purpose, and neither are vibration, Workday or the widget. On a TV, OK pauses a session and Back ends it.</p>

    <h2>On a TV, how do I open a link?</h2>
    <p>A TV has no browser, so a link opens a QR code. Point your phone's camera at it to open the page on your phone.</p>

    <h2>Is it a medical app?</h2>
    <p>No. Breath Switch is a relaxation and wellbeing app. It is not a medical device and does not diagnose, treat, cure, or prevent any medical condition. It is not a treatment for anxiety disorders, sleep problems or high blood pressure. If you have a health condition, talk to your doctor before starting any breathing practice.</p>
    </div>
""")

page("report.html", "Report a bug", "How to report a Breath Switch bug or ask for a feature on GitHub.", f"""
    <div class="doc" style="max-width:none">
    <p class="lbl">Report</p>
    <h1>Report a bug or ask for a feature</h1>
    <p style="margin-top:16px">Found something broken, or have an idea? Tell us on GitHub. A free GitHub account is all you need.</p>
    <div class="cards">
      <div class="card plate"><h2 class="h3">Bug report</h2><p>Something does not work, sounds wrong, or crashes.</p><a class="key filled" href="{REPO}/issues/new?template=bug_report.yml">Report a bug</a></div>
      <div class="card plate"><h2 class="h3">Feature request</h2><p>A session, a sound or something you would like Breath Switch to do.</p><a class="key tonal" href="{REPO}/issues/new?template=feature_request.yml">Ask for a feature</a></div>
    </div>
    </div>
    <div class="doc">
    <h2>Before you write</h2>
    <ul>
      <li>Search the <a href="{REPO}/issues">open issues</a> first. If yours is there, add a thumbs up or a comment.</li>
      <li>Check the <a href="faq.html">questions and fixes</a> page.</li>
      <li>One problem per report makes it faster to fix.</li>
    </ul>

    <h2>What helps</h2>
    <dl class="rows plate">
      <div><dt>App version</dt><dd>Settings, About, or Android settings, Apps, Breath Switch.</dd></div>
      <div><dt>Device and Android version</dt><dd>Android settings, About phone (on a TV, Settings, System, About).</dd></div>
      <div><dt>Which screen</dt><dd>Home, a session by name, Sessions, Science, the done screen, Settings, the widget, a reminder, or the TV rail and remote.</dd></div>
      <div><dt>Steps</dt><dd>What you did, one step per line, so we can do the same.</dd></div>
      <div><dt>Expected and actual</dt><dd>What you thought would happen, and what happened.</dd></div>
      <div><dt>A picture or a recording</dt><dd>A screenshot or a short screen recording. Drag it into the form.</dd></div>
    </dl>
    <p style="margin-top:16px">Issues on GitHub are public. Before you attach a screenshot, crop or cover anything private.</p>

    <h2>Other ways</h2>
    <p>Prefer not to use GitHub? Write to <span class="mail">{MAIL}</span> (<a href="mailto:{MAIL}">write an email</a>).</p>
    </div>
""")
