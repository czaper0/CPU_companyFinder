import tkinter, tkinter.messagebox, customtkinter, requests, json
from datetime import datetime
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # window
        self.title("Company finder")
        self.geometry(f"{900}x{1200}")

        # grid 
        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=3, weight=1)
        
        # entries
        current_row = 0
        current_column = 0
        self.label = customtkinter.CTkLabel(self, text="Imię:", anchor="w")
        self.label.grid(row=current_row, column=current_column, padx=20, pady=(10, 0))
        self.entry_name = customtkinter.CTkEntry(self, placeholder_text="Podaj imię")
        self.entry_name.grid(row=current_row, column=current_column+1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        # current_row += 1
        current_column = (current_column + 2) % 4
        self.label = customtkinter.CTkLabel(self, text="Nazwisko:", anchor="w")
        self.label.grid(row=current_row, column=current_column, padx=20, pady=(10, 0))
        self.entry_surname = customtkinter.CTkEntry(self, placeholder_text="Podaj nazwisko")
        self.entry_surname.grid(row=current_row, column=current_column+1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        current_row += 1
        self.switch = customtkinter.CTkSwitch(master=self, text='Kryteria pomocnicze', command=self.toggle_switch)
        self.switch.grid(row=current_row, column=1, columnspan=3, padx=20, pady=(10, 0), sticky="nsew")


        current_row += 1
        self.additional_fields = customtkinter.CTkFrame(self)
        self.additional_fields.grid(row=current_row, column=0, columnspan=4, padx=0, pady=(0, 0), sticky="nsew")
        self.additional_fields.grid_columnconfigure(index=1, weight=1)
        self.additional_fields.grid_columnconfigure(index=3, weight=1)
        current_row += 1
        current_column = (current_column + 2) % 4
        self.label_1 = customtkinter.CTkLabel(self.additional_fields, text="Nazwa:", anchor="w")
        self.label_1.grid(row=current_row, column=current_column, padx=20, pady=(10, 0))
        self.entry_company_name = customtkinter.CTkEntry(self.additional_fields, placeholder_text="Podaj Nazwę firmy")
        self.entry_company_name.grid(row=current_row, column=current_column+1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        current_column = (current_column + 2) % 4
        self.label_2 = customtkinter.CTkLabel(self.additional_fields, text="Miasto:", anchor="w")
        self.label_2.grid(row=current_row, column=current_column, padx=20, pady=(10, 0))
        self.entry_town = customtkinter.CTkEntry(self.additional_fields, placeholder_text="Podaj miasto")
        self.entry_town.grid(row=current_row, column=current_column+1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        current_row += 1
        current_column = (current_column + 2) % 4
        self.label_3 = customtkinter.CTkLabel(self.additional_fields, text="NIP:", anchor="w")
        self.label_3.grid(row=current_row, column=current_column, padx=20, pady=(10, 0))
        self.entry_nip = customtkinter.CTkEntry(self.additional_fields, placeholder_text="Podaj numer NIP")
        self.entry_nip.grid(row=current_row, column=current_column+1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        current_column = (current_column + 2) % 4
        self.label_4 = customtkinter.CTkLabel(self.additional_fields, text="REGON:", anchor="w")
        self.label_4.grid(row=current_row, column=current_column, padx=20, pady=(10, 0))
        self.entry_regon = customtkinter.CTkEntry(self.additional_fields, placeholder_text="Podaj numer REGON")
        self.entry_regon.grid(row=current_row, column=current_column+1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        current_row += 1
        current_column = (current_column + 2) % 4
        self.label_3 = customtkinter.CTkLabel(self.additional_fields, text="NIP SC:", anchor="w")
        self.label_3.grid(row=current_row, column=current_column, padx=20, pady=(10, 0))
        self.entry_nip_sc = customtkinter.CTkEntry(self.additional_fields, placeholder_text="Podaj numer NIP spółki cywilnej")
        self.entry_nip_sc.grid(row=current_row, column=current_column+1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        current_column = (current_column + 2) % 4
        self.label_4 = customtkinter.CTkLabel(self.additional_fields, text="REGON SC:", anchor="w")
        self.label_4.grid(row=current_row, column=current_column, padx=20, pady=(10, 0))
        self.entry_regon_sc = customtkinter.CTkEntry(self.additional_fields, placeholder_text="Podaj numer REGON spółki cywilnej")
        self.entry_regon_sc.grid(row=current_row, column=current_column+1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # buttons
        current_row += 1
        self.label = customtkinter.CTkLabel(self, text="Baza danych:", anchor="w")
        self.label.grid(row=current_row, column=0, padx=20, pady=(10, 0))
        self.option_menu = customtkinter.CTkOptionMenu(self, values=["CEiDG", "KRS", "VAT"])
        self.option_menu.grid(row=current_row, column=1, columnspan=2,padx=20, pady=(10, 10), sticky="w")
        self.find_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),text='Znajdź', command=self.find_button_event)
        self.find_button.grid(row=current_row, column=2,columnspan=2, padx=(20, 20), pady=(20, 20), sticky="e")

        # textbox
        current_row += 1
        self.grid_rowconfigure(current_row, weight=1)
        self.label = customtkinter.CTkLabel(self, text="Firmy:", anchor="w")
        self.label.grid(row=current_row, column=0, padx=20, pady=(10, 0))
        self.output_textbox = customtkinter.CTkTextbox(self, width=250,state='disabled')
        self.output_textbox.grid(row=current_row, column=1,columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        # log
        current_row += 1
        self.grid_rowconfigure(current_row, weight=0)
        self.label = customtkinter.CTkLabel(self, text="Logi:", anchor="w")
        self.label.grid(row=current_row, column=0, padx=20, pady=(10, 0))
        self.log_textbox = customtkinter.CTkTextbox(self, width=250,state='disabled')
        self.log_textbox.grid(row=current_row, column=1,columnspan=3,padx=(20, 20), pady=(20, 20), sticky="sew")

        self.toggle_switch()

    #functions
    def find_button_event(self):
        name = self.entry_name.get()
        surname = self.entry_surname.get()
        town = self.entry_town.get()
        database = self.option_menu.get()
        nip = self.entry_nip.get()
        regon = self.entry_regon.get()
        nip_sc = self.entry_nip_sc.get()
        regon_sc = self.entry_regon_sc.get()
        company_name = self.entry_company_name.get()

        self.log(f"Wciśnięto przycisk 'Znajdź'")
        self.log(f"Wczytano: {name} {surname} {company_name} {town} {database} {nip} {regon} {nip_sc} {regon_sc}")
        if database == "CEiDG":
            result = self.find_CEiDG(name=name, surname=surname, town=town, nip=nip, regon=regon, company_name=company_name,nip_sc=nip_sc,regon_sc=regon_sc)
        elif database == "VAT":
            result = self.find_VAT(name=name, surname=surname, town=town, nip=nip, regon=regon, company_name=company_name)
        elif database == "KRS":
            result = self.find_KRS(name=name, surname=surname, town=town, nip=nip, regon=regon, company_name=company_name)
        self.log(f"Zakończono wyszukiwanie")

        self.output_textbox.configure(state='normal')
        self.output_textbox.delete("1.0", tkinter.END)
        self.output_textbox.insert(tkinter.INSERT, f"{result}")
        self.output_textbox.configure(state='disabled')

    def find_CEiDG(self, name='', surname='', town='', nip='', regon='', company_name='',nip_sc='',regon_sc=''):
        self.log(f"Wyszukiwanie w bazie CEiDG")
        url = "https://dane.biznes.gov.pl/api/ceidg/v1/"
        sufix = "firmy"
        params = {}
        if name: params['imie'] = name
        if surname: params['nazwisko'] = surname
        if town: params['miasto'] = town
        if nip: params['nip'] = nip
        if regon: params['regon'] = regon
        if company_name: params['nazwa'] = company_name
        if nip_sc: params['nip_sc'] = nip_sc
        if regon_sc: params['regon_sc'] = regon_sc
        
        headers = {
        'Authorization': 'Bearer eyJraWQiOiJjZWlkZyIsImFsZyI6IkhTNTEyIn0.eyJnaXZlbl9uYW1lIjoiUGlvdHIiLCJwZXNlbCI6Ijk3MDEyMzEyMzk1IiwiaWF0IjoxNjcwNDQ2MDA4LCJmYW1pbHlfbmFtZSI6IlNhZHVyYSIsImNsaWVudF9pZCI6IlVTRVItOTcwMTIzMTIzOTUtUElPVFItU0FEVVJBIn0.bm1Hb7IoamZtXtci7yqlc4bDKZEObyKc3GOtymJLUgrk590MZvwY-zDmOUZGVgFmGkoZTERTUjRU2Wwof52_ew',
        'Cookie': 'cookiesession1=678B2877890123ABCDEFGHIOPQRS8515'
        }
        response = requests.request("GET",url+sufix,headers=headers,params=params) 
        if response.status_code != 200:
            self.log(f"Nie udało się pobrać danych z bazy CEiDG")
            return "Nie udało się pobrać danych z bazy CEiDG"

        result = []
        for company in response.json()['firmy']:
            link = company['link']
            response = requests.request("GET",link,headers=headers)
            result.append(self.parse_CEiDG_company(response.json()))
        result = '_________________________________________________________________________________________________________________________\n\n'.join(result)
        return result

    def parse_CEiDG_company(self, data):
        data = data['firma'][0]
        text = ''
        if 'nazwa' in data.keys(): text += f"Nazwa:\t\t\t{data['nazwa']}\n"
        if 'status' in data.keys(): text += f"Status:\t\t\t{data['status']}\n"
        if 'wlasciciel' in data.keys(): text += self.parse_CEiDG_owner(data['wlasciciel'])
        if 'adresDzialalnosci' in data.keys(): text += 'Adres działalności:\t\t\t'+self.parse_CEiDG_address(data['adresDzialalnosci'])
        if 'adresKorespondencyjny' in data.keys(): text += 'Adres korespondencyjny:\t\t\t'+self.parse_CEiDG_address(data['adresKorespondencyjny'])
        if 'pkd' in data.keys() and data['pkd']: text += f"PKD:\t\t\t{', '.join(data['pkd'])}\n"
        if 'spolki' in data.keys() and data['spolki']: text += self.parse_CEiDG_spolki(data['spolki'])
        return text

    def parse_CEiDG_owner(self, data):
        text = 'Właściciel:\t\t\t'
        if 'imie' in data.keys(): text += f"{data['imie']}"
        if 'nazwisko' in data.keys(): text += f" {data['nazwisko']}"
        if 'nip' in data.keys(): text += f", NIP: {data['nip']}"
        if 'regon' in data.keys(): text += f", REGON: {data['regon']}"
        return text+'\n'

    def parse_CEiDG_address(self, data):
        text = ''
        if 'ulica' in data.keys(): text += f"{data['ulica']}"
        if 'budynek' in data.keys(): text += f" {data['budynek']}"
        if 'kod' in data.keys(): text += f", {data['kod']}" 
        if 'miasto' in data.keys(): text += f" {data['miasto']}"
        return text+'\n'
    
    def parse_CEiDG_spolki(self, data):
        text = 'Spółki:\n'
        for index,spolka in enumerate(data):
            text += f"\t{index+1}. "
            if 'nazwa' in spolka.keys(): text += f"\t{spolka['nazwa']}"
            else: text += f"Nazwa nieznana"
            if 'nip' in spolka.keys(): text += f", NIP: {spolka['nip']}"
            if 'regon' in spolka.keys(): text += f", REGON: {spolka['regon']}"
            text += '\n'
        return text

    def find_VAT(self, name='', surname='', town='', nip='', regon='', company_name=''):
        if not nip and not regon: return "Nie podano numeru NIP ani REGON, które są wymagane do wyszukania w bazie VAT."
        self.log(f"Wyszukiwanie w bazie VAT")
        url = "https://wl-api.mf.gov.pl/api/search/"
        query = {'date': datetime.now().strftime("%Y-%m-%d")}
        if nip: url = url + "nip/" + nip
        elif regon: url = url + "regon/" + regon
        response = requests.get(url, params=query)
        result = self.parse_VAT(response.json())
        return result

    def parse_VAT(self, data):
        if 'code' in data.keys(): return data['message']
        text = ''
        data = data['result']['subject']
        if 'name' in data.keys() and data['name']: text += f"Nazwa:\t\t\t{data['name']}\n"
        if 'statusVat' in data.keys() and data['statusVat']: text += f"Status:\t\t\t{data['statusVat']}\n"
        if 'nip' in data.keys() and data['nip']: text += f"NIP:\t\t\t{data['nip']}\n"
        if 'regon' in data.keys() and data['regon']: text += f"REGON:\t\t\t{data['regon']}\n"
        if 'krs' in data.keys() and data['krs']: text += f"KRS:\t\t\t{data['krs']}\n"
        if 'workingAddress' in data.keys() and data['workingAddress']: text += f"Adres:\t\t\t{data['workingAddress']}\n"
        return text

    def find_KRS(self, name='', surname='', town='', nip='', regon='', company_name=''):
        self.log(f"Wyszukiwanie w bazie KRS")
        return "Baza danych KRS obecnie nie jest dostępna."

    def toggle_switch(self):
        if self.switch.get():
            self.additional_fields.grid(row=2, column=0, columnspan=4, padx=20, pady=(10, 0), sticky="nsew")
        else:
            self.additional_fields.grid_forget()

    def log(self,text):
        self.log_textbox.configure(state='normal')
        self.log_textbox.insert(tkinter.END,"["+str(datetime.now())+"] "+text+"\n")
        self.log_textbox.configure(state='disabled')


if __name__ == "__main__":
    app = App()
    app.mainloop()
