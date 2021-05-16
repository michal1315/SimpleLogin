import data
import messages

file_operation = open(data.file_name, mode="r+", encoding="utf-8")
lines_read = file_operation.readlines()


def show_message(text):
    print(text)


def type_login():
    data.usr_login = input()


def type_password():
    data.usr_pass = input()


def add_new_account():
    log_write()
    pass_write()
    return 0


def credential_check():
    file_lines_num = file_len()
    current_line = 0

    for read_line in range(file_lines_num):
        if current_line < file_lines_num:
            login = lines_read[current_line].strip("\n")
            password = lines_read[current_line + 1].strip("\n")
            # print(f"login: {login}")
            # print(f"pass: {password}")
            # print(f"login podany: {data.usr_login}")
            # print(f"pass podany: {data.usr_pass}")
            current_line += 2

            if login == data.usr_login and password == data.usr_pass:
                show_message(messages.good_credential)
                break
        else:
            show_message(messages.bad_credential)
            show_message(messages.create_account_answer)
            create_account_chose()


def create_account_chose():
    answer = input()
    if answer.lower() == "y":

        show_message(messages.create_account_yes)
        log_write()
        pass_write()
        show_message(messages.create_account_finish)
        exit()
    else:
        show_message(messages.create_account_no)
        exit()


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

