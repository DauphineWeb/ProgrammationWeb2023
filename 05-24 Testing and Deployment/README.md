Testing and Deployment
======================


# Uploading files

A simple way to host user uploaded files is to set the `MEDIA_ROOT` and `MEDIA_URL` variables in `settings.py`, adding these paths to our application and letting Django handle the rest.

1. Setting `MEDIA_ROOT` (the physical directory) and `MEDIA_URL` (the path in the url) where user uploaded media is saved.

```py
# https://stackoverflow.com/a/72083188/7669319
# absolute path to the directory where uploaded files are stored
# setting "MEDIA_ROOT" never ever influence to media file URL
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# set the url path from which the media can be retreived
MEDIA_URL = '/media/'
```

2. In our model, add something that uses files or images. In the case of an `ImageField`, [pillow](https://pillow.readthedocs.io/en/stable/) needs to be installed. 

```py
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', default='default.jpg')
```

3. From the model, create a form that includes the field requiring user uploaded data.

```py
from django import forms
from .models import UserProfile

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']
```

4. Create a view containing the form. Here are two ways to do this; one using Django's [class based views](https://docs.djangoproject.com/en/4.2/topics/class-based-views/)...

```py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import UserProfile
from . import forms

@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'users/profile.html', { 'profile': profile.profile_picture })

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['profile_picture']
    template_name = 'users/user_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.userprofile
```

... and one using reqular old view functions.

```py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'users/profile.html', { 'profile': profile.profile_picture })

@login_required
def user_profile_update(request):
    if request.method == 'POST':
        form = forms.ProfilePictureForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = forms.ProfilePictureForm(instance=request.user.userprofile)

    context = {
        'form': form,
    }
    return render(request, 'users/user_profile.html', context)
```

5. Add the view to `urls.py`. In particular, we need to include `+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` after the `urlpatterns` list.

```py
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.UserProfileUpdateView.as_view(), name='edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Doing it with Microsoft

Using the project's local storage for saving user uploaded data is bad practice.
Normally, using some static storage options is the way to go (i.e., [Amazon S3 object storage](https://aws.amazon.com/s3/), [Microsoft Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs/), [Google Cloud storage](https://cloud.google.com/storage), ...). These three listed offer an easy way to integrate their storage system into your Django application, usually just by installing and adding some middleware and changing some settings (i.e., [Amazon S3](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html), [Azure Storage](https://django-storages.readthedocs.io/en/latest/backends/azure.html), [Google Cloud Storage](https://django-storages.readthedocs.io/en/latest/backends/gcloud.html)).

Here is just an example on how to incorporate Microsoft's [Azure Storage](https://django-storages.readthedocs.io/en/latest/backends/azure.html) into Django.

1. Install the `django-storages[azure]` package.

```
pip3 install django-storages[azure]
```

2. Add `storages` to the list of installed apps in `settings.py`, call `load_dotenv()`, and set the default values and credentials associated with your Azure account.

```py
from dotenv import load_dotenv
load_dotenv()

INSTALLED_APPS = [
    # ...
    'storages',
    # ...
]

AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = os.getenv('AZURE_ACCOUNT_KEY')
AZURE_CONTAINER = os.getenv('AZURE_CONTAINER')

DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
MEDIA_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER}/"
```

3. In the case of environment variables, make sure to set them somewhere (either on your system itself, in some `.env` file, by passing these variables directly on startup to the program or in the docker container)

```
AZURE_ACCOUNT_NAME=<your-account-name>
AZURE_ACCOUNT_KEY=<your-account-key>
AZURE_CONTAINER=<your-container-name>
```

That's it!

## SAS

The uploaded files are currently visible to everyone. To manage permissions and who gets to access them, [Shared Access Signatures](https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview) is one way to control it. SAS is specific to Azure; for Amazon S3 you'd use [presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html), for Google Cloud [signed URLs](https://cloud.google.com/storage/docs/access-control/signed-urls).

All of them are similar, in that the credentials to some data is directly stored in the URL itself.

![SAS Storage URI](res/sas-storage-uri.svg)

Here, we will look how this is done in the specific case of Microsoft's Azure Blob Storage.

1. Install `azure-storage-blob`.

```
pip install azure-storage-blob
```

2. Create a private storage class in `myapp/storage_backends.py`. The `url()` function generates a URL to a file that has a SAS token attached to it.

```py
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from storages.backends.azure_storage import AzureStorage
from datetime import datetime, timedelta

