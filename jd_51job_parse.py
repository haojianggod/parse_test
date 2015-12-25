#coding=utf-8

from html_find import HtmlFind
import re

class Jd51Job_HtmlFind(HtmlFind):
    def __init__(self, doc):

        super(Jd51Job_HtmlFind, self).__init__(doc.decode('gb2312'))
        self._init_keys_map()
        self.result = {}

    def _init_keys_map(self):
        self.keys_map = {
            "工作职位": 'jobPosition',
            "发布日期": 'puDate',
            "工作地点": 'jobWorkLoc',
            "招聘人数": 'jobPersonNumber',
            "工作年限": 'jobWorkAge',
            "学历要求": 'jobDiploma',
            "薪资范围": 'jobSalary',
            "上班地址": 'jobWorkLocExt',
            "职能类别": 'jobCate',
            "职位标签": 'jobTags',
            "薪酬福利": 'jobWelfare',
            "工作描述": 'jobDescription',
            "公司名":   'incName',
            "公司行业": 'incIndustry',
            "公司性质": 'incType',
            "公司规模": 'incScale',
            "公司地址": 'incAddress',
            "公司介绍": 'incIntro',
        }

    def set_field(self, key, value):
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if key not in self.keys_map:
            return

        if key not in ['公司介绍', '工作描述']:
            self.result[self.keys_map[key]] = re.sub(ur'[\n]+', ' ', value)
            return

        self.result[self.keys_map[key]] = value

    def find_fields(self):
        self.result.clear()
        dts = self.findTag('dt', text_pattern=u'(.*?)：')
        dds = self.findTag('dd', text_pattern=u'(.*?)')

        dl_i = 0
        dd_i = 0

        for dl in dts:
            if dl.encode('utf-8') in ['公司地址']:
                dd_i += 1
                continue

            key = self.remove_tag(dts[dl_i])
            value = self.remove_tag(dds[dd_i])
            self.set_field(key, value)

            dl_i += 1
            dd_i += 1

        self.find_other_fields()

    # jobPosition, jobDescription, incName, incIntro
    def find_other_fields(self):
        jobElem = self.findElemByPattern(ur'<li class="tCompany_job_name">(.*?)</li>.*<div class="tCompany_text">(.*?)</div>')
        incName_Elem = self.searchElemByPattern(ur'<div class=".*?job_page_company">(.*?)</h[^>]*>')
        incIntro_Elem = self.searchElemByPattern(ur'<div class=.*?tCompany_text_gsjs.*?>(.*?)</div>')
        incUrl_Elem = self.searchElemByPattern(ur'<li><a href="([^>]*?)">查看公司简介.*?</a></li>')

        if len(jobElem) and len(jobElem[0]) < 2:
            raise Exception("find jobPosition error..")

        self.result['jobPosition'] = self.remove_tag(jobElem[0][0])
        self.result['jobDescription'] = self.remove_tag(jobElem[0][1])

        if len(incName_Elem):
            self.result['incName'] = self.remove_tag(incName_Elem[0])
        if len(incIntro_Elem):
            self.result['incIntro'] = self.remove_tag(incIntro_Elem[0])
        if len(incUrl_Elem):
            self.result['inUrl'] = incUrl_Elem[0]

    def prt(self):
        for key, value in self.result.items():
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            print '{} : {}'.format(key, value)

if __name__ == '__main__':
    with open('jd_51job3.html', 'rb') as f:
        doc = f.read()

    find = Jd51Job_HtmlFind(doc)
    find.find_fields()
    find.prt()