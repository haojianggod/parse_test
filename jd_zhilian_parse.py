# coding=utf-8

from html_find import HtmlFind
import re

class JdZhilianHtmlFind(HtmlFind):
    def __init__(self, doc):
        super(JdZhilianHtmlFind, self).__init__(doc)
        self._init_keys_map()
        self._result = {}

    def _init_keys_map(self):
        self.keys_map = {

            "职位月薪": 'jobSalary',
            "工作地点": 'jobWorkLoc',
            "发布日期": 'pubDate',
            "工作性质": 'jobType',
            "工作经验": 'jobWorkAge',
            "最低学历": 'jobDiploma',
            "招聘人数": 'jobPersonNumber',
            "职位类别": 'jobCate',
            "公司规模": 'incScale',
            "公司性质": 'incType',
            "公司行业": 'incIndustry',
            "公司地址": 'incAddress',

        }

    def set_field(self, key, value):
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if key not in self.keys_map:
            return

        if key in ['工作地点', '职位类别', '发布日期']:
            self._result[self.keys_map[key]] = self.remove_tag(value)
            return
        if key in ['公司行业']:
            self._result[self.keys_map[key]] = self.remove_tag(value)
            return

        self._result[self.keys_map[key]] = value

    def find_fields(self):
        top_elems = self.findTag('div', 'fixed-inner-box')
        if not len(top_elems):
            raise Exception("find position exception..")
        # print top_elems[0]

        position = re.findall(r'<h1>(.*?)</h1>', top_elems[0], re.S)
        for e in position:
            # print "position: ", e
            self._result['jobPosition'] = e


        job_mid_elems = self.findTag('ul', 'terminal-ul clearfix')
        if not len(job_mid_elems):
            raise Exception('find job mid elems exception..')
        # print job_mid_elems[0]

        spans = re.findall(r'<span>(.*?)：</span>', job_mid_elems[0], re.S)
        strongs = re.findall(r'<strong>(.*?)</strong>', job_mid_elems[0], re.S)

        for i in range(len(spans)):
            self.set_field(spans[i], strongs[i])

        # 工作描述， 公司描述
        button_elems = self.findTag('div', 'tab-inner-cont')
        if len(button_elems) != 2:
            raise Exception("parse job desc and incIntro exception")
        self._result['jobDescription'] = self.remove_tag(button_elems[0])
        self._result['incIntro'] = self.remove_tag(button_elems[1])

        # 公司额外信息
        company_elems = self.findTag('div', 'company-box')
        if not company_elems or len(company_elems)< 0:
            raise Exception("company fields parse exception...")
        spans = re.findall(r'<span>(.*?)：</span>', company_elems[0], re.S)
        strongs = re.findall(r'<strong>(.*?)</strong>', company_elems[0], re.S)
        for i in range(len(spans)):
            self.set_field(spans[i], strongs[i])

        company_name_info = re.findall(r'<p[^<>]*?company-name-t[^<>]*>.*?<a[^<>]*?href="(.*?)"[^<>]*?>(.*?)</a>', company_elems[0], re.S)
        if not company_name_info or len(company_name_info) < 1:
            raise Exception("parse company name, url exception...")
        self._result['incUrl'] = company_name_info[0][0]
        self._result['incName'] = self.remove_tag(company_name_info[0][1])



    def prt(self):
        for key, value in self._result.items():
            print key, " : ", value



if __name__ == '__main__':
    with open('jd_zhilian.html', 'rb') as f:
        doc = f.read()

    zhilian_find = JdZhilianHtmlFind(doc)
    zhilian_find.find_fields()
    zhilian_find.prt()