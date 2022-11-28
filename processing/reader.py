def read_history(username, chat_id):
    categories = {}
    try:
        with open(f'userdata/{username}{chat_id}.txt', 'r',
                  encoding='utf-8') as file:
            for line in file.readlines():
                categories[line.strip('\n').split(' - ')[0]] = int(line.strip('\n').split(' - ')[1])
        return categories
    except IOError:
        with open(f'userdata/{username}{chat_id}.txt', 'w',
                  encoding='utf-8'):
            return categories
