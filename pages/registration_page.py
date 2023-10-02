import allure
import os
from dataclasses import dataclass

from selene import browser, have, command

from data.users import User

FILE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../tests/image'))


@dataclass()
class RegistrationPage(User):
    def __init__(self):
        self.firstName = browser.element('#firstName')
        self.lastName = browser.element('#lastName')
        self.userEmail = browser.element('#userEmail')
        self.userGender = browser.all('[name=gender]')
        self.phoneNumber = browser.element('#userNumber')
        self.currentAddress = browser.element('#currentAddress')
        self.userSubjects = browser.element('#subjectsInput')
        self.userState = browser.element('#state')
        self.userCity = browser.element('#city')
        self.userPicture = browser.element('#uploadPicture')
        self.submitForm = browser.element('#submit')
        self.resultTable = browser.all('.modal-content td')

    @staticmethod
    @allure.step("Открываем страницу для заполнения формы")
    def open():
        browser.open('https://demoqa.com/automation-practice-form')
        browser.execute_script('document.querySelector("#fixedban").remove()')
        browser.element('footer').execute_script('element.remove()')

    #@allure.step('Заполняем форму для регистрации')
    def register(self, user):
        self.firstName.type(user.first_name)
        self.lastName.type(user.last_name)
        self.userEmail.type(user.email)
        self.userGender.element_by(have.value(f'{user.gender}')).element('..').click()
        self.phoneNumber.type(f'{user.phone}')
        self.fill_birthday(user.birth_date['day'], user.birth_date['month'], user.birth_date['year'])
        browser.element(f'//label[contains(text(), "{user.hobbies}")]').click()

        for _ in user.subjects:
            self.userSubjects.type(_).press_enter()

        self.userPicture.send_keys(os.path.join(FILE_DIR, f'{user.picture}'))
        self.currentAddress.type(f'{user.current_address}')
        browser.element('#stateCity-wrapper') \
            .perform(command.js.scroll_into_view)
        self.userState.click()
        browser.element(f'//*[.="{user.state}"]').click()
        self.userCity.click()
        browser.element(f'//*[.="{user.city}"]').click()
        self.userState.click()
        self.submitForm.click().press_enter()

    @staticmethod
    def fill_birthday(day, month, year):
        browser.element('#dateOfBirthInput').click()
        browser.element('.react-datepicker__month-select').type(month)
        browser.element('.react-datepicker__year-select').type(year)
        browser.element(
            f'.react-datepicker__day--0{day}:not(.react-datepicker__day--outside-month)'
        ).click()

    @staticmethod
    @allure.step("Проверяем данные пользователя")
    def should_have_registered(user):
        browser.all('.modal-content td').should(have.exact_texts(
            ('Student Name', f'{user.first_name} {user.last_name}'),
            ('Student Email', user.email),
            ('Gender', user.gender),
            ('Mobile', user.phone),
            ('Date of Birth', f'{user.birth_date["day"]} {user.birth_date["month"]},{user.birth_date["year"]}'),
            ('Subjects', ', '.join(user.subjects)),
            ('Hobbies', user.hobbies),
            ('Picture', user.picture),
            ('Address', user.current_address),
            ('State and City', f'{user.state} {user.city}')))

    @staticmethod
    @allure.step("закрываем форму")
    def close_submit_form():
        browser.element('#closeLargeModal') \
            .perform(command.js.scroll_into_view).click()
        browser.element('#example-modal-sizes-title-lg') \
            .should(have.no.text('Thanks for submitting the form'))
