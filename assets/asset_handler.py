import json
from assets import models


class NewAsset(object):
    def __init__(self, request, data):
        self.request = request
        self.data = data

    def add_to_new_assets_zone(self):
        defaults = {
            'data': json.dumps(self.data),
            'aud_asset_type': self.data.get('aud_asset_type'),
            'aud_name': self.data.get('aud_name'),
            'aud_manage_ip': self.data.get('aud_manage_ip'),
            'aud_in_ip': self.data.get('aud_in_ip'),
            'aud_out_ip': self.data.get('aud_out_ip'),
            'aud_visit_url': self.data.get('aud_visit_url'),
            'aud_url_status': self.data.get('aud_url_status'),
            'aud_business_style': self.data.get('aud_business_style'),
            'aud_contract': self.data.get('aud_contract'),
            'aud_department_per': self.data.get('aud_department_per'),
            'aud_phone': self.data.get('aud_phone'),
            'aud_mail': self.data.get('aud_mail'),
            'aud_regional': self.data.get('aud_regional'),
            'aud_deployment': self.data.get('aud_deployment'),
            'aud_status': self.data.get('aud_status'),
            'aud_le_status': self.data.get('aud_le_status'),
            'aud_memo': self.data.get('aud_memo'),
        }

        idcs = {
            'data': json.dumps(self.data),
            'idc_name': self.data.get('idc_name'),
            'idc_link': self.data.get('idc_link'),
            'idc_cab': self.data.get('idc_cab'),
            'idc_num': self.data.get('idc_num'),
            'idc_memo': self.data.get('idc_memo'),
        }

        manufacturers = {
            'data': json.dumps(self.data),
            'man_name': self.data.get('man_name'),
            'man_frame': self.data.get('man_frame'),
            'man_language': self.data.get('man_language'),
            'man_version': self.data.get('man_version'),
            'man_department': self.data.get('man_department'),
            'man_department_per': self.data.get('man_department_per'),
            'man_phone': self.data.get('man_phone'),
            'man_mail': self.data.get('man_mail'),
            'man_status': self.data.get('man_status'),
            'man_stime': self.data.get('man_stime'),
            'man_etime': self.data.get('man_etime'),
            'man_memo': self.data.get('man_memo'),
        }

        models.NewAssetApprovalZone.objects.update_or_create(aud_sn=self.data['aud_sn'], defaults=defaults)
        models.NewAssetApprovalZone.objects.update_or_create(aud_sn=self.data['aud_sn'], defaults=idcs)
        models.NewAssetApprovalZone.objects.update_or_create(aud_sn=self.data['aud_sn'], defaults=manufacturers)
        return 'All资产已经加入或者更新待审批区域！'

    def add_to_new_assets_zone_server(self):
        servers = {
            'data': json.dumps(self.data),
            'ser_sub_asset_type': self.data.get('ser_sub_asset_type'),
            'ser_os_type': self.data.get('ser_os_type'),
            'ser_os_release': self.data.get('ser_os_release'),
            'ser_model': self.data.get('ser_model'),
            'ser_department_per': self.data.get('ser_department_per'),
            'ser_phone': self.data.get('ser_phone'),
            'ser_mail': self.data.get('ser_mail'),
            'ser_memo': self.data.get('ser_memo'),
        }
        services = {
            'data': json.dumps(self.data),
            'serv_ser': self.data.get('serv_ser'),
            'serv_port': self.data.get('serv_port'),
            'serv_visit': self.data.get('serv_visit'),
            'serv_memo': self.data.get('serv_memo'),
        }
        databases = {
            'data': json.dumps(self.data),
            'data_model': self.data.get('data_model'),
            'data_version': self.data.get('data_version'),
            'data_department_per': self.data.get('data_department_per'),
            'data_phone': self.data.get('data_phone'),
            'data_mail': self.data.get('data_mail'),
            'data_memo': self.data.get('data_memo'),
        }

        middleware = {
            'data': json.dumps(self.data),
            'mid_model': self.data.get('mid_model'),
            'mid_version': self.data.get('mid_version'),
            'mid_department_per': self.data.get('mid_department_per'),
            'mid_phone': self.data.get('mid_phone'),
            'mid_mail': self.data.get('mid_mail'),
            'mid_memo': self.data.get('mid_memo'),
        }
        models.NewAssetApprovalZone.objects.update_or_create(aud_sn=self.data['aud_sn'], defaults=servers)
        models.NewAssetApprovalZone.objects.update_or_create(aud_sn=self.data['aud_sn'], defaults=services)
        models.NewAssetApprovalZone.objects.update_or_create(aud_sn=self.data['aud_sn'], defaults=databases)
        models.NewAssetApprovalZone.objects.update_or_create(aud_sn=self.data['aud_sn'], defaults=middleware)
        return '服务器资产已经加入或者更新待审批区域！'

    def add_to_new_assets_zone_securitydevice(self):
        securitydevice = {
            'data': json.dumps(self.data),
            'sec_sub_asset_type': self.data.get('sec_sub_asset_type'),
            'sec_model': self.data.get('sec_model'),
            'sec_version': self.data.get('sec_version'),
            'sec_department': self.data.get('sec_department'),
            'sec_department_per': self.data.get('sec_department_per'),
            'sec_phone': self.data.get('sec_phone'),
            'sec_mail': self.data.get('sec_mail'),
            'sec_memo': self.data.get('sec_memo'),
        }

        models.NewAssetApprovalZone.objects.update_or_create(aud_sn=self.data['aud_sn'], defaults=securitydevice)
        return '安全设备资产已经加入或者更新待审批区域！'

