import env_utils


class UsersConfigVless:
    def __init__(self):
        self.path_config = env_utils.get_envvar()['PATH_CONFIG_JSON']


    def gen_uuid(self):
        '''генерация uuid для нового пользователя'''
        import uuid as u
        return str(u.uuid4())


    def gen_new_user(self, email):
        '''генерация нового пользователя в конфиг'''
        return {'id': self.gen_uuid(), 'flow': 'xtls-rprx-vision', 'level': 0, 'email': email}


    def get_config(self):
        '''достает json конфиг из файла'''
        import json
        with open(self.path_config, "r", encoding="utf-8") as file:
            return json.load(file)  # json конфига


    def add_new_user_to_config(self, new_user, config):
        '''добавление нового пользователя в конфиг'''
        config["inbounds"][0]["settings"]["clients"].append(new_user)


    def write_new_config(self, config):
        '''запись конфига с новым пользователем в файл config.json'''
        import json
        with open(self.path_config, "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)


    def create_new_user(self, email):
        '''метод для добавления новго пользователя в конфиг'''
        config = self.get_config()

        self.add_new_user_to_config(
            new_user=self.gen_new_user(email=email),
            config=config
        )

        self.write_new_config(config=config)

    
    def encoder_to_base64(self, string):
        '''кодирует строку в base64'''
        import base64

        string += "\n"
        return base64.b64encode(string.encode("utf-8")).decode()





if __name__ == "+__main__":
    email = str(input("Email: "))
    s = UsersConfigVless()
    s.create_new_user(email=email)