class AzurePrivateStorage(AzureStorage):
    def url(self, name, expire=timedelta(hours=1)):
        blob_url = super().url(name)
        sas_token = generate_blob_sas(
            account_name=self.account_name,
            account_key=self.account_key,
            container_name=self.azure_container,
            blob_name=name,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + expire
        )
        return blob_url + '?' + sas_token
```

3. Set the newly createed `AzurePrivateStorage` class as the default backend (make sure to change `myapp` to your application name).

```py
DEFAULT_FILE_STORAGE = 'myapp.storage_backends.AzurePrivateStorage'
```

# Testing

So far we have only built our Django applications and, through experimentation and experience, determined if a program works the way it should or not.
As projects grow more complex, it is always highly advisable to start testing each component (it should usually already start right from the get-go).

```py
# show testing with print statements
# automate tests!
```

## Assertions

In Python, the `assert` statement is one of the simplest way to test the state of a certain variable.
This keyword is followed by a boolean expression that must result in `True` during runtime.
If it is `True`, nothing happens, else, the entire program crashes with an `AssertionError`.

```py
def square(x):
    x * x

# left: actual value
# right: expected value
assert square(10) == 100
```

Here, the square function works as expected.
`square(10)` produces the result `100`, which in turn means that the `square(10) == 100` evaluates to true, which tells `assert` that our program is in the state we expect it in.
Suppose we have made a simple mistake and used a `+` instead of a `*` symbol.

```py
def square(x):
    x + x

assert square(10) == 100
# Traceback (most recent call last):
#   File "assert.py", line 4, in <module>
# AssertionError
```

Here, the program crashes and we are notified exactly in what line that error was thrown.

Assertion statements typically reside in the production code itself.
Because an `AssertionError` has such a severe consequence to our program, it should only be used if the subsequent code cannot run if a certain evaluation is not met.
A comment on [StackOverflow](https://stackoverflow.com/a/424063/7669319) puts this fairly nicely into perspective.

> Assertions are comments that do not become outdated.
> They document which theoretical states are intended, and which states should not occur.
> If code is changed so states allowed change, the developer is soon informed and needs to update the assertion.


## Automating tests

Instead of hacking with assertions in our production code, it makes sense to split our tests from the actual functions we want to test.
We create a `palindrome.py` file that contains a function, checking if a given word is a palindrome or not.

```py
# palindrome.py
def is_palindrome(word):
    return word == word[::-1]
```

Then, we create a separate file, `tests.py`, that we intend to use for all of our testing purposes.

```py
# tests.py
from palindrome import is_palindrome

assert is_palindrome('tôt') == True
assert is_palindrome('') == True
assert is_palindrome('bientôt') == False
assert is_palindrome('Level') == True
assert is_palindrome('racecar') == True
assert is_palindrome('my gym') == True
assert is_palindrome('forward') == False
assert is_palindrome('Anna') == True
```

Running `tests.py` already tells us that there is something wrong with our function.

```
Traceback (most recent call last):
  File "tests.py", line 6, in <module>
    assert is_palindrome('Level') == True
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
```

The output itself isn't necessarily bad, we would be able to locate our bug rather quickly.
But we may be able to improve the testing behavior.
For example, we may not want the tests to crash once an error was found.
Furthermore, it might be nice to see how many tests have succeeded and how many have failed.

```py
# tests.py
from palindrome import is_palindrome

total = 0
succeeded = 0

def test_palindrome(input, expected):
    global total, succeeded
    total += 1
    result = is_palindrome(input)
    if result == expected:
        succeeded += 1
    else:
        print(f"Error in is_palindrome('{input}'): expected {expected}, got {result}")

test_palindrome('tôt', True)
test_palindrome('', True)
test_palindrome('bientôt', False)
test_palindrome('Level', True)
test_palindrome('racecar', True)
test_palindrome('my gym', True)
test_palindrome('forward', False)
test_palindrome('Anna', True)

