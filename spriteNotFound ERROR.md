#How to fix it:

If you encounter an error where it cant find the sprites in the directory that is specified:
go to the respective path.py file and change the directory to go to the respective "files" folder.
Lets say you want to play pong:

    1. find the "pong_files" folder that can be where ever you want (as long as it is on the
       same user)

    2. right click the folder and click properties, switch to "General" and copy the path.
       These exact instructions apply to windows. on MacOS and linux it is probably different but the important thing is to find the exact folder path.

    3. open "pong_path.py" file and paste the path inside of quotation marks.
       you want to delete the part where it specifies the user that should look something like 'C:\Users\User'

       make sure:
        that every backslash '\' is doubled and there is a double backslash at the end. This is because backslashes in python can be used in strings to modify them. a double backslash cancels the command (example: 'Desktop\\Games\\pong_files\\').

        also make sure that the path .py and the actual main .py files are in the same directory
