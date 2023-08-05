# Full PybaseKit Code
import os, random, json

class Encryption:
    '''
        This is a very simple encryption method not meant to be use outside home project.
        If used outside home/personal projects use a diffrent method or you will be at risk
    '''
    @staticmethod
    def encrypt(text):
        encrypted_text = ""
        for c in text:
            block = str(ord(c) * 7719)
            block = "0" * (3 - len(block)) + block
            encrypted_text += block + "."
        return encrypted_text[:-1]

    @staticmethod
    def decrypt(text):
        decrypted_text = ""
        blocks = text.split(".")
        for block in blocks:
            if block:
                value = int(block) // 7719
                decrypted_text += chr(value)
        return decrypted_text


class Start:
    '''
      Start class to start the services and hold all the other classes and functions, sets the main folder to hold all database information.
    '''
    Folder = "pybase_db"

    def __init__(self, folder_name=None):
        if folder_name is not None:
            self.__class__.Folder = folder_name
        if not os.path.exists(self.Folder):
            os.makedirs(self.Folder)

    class CreateDB:
        '''
          User sets a key and class creates a new .pybase file with simple encrypted key and database base information returns 200 OK if runned correctly
        '''
        def __init__(self, name, key):
            self.name = name

        def __new__(self, name, key):
            self.__key = key
            if os.path.exists(f"{Start.Folder}/{name}.pybase") == False:
                start = open(f"{Start.Folder}/{name}.pybase", "a+")
                build = Encryption.encrypt(
                    '{  "DatabaseData": {    "SectionTitles": {}  },  "Data": {}}'
                )
                start.write(f"{Encryption.encrypt(self.__key)}\n{build}")
                return "200 OK"
            else:
                return "404"

    class ConnectDB:
        '''
          Connects to a .pybase file if access key is correct if not will return 401 if connects returns 200 OK
        '''
        def __init__(self, db_name, access_key):
            self.name = db_name
            self.key = access_key

        def VerifyAUTH(self):
            '''
              Verifys thast the user is connected to the .pybase file if authed returns true else returns false. User should not usally use this function its just for the other functions to work correctly
            '''
            if os.path.exists(f"{Start.Folder}/{self.name}.pybase") == True:
                data = open(f"{Start.Folder}/{self.name}.pybase", "r+")
                if str(self.key) == str(
                    Encryption.decrypt(data.readline().strip("\n"))
                ):
                    return True
                else:
                    return False
            else:
                return "404"

        def __str__(self):
          # If Authed, connects
            AUTH = self.VerifyAUTH()
            if AUTH == "404":
                return "Failed to connect: 404"
            else:
                if AUTH == True:
                    return "200 OK"
                else:
                    return "Failed to connect: 401"

        def create_section(self, section_title):
            '''
              Checked if authed is so creates a new section for the database if section is not already created.
            '''
            auth = self.VerifyAUTH()
            if auth == True:
                lines = []
                with open(f"{Start.Folder}/{self.name}.pybase") as Data:
                    lines = Data.readlines()[1:]
                    data = Encryption.decrypt(lines[0])
                    data = data.replace("'", '"')
                    undata = json.loads(data)
                    if section_title in undata["DatabaseData"]["SectionTitles"]:
                        return "Section is already created"
                    else:
                        newValue = {
                            "DatabaseData": {
                                "SectionTitles": {section_title: section_title}
                            }
                        }
                        newValue2 = {"Data": {section_title: {}}}
                        undata.update(newValue)
                        undata.update(newValue2)
                        t = open(f"{Start.Folder}/{self.name}.pybase", "w")
                        undata = Encryption.encrypt(str(undata))
                        tt = Encryption.encrypt(self.key)
                        t.write(tt + "\n" + undata)
                        return section_title
            else:
                return "401"

        def insert_data(self, section, Data_Title, Data_Value):
            '''
              If authed will insert data if data title is not already in section if the section is valid
            '''
            AUTH = self.VerifyAUTH()
            if AUTH == True:
                lines = []
                with open(f"{Start.Folder}/{self.name}.pybase") as Data:
                    lines = Data.readlines()[1:]
                    data = Encryption.decrypt(lines[0])
                    data = data.replace("'", '"')
                    undata = json.loads(data)
                    if section in undata["DatabaseData"]["SectionTitles"]:
                        if str(Data_Title) not in undata["Data"][str(section)]:
                            new = {"Data": {section: {Data_Title: Data_Value}}}
                            undata.update(new)
                            t = open(f"{Start.Folder}/{self.name}.pybase", "w")
                            t.write(
                                f"{Encryption.encrypt(self.key)}\n{Encryption.encrypt(str(undata))}"
                            )
                        else:
                            return "Data Title is already in section"
                    else:
                        return "Could not find section: 404"
                return "200 OK"
            else:
                return "401"
            
        def insert_list(self, section, Data_Title, List):
            AUTH = self.VerifyAUTH()
            if AUTH:
                if type(List) == list:
                    lines = []
                    with open(f"{Start.Folder}/{self.name}.pybase") as Data:
                        lines = Data.readlines()[1:]
                        data = Encryption.decrypt(lines[0])
                        data = data.replace("'", '"')
                        undata = json.loads(data)
                        if section in undata["DatabaseData"]["SectionTitles"]:
                            if str(Data_Title) not in undata["Data"][str(section)]:
                                new = {"Data": {section: {Data_Title: List}}}
                                undata.update(new)
                                t = open(f"{Start.Folder}/{self.name}.pybase", "w")
                                t.write(
                                    f"{Encryption.encrypt(self.key)}\n{Encryption.encrypt(str(undata))}"
                                )
                            else:
                                return "Data Title is already in section"
                        else:
                            return "Could not find section: 404"
                    return "200 OK"
                else:
                    return f"List is not in correct format. Your type is currently at {type(List)}"
            else:
                return "Error 401"
            
        def get_data(self, section, Data_Title):
            AUTH = self.VerifyAUTH()
            if AUTH == True:
                lines = []
                with open(f"{Start.Folder}/{self.name}.pybase") as Data:
                    lines = Data.readlines()[1:]
                    data = Encryption.decrypt(lines[0])
                    data = data.replace("'", '"')
                    undata = json.loads(data)
                    if section in undata["DatabaseData"]["SectionTitles"]:
                        if str(Data_Title) in undata["Data"][str(section)]:
                            return undata["Data"][str(section)][str(Data_Title)]
                        else:
                            return "Could not find data: 404"
                    else:
                        return "Could not find section: 404"
            else:
                return "401"

        def remove_data(self, section, Data_Title):
            AUTH = self.VerifyAUTH()
            if AUTH == True:
                lines = []
                with open(f"{Start.Folder}/{self.name}.pybase") as Data:
                    lines = Data.readlines()[1:]
                    data = Encryption.decrypt(lines[0])
                    data = data.replace("'", '"')
                    undata = json.loads(data)
                    if section in undata["DatabaseData"]["SectionTitles"]:
                        if str(Data_Title) in undata["Data"][str(section)]:
                            del undata["Data"][str(section)][str(Data_Title)]
                            t = open(f"{Start.Folder}/{self.name}.pybase", "w")
                            t.write(
                                f"{Encryption.encrypt(self.key)}\n{Encryption.encrypt(str(undata))}"
                            )
                            return "200 OK"
                        else:
                            return "Could not find data: 404"
                    else:
                        return "Could not find section: 404"
            else:
                return "401"
        
        def update_data_value(self, section, Data_Title, New_Value):
            AUTH = self.VerifyAUTH()
            if AUTH == True:
                lines = []
                with open(f"{Start.Folder}/{self.name}.pybase") as Data:
                    lines = Data.readlines()[1:]
                    data = Encryption.decrypt(lines[0])
                    data = data.replace("'", '"')
                    undata = json.loads(data)
                    if section in undata["DatabaseData"]["SectionTitles"]:
                        if str(Data_Title) in undata["Data"][str(section)]:
                            undata["Data"][str(section)][str(Data_Title)] = New_Value
                            t = open(f"{Start.Folder}/{self.name}.pybase", "w")
                            t.write(
                                f"{Encryption.encrypt(self.key)}\n{Encryption.encrypt(str(undata))}"
                            )
                            return undata["Data"][str(section)][str(Data_Title)]
                        else:
                            return "Could not find data: 404"
                    else:
                        return "Could not find section: 404"
            else:
                return "401"
            
        def get_all_data(self):
            AUTH = self.VerifyAUTH()
            if AUTH == True:
                lines = []
                with open(f"{Start.Folder}/{self.name}.pybase") as Data:
                    lines = Data.readlines()[1:]
                    data = Encryption.decrypt(lines[0])
                    data = data.replace("'", '"')
                    undata = json.loads(data)
                    return undata["Data"]
            else:
                return "401"

        def get_section_data(self, section):
            AUTH = self.VerifyAUTH()
            if AUTH == True:
                lines = []
                with open(f"{Start.Folder}/{self.name}.pybase") as Data:
                    lines = Data.readlines()[1:]
                    data = Encryption.decrypt(lines[0])
                    data = data.replace("'", '"')
                    undata = json.loads(data)
                    if section in undata["DatabaseData"]["SectionTitles"]:
                        return undata["Data"][str(section)]
                    else:
                        return "Could not find section: 404"
            else:
                return "401"