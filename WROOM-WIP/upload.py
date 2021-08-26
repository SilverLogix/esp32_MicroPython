import cgi
import os


print("Content-Type: text/html")
print('')
print('start!')
form = cgi.FieldStorage()
filedata = form['upload']

print(filedata)

f = open('test.bin', 'w')
f.write(filedata.file.read())
f.close()

os.listdir()
