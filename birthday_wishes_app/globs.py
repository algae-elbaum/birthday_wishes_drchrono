from requests_oauthlib import OAuth1

# Vars in this file are those that possibly want to be used in multiple files.
# In reality they will probably only be used in models.py, so they may all just
# get transferred back there in the end.

# For authenticating:
redirect_uri = 'http://gaster.caltech.edu/'
client_id = 'xMhsSBQKKJKU4iyc5QMh7Ivkn7kxNxAYTdRUgqtC'
client_secret = 'iqoC6ROaulYVkX9uoVlhlYEVioOMpbkOPuKK7gF7OCfo8URKBevGbkIVVNtTqGo8sqAj9yeAAl9xtyaaMHX4PZuHfOazP4pqVqjS6arPKQONtKrHKSzk7R0ehFmcadnw'
# Not sure if messages actually sends messages or if it just sticks it into a list
# that the doctor has to deal with manually (the responsible_user field confuses me)
scopes = 'patients' 

# Max len is largely arbitrary
max_msg_len = 500

# Val for whether any messages should ever be sent
birthday_messages_on = True