print(f"{succeeded} of {total} tests succeeded {'🎉' if succeeded == total else '🚩'}")
```

Now the output seems a little nicer.

```
$ python3 tests.py
Error in is_palindrome(Level): expected True, got False
Error in is_palindrome(my gym): expected True, got False
Error in is_palindrome(Anna): expected True, got False
5 of 8 tests succeeded 🚩
```

As it turns out, our function does not take capitalization and spaces into account.
These should be easily fixable.

```py
# palindrome.py
def is_palindrome(word):
    word = word.replace(' ', '').lower()
    return word == word[::-1]
```

Now all our tests succeed.

```
$ python3 tests1.py
8 of 8 tests succeeded 🎉
```

It would also be beneficial to also test for cases where the function does to receive a value it expects, i.e., a number.
In our case, we would simply want the program to throw an error.
We could encorporate testing for these expected errors into our test suite - but as it turns out, there is already a rich ecosystem of packages in Python that does it for us.

## Unit testing

Unit testing is a type of software testing where individual components of a software are tested.
The purpose is to validate that each unit of the software performs as designed.

We already created a form of unit tests in the previous section.
However, Python already comes packed with its own [`unittest`](https://docs.python.org/3/library/unittest.html) library.

We begin by defining a new function that returns the average of a list of elements.

```py
# avg.py
def avg(els):
    return sum(els) / len(els)
```

To use `unittest`, we create a test class

```py
import unittest
from avg import avg

class Tests(unittest.TestCase):

    def test_1(self):
        """Test avg with an empty list"""
        self.assertEqual(avg([]), 0)

    def test_2(self):
        """Test lists with a single element"""
        self.assertEqual(avg([-3]), -3)
        self.assertEqual(avg([0]), 0)
        self.assertEqual(avg([3]), 3)
    
    def test_3(self):
        """Test lists with two elements"""
        self.assertEqual(avg([1,2]), 1.5)
        self.assertEqual(avg([-1,1]), 0)
    
    def test_4(self):
        """Test with lists containing more than two elements"""
        self.assertEqual(avg([1,2,4,8]), 7.5)
        self.assertEqual(avg([2,2,4,8]), 4)
        self.assertEqual(avg(list(range(101))), 50)

if __name__ == '__main__':
    unittest.main()
```

A few things are going on here.

* The test class must inherit from `unittest.TestCase`.
* Each test function must start with `test_` for `unittest` to be recognized as such.
* Each test function starts with a [docstring](https://www.docstring.fr/glossaire/docstring/) (surrounded by three quotation marks). It is optional, but `unittest` prints these docs if an error occurs, helping us to more easily spot which test function failed.
* Each testing function provided by `unittest` starts is of the form `assertSomething(...)`. Here, we only made use of `assertEqual()`, but we could have also made use of [`assertTrue()`](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertTrue), [`assertFalse()`](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertFalse), [`assertGreater()`](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertGreater), [`assertRaises()`](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaises), etc.

Running our test now produces this output.

```
$ python3 tests.py
E..F
======================================================================
ERROR: test_1 (__main__.Tests.test_1)
Test avg with an empty list
----------------------------------------------------------------------
Traceback (most recent call last):
  File "tests.py", line 8, in test_1
    self.assertEqual(avg([]), 0)
                     ^^^^^^^
  File "avg.py", line 3, in avg
    return sum(els) / len(els)
           ~~~~~~~~~^~~~~~~~~~
ZeroDivisionError: division by zero

======================================================================
FAIL: test_4 (__main__.Tests.test_4)
Test with lists containing more than two elements
----------------------------------------------------------------------
Traceback (most recent call last):
  File "tests.py", line 23, in test_4
    self.assertEqual(avg([1,2,4,8]), 7.5)
AssertionError: 3.75 != 7.5

----------------------------------------------------------------------
Ran 4 tests in 0.000s

