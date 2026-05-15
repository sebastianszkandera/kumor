[app]
# (str) Title of your application
title = MindFree

# (str) Package name
package.name = mindfree

# (str) Package domain (needed for android)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = python3,kivy,plyer

# (str) Supported orientation
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (str) Presplash
presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon path
icon.filename = %(source.dir)s/icon.png

# (str) Android entrypoint, default is ok
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android application package
android.apptitle = MindFree
