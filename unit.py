from settings import Settings


setting = Settings()
setting.parse()

print("-"*20)

for k in setting:
    print("%s = %s" %(k,setting[k]))
    
setting.update_settings()
