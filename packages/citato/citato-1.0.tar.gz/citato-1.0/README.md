# 🤖 Citato - Simple Instagram API
[![PyPI](https://img.shields.io/pypi/v/citato)](https://pypi.org/project/citato)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/citato)]()
[![Downloads](https://static.pepy.tech/badge/citato)](https://pepy.tech/project/citato)

This package lets you use Instagram's Internal Web API through simple functions and classes. Citato uses Instagram's Original Web API to scrape data which makes it a reliable choice over other third-party scrapers. This library mainly focuses on Simplicity & Reliability.

Two type of classes are supported - ***Guest & Host***.

## 📢 Announcements
**[#02]** [AutoHost](https://github.com/ekosijabat/citato/) is released! Authentication update to the *Host Class*.

**[#01]** Users can now log in through their **Username** and **Password** to generate SessionId! [See this](https://github.com/ekosijabat/citato#:~:text=NewSessionID(%22username%22%2C%20%22password%22))

## Installation
To install this package using [Python's PIP](https://pypi.org/project/pip/), run this command in a terminal window:
```shell
$ pip install citato
```

To update the existing package, run:
```shell
$ pip install citato --upgrade
```

## 🧔🏻‍♂️ Guest Mode
This mode doesn't require login and can be used to fetch publicly available data from Instagram's Servers. Following methods are supported till now:
- Check if username is available for registration
- Fetch someone's profile data
- Convert username to userid
- Convert userid to username

Here's an example where an instance of *Guest Class* is created to fetch [Cristiano Ronaldo's](https://www.instagram.com/cristiano/) profile information:

```python
from citato import Guest

guest = Guest()
profile = guest.profile("cristiano")

if profile is None:
    print("Something went wrong.")
else:
    print(profile.biography)
    print(profile.follower_count)
    print(profile.following_count)
```

## 🧔🏻‍♂️ Host Mode
Host mode requires login through SessionID, which should be passed as an argument during initialization.
It can be used to take actions that require login. Additionally, users can manage their own profile through this class.

These are the methods supported till now:
- Check authentication status of the user
- Follow/unfollow users
- Fetch someone's follower/following list
- Switch account type - 'Public' or 'Private'

Here's an example where an instance of *Host Class* is created to follow [Cristiano Ronaldo's](https://www.instagram.com/cristiano/) account:

```python
from citato import Host, NewSessionID

sessionid = NewSessionID("username", "password")

host = Host(sessionid)
status = host.follow("cristiano")

if status is None:
    print("Something went wrong.")
else:
    if status.following:
        print("Following!")
    
    elif status.follow_requested:
        print("Requested to follow!")
```

> ### **Note:**
> When you create a new sessionid through *NewSessionID()*, it's recommended to save it somewhere, and use the same sessionid (instead of creating a new one each time you need) until it expires or becomes invalid.
>
> This should be done to avoid unnecessary prolonged wait time while generating a new sessionid and also to prevent getting your account from getting flagged because of repetitive logins.

## 📋 Remember
Every function should return **None** on failure. So, it's recommended to add an *if statement* before using the actual data to avoid TypeErrors. Here's an example:
```python
from citato import Guest

guest = Guest()
available = guest.username_availability("cristiano")

if available is None:  # 'None' indicates failure
    print("Something went wrong.")
else:
    print(available)
```

## Disclaimer
This is a third-party package, and not approved by Instagram. It doesn't promote illegal activities or activities that violate [Instagram's Community Guidelines](https://help.instagram.com/477434105621119/) such as spamming users, creating bot accounts, misusing data etc. You are solely responsible for all the actions you take using this package.
