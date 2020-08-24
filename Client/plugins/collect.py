# -*- coding:utf-8 -*-

import subprocess


def collect():
    data = dict()
    data['sn'] = 'Ser-005'
    data['asset_type'] = 'server'
    data['name'] = '测试名称4'
    data['manage_ip'] = '1.1.1.1'
    data['in_ip'] = '192.168.1.1'
    data['out_ip'] = '12.18.11.11'
    data['visit_url'] = 'www.xxx.com'
    data['url_status'] = '200'
    data['business_style'] = 'web'
    data['department_per'] = '李二狗'
    data['phone'] = '13829328231'
    data['mail'] = 'mail03@test.com'
    data['regional'] = 'DMZ区'
    data['location'] = '串接'
    data['status'] = '0'
    data['le_status'] = '0'
    data['memo'] = '这是备注'
    data['approved'] = 'True'
    return data


if __name__ == "__main__":
    # 收集信息功能测试
    data = collect()
    print(data)