from settings import Settings, SettingsObj


setting = Settings()
setting.parse()

print("-"*20)

for k in setting:
    print("%s = %s" %(k,setting[k]))
setting['USERS'] = 10
setting.update_settings()
obj = SettingsObj('app')
