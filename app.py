import logic
import messages


logic.show_message(messages.hello_txt)
logic.show_message(messages.login_txt)
logic.type_login()
logic.show_message(messages.pass_txt)
logic.type_password()
# print(f"Podane log: {data.usr_login}")
# print(f"Podane hasło: {data.usr_pass}")

logic.credential_check()
