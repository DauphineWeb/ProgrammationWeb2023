-   [Django](#django)
    -   [Setup](#setup)

# Django

In the first lecture, we have discussed from a high-level overview of
how the web works. To recapitulate, once a URL is entered into the
browser, the browser looks for the corresponding IP address using via
DNS, connects to a server, sends the user’s *request* using the HTTP
(hyper-text transfer protocol) and in turn waits for the server to
process and *respond* to that request.

So far, we have only looked at the basic building blocks that the
browser understands, namely HTML, CSS, and JavaScript. These are
considered *frond-end* technologies, stuff that is directly visible to
the user.

Now, we will take a look at [Django](https://www.djangoproject.com), a
Python web framework that lets us build a *back-end* server. Django lets
us receive HTTP requests and respond with anything we wish, be it static
HTML and CSS files or dynamically generated HTML files or JSON objects.

## Setup

Make sure [Python 3](https://www.python.org/downloads/) and
[pip3](https://pypi.org/project/pip/) are installed. Then, in the
command line (i.e., Terminal), run `pip3 install Django` to install
Django.

To create a project, run the following commands (alternatively you can
take a look at
[PyCharm](https://www.jetbrains.com/help/pycharm/creating-and-running-your-first-django-project.html)):

1.  `django-admin startproject PROJECT_NAME`: create the basic structure
    of the project.
2.  `cd PROJECT_NAME`: navigate into the project folder.
3.  `python manage.py runserver`: Start the server. (you may need to
    specify `python3 manage.py runserver` depending on how Python is
    installed on your machine)

You should see something like this:

    $ python3 manage.py runserver
    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).

    You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
    Run 'python manage.py migrate' to apply them.
    March 08, 2023 - 20:01:00
    Django version 4.1.7, using settings 'PROJECT_NAME.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

We can savely ignore most debug messages and focus on the second-last
row. It says that the server can be reached using via
`http://127.0.0.1:8000/`. Recall that `http` stands for the protocol,
`127.0.0.1` is the IP address (which here is the same as `localhost`)
and `:8000` is the port the server listens to.

Opening the URL should show you a default page Django has prepared.

[!Django homepage](res/django_screenshot.png)
