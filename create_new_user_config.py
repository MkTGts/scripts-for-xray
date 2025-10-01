import env_utils


class UsersConfigVless:
    v = "0.0.2"

    def __init__(self):
        self._config = env_utils.get_envvar()
        self.uuid = ""


    def gen_uuid(self):
        '''генерация uuid для нового пользователя'''
        import uuid as u
        return str(u.uuid4())


    def gen_new_user(self, email, uuid):
        '''генерация нового пользователя для json'''
        return {'id': uuid, 'flow': 'xtls-rprx-vision', 'level': 0, 'email': email}


    def get_config(self):
        '''достает json конфиг из файла'''
        import json
        with open(self._config['PATH_CONFIG_JSON'], "r", encoding="utf-8") as file:
            return json.load(file)  # json конфига
        


    def add_new_user_to_config(self, new_user, config):
        '''добавление нового пользователя в конфиг '''
        config["inbounds"][0]["settings"]["clients"].append(new_user)
        return config


    def write_new_config(self, config):
        '''запись конфига с новым пользователем в файл config.json'''
        import json
        with open(self._config['PATH_CONFIG_JSON'], "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)


    def create_new_user_to_config_json(self, email):
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
    

    def gen_vless_uri(self,
                      uuid: str,
                      site: str,
                      name: str,
                      port: str
                      ):
        '''генерация ссылки vless'''
        pattern_uri: str = self._config["USER_CONFIG_PATTERN"]
        pattern_uri = pattern_uri.replace("uuid", uuid)
        pattern_uri = pattern_uri.replace("site", site)
        pattern_uri = pattern_uri.replace("Name", name)
        pattern_uri= pattern_uri.replace("port", port)
        
        return self.encoder_to_base64(string=pattern_uri)
    

    def create_user_config_file(self, name, filename, port):
        '''создает файл конфига который будет устанавливать пользователь'''
        with open(self._config["PATH_USER_CONFIG"]+filename, "w", encoding="utf-8") as file:
            file.write(self.gen_vless_uri(
                uuid=self.uuid,
                site=self._config["SITE"],
                name=name,
                port=port
            ))

    
    def add_new_user(self):
        try:
            email = input("Email: ")
            uuid = self.gen_uuid()  # генерируется uuid для новго пользователя
            new_user = self.gen_new_user(email=email, uuid=uuid)  # словарь с новым пользователем для конфига json
            full_json_config = self.get_config()  # получение полнонго конфина из файла конфига
            new_full_json_config = self.add_new_user_to_config(new_user=new_user, config=full_json_config)  # новый конфиг с добавленным пользователем
            self.write_new_config(config=new_full_json_config)  # перезапись нового кофига в файл json конфиг

            self.create_user_config_file(name=email, filename=email, port="443")
            print(f"Ссылка на когфиш для пользователя {self._config["SITE_USER_CONFIGS_URL"]}/{email}")
        except Exception as err:
            print(f"Возникла ошибка {err}")





if __name__ == "__main__":
    s = UsersConfigVless()
    s.add_new_user()


