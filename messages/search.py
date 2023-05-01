from operator import itemgetter

def binary_search(users_list, user_id):
    low = 0
    high = len(users_list)-1

    while low <= high:
        mid = (low + high)
        guess = int(users_list[mid]["id"])
        if guess == user_id:
            return mid
        if guess > user_id:
            high = mid - 1
        else:
            low = mid + 1
    return None


def get_users_data():
    users_list = []
    try:
        with open('users.txt', 'r', encoding='utf-8') as users_file:
            line = users_file.readline(50)
            while line:
                lin = line.rstrip('\n')
                users_data = lin.split(':')
                users_list.append({"id": int(users_data[0]), "full_name": users_data[1], "user_name": users_data[2]})
                line = users_file.readline(50)
    except FileNotFoundError:
        return ''

    return users_list

def add_user_data(message, users_list):
    users_data = sorted(users_list, key=itemgetter("id"))
    result = binary_search(users_data, message.from_user.id)
    

    if result == None:
        with open('users.txt', 'a', encoding='utf-8') as users_file:
            users_file.write(f"{message.from_user.id}:{message.from_user.first_name}:{message.from_user.username}" + '\n')