FAILED (failures=1, errors=1)
```

From the last line, we see that one test function failed and one other actually raised an error. At the top, `E..F` signifies the result of each test function.

* `.`: All assertions in the test function succeeded.
* `F`: An assertion in the test function failed.
* `E`: An assertion in the test function unexpectedly raised an error.

Going through the errors, we can spot that for `test_1()` a `ZeroDivisionError` was raised, because the denominator `len(els)` of the division is 0.
As for the failed test, we see that `avg([1,2,4,8])` was evaluated to `3.75` and not `7.5`. This might be a mistake from the side of the written test: truth be told, I accidentally divided the some of 1, 2, 4, and 8 by two and not four.

Let's fix the function to take empty lists into account.

```py

def avg(els):
    if len(els) == 0:
        return 0
    return sum(els) / len(els)
```

Updating `test_4()` to use the correct values, running the tests now produces no errors.

```
$ python3 tests.py
....
----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
```

Tests are especially useful if the function already works as expected, but we want to change some of the internals, i.e., refactoring nested function calls or optimizing the code itself. This ensures that changes we do to our code does not change its overall behavior.

## Testing in Django

Django offers its own extension of a testing framework that is very similar to what we have just seen.

To start off, we'll introduce two models, `Actor` and `Movie`.

```py
# models.py
from django.db import models
from django.contrib.auth.models import User

class Actor(models.Model):
    name = models.CharField(max_length=100)

class Movie(models.Model):
    title = models.CharField(max_length=128)
    duration = models.IntegerField()
    rating = models.SmallIntegerField()
    actors = models.ManyToManyField(Actor)
    favorited_by = models.ManyToManyField(User, related_name='favorite_movies')

    def is_valid(self):
        return (self.duration >= 0) or (1 <= self.rating <= 5)
```

Next, in `tests.py`, we import `TestCase` from `django.test`. Inside our test class, we first define a `setUp` function. This function is called before running the test functions. It creates a temporary database with temporary tables that will be destroyed after each test.

```py
# tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Movie, Actor

class MovieModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        self.actor1 = Actor.objects.create(name='Actor 1')
        self.actor2 = Actor.objects.create(name='Actor 2')

        self.movie1 = Movie.objects.create(title="Movie 1", duration=120, rating=5)
        self.movie1.actors.add(self.actor1, self.actor2)
        self.movie1.favorited_by.add(self.user1)

        self.movie2 = Movie.objects.create(title="Movie 2", duration=100, rating=4)
        self.movie2.actors.add(self.actor1)
        self.movie2.favorited_by.add(self.user1, self.user2)
```

Finally, we'll create several `test_` functions to check if our models and its utility functions behave the way we expect them to.

```python
class MovieModelTest(TestCase):

    def setUp(self):
        # ...
    
    def test_valid(self):
        movie = Movie(title="Test Movie", duration=120, rating=5)
        self.assertTrue(movie.is_valid())
    
    def test_invalid_duration(self):
        movie = Movie(title="Test Movie", duration=-5, rating=5)
        self.assertFalse(movie.is_valid())

    def test_invalid_rating(self):
        movie = Movie(title="Test Movie", duration=120, rating=6)
        self.assertFalse(movie.is_valid())
        
    def test_invalid_duration_and_rating(self):
        movie = Movie(title="Test Movie", duration=-5, rating=0)
        self.assertFalse(movie.is_valid())
        
    def test_favorites(self):
        # Test that users have correct favorite movies
        self.assertEqual(list(self.user1.favorite_movies.all()), [self.movie1, self.movie2])
        self.assertEqual(list(self.user2.favorite_movies.all()), [self.movie2])

    def test_actors(self):
        # Test that movies have correct actors
        self.assertEqual(list(self.movie1.actors.all()), [self.actor1, self.actor2])
        self.assertEqual(list(self.movie2.actors.all()), [self.actor1])
```

## Testing views with Client

Testing views requires some extra setup as we want to simulate the normal conversation a browser has with the server. In other words, we wish to simulate an entire HTTP request.

In Django, this is done with the [Client](https://docs.djangoproject.com/en/4.2/topics/testing/tools/#the-test-client) class.

First, we introduce an index page that returns a page containing all movies.

```py
# views.py
def index(request):
    movies = Movie.objects.all()
    return render(request, 'movies/index.html', {'movies': movies})
