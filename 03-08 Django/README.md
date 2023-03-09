- [Django](#django)
- [1 Setup](#setup)
  - [1.1 Creating a project](#creating-a-project)
  - [1.2 Structure](#structure)
- [2 Applications](#applications)
- [3 Routes](#routes)
  - [3.1 Routing to your app](#routing-to-your-app)
  - [3.2 Parameterized routes](#parameterized-routes)
- [4 Templates](#templates)
  - [4.1 Loops](#loops)
  - [4.2 if-else](#if-else)

# Django

In the first lecture, we have discussed from a high-level how the web
works. To recapitulate, once a URL is entered into the browser, the
browser looks for the corresponding IP address via DNS lookup, connects
to a server, sends the user’s **request** using HTTP (hyper-text
transfer protocol) and in turn waits for the server to process and
**respond** to that request.

So far, we have looked at the basic building blocks that the browser
understands, namely HTML, CSS, and JavaScript. These are considered
**frond-end** technologies, stuff that is directly visible to the user.

Now, we will take a look at [Django](https://www.djangoproject.com), a
Python web framework that lets us build a **back-end** server. Django
allows us to receive HTTP requests and respond with anything we wish, be
it static files (html, css, images, etc.), dynamically generated HTML
files, or JSON objects, to name a few.

# 1 Setup

## 1.1 Creating a project

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
row. It says that the server can be reached via
`http://127.0.0.1:8000/`. Recall that `http` stands for the protocol,
`127.0.0.1` the IP address (which here is a special address only
accessible from our own device, also known as `localhost`) and `:8000`
the port the server listens to.

<details>
<summary>
Opening the URL should show you a default page Django has prepared.
</summary>

<figure>
<img src="res/django_screenshot.png" alt="Django homepage" />
<figcaption aria-hidden="true">Django homepage</figcaption>
</figure>

</details>

## 1.2 Structure

Open the project in your editor of choice. It should contain the
following files and folders.

    .
    ├── db.sqlite3
    ├── manage.py
    └── PROJECT_NAME/
        ├── __init__.py
        ├── __pycache__/
        │   ├── ...
        ├── asgi.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py

The important files to take note of are:

- `manage.py`: We won’t edit that file, but use it to run a bunch of
  commands. Simply running `python manage.py` gives you a bunch of
  available subcommands.
- `settings.py`: Settings for the project, such as installed apps,
  middleware, directories for static files, etc.
- `urls.py`: routing information, which app handles what subroutes.

# 2 Applications

A Django project is split into several **applications**. This helps us
split a big project into smaller chunks, each with its own distinct
purpose.

Within your project, create a new app by

1.  running `python manage.py startapp APP_NAME`, and
2.  adding `APP_NAME` to the list `INSTALLED_APPS` inside `settings.py`.
3.  Add the specific route to your app in `PROJECT_NAME/urls.py`.

<details>
<summary>
(the third step will be delved into in the next section, but you can
view the code here)
</summary>

``` python
from django.contrib import admin
from django.urls import path, include # don't forget to import include

urlpatterns = [
  path('myapp/', include('APP_NAME.urls')),
  path('admin/', admin.site.urls),
]
```

</details>

Running the `startapp` subcommand creates a new directory.

    ├── myapp/
    │   ├── __init__.py
    │   ├── __pycache__/
    │   │   ├── ...
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations/
    │   │   ├── ...
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py

# 3 Routes

## 3.1 Routing to your app

In order to tell Django what the user should receive depending on the
URL they have typed in, we need to create functions in Python that take
in a **request** object as a parameter and return some type of
**response** object for Django to send back to the user.

1.  Open `myapp/views.py`.
2.  Add a function creating a response.

<details>
<summary>
Code
</summary>

``` python
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

def index(request):
  return HttpResponse('Hello, World!')

def get_data(request):
  obj = {
    'name': 'Alex',
    'age': 42
  }
  return JsonResponse(obj)
```

</details>

3.  Create a file `myapp/urls.py`. This lets us **route** URLs to the
    corresponding functions in Python that we have created.
4.  Add the paths linking up the URLs to your corresponding Python
    function the newly created `myapp/urls.py` file.

<details>
<summary>
Code
</summary>

``` python
from django.urls import path
from . import views

# a namespace for our app, this will become important in the Templates section
app_name = 'myapp'

# we call the path function to let Django know what of our Python function should be
# called when a certain URL has been entered.
# The name parameter is optional, but lets us later more conveniently link between pages.
urlpatterns = [
  path('', views.index, name='index'),
  path('data', views.get_data, name='data')
]
```

</details>

5.  If not done already, add the route to your app to the project in
    `PROJECT_NAME/urls.py`.

<details>
<summary>
Code
</summary>

``` python
from django.contrib import admin
from django.urls import path, include # don't forget to import include

urlpatterns = [
  path('myapp/', include('APP_NAME.urls')),
  path('admin/', admin.site.urls)
]
```

</details>

If we now start the server using `python manage.py runserver`, opening
up `127.0.0.1:8000/myapp` returns the `HttpResponse` from step 2. If we
open `127.0.0.1:8000/myapp/data`, we should see a JSON response.

## 3.2 Parameterized routes

You may have noticed that in sites like
[github.com](https://www.github.com/) you are able to append any string
such that it leads you to the page of a user and their projects (i.e.,
`https://github.com/DauphineWeb/ProgrammationWeb2023` leads to the
`ProgrammationWeb2023` project by the user `DauphineWeb`).

Django lets us **parameterize** the URL, letting us know what type of
string we are expecting in the URL. The `path()` call in `myapp/urls.py`
could look something like this.

``` python
path('<str:user>/<int:project_id>', views.get_project, name='get_project')
```

Here, we expect two parameters, a string and an integer. When calling
our function in `views.py`, we then simply add these parameters to the
corresponding function.

``` python
def get_project(request, user, project_id):
  return HttpResponse(f'Looking at project #{project_id} by the user {user}.')
```

Now, URLs such as `localhost:8000/myapp/martha/1` or
`localhost:8000/myapp/sarah/99` calls `get_project` and correctly sets
the parameters `user` and `project_id` to the corresponding URL segment.

# 4 Templates

Technically, we are able to put html directly into an `HtmlResponse`
object.

``` python
def index(request):
  return HttpRequest('<html><body><h1>Hello there</h1><script>alert("Ah, an alert!")</script></body></html>')
```

It should be immediately clear, however, that this becomes unwieldy
quickly. This is also bad design, as we may want to keep our html, css
and js separate from any back-end logic.

Instead, we will take a look at [Django’s
templates](https://docs.djangoproject.com/fr/2.2/topics/templates/).

Inside your app (here called `myapp`), create a folder called
`templates/myapp` and add a file called `index.html` with some HTML
content. Your folder structure should look like this.

    .
    ├── myapp/
    │   ├── ...
    │   ├── templates/
    │   │   └── myapp/
    │   │       └── index.html
    │   ├── urls.py
    │   └── views.py
    ├── ...

Then, inside `views.py`, we call `render()` to return the page.

``` python
from django.shortcuts import render

def index(request):
  return render(request, 'myapp/index.html')
```

This now lets us return basic html files. To make the html now dynamic,
Django offers a custom [templating
language](https://docs.djangoproject.com/en/4.1/ref/templates/language/)
that changes the html before it is returned to the user.

To do this, we need to pass objects to the html file.

``` python
def index(request):
  return render(request, 'myapp/index.html', {
    'some_value': 42
  })
```

Then, in our html file, using the special templating syntax, we can
insert values passed in using double curly braces.

``` html
<!doctype html>
<html>
  <body>
    <h1>Today's lucky number: {{ some_value }}</h1>
  </body>
</html>
```

Once the user receives the html, they do not see any of the curly braces
or what’s within them. It will be replaced by the number 42.

What follows are some examples on what other features the templating
language includes.

## 4.1 [Loops](https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#std-templatetag-for)

*Python file*

``` python
def index(request):
  return render(request, 'myapp/index.html', {
    'lotto_numbers': [1, 2, 3, 4, 'cat', 5]
  })
```

*html file*

``` html
<!doctype html>
<html>
  <body>
    <ul>
      {% for number in lotto_numbers %}
      <li>{{ number }}</li>
      {% endfor %}
    </ul>
  </body>
</html>
```

<details>
<summary>
*Resulting html*
</summary>

``` html
<!doctype html>
<html>
  <body>
    <ul>
      
      <li>1</li>
      
      <li>2</li>
      
      <li>3</li>
      
      <li>4</li>
      
      <li>cat</li>
      
      <li>5</li>
      
    </ul>
  </body>
</html>
```

</details>

## 4.2 [if-else](https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#if)

*Python file*

``` python
import datetime
def index(request):
  return render(request, 'myapp/index.html', {
    'isLeapYear': datetime.datetime.now().year % 4 == 0
  })
```

*html file*

``` html
<!doctype html>
<html>
  <body>
    {% if isLeapYear %}
      <h1>It (probably) is a leap year.</h1>
    {% else %}
      <h1>This is definitely not a leap year.</h1>
    {% endif %}
  </body>
</html>
```

<details>
<summary>
*Resulting html*
</summary>

``` html
<!doctype html>
<html>
  <body>
    
      <h1>This is definitely not a leap year.</h1>
    
  </body>
</html>
```

(there’s roughly a 3/4 chance that this your output is different)
</details>