def log(log_type, msg=None, asset=None, new_asset=None, request=None):
    """
    记录日志
    """
    event = models.EventLog()
    if log_type == "upline":
        event.log_name = "%s <%s> ：  上线" % (asset.name, asset.sn)
        event.asset = asset
        event.log_detail = "资产成功上线！"
        event.log_user = request.user
    elif log_type == "approve_failed":
        event.log_name = "%s <%s> ：  审批失败" % (new_asset.asset_type, new_asset.sn)
        event.log_new_asset = new_asset
        event.log_detail = "审批失败！\n%s" % msg
        event.log_user = request.user
        # 更多日志类型.....
    elif log_type == "update":
        event.log_name = "%s <%s> ：  数据更新！" % (asset.asset_type, asset.sn)
        event.asset = asset
        event.log_detail = "更新成功！"
    elif log_type == "update_failed":
        event.log_name = "%s <%s> ：  更新失败" % (asset.asset_type, asset.sn)
        event.asset = asset
        event.log_detail = "更新失败！\n%s" % msg
    event.save()


class ApproveAsset:
    """
    审批资产并上线。
    """

    def __init__(self, request, asset_id):
        self.request = request
        self.new_asset = models.NewAssetApprovalZone.objects.get(id=asset_id)
        self.data = json.loads(self.new_asset.data)

    def asset_upline(self):
        # 为以后的其它类型资产扩展留下接口
        func = getattr(self, '_%s_upline' % self.new_asset.aud_asset_type)  # _server_upline
        ret = func()
        return ret

    def _server_upline(self):
        # 在实际的生产环境中，下面的操作应该是原子性的整体事务，任何一步出现异常，所有操作都要回滚。
        asset = self._create_asset()
        try:
            self._create_server(asset)  # 创建服务器
            self._create_idc(asset)  # 创建机房
            self._create_services(asset)  # 创建Services
            self._create_databases(asset)  # 创建数据库
            self._create_middleware(asset)  # 创建中间件
            self._create_manufacturer(asset)  # 创建厂商
            # self._create_disk(asset)  # 创建fu
            # self._create_nic(asset)  # 创建网卡
            # self._create_tag(asset)  # 创建标签

            self._delete_original_asset()  # 从待审批资产区删除已审批上线的资产
        except Exception as e:
            asset.delete()
            log('approve_failed', msg=str(e), new_asset=self.new_asset, request=self.request)
            print(e)
            return False
        else:
            # 添加日志
            log("upline", asset=asset, request=self.request)
            print(self.new_asset, "新服务器上线!")
            return True

    def _securitydevice_upline(self):
        # 在实际的生产环境中，下面的操作应该是原子性的整体事务，任何一步出现异常，所有操作都要回滚。
        asset = self._create_asset()
        try:
            self._create_securitydevice(asset)  # 创建安全设备
            self._create_idc(asset)  # 创建机房
            self._create_manufacturer(asset)  # 创建厂商
            self._delete_original_asset()  # 从待审批资产区删除已审批上线的资产
        except Exception as e:
            asset.delete()
            log('approve_failed', msg=str(e), new_asset=self.new_asset, request=self.request)
            print(e)
            return False
        else:
            # 添加日志
            log("upline", asset=asset, request=self.request)
            print(self.new_asset, "新安全设备上线!")
            return True

    def _create_asset(self):
        """
        创建资产并上线
        :return:
        """
        # 利用request.user自动获取当前管理人员的信息，作为审批人添加到资产数据中。
        asset = models.Asset.objects.create(sn=self.new_asset.aud_sn,
                                            asset_type=self.new_asset.aud_asset_type,
                                            name=self.new_asset.aud_name,
                                            manage_ip=self.new_asset.aud_manage_ip,
                                            in_ip=self.new_asset.aud_in_ip,
                                            out_ip=self.new_asset.aud_out_ip,
                                            visit_url=self.new_asset.aud_visit_url,
                                            url_status=self.new_asset.aud_url_status,
                                            business_style=self.new_asset.aud_business_style,
                                            contract=self.new_asset.aud_contract,
                                            department_per=self.new_asset.aud_department_per,
                                            phone=self.new_asset.aud_phone,
                                            mail=self.new_asset.aud_mail,
                                            regional=self.new_asset.aud_regional,
                                            deployment=self.new_asset.aud_deployment,
                                            status=self.new_asset.aud_status,
                                            le_status=self.new_asset.aud_le_status,
                                            memo=self.new_asset.aud_memo,
                                            approved_by=self.request.user,
                                            )
        return asset

    def _create_server(self, asset):
        """
       创建服务器
       :param asset:
       :return:
       """
        models.Server.objects.create(asset=asset,
                                     ser_sub_asset_type=self.new_asset.ser_sub_asset_type,
                                     ser_os_type=self.new_asset.ser_os_type,
                                     ser_os_release=self.new_asset.ser_os_release,
                                     ser_model=self.new_asset.ser_model,
                                     ser_department_per=self.new_asset.ser_department_per,
                                     ser_phone=self.new_asset.ser_phone,
                                     ser_mail=self.new_asset.ser_mail,
                                     ser_memo=self.new_asset.ser_memo,
                                     )

    def _create_securitydevice(self, asset):
        """
       创建安全设备
       :param asset:
       :return:
       """
        models.SecurityDevice.objects.create(asset=asset,
                                             sec_sub_asset_type=self.new_asset.sec_sub_asset_type,
                                             sec_model=self.new_asset.sec_model,
                                             sec_version=self.new_asset.sec_version,
                                             sec_department=self.new_asset.sec_department,
                                             sec_department_per=self.new_asset.sec_department_per,
                                             sec_phone=self.new_asset.sec_phone,
                                             sec_mail=self.new_asset.sec_mail,
                                             sec_memo=self.new_asset.sec_memo,
                                             )

    def _create_idc(self, asset):
        """
       创建机房
       :param asset:
       :return:
       """
        # idc = models.IDC.objects.create(asset=asset)
        # idc.name = self.new_asset.idc_name,
        # idc.name_1 = self.new_asset.name_1,
        # idc.name_2 = self.new_asset.name_2,
        # idc.name_3 = self.new_asset.name_3,
        # idc.memo = self.new_asset.idc_memo,
        # idc.save()

        models.IDC.objects.create(asset=asset,
                                  idc_name=self.new_asset.idc_name,
                                  idc_link=self.new_asset.idc_link,
                                  idc_cab=self.new_asset.idc_cab,
                                  idc_num=self.new_asset.idc_num,
                                  idc_memo=self.new_asset.idc_memo,
                                  )
        # print(self.new_asset)

    def _create_tag(self, asset):
        """
       创建标签
       :param asset:
       :return:
       """
        # m = self.new_asset.tags
        # print(m)
        # if m:
        #     tag_obj, _ = models.Tag.objects.get_or_create(name=m)
        #     print("23423", tag_obj)
        #     asset.tags = tag_obj
        #     asset.save()
        tag_list = self.data.get('tags')

        if not tag_list:
            print("tag_list is Null")
            return
        for tag in tag_list:
            tags = models.Tag()
            tags.asset = asset
            tags.name = tag
            tags.save()

    def _create_services(self, asset):
        """
        创建服务.
        :param asset:
        :return:
        """
        models.Services.objects.create(asset=asset,
                                       serv_ser=self.new_asset.serv_ser,
                                       serv_port=self.new_asset.serv_port,
                                       serv_visit=self.new_asset.serv_visit,
                                       serv_memo=self.new_asset.serv_memo,
                                       )
        # services = models.Services.objects.create(asset=asset)
        # services.ser_ser = self.new_asset.ser_ser
        # services.ser_port = self.new_asset.ser_port
        # services.ser_visit = self.new_asset.ser_visit
        # services.save()

    def _create_databases(self, asset):
        """
        创建数据库.
        :param asset:
        :return:
        """
        models.Database.objects.create(asset=asset,
                                       data_model=self.new_asset.data_model,
                                       data_version=self.new_asset.data_version,
                                       data_department_per=self.new_asset.data_department_per,
                                       data_phone=self.new_asset.data_phone,
                                       data_mail=self.new_asset.data_mail,
                                       data_memo=self.new_asset.data_memo,
                                       )

    def _create_middleware(self, asset):
        """
        创建中间件.
        :param asset:
        :return:
        """
        models.Middleware.objects.create(asset=asset,
                                         mid_model=self.new_asset.mid_model,
                                         mid_version=self.new_asset.mid_version,
                                         mid_department_per=self.new_asset.mid_department_per,
                                         mid_phone=self.new_asset.mid_phone,
                                         mid_mail=self.new_asset.mid_mail,
                                         mid_memo=self.new_asset.mid_memo,
                                         )

    def _create_manufacturer(self, asset):
        """
        创建服务商.
        :param asset:
        :return:
        """
        models.Manufacturer.objects.create(asset=asset,
                                           man_name=self.new_asset.man_name,
                                           man_frame=self.new_asset.man_frame,
                                           man_language=self.new_asset.man_language,
                                           man_version=self.new_asset.man_version,
                                           man_department=self.new_asset.man_department,
                                           man_department_per=self.new_asset.man_department_per,
                                           man_phone=self.new_asset.man_phone,
                                           man_mail=self.new_asset.man_mail,
                                           man_status=self.new_asset.man_status,
                                           man_stime=self.new_asset.man_stime,
                                           man_etime=self.new_asset.man_etime,
                                           man_memo=self.new_asset.man_memo,
                                           )

    def _delete_original_asset(self):
        """
        这里的逻辑是已经审批上线的资产，就从待审批区删除。
        也可以设置为修改成已审批状态但不删除，只是在管理界面特别处理，不让再次审批，灰色显示。
        不过这样可能导致待审批区越来越大。
        :return:
        """
        self.new_asset.delete()


