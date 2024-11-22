pyssh.py
creates a python-shell on remote server. (str) -> str
incomplete; made for testing module ssh() in fmnss/sendnodes() can be used interactively.
during interactive command `nano` can be used but will have unexpected results, you can create and save files but will need to be sure to clear what has been cached so it will not write to the file.
`cd` works but will throw an error if you dont use the complete path, but it still changes your directory i just havent put an exception in.

usage: `python3 pyssh.py user_name ip_address port keyname`
output `username@ip_address:current_working_directory$`