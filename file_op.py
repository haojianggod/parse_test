# coding=utf-8

def read_file(file_name):
    with open(file_name, 'rb') as f:
        r = f.read()
    return r

print type(read_file('jd_51job.html'))