class UpdateAsset:
    """
    自动更新已上线的资产。
    如果想让记录的日志更详细，可以逐条对比数据项，将更新过的项目记录到log信息中。
    """

    def __init__(self, request, asset, report_data):
        self.request = request
        self.asset = asset
        self.report_data = report_data  # 此处的数据是由客户端发送过来的整个数据字符串
        self.asset_update()

    def asset_update(self):
        # 为以后的其它类型资产扩展留下接口
        func = getattr(self, "_%s_update" % self.report_data['aud_asset_type'])
        ret = func()
        return ret

    def _server_update(self):
        try:
            self._update_assets()         # 更新资产总表
            self._update_server()         # 更新服务器
            self._update_idc()  # 更新机房
            self._update_services()  # 更新Services
            self._update_databases()  # 更新数据库
            self._update_middleware()  # 更新中间件
            self._update_manufacturer()  # 更新厂商
            self.asset.save()
        except Exception as e:
            log('update_failed', msg=e, asset=self.asset, request=self.request)
            print(e)
            return False
        else:
            # 添加日志
            log("update", asset=self.asset)
            print(self.asset, "服务器资产数据被更新!")
            return True

    def _securitydevice_update(self):
        try:
            self._update_assets()         # 更新资产总表
            self._update_securitydevice()         # 更新安全设备
            self._update_idc()  # 更新机房
            self._update_manufacturer()  # 更新厂商
            self.asset.save()
        except Exception as e:
            log('update_failed', msg=e, asset=self.asset, request=self.request)
            print(e)
            return False
        else:
            # 添加日志
            log("update", asset=self.asset)
            print(self.asset, "安全设备资产数据被更新!")
            return True

    def _update_assets(self):
        """
        更新资产总表
        """
        self.asset.sn = self.report_data.get('aud_sn')
        self.asset.asset_type = self.report_data.get('aud_asset_type')
        self.asset.name = self.report_data.get('aud_name')
        self.asset.manage_ip = self.report_data.get('aud_manage_ip')
        self.asset.in_ip = self.report_data.get('aud_in_ip')
        self.asset.out_ip = self.report_data.get('aud_out_ip')
        self.asset.visit_url = self.report_data.get('aud_visit_url')
        self.asset.url_status = self.report_data.get('aud_url_status')
        self.asset.business_style = self.report_data.get('aud_business_style')
        self.asset.contract = self.report_data.get('aud_contract')
        self.asset.department_per = self.report_data.get('aud_department_per')
        self.asset.phone = self.report_data.get('aud_phone')
        self.asset.mail = self.report_data.get('aud_mail')
        self.asset.regional = self.report_data.get('aud_regional')
        self.asset.deployment = self.report_data.get('aud_deployment')
        self.asset.status = self.report_data.get('aud_status')
        self.asset.le_status = self.report_data.get('aud_le_status')
        self.asset.memo = self.report_data.get('aud_memo')
        self.asset.save()

    def _update_server(self):
        """
        更新服务器
        """
        self.asset.server.ser_sub_asset_type = self.report_data.get('ser_sub_asset_type')
        self.asset.server.ser_os_type = self.report_data.get('ser_os_type')
        self.asset.server.ser_os_release = self.report_data.get('ser_os_release')
        self.asset.server.ser_model = self.report_data.get('ser_model')
        self.asset.server.ser_department_per = self.report_data.get('ser_department_per')
        self.asset.server.ser_phone = self.report_data.get('ser_phone')
        self.asset.server.ser_mail = self.report_data.get('ser_mail')
        self.asset.server.ser_memo = self.report_data.get('ser_memo')
        self.asset.server.save()

    def _update_securitydevice(self):
        """
        更新安全设备
        """
        self.asset.securitydevice.sec_sub_asset_type = self.report_data.get('sec_sub_asset_type')
        self.asset.securitydevice.sec_model = self.report_data.get('sec_model')
        self.asset.securitydevice.sec_version = self.report_data.get('sec_version')
        self.asset.securitydevice.sec_department = self.report_data.get('sec_department')
        self.asset.securitydevice.sec_department_per = self.report_data.get('sec_department_per')
        self.asset.securitydevice.sec_phone = self.report_data.get('sec_phone')
        self.asset.securitydevice.sec_mail = self.report_data.get('sec_mail')
        self.asset.securitydevice.sec_memo = self.report_data.get('sec_memo')
        self.asset.securitydevice.save()

    def _update_idc(self):
        """
        更新机房信息
        """
        self.asset.idc.idc_name = self.report_data.get('idc_name')
        self.asset.idc.idc_link = self.report_data.get('idc_link')
        self.asset.idc.idc_cab = self.report_data.get('idc_cab')
        self.asset.idc.idc_num = self.report_data.get('idc_num')
        self.asset.idc.idc_memo = self.report_data.get('idc_memo')
        self.asset.idc.save()

    def _update_services(self):
        """
        更新服务信息
        """
        self.asset.services.serv_ser = self.report_data.get('serv_ser')
        self.asset.services.serv_port = self.report_data.get('serv_port')
        self.asset.services.serv_visit = self.report_data.get('serv_visit')
        self.asset.services.serv_memo = self.report_data.get('serv_memo')
        self.asset.services.save()

    def _update_databases(self):
        """
        更新数据库信息
        """
        self.asset.database.data_model = self.report_data.get('data_model')
        self.asset.database.data_version = self.report_data.get('data_version')
        self.asset.database.data_department_per = self.report_data.get('data_department_per')
        self.asset.database.data_phone = self.report_data.get('data_phone')
        self.asset.database.data_mail = self.report_data.get('data_mail')
        self.asset.database.data_memo = self.report_data.get('data_memo')
        self.asset.database.save()

    def _update_middleware(self):
        """
        更新中间件信息
        """
        self.asset.middleware.mid_model = self.report_data.get('mid_model')
        self.asset.middleware.mid_version = self.report_data.get('mid_version')
        self.asset.middleware.mid_department_per = self.report_data.get('mid_department_per')
        self.asset.middleware.mid_phone = self.report_data.get('mid_phone')
        self.asset.middleware.mid_mail = self.report_data.get('mid_mail')
        self.asset.middleware.mid_memo = self.report_data.get('mid_memo')
        self.asset.middleware.save()

    def _update_manufacturer(self):
        """
        更新厂商信息
        """
        self.asset.manufacturer.man_name = self.report_data.get('man_name')
        self.asset.manufacturer.man_frame = self.report_data.get('man_frame')
        self.asset.manufacturer.man_language = self.report_data.get('man_language')
        self.asset.manufacturer.man_version = self.report_data.get('man_version')
        self.asset.manufacturer.man_department = self.report_data.get('man_department')
        self.asset.manufacturer.man_department_per = self.report_data.get('man_department_per')
        self.asset.manufacturer.man_phone = self.report_data.get('man_phone')
        self.asset.manufacturer.man_mail = self.report_data.get('man_mail')
        self.asset.manufacturer.man_status = self.report_data.get('man_status')
        self.asset.manufacturer.man_stime = self.report_data.get('man_stime')
        self.asset.manufacturer.man_etime = self.report_data.get('man_etime')
        self.asset.manufacturer.man_memo = self.report_data.get('man_memo')
        self.asset.manufacturer.save()
