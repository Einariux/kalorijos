import PySimpleGUI as sg
import json

# Pradinių duomenų lentelė
data = []

# Lentelės stulpelių antraštės
header = ['Data', 'Atlikti pratimai', 'Pakartojimų skaičius', 'Irankio Svoris (kg)']

# Nustatykite pradinį lango dydį (priklauso nuo jūsų poreikių)
initial_window_size = (800, 400)

# Sukuriamas lango išdėstymas
layout = [
    [sg.Table(values=data, headings=header, auto_size_columns=True, justification='right',
              display_row_numbers=False, num_rows=min(35, len(data)), key='Table')],
    [sg.Button('Pridėti', size=(15, 1)), sg.Button('Redaguoti', size=(15, 1)),
     sg.Button('Ištrinti', size=(15, 1)), sg.Button('Saugoti į failą', size=(15, 1)),
     sg.Button('Atkurti iš failo', size=(15, 1)), sg.Button('Duomenų apdorojimas', size=(15, 1)),
     sg.Button('Išeiti', size=(15, 1))]
]

# Sukuriame langą su nurodytu dydžiu
window = sg.Window('Sportininko treniruočių duomenys', layout, size=initial_window_size)

# Funkcija, kuri atnaujina lentelę
def update_table():
    window['Table'].update(values=data)

# Programos vykdomoji dalis
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Išeiti':
        break
    elif event == 'Pridėti':
        # Įvedimo langas
        input_layout = [
            [sg.Text('Data:'), sg.InputText()],
            [sg.Text('Atlikti pratimai:'), sg.InputText()],
            [sg.Text('Pakartojimų skaičius:'), sg.InputText()],
            [sg.Text('Svoris (kg):'), sg.InputText()],
            [sg.Button('Pridėti'), sg.Button('Atšaukti')]
        ]

        input_window = sg.Window('Pridėti naują įrašą', input_layout)

        while True:
            event, values = input_window.read()

            if event == sg.WIN_CLOSED or event == 'Atšaukti':
                input_window.close()
                break
            elif event == 'Pridėti':
                data.append([values[0], values[1], values[2], values[3]])
                update_table()
                input_window.close()

    elif event == 'Redaguoti':
        selected_row = values['Table'][0]
        if selected_row:
            # Redagavimo langas
            edit_layout = [
                [sg.Text('Data:'), sg.InputText(data[selected_row][0])],
                [sg.Text('Atlikti pratimai:'), sg.InputText(data[selected_row][1])],
                [sg.Text('Pakartojimų skaičius:'), sg.InputText(data[selected_row][2])],
                [sg.Text('Svoris (kg):'), sg.InputText(data[selected_row][3])],
                [sg.Button('Išsaugoti'), sg.Button('Atšaukti')]
            ]

            edit_window = sg.Window('Redaguoti įrašą', edit_layout)

            while True:
                event, values = edit_window.read()

                if event == sg.WIN_CLOSED or event == 'Atšaukti':
                    edit_window.close()
                    break
                elif event == 'Išsaugoti':
                    data[selected_row] = [values[0], values[1], values[2], values[3]]
                    update_table()
                    edit_window.close()

    elif event == 'Ištrinti':
        selected_row = values['Table'][0]
        if selected_row:
            del data[selected_row]
            update_table()

    elif event == 'Saugoti į failą':
        with open('treniruotes.json', 'w') as file:
            json.dump(data, file)

    elif event == 'Atkurti iš failo':
        try:
            with open('treniruotes.json', 'r') as file:
                data = json.load(file)
                update_table()
        except FileNotFoundError:
            sg.popup_error('Failas nerastas.')

    elif event == 'Duomenų apdorojimas':
        # Čia galite pridėti savo duomenų apdorojimo kodą
        pass

window.close()
