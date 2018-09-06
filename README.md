# SimpleTwitterApp
This is a light-weight application, developed on [Flask](https://github.com/pallets/flask).
Specially for Anymind Group.

## Installation
Application was developed and tested on _Python 3.6.4_, so it is recommended to use it.
However Python of a higher version should be satisfactorily as well.

Start by cloning this repository:

    git clone https://github.com/godis-michael/SimpleTwitterApp.git
    cd SimpleTwitterApp

Install required packages from requirements.txt:
    
    pip install -r requirements.txt
    
To be able to connect to the Twitter API, the application uses credentials from `.env` file or system environment.
Variables, that should be set are:
* CONSUMER_KEY
* CONSUMER_SECRET
* ACCESS_TOKEN
* ACCESS_TOKEN_SECRET

Consider modifying `.env` file in a following format:

    CONSUMER_KEY=somevalue
    CONSUMER_SECRET=somevalue
    ACCESS_TOKEN=somevalue
    ACCESS_TOKEN_SECRET=somevalue
    
Otherwise, set system variables like `set CONSUMER_KEY=somevalue` (for Windows) or `CONSUMER_KEY=somevalue` (for Linux).

## Usage
When everything is configured, it is time to start the application ;)

Simply run:

    python SimpleTwitterApp.py
    
If all required variables are set correctly, you will see a message about server running under `http://127.0.0.1:5000/`.
Enter a browser and go to that address. You will see the welcome page.

This application has 2 endpoints for retrieving an information from the Twitter:
* get tweets by a hashtag: _http://127.0.0.1:5000/hashtags/SomeHashtag/_
* get user tweets: _http://127.0.0.1:5000/users/SomeUser/_

Replace `SomeHashtag` or `SomeUser` respectively with your information and make a request.

`?pages_limit` parameter is also accepted and could be used in the following way:

    http://127.0.0.1:5000/users/SomeUser?pages_limit=3
    
By default returned number of pages is equal to **1**.

There is also error handling implemented, so if you try to make request with an invalid username, some unexpected value,
passed to the `?pages_limit` parameter or so on, you will get _json_ object with error description.

Check this out:

    >>> http://127.0.0.1:5000/hashtags/Hello World/  # space in hashtag name
    >>>
    {
        "error": "hashtag format is not valid"
    }
    
## Debug
To evaluate tests enter the root directory and run:

    python -m pytest
    
You should be notified about successful evaluation of 32 tests. 

_**Note:**_ tests evauation also requires the Twitter API credentials to be set properly.