```

For completeness' sake, here is what the html could look like.

```html
<!-- templates/movies/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Movie List</title>
</head>
<body>
    <h1>Movie List</h1>
    <ul>
        {% for movie in movies %}
            <li>{{ movie.title }} ({{ movie.duration }} min, {{ movie.rating }} stars)</li>
        {% empty %}
            <li>No movies available.</li>
        {% endfor %}
    </ul>
</body>
</html>
```

Next, our `setUp()` function creates a new `Client` object.

```py
# tests.py
class MovieViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.movie1 = Movie.objects.create(title="Movie 1", duration=120, rating=5)
        self.movie2 = Movie.objects.create(title="Movie 2", duration=100, rating=4)
```

Finally, we can use `client.get()` or `client.post()` to simulate some request and check the response we got back. Below are just some examples for values we can look for.

```py
# tests.py
class MovieViewTest(TestCase):
    def setUp(self):
        # ...

    def test_index_view(self):
        # Use the client to perform actions just like a user
        response = self.client.get(reverse('index'))

        # Check that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct templates were used
        self.assertTemplateUsed(response, 'movies/index.html')

        # Check that the context data contains the right movies
        movies_in_context = response.context['movies']
        self.assertEqual(list(movies_in_context), [self.movie1, self.movie2])

        # Check that the movie titles appear in the rendered HTML
        self.assertContains(response, str(self.movie1.title))
        self.assertContains(response, str(self.movie2.title))
```

## Browser Testing

Finally, for more complex tasks, it is also possible to simulate user actions in the browser itself. This includes, for instance, clicking a button, typing things into a search field, waiting for images to load and much more.

For simplicity sake, below is an example of a simple account HTML file.

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>CodePen - A Pen by DauphineWeb</title>
    <link rel="stylesheet" href="./style.css">

    <script>
        let countElement;
        let counter = 0;
        function changeCounter(amount) {
            counter += amount;
            countElement.innerText = counter;
        }
        document.addEventListener('DOMContentLoaded', function (event) {
            countElement = document.querySelector('#count');
            document.querySelector('#increment').onclick = () => changeCounter(1);
            document.querySelector('#decrement').onclick = () => changeCounter(-1);
        });
    </script>

    <style>
        * {
            text-align: center;
            font-size: 20pt;
            font-family: sans-serif;
            margin: 20px;
        }

        button {
            padding: 10px;
        }
    </style>
</head>

<body>
    <p>Current count: <span id="count">0</span><br>
        <button id="increment">Increment</button>
        <button id="decrement">Decrement</button>
    </p>

</body>

</html>
```

