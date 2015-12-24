# coding=utf-8

import file_op
import re
import sys
from lxml import html
reload(sys)
sys.setdefaultencoding('utf-8')


test_pat = "//div[@class='123']"


def convert1(pat):
    doc = file_op.read_file('jd_51job.html')
    if isinstance(doc, unicode):
        doc = doc.encode('utf-8')
    reg_pet = ur'<li class="tCompany_job_name"><h1 title="(.*)">'
    r = re.findall(reg_pet, doc)
    # if r:
    #     print r[0].decode('gb2312')

# print convert(test_pat)

def convert2():
    doc = file_op.read_file('jd_51job.html')
    doc = html.fromstring(doc)
    a = doc.xpath('//li[@class="tCompany_job_name"]')
    # print a[0].text_content()

def remove_tag(s):
    r = re.sub(r'<br>|<p>','\n', s)
    r = re.sub(r'(<[^>]*>)|&nbsp;','',r)
    r = re.sub(r'[\t\r]+', ' ', r)
    r = re.sub(r'\s+\n+\s+', '\n', r)
    r = re.sub(r'^\s+', '', r)
    return r

def getinfo1(doc):
    dl_pat = ur'<dt>(.*?)：</dt>'
    dd_pat = ur'<dd[^>]*>(.*?)</dd>'
    r = re.findall(dl_pat, doc.decode('gb2312'), re.S)
    dd = re.findall(dd_pat, doc.decode('gb2312'), re.S)


    print len(r)
    print len(dd)
    print "====="

    r_i = 0
    dd_i = 0

    for i in range(0, len(r)):

        if r[i].encode('utf-8') in ['公司地址']:
             dd_i += 1
             continue

        print r[r_i], " : ", remove_tag(dd[dd_i])
        r_i += 1
        dd_i += 1

    for e in r:
        print e

    print "===="

    for e in dd:
        print re.sub(u'&nbsp|;','', e)

import time
if __name__ == '__main__':

    doc = file_op.read_file('jd_51job.html')
    # doc = html.fromstring(doc)
    start = time.time()
    for i in range(0,1):
        # convert1("") #0.0007
        # convert2()  # 0.016
        getinfo1(doc)
    print time.time() - start
