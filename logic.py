import time
import data
import messages
import os
import sys

file_operation = open(data.file_name, mode="r+", encoding="utf-8")
lines_read = file_operation.readlines()


def show_message(text):
    print(text)


def type_login():
    data.usr_login = input()


def type_password():
    data.usr_pass = input()


def run():
    show_message(messages.hello_txt)
    typing_data()


def restart():
    console_clear()
    file_operation.flush()
    file_operation.close()
    os.execv(sys.executable, ['python'] + sys.argv)


def program_terminate():
    sys.exit()


def console_clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def typing_data():
    show_message(messages.login_txt)
    type_login()
    show_message(messages.pass_txt)
    type_password()
    credential_parser()


def credential_parser():
    logins_array = []
    passwords_array = []
    file_lines_num = file_len()
    current_line = 0
    for read_line in range(file_lines_num):
        if current_line < file_lines_num:
            login = lines_read[current_line].strip("\n")
            password = lines_read[current_line + 1].strip("\n")
            current_line += 2
            logins_array.append(login)
            passwords_array.append(password)
        else:
            # print(f"login podany: {data.usr_login}")
            # print(f"pass podany: {data.usr_pass}")
            # print(logins_array)
            # print(password_array)
            credential_check(logins_array, passwords_array)


def credential_check(logins_array, passwords_array,):
    if data.usr_login in logins_array and data.usr_pass in passwords_array:
        show_message(messages.good_credential)
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
        log_write()
        pass_write()
        console_clear()
        show_message(messages.create_account_finish)
        heartbeat()
        restart()
    else:
        show_message(messages.create_account_no)
        program_terminate()


def file_len():
    lines_num = 0
    for data in lines_read:
        lines_num += 1
    return lines_num


def log_write():
    show_message(messages.create_account_log)
    data.log_to_write = input()
    write_line(data.log_to_write)


def pass_write():
    show_message(messages.create_account_pass)
    data.pass_to_write = input()
    write_line(data.pass_to_write)


def write_line(to_write):
    file_operation.write(to_write + "\n")


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
