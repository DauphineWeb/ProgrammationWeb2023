- [Django](#django)
- [1 Setup](#1-setup)
  - [1.1 Creating a project](#11-creating-a-project)
  - [1.2 Structure](#12-structure)
- [2 Applications](#2-applications)
- [3 Routes](#3-routes)
  - [3.1 Routing to your app](#31-routing-to-your-app)
  - [3.2 Parameterized routes](#32-parameterized-routes)
- [4 Templates](#4-templates)
  - [4.1 Inserting variables](#41-inserting-variables)
  - [4.2 Loops](#42-loops)
  - [4.3 if-else](#43-if-else)
  - [4.4 Lorem ipsum](#44-lorem-ipsum)
  - [4.5 Linking to static files](#45-linking-to-static-files)
  - [4.6 Linking between pages](#46-linking-between-pages)
  - [4.7 Blocks (or template inheritance)](#47-blocks-or-template-inheritance)
  - [4.8 csrf tokens](#48-csrf-tokens)
- [5 Forms](#5-forms)
  - [5.1 Handling POST requests](#51-handling-post-requests)
  - [5.2 Using Django forms](#52-using-django-forms)
- [6 Sessions](#6-sessions)

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

This now lets us return basic html files.

## 4.1 Inserting variables

To make the html now dynamic, Django offers a custom [templating
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

Below are some more of the functionalities that this templating language
enables us to do.

## 4.2 [Loops](https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#std-templatetag-for)

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
Resulting html
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

## 4.3 [if-else](https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#if)

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
Resulting html
</summary>

``` html
<!doctype html>
<html>
  <body>
    
      <h1>This is definitely not a leap year.</h1>
    
  </body>
</html>
```

(there’s roughly a 3/4 chance that your output is different)
</details>

## 4.4 [Lorem ipsum](https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#lorem)

Create some generic lorem-ipsum text. No data is necessary from the
`render()` function.

``` html
<!doctype html>
<html>
  <body>
    <h1>Some latin text</h1>
    {% lorem 3 p %}
  </body>
</html>
```

<details>
<summary>
Resulting html
</summary>

``` html
<!doctype html>
<html>
<body>
    <h1>Some latin text</h1>
    <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>

    <p>In reiciendis enim voluptates sit repellendus quisquam, recusandae necessitatibus minus illo atque maiores, nobis nisi tenetur ea, cupiditate doloribus facilis error? Itaque aspernatur esse odit voluptates soluta nisi voluptatibus fuga commodi facilis. Consectetur ratione neque repellendus fuga eos, est esse explicabo eligendi accusantium, voluptate fugiat accusamus dicta ullam ut voluptas repellendus provident dolores tenetur beatae, tenetur aliquid molestiae dolorum officiis exercitationem amet dignissimos quidem? Sit error suscipit accusantium est quasi distinctio deleniti aperiam vero voluptate vitae, perspiciatis molestiae quia tenetur sit dolor nobis enim numquam reprehenderit nostrum ab, dicta rem quis aliquid culpa totam consequuntur vel repellat in quasi officiis, doloremque harum aliquam deleniti soluta quia cum, quo pariatur eaque?</p>

    <p>Iusto sequi vero, suscipit repellendus cupiditate totam vel iure delectus nesciunt culpa odio aliquid. Cumque inventore earum vero nesciunt provident facilis ex eveniet aspernatur optio explicabo, hic perferendis expedita magni dicta nulla, consequuntur non magnam inventore reiciendis cumque, cumque nulla dolorum facere amet accusantium dignissimos laboriosam culpa voluptate eius facilis? Delectus nostrum culpa, ipsam labore provident corporis eligendi cumque quaerat aut iure. Quod provident quia non illo officia laborum aspernatur, dolorum repudiandae amet eius ullam minus aspernatur eligendi, quibusdam explicabo mollitia beatae eveniet laborum nostrum maxime repudiandae aperiam cupiditate harum, sunt obcaecati quia adipisci, accusantium enim adipisci sed natus porro cupiditate velit omnis deleniti voluptates.</p>
</body>
</html>
```

</details>

## 4.5 [Linking to static files](https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#static)

Static files, such as images, css and js files should be located in
`myapp/static/myapp/`. I.e., suppose the folder structure looks as
follows

    .
    ├── myapp/
    │   ├── ...
    │   ├── static/
    │   │   └── myapp/
    │   │       └── styles.css
    │   ├── templates/
    │   │   └── myapp/
    │   │       └── index.html
    │   ├── urls.py
    │   └── views.py
    ├── ...

Then, we can dynamically link to that file in our template.

``` html
<!doctype html>
<html>
  <head>
    {% load static %}
    <link rel="stylesheet" href="{% static 'myapp/styles.css' %}">
  </head>
  <body></body>
</html>
```

<details>
<summary>
Resulting html
</summary>

``` html
<!doctype html>
<html>
  <head>
    
    <link rel="stylesheet" href="/static/myapp/styles.css">
  </head>
  <body></body>
</html>
```

</details>

## 4.6 [Linking between pages](https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#url)

Recall the `myapp/urls.py` file.

``` python
from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
  path('', views.index, name='index'),
  path('data', views.get_data, name='get_data')
]
```

If we want to link between these pages, we could theoretically enter the
given url paths (here `/myapp` and `/myapp/data`). To stay flexible,
however, it is recommended to use the `name` we have specified in our
`path()` function call and let Django convert it to a valid url.

``` html
<!doctype html>
<html>
  <body>
    <h1>Visit one of our many sites</h1>
    <a href="{% url 'myapp:index' %}">The index page</a>
    <a href="{% url 'myapp:get_data' %}">The data page</a>
  <body/>
</html>
```

<details>
<summary>
Resulting html
</summary>

``` html
<!doctype html>
<html>
  <body>
    <h1>Visit one of our many sites</h1>
    <a href="/myapp/">The index page</a>
    <a href="/myapp/data">The data page</a>
  <body/>
</html>
```

</details>

## 4.7 [Blocks](https://docs.djangoproject.com/en/4.1/ref/templates/language/#template-inheritance) (or template inheritance)

Many html files share the same structure (i.e., the same sceleton
throughout, the same navigation bar, the same footer, etc.). To avoid
duplications, Django allows us to structure our html into block, or, for
some html to inherit from other html files, also known as **template
inheritance**.

Assume the following folder structure.

    .
    ├── myapp/
    │   ├── ...
    │   ├── templates/
    │   │   └── myapp/
    │   │       ├── index.html
    │   │       └── layout.html
    │   ├── urls.py
    │   └── views.py
    ├── ...

The `layout.html` file creates the basic html elements surrounding our
main content.

``` html
<!doctype html>
<html>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    {% load static %}
    <link rel="stylesheet" href="{% static 'myapp/styles.css' %}">
  </head>
  <body>
    {% block body %}
    {% endblock %}
  </body>
</html>
```

For our main content, we only have to extend from the layout and fill in
the necessary blocks.

``` html
{% extends "myapp/layout.html" %}

{% block body %}
  <h1>Hello world</h1>
  <p>Welcome to my site.</p>
{% endblock %}
```

<details>
<summary>
Resulting html
</summary>

``` html
<!doctype html>
<html>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    
    <link rel="stylesheet" href="/static/myapp/styles.css">
  </head>
  <body>
    
  <h1>Hello world</h1>
  <p>Welcome to my site.</p>

  </body>
</html>
```

</details>

## 4.8 [csrf tokens](https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#csrf-token)

`form`s using POST requests are vulnerable to [Cross-Site Request
Forgery
(CSRF)](https://www.squarefree.com/securitytips/web-developers.html#CSRF)
attacks. Django automatically protects against those by requiring these
POST request to come with a unique CSRF token. Not including those in a
form will lead to an error.

``` html
<!doctype html>
<html>
  <body>
    <h1>Enter your credit card number</h1>
    <form action="{% url 'myapp:index' %}" method="post">
      <!-- add csrf protection -->
      {% csrf_token %}
      <!-- user input below -->
      <input type="text" name="name" />
      <input type="submit" />
    </form>
  <body/>
</html>
```

<details>
<summary>
Resulting html
</summary>

``` html
<!doctype html>
<html>
  <body>
    <h1>Enter your credit card number</h1>
    <form action="/myapp/" method="post">
      <!-- add csrf protection -->
      <input type="hidden" name="csrfmiddlewaretoken" value="lcob9Z7kdi7HM7x067aeSZjw4vEqg3U76JrWKBydiUpfNIhXsY7oh0lPGm7dRb0G">
      <!-- user input below -->
      <input type="text" name="name" />
      <input type="submit" />
    </form>
  <body/>
</html>
```

The value of the csrf token will change with every refresh.
</details>

# 5 [Forms](https://docs.djangoproject.com/en/4.1/topics/forms/)

## 5.1 Handling POST requests

<details>
<summary>
Assume the form from before.
</summary>

``` html
<html>
  <body>
    <h1>Enter your credit card number</h1>
    <form action="{% url 'myapp:index' %}" method="post">
      <!-- add csrf protection -->
      {% csrf_token %}
      <!-- user input below -->
      <input type="text" name="name" />
      <input type="submit" />
    </form>
  <body/>
</html>
```

</details>

Once the user has entered their name into the textfield and hit submit,
we can check for the values in the `request` parameter.

- `request.method` tells us the method used (i.e., `GET`, `POST`, `PUT`,
  etc.)
- `request.POST.get('FIELD_IN_FORM')` returns the value of a submitted
  field, or `None` if it is missing. This is analogous for `GET`
  requests.

``` python
from django.shortcuts import render, redirect

def index(request):
  if request.method == 'POST':
    name = request.POST.get('name')
    # do something with name
    # redirect to the same page
    return redirect('myapp:index')
  
  # this part is reached if we did not receive a POST request
  return render(request, 'myapp/index.html')
```

## 5.2 Using [Django forms](https://docs.djangoproject.com/en/4.1/topics/forms/#building-a-form-in-django)

Instead of relying on the html on what information we want to gather, we
can also make use of Django forms. A form is a Python class inheriting
`forms.Form` from the `django` package. It is here where we specify the
attributes, or values, that we want to gather.

``` python
# views.py
from django import forms

class NewPersonForm(forms.Form):
  name = forms.CharField(label='Name')
  age = forms.IntegerField(label='Age', min_value=0, max_value=120)

# to include the form in the html, pass an instance of the class to the template
def index(request):
  return render(request, 'myapp/index.html', {
    'person_form': NewPersonForm()
  })
```

Notice how we have specified some additional information about the
fields, i.e., what label they have, if they accept characters or just
numbers, and what numbers the input should not exceed. There are [many
more
fields](https://docs.djangoproject.com/en/4.1/ref/forms/fields/#core-field-arguments)
we could specify.

Then, to include the Django form inside our html, we simply put the
variable inside two curly braces.

``` html
<!doctype html>
<html>
  <body>
    <h1>Visit one of our many sites</h1>
    <form action="{% url 'myapp:index' %}" method="post">
      <!-- add csrf protection -->
      {% csrf_token %}
      <!-- user content -->
      {{ person_form }}
      <input type="submit" value="Submit" />
    </form>
  <body/>
</html>
```

<details>
<summary>
Resulting html
</summary>

``` html
<!doctype html>
<html>
  <body>
    <h1>Visit one of our many sites</h1>
    <form action="/myapp/" method="post">
      <!-- add csrf protection -->
      <input type="hidden" name="csrfmiddlewaretoken" value="BLHFM6KYZlC4OCECmoP1pSw1o4yb7zemmiKqnIbR4XUCPdozIfMbOTyk0V1YIHkV">
      <!-- user content -->
      <tr>
    <th><label for="id_name">Name:</label></th>
    <td>
      
      <input type="text" name="name" required id="id_name">
      
      
    </td>
  </tr>

  <tr>
    <th><label for="id_age">Age:</label></th>
    <td>
      
      <input type="number" name="age" required id="id_age">
      
      
        
      
    </td>
  </tr>
      <input type="submit" value="Submit" />
    </form>
  <body/>
</html>
```

</details>

Doing this has several advantages.

- For one, it lets Django automatically perform client-side validation,
  giving direct feedback to the user when something is wrong with what
  they have entered.
- Second, it also allows us to perform simple server-side checks. This
  is necessary as it is possible for the user to circumvent checks.
- This also transitions nicely to the way models are handled in Django.
  This will not be discussed here, however.

With the form set up, the only thing left to do is to check on the
server if the given input is valid.

``` python
def index(request):
  # if it isn't a POST request, simply render the page
  if request.method != 'POST':
    return render(request, 'myapp/index.html', { 'person_form': NewPersonForm() })
  
  # we have received a POST request. Try to read it into a variable.
  form = NewPersonForm(request.POST)
  
  # perform server-side check if the input is valid or not.
  # If it isn't, re-render the page with the input the user has entered.
  if not form.is_valid():
    return render(request, 'myapp/index.html', { 'person_form': form })

  # checks passed, we are working with clean data!
  # in that case, we are just reading out the information and returning a JSON response.
  name = form.cleaned_data['name']
  age = form.cleaned_data['age']
  return JsonResponse({
    'name': name,
    'age': age
  })
```

# 6 Sessions

For the next time :)
