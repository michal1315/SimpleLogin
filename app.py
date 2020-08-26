import messages
import log_logic


messages.show_message(messages.hello_txt)
messages.show_message(messages.login_txt)
log_logic.type_login()
messages.show_message(messages.pass_txt)
log_logic.type_password()
# print(f"Podane log: {data.usr_login}")
# print(f"Podane hasło: {data.usr_pass}")

log_logic.credential_check()
