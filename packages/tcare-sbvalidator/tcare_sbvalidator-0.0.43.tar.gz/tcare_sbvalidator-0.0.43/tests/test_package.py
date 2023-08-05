from tcare_sbvalidator import sb_validator

msg = sb_validator.create_sms("jnsdj24", "123", "456", "Well hey!")
print(sb_validator.sms(msg).data)