[Selenium](https://www.selenium.dev) now lets us open the page and perform user actions for us. This also requires a browser that allows for it to be controlled by some external software - here we will use Chrome and install the necessary [ChromeDriver](https://chromedriver.chromium.org) package.

```
pip install selenium
pip install chromedriver-py
```

Opening an html file requires the absolute path to the file, for which the `file_uri()` function has been introduced.

```py
import os
import pathlib
import unittest

from selenium import webdriver

# Finds the Uniform Resourse Identifier of a file
def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()

# Sets up web driver using Google chrome
driver = webdriver.Chrome()
```

`webdriver.Chrome()` opens the web browser. From here, we can use `driver.get()` to open up a webpage and start messing around with its content.

```py
driver.get(file_uri('counter.html'))
driver.title
# 'Counter'
driver.page_source
# <html lang="en"> ... </html>
# access elements and their content
driver.find_element_by_name('password')
driver.find_element_by_tag_name('h1').text

increment = driver.find_element_by_id('increment')
decrement = driver.find_element_by_id('decrement')
# interact with these elements
increment.click()
decrement.click()
for i in range(100):
    increment.click()
```

If there are some text fields, we can use `.send_keys()` to simulate keyboard input.

```py
username_field = driver.find_element_by_name("username")
password_field = driver.find_element_by_name("password")
submit_button = driver.find_element_by_name("submit")

username_field.send_keys("my_username")
password_field.send_keys("my_password")
submit_button.click()
```

In some cases we may need to wait for certain elements to load, i.e., in react until all the components are ready to be used.
Here, `WebDriverWait(..., 10).until(...)` signifies that Selenium should wait for a certain element to be loaded. If it doesn't appear after 10 seconds, it quits.

```py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Wait for up to 10 seconds for an element to be present
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "myElement"))
)
```

### Selenium in Django

Finally, here is a quick demonstration how Selenium could be used to test the functionality inside our movies project.

```py
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class MovieSearchTest(LiveServerTestCase):

    def setUp(self):
        Movie.objects.create(title="Inception", duration=120, rating=5)
        Movie.objects.create(title="Star Wars", duration=180, rating=3)
        self.browser = webdriver.Chrome()  # make sure the ChromeDriver is in your path

    def tearDown(self):
        self.browser.quit()

    def test_search_for_movie(self):
        # user goes to the home page
        self.browser.get(self.live_server_url)

        # user sees a search box
        search_box = self.browser.find_element_by_id('search_box')

        # user enters "Inception" into the search box
        search_box.send_keys('Inception')

        # user hits enter to submit the search
        search_box.send_keys(Keys.RETURN)

        # user sees "Inception" in the list of movies
        movies = self.browser.find_elements_by_class_name('movie')
        self.assertIn('Inception', [movie.text for movie in movies])
```

# CI/CD

Continuous Integration and Continuous Delivery describes a set of best-practices that a group of developers should follow when working as a team on a project.

CI is a software development practice where developers regularly merge their code changes into a central repository, typically multiple times a day. Once the code is merged, automated builds and tests are done to ensure some level of code quality. It should (hopefully) catch bugs as early as possible.

In the next stage, CD is an approach in which release cycles of a software are rather short. This ensures that any version of the software can be released reliably at any time. In the past, software companies typically released major version upgrades with a bunch of new features. This is slowly falling out of favor.

Here are some of the key benefits of using CI/CD:

* reducing compatibility issues when teams are working together,
* quickly isolate and find problems through automated testing with every merge,
* quickly publish a new release of the software when a bug has been found during production,
* incremental changes are not as jarring to the user,
* staying ahead of the competitive market.

## GitHub Actions

[GitHub Actions](https://github.com/features/actions) is a popular tool used for CI.
These actions are event-driven, they happen when some event occurs (i.e., a pushed commit, a merge to the main branch, pull requests, new comments, scheduled actions, etc.).

Some popular tasks or actions include:

* automated testing,
* CI/CD, run tests and deploy the app in a testing environment,
* code linting, notify the user on a pull request when their code is malformatted,
* issue management, if a user opens a new issue, the action could automatically assign tags based on its content,
* package publication when something is merged to the main branch,
* scheduled jobs, close issues where nothing happend over the last two months.

Each action is based on a [_workflow_](https://docs.github.com/en/actions/using-workflows). Each workflow is described in a [yaml](https://en.wikipedia.org/wiki/YAML) file in the `.github/workflows/` directory. A simple action might be this.

```yml
# .github/workflows/ci.yml
name: Test suite
on: [push, pull_request]

jobs:
  run_test_suite:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Run Django unit tests
      run: |
        pip3 install --user django
        python3 manage.py test
```

<details><summary>The yaml file explained in detail</summary>

```yml
# The name of your workflow, it will appear this way in the Actions tab.
name: Test suite

# The events that trigger the workflow execution. Here, it's on any push or pull request.
on: [push, pull_request]

# The collection of jobs to be run. Jobs run in parallel by default.
jobs:
  # The identifier of a job. This is the name you give to an execution unit.
  run_test_suite:
    # The type of machine to run the job on. Here, it's the latest version of Ubuntu.
    runs-on: ubuntu-latest

    # The sequence of tasks that make up a job. Steps are executed in the order they appear.
    steps:
      # This step uses a pre-configured action. The checkout action checks out your repository under $GITHUB_WORKSPACE.
      - uses: actions/checkout@v2
    
      # This is a name for the next step. It's optional but makes your workflow easier to understand.
      - name: Run Django unit tests

        # The run keyword executes commands in the runner's shell. It runs one line at a time, unless you use the pipe character (|) to run multiple lines.
        # Notice that there is no dash before `run:`. This means it belongs to the "Run Django unit tests" job.
        run: |
          pip3 install --user django
          python3 manage.py test
```

In yaml, dashes (`-`) denote a list of items. If a line does not start with a dash, it is interpreted as a key-value pair.

</details>

For many of the popular programming languages and software libraries, there is a good chance that you will find a template yaml file that can be used to run those tests.

## Docker

Working on different machines with different people can be at times difficult. The operating systems may vary, what tools have been installed may be different, and things like environment variables and system settings can influence how or even if a program runs.

Docker mitigates this by abstracting the operating system and instead offering a consistent workflow that describes, (a), what needs to be installed for a prorgam to run, and (b), how that program can be executed.

At the root level of our Django project, we may create a Dockerfile (called `Dockerfile`) with the following contents.

```Dockerfile
FROM python:3
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
```

<details><summary>Expand to read each line in detail</summary>

```Dockerfile
# Set the base image for your Docker container. Here, we're using the official Python 3 Docker image.
# https://hub.docker.com/_/python
FROM python:3

# Copy everything from the current directory on our local machine (denoted by the '.') to the '/app' directory inside the Docker container.
COPY . /app

# Set the working directory inside the Docker container.
# All subsequent Dockerfile commands (like RUN, CMD, etc.) will be run inside this directory.
WORKDIR /app

# Run pip install command inside the Docker container to install the Python dependencies listed in the requirements.txt file.
RUN pip install -r requirements.txt

# optinoal
# Make port 80 available to the world outside this container
EXPOSE 80

# Default command to run when when our image is launched.
# It starts the Django development server.
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
```

</details>

Here, we use `python:3` as our base image. For a list of all the other docker images that are available, [click here](https://hub.docker.com/search?q=&type=image&image_filter=official).

In the command line, we then can:

1. build the container (which runs the Dockerfile line by line, installing all the required software on the way),
2. run the container.

Once the container is run, it should be available over port 80 (depending on the port specified in the Dockerfile after `EXPOSE`).

```sh
# build docker image, give it a name
docker build -t my_script .

# run docker image
docker run my_script
# hit ctrl+c to stop the process

# run docker image in the background (-d <=> daemon process)
# it returns the id of the container
docker run -d my_script
# stop corresponding container (given the id)
docker stop <container>

# run docker image in the background, restart if it stops unexpectedly
docker run -d --restart on-failure my_script

# docker runs in the background, view its logs
docker logs -f my_script

# list actively running images
docker ps

# list all images
docker ps -a

# run command line inside the container
docker exec -i <container> /bin/bash
docker exec -i <container> bash -l

# list images
docker images

# remove container
docker rm

# remove image
docker rmi
```

# Deployment

## Prepare settings.py

1. Create new folder structure.

```
project/
  settings/
    __init__.py
    dev.py
    prod.py
```

2. Set env var

```sh
export DJANGO_SETTINGS_MODULE=my_project.settings.dev
python manage.py runserver
```

Through the Azure app service configurable.

3. manage.py

```py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings.dev')
```

4. Update wsgi.py and asgi.py

```py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings.prod')
```

## Deploy checklist

<https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/>

## Deploying on Azure

1. Install the CLI

<https://learn.microsoft.com/en-us/cli/azure/install-azure-cli>

2. Create resource group container. Location i.e. `westus2`

```
az group create --name <resource-group-name> --location <location>
```

3. Create app service plan

```
az appservice plan create --name <plan-name> --resource-group <resource-group-name> --sku B1 --is-linux
```

4. Create web app

```
az webapp create --resource-group <resource-group-name> --plan <plan-name> --name <app-name> --runtime "PYTHON|3.8" --deployment-local-git
```

5. Configure Django app

Before you deploy your app, you'll need to make a few changes to your Django settings:

* Set ALLOWED_HOSTS to include your Azure web app URL.
* Set DEBUG to False.
* Azure uses the WEBSITE_HOSTNAME environment variable to determine the server's hostname, so add this to your settings.py:

```py
if 'WEBSITE_HOSTNAME' in os.environ:
    import django_heroku
    django_heroku.settings(locals())
```

6. Deploy

```
git remote add azure <deployment-local-git-url-from-create-step>
git add .
git commit -m "Initial commit"
git push azure master
```

7. Set environ vars
