def get_envvar():
    '''извлечение переменных из .env'''
    envvars = {}
    with open(".env", "r", encoding="utf-8") as file:
        for line in file:
            line = line.replace("\n", "")

            if not line or line.startswith("#"):
                continue

            else:
                line = line.split("=")
                envvars[line[0]] = line[1]
    return envvars

