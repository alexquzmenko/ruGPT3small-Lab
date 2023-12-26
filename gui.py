import PySimpleGUI as sg
from test_task import *

layout = [
    [sg.Text('Ваш запрос: '), sg.InputText(key='input')],
    [sg.Output(size=(125, 30), key='-OUTPUT-')],
    [sg.Submit('Сгенерировать'), sg.Cancel()]
]

window = sg.Window('ru_gpt', layout)

while True:  # The Event Loop
    event, values = window.read()
    if event in (None, 'Выход', 'Отмена'):
        break
    if event == 'Сгенерировать':
        window['-OUTPUT-'].update('')
        try:
            response = generate_response(values['input'])
            print(response)
        except Exception as e:
            print(f"Произошла ошибка: {e}")

