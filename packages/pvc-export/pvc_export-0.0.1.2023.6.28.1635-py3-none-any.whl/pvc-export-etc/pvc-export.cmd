rem copy it into path-to-python-scripts, like C:\Programs\Python\Scripts
rem useful in cmd.exe interactive session, not useful in the Windows registry

@python3 -m pvc_export %*

rem or, in place of python3 above, use the path to python3 in the (virtual) environment
rem where pvc_export package is installed
