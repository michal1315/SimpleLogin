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
    file_evaluation()
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
    file_elements = 0
    current_line = 0
    for read_line in range(file_lines_num):
        if current_line < file_lines_num:
            db_line = lines_read[current_line].strip("\n")
            current_line += 1
            # print(len(line_splitter(db_line)))
            file_elements += len(line_splitter(db_line))
    # print(file_elements)
    if file_elements % 3 != 0 or file_lines_num == 0:
        if data.db_file_exist:
            show_message(messages.data_file_error)
            show_message(messages.new_data_file_question)
            answer = input()
        if answer.lower() == "y":
            login = dummy_data()
            password = dummy_data()
            salt = dummy_data()
            file_operation.truncate(0)
            file_operation.seek(0)
            data_to_write = db_data_generator(login, salt, data_hashing(password, salt))
            # Write dummy login and password to db file
            write_line(data_to_write)
            restart()
        else:
            show_message(messages.good_bay)
            heartbeat(5)
            program_terminate()


def credential_parser():
    file_lines_num = file_len()
    current_line = 0
    for read_line in range(file_lines_num):
        if current_line < file_lines_num:
            db_line = lines_read[current_line].strip("\n")
            data.credentials_array.insert(current_line, line_splitter(db_line))
            current_line += 1
    # print(credentials_array[1][2])
    # print(len(credentials_array))
    credential_check()


def credential_check():
    for row in range(len(data.credentials_array)):
        login = data.credentials_array[row][0]
        salt = data.credentials_array[row][1]
        password = data.credentials_array[row][2]
        if data.usr_login == login and data_hashing(data.usr_password, salt) == password:
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
        creating_account_typing()
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


def creating_account_typing(login_occupied=False, big_letter_in_pass=True,
                            small_letter_in_pass=True, digit_in_pass=True,
                            pass_mini_len=True):
    console_clear()
    if login_occupied or not big_letter_in_pass or not small_letter_in_pass or not digit_in_pass or not pass_mini_len:
        show_message(messages.create_account_failure)
        if login_occupied:
            show_message(messages.login_occupied_txt)
        if not big_letter_in_pass:
            show_message(messages.lack_big_letter_in_pass)
        if not small_letter_in_pass:
            show_message(messages.lack_small_letter_in_pass)
        if not digit_in_pass:
            show_message(messages.lack_digit_in_pass)
        if not pass_mini_len:
            show_message(messages.pass_to_short)
    show_message(messages.create_account_log)
    data.log_to_write = input()
    show_message(messages.password_hint)
    show_message(messages.create_account_pass)
    data.pass_to_write = input()
    data.salt = dummy_data()
    creating_account_validation()


def creating_account_validation():
    logins_array = []
    login_occupied = False
    big_letter_in_pass = False
    small_letter_in_pass = False
    digit_in_pass = False
    pass_mini_len = False
    for row in range(len(data.credentials_array)):
        login = data.credentials_array[row][0]
        logins_array.append(login)
    if data.log_to_write in logins_array:
        login_occupied = True
        if data.creating_account_attempts == 3:
            console_clear()
            show_message(messages.create_account_failure)
            show_message(messages.good_bay)
            heartbeat(5)
            program_terminate()
        data.creating_account_attempts += 1
    for char in data.pass_to_write:
        if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            big_letter_in_pass = True
        if char in "abcdefghijklmnopqrstuvwxyz":
            small_letter_in_pass = True
        if char in "0123456789":
            digit_in_pass = True
        if len(data.pass_to_write) >= 8:
            pass_mini_len = True
    if not login_occupied and big_letter_in_pass and small_letter_in_pass and digit_in_pass and pass_mini_len:
        creating_account_db_write()
    else:
        creating_account_typing(login_occupied, big_letter_in_pass,
                                small_letter_in_pass, digit_in_pass,
                                pass_mini_len)


def creating_account_db_write():
    data_to_write = db_data_generator(data.log_to_write, data.salt, data_hashing(data.pass_to_write, data.salt))
    write_line(data_to_write)


def write_line(to_write):
    file_operation.write(to_write + "\n")


def data_hashing(data_to_hash, salt):
    hashing = hashlib.sha256()
    hashing.update(str(data_to_hash+salt).encode("utf-8"))
    # https://murgemusic.bandcamp.com/track/cant-hurt-me-now-feat-sierra-lundy
    # print(hashing.hexdigest())
    return hashing.hexdigest()


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
