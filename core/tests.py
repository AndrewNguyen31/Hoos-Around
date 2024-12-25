from django.test import TestCase
from django.urls import reverse
from .models import User
from .models import Place
from .models import Task
from .models import Picture

# Create your tests here.
def create_test_user(username, first_name,last_name):
    return User.objects.create_user(username=username, first_name=first_name, last_name=last_name)

def create_test_place(name, description):
    place = Place(name = name, description = description)
    return place

def create_test_task():
    task = Task()
    return task

def create_test_picture():
    pic = Picture()
    return pic
class DisplayAccountTests(TestCase):
    def test_user(self):
        user = create_test_user('zohaibk04', 'Zohaib', 'Khalid')
        self.user = user
        self.assertEquals(user.role, "base")
        user.role = "super"
        self.assertEquals(user.role, "super")

    def test_place(self):
        place = create_test_place('Ummas', 'Restaurant Korean Food')
        self.assertTrue(place)
        #tests if values are correct
        label =  place._meta.get_field('name').verbose_name
        self.assertEqual(label, 'name')
        label2 = place._meta.get_field('description').verbose_name
        self.assertEqual(label2, 'description')
        #test if max length is correct
        max_length = place._meta.get_field('name').max_length
        self.assertEquals(max_length,500)
    def test_task(self):
        task = create_test_task()
        self.assertFalse(task.completed)
        task.completed = True
        self.assertTrue(task.completed)



    def test_pic(self):
        pic = create_test_picture()





