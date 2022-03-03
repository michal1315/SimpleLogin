import random
import time
import data
import messages
import os
import sys
import hashlib

try:
    file_operation = open(data.db_file, mode="r+", encoding="utf-8")
    lines_read = file_operation.readlines()
except FileNotFoundError:
    if os.name == "nt":
        os.system("fsutil file createnew " + data.db_file + " 0")
        os.system("fsutil file createnew " + data.restart_file_name + " 0")
    else:
        os.system("touch " + data.db_file)
        os.system("touch " + data.restart_file_name)
    os.execv(sys.executable, ['python'] + sys.argv)


def show_message(text):
    print(text)


def run():
    no_db_restart_detect()
    # file_evaluation()
    show_message(messages.hello_txt)
    typing_data()


def restart():
    console_clear()
    file_operation.flush()
    file_operation.close()
    os.execv(sys.executable, ['python'] + sys.argv)


def no_db_restart_detect():
    if os.path.isfile(data.restart_file_name):
        data.db_file_exist = False
        if os.name == "nt":
            os.system("del " + data.restart_file_name)
        else:
            os.system("rm " + data.restart_file_name)
        # print("wykryto restart")
        # print(data.db_file_exist)
        # heartbeat(3)


def program_terminate():
    sys.exit()


def console_clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def typing_data():
    show_message(messages.login_txt)
    data.usr_login = input()
    show_message(messages.pass_txt)
    data.usr_password = input()
    credential_parser()


def dummy_data():
    counter = 0
    data_length = 12
    dummy_string = ""
    character_set = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while counter < data_length:
        char_num = random.randint(0, 61)
        generated_char = character_set[char_num]
        dummy_string += generated_char
        counter += 1
    return dummy_string


def file_evaluation():
    answer = "y"
    file_lines_num = file_len()
    # print(file_lines_num % 2 != 0)
    if file_lines_num % 2 != 0 or file_lines_num == 0:
        if data.db_file_exist:
            show_message(messages.data_file_error)
            show_message(messages.new_data_file_question)
            answer = input()
        if answer.lower() == "y":
            dummy_data()
            file_operation.truncate(0)
            file_operation.seek(0)
            # Write dummy login and password to db file
            write_line(dummy_data())
            write_line(dummy_data())
            restart()
        else:
            show_message(messages.good_bay)
            heartbeat(5)
            program_terminate()


def credential_parser():
    credentials_array = []
    file_lines_num = file_len()
    current_line = 0
    for read_line in range(file_lines_num):
        if current_line < file_lines_num:
            db_line = lines_read[current_line].strip("\n")
            credentials_array.insert(current_line, line_splitter(db_line))
            current_line += 1
    # print(credentials_array[1][2])
    # print(len(credentials_array))
    credential_check(credentials_array)


def credential_check(credentials_array):
    login = 0
    password = 2
    for row in range(len(credentials_array)):
        if data.usr_login == credentials_array[row][login] and data.usr_password == credentials_array[row][password]:
            # print("dobrze")
            show_message(messages.good_credential)
            heartbeat(5)
            program_terminate()
    else:
        show_message(messages.bad_credential)
        show_message(messages.create_account_answer)
        create_account_chose()


def create_account_chose():
    answer = input()
    if answer.lower() == "y":
        console_clear()
        show_message(messages.create_account_yes)
        creating_account()
        console_clear()
        show_message(messages.create_account_finish)
        heartbeat()
        restart()
    else:
        show_message(messages.good_bay)
        heartbeat(5)
        program_terminate()


def file_len():
    lines_num = 0
    for line in lines_read:
        lines_num += 1
    return lines_num


def creating_account():
    show_message(messages.create_account_log)
    data.log_to_write = input()
    show_message(messages.create_account_pass)
    data.pass_to_write = input()
    data_to_write = db_data_generator(data.log_to_write, dummy_data(), data.pass_to_write)
    write_line(data_to_write)


def write_line(to_write):
    file_operation.write(to_write + "\n")


def data_hashing(data_to_hash):
    hashing = hashlib.sha256()
    hashing.update(str(data_to_hash + data.salt).encode("utf-8"))
    # print(hashing.hexdigest())


def db_data_generator(login, salt, password):
    db_data = login + ", " + salt + ", " + password
    # print(db_data)
    return db_data


def line_splitter(db_line):
    db_elements = str(db_line)
    elements_array = db_elements.split(", ")
    return elements_array


def heartbeat(time_out=3):
    time_counting = True
    counter = 0
    while time_counting:
        print(".", end="")
        time.sleep(1)
        # https://rumprecordings.bandcamp.com/track/asleep-bwoy-de-bhajan-remix
        counter += 1
        # print(counter)
        if counter == time_out:
            print("\n")
            break
