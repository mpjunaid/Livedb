from database import Livedb
import time

database = Livedb()
# database.drop_table()
email = "test@example.com"
user_code, success = database.insert_user(email)
print(user_code, success)
user_code, success = database.insert_user(email)
print(user_code, success)


print(database.list_users())
database.update_last_used(email)
time.sleep(3)
print(database.list_users())


database.close_connection()
