# coding=utf-8

from html_find import HtmlFind
import re


class JdLagouHtmlFind(HtmlFind):
    def __init__(self, doc):
        super(JdLagouHtmlFind, self).__init__(doc)

        self.result = {}


    def find_fields(self):
        job_part_one = self.findTag('dd', 'job_request')
        for e in job_part_one:
            print e
            sear = re.findall(ur'.*<span[^>]*>(.*)</span>',e)
            t = re.findall(ur'<p[^>]*>([^<>]*?)</p>', e)
            for m in sear:
                print m
            for p in t:
                print p

        job_desc = self.findTag('dd', 'job_bt')
        for e in job_desc:
            e = self.remove_tag(e)
            print e

        dt = self.findTag('dt', 'clearfix join_tc_icon')
        for m in dt:
            # m = self.remove_tag(m)
            title = re.findall(r'.*<h[^<>]* title="(.*?)"[^<>]*>.*?<div>([^<>]*?)</div>', m, re.S)
            for t in title:
                for s in t:
                    print s

        company = self.findTag('dl', 'job_company')
        for c in company:
            cinfo = re.findall(r'.*?<img[^<>]*alt="(.*?)"[^<>]*>'
                              r'.*领域</span>([^<>]*)'
                              r'.*规模</span>([^<>]*)'
                              r'.*主页</span>.*<a[^<>]*href="(.*?)"[^<>]*>'
                              r'.*目前阶段</span>([^<>]*)'
                              r'.*工作地址</h[^<>]*>.*?<div>([^<>]*)</div>', c, re.S)
            if cinfo:

                for m in cinfo[0]:
                    print m



        # feature = self.searchElemByPattern(r'<dl[^<>]*"job_detail">.*<h[^<>]* title="(.*?)"[^<>]*>'
        #                                    r'.*?<div>([^<>]*?)</div>'
        #                                    r'.*领域</span>([^<>]*)'
        #                                    r'.*规模</span>([^<>]*)'
        #                                    r'.*主页</span>.*<a[^<>]*href="(.*?)"[^<>]*>'
        #                                    r'.*目前阶段</span>([^<>]*)'
        #                                    r'.*工作地址</h[^<>]*>.*?<div>([^<>]*)</div>')
        #
        #
        #
        # for s in feature:
        #     print s

        # title = self.searchElemByPattern(r'<dl[^<>]*"job_detail">.*<h[^<>]* title="(.*?)"[^<>]*>'
        #                                  r'.*?<div>([^<>]*?)</div>')
        #
        # for t in title:
        #     print t






if __name__ == '__main__':
    with open('jd_lgJob.html', 'rb') as f:
        doc = f.read()

    lagou_find = JdLagouHtmlFind(doc)
    lagou_find.find_fields()