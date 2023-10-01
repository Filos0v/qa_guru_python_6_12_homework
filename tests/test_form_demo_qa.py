from pages.registration_page import RegistrationPage, User


def test_filling_form():
    demo_user = User(first_name='Aleksandr',
                     last_name='Shevchenko',
                     email='a.shevchenko666@mail.com',
                     gender='Male',
                     phone='8005553535',
                     hobbies='Music',
                     subjects=['Computer Science'],
                     current_address='SPB Russia',
                     picture='image_1.jpg',
                     birth_date={'day': '24', 'month': 'December', 'year': '1995'},
                     state='Haryana',
                     city='Karnal'
                     )

    registration_page = RegistrationPage()

    registration_page.open()
    registration_page.register(demo_user)
    registration_page.should_have_registered(demo_user)
    registration_page.close_submit_form()
