from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Asset(models.Model):
    """所有资产的共有数据表"""

    asset_type_choice = (
        ('server', '服务器'),
        ('securitydevice', '安全设备'),
        ('networkdevice', '网络设备'),
        ('otherdevice', '其它设备'),
        # ('software', '软件资产'),
    )

    asset_status = (
        (0, '在线'),
        (1, '下线'),
        (2, '未知'),
        (3, '故障'),
        (4, '备用'),
    )


    level_status = (
        (5, '非常高'),
        (4, '高'),
        (3, '中'),
        (2, '低'),
        (1, '可忽略'),
    )
    sn = models.CharField(max_length=128, unique=True, verbose_name="资产序列号")  # 不可重复
    asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='server', verbose_name="资产类型")
    name = models.CharField(null=True, max_length=64, verbose_name="资产名称")
    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP')
    in_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='内网IP')  # Michael
    out_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='公网IP')  # Michael
    visit_url = models.CharField(max_length=64, null=True, blank=True, verbose_name='域名/URL')  # Michael
    url_status = models.CharField(max_length=64, null=True, blank=True, verbose_name='域名状态')  # Michael
    business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True, verbose_name='所属业务线',
                                      on_delete=models.SET_NULL)
    business_style = models.CharField(max_length=64, null=True, blank=True, verbose_name="业务类型")
    contract = models.CharField(max_length=64, null=True, blank=True, verbose_name='业务部门')
    # contract = models.ForeignKey('Contract', null=True, blank=True, verbose_name='业务部门', on_delete=models.SET_NULL)
    department_per = models.CharField(max_length=64, null=True, blank=True, verbose_name="总负责人")
    phone = models.CharField(max_length=64, null=True, blank=True, verbose_name="总负责人-电话")
    mail = models.EmailField(null=True, blank=True, verbose_name="总负责人-邮箱")
    # idc = models.ForeignKey('IDC', null=True, blank=True, verbose_name='所在机房', on_delete=models.SET_NULL)
    regional = models.CharField(max_length=64, null=True, blank=True, verbose_name="部署区域")
    deployment = models.CharField(max_length=64, null=True, blank=True, verbose_name="部署方式")
    status = models.SmallIntegerField(choices=asset_status, default=0, verbose_name='资产状态')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    le_status = models.SmallIntegerField(choices=level_status, default=5, verbose_name='重要程度')
    approved_by = models.ForeignKey(User, null=True, blank=True, verbose_name='批准人', related_name='approved_by',
                                    on_delete=models.SET_NULL)
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='录入日期')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')
    memo = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return '<%s>  %s' % (self.get_asset_type_display(), self.name)

    class Meta:
        verbose_name = '00-资产总表'
        verbose_name_plural = "00-资产总表"
        ordering = ['-c_time']


class Server(models.Model):
    """服务器设备"""

    sub_asset_type_choice = (
        (0, '物理服务器'),
        (1, '虚拟机'),
        (2, '其它设备'),
    )

    created_by_choice = (
        ('auto', '自动添加'),
        ('manual', '手工录入'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)  # 非常关键的一对一关联！asset被删除的时候一并删除server
    ser_sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="服务器类型")
    ser_created_by = models.CharField(choices=created_by_choice, max_length=32, default='auto', verbose_name="添加方式")
    ser_hosted_on = models.ForeignKey('self', related_name='hosted_on_server',
                                  blank=True, null=True, verbose_name="宿主机", on_delete=models.CASCADE)  # 虚拟机专用字段
    ser_os_type = models.CharField('操作系统类型', max_length=64, blank=True, null=True)
    ser_os_release = models.CharField('操作系统版本', max_length=64, blank=True, null=True)
    ser_model = models.CharField(max_length=128, null=True, blank=True, verbose_name='内核信息')
    ser_department_per = models.CharField(max_length=64, null=True, blank=True, verbose_name="系统负责人")
    ser_phone = models.CharField(max_length=64, null=True, blank=True, verbose_name="联系电话")
    ser_mail = models.EmailField(null=True, blank=True, verbose_name="联系邮箱")
    ser_memo = models.CharField('备注', max_length=64, blank=True, null=True)

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_ser_sub_asset_type_display(), self.ser_model, self.asset.sn)

    class Meta:
        verbose_name = '01-服务器'
        verbose_name_plural = verbose_name


class SecurityDevice(models.Model):
    """安全设备"""

    sec_sub_asset_type_choice = (
        (0, '防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'),
        (4, '运维审计系统'),
        (5, '其它设备'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sec_sub_asset_type = models.SmallIntegerField(choices=sec_sub_asset_type_choice, default=0, verbose_name="安全设备类型")
    sec_model = models.CharField(max_length=128, default='未知型号', verbose_name='设备型号')
    sec_version = models.CharField(max_length=64, default='未知版本', verbose_name='软件版本')
    sec_department = models.CharField(max_length=64, null=True, blank=True, verbose_name="运维部门")
    sec_department_per = models.CharField(max_length=64, null=True, blank=True, verbose_name="运维负责人")
    sec_phone = models.CharField(max_length=64, null=True, blank=True, verbose_name="联系电话")
    sec_mail = models.EmailField(null=True, blank=True, verbose_name="联系邮箱")
    sec_memo = models.CharField('安全设备备注', max_length=64, blank=True, null=True)

    def __str__(self):
        return self.asset.name + "--" + self.get_sec_sub_asset_type_display() + str(self.sec_model) + " id:%s" % self.id
        # return str(self.model)

    class Meta:
        verbose_name = '02-安全设备'
        verbose_name_plural = verbose_name


class NetworkDevice(models.Model):
    """网络设备"""

    sub_asset_type_choice = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '负载均衡'),
        (4, 'VPN设备'),
        (5, '其它设备'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    net_sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="网络设备类型")
    net_model = models.CharField(max_length=128, default='未知型号', verbose_name='设备型号')
    net_version = models.CharField(max_length=64, default='未知版本', verbose_name='软件版本')
    net_department = models.CharField(max_length=64, null=True, blank=True, verbose_name="运维部门")
    net_department_per = models.CharField(max_length=64, null=True, blank=True, verbose_name="运维负责人")
    net_phone = models.CharField(max_length=64, null=True, blank=True, verbose_name="联系电话")
    net_mail = models.EmailField(null=True, blank=True, verbose_name="联系邮箱")
    net_memo = models.CharField('备注', max_length=64, blank=True, null=True)

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_net_sub_asset_type_display(), self.net_model, self.asset.sn)

    class Meta:
        verbose_name = '03-网络设备'
        verbose_name_plural = verbose_name


class OtherDevice(models.Model):
    """其它设备"""

    sub_asset_type_choice = (
        (0, '打印机'),
        (1, '网络存储器'),
        (2, '磁盘阵列'),
        (3, '其它'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    oth_sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="设备类型")
    oth_model = models.CharField(max_length=128, default='未知型号', verbose_name='设备型号')
    oth_version = models.CharField(max_length=64, default='未知版本', verbose_name='软件版本')
    oth_department = models.CharField(max_length=64, null=True, blank=True, verbose_name="运维部门")
    oth_department_per = models.CharField(max_length=64, null=True, blank=True, verbose_name="设备负责人")
    oth_phone = models.CharField(max_length=64, null=True, blank=True, verbose_name="联系电话")
    oth_mail = models.EmailField(null=True, blank=True, verbose_name="联系邮箱")
    oth_memo = models.CharField('备注', max_length=64, blank=True, null=True)
    def __str__(self):
        return self.asset.name + "--" + self.get_oth_sub_asset_type_display() + str(self.oth_model) + " id:%s" % self.id

    class Meta:
        verbose_name = '04-其它设备'
        verbose_name_plural = verbose_name


# class Software(models.Model):
#     """
#     只保存付费购买的软件
#     """
#     sub_asset_type_choice = (
#         (0, '操作系统'),
#         (1, '办公\开发软件'),
#         (2, '业务软件'),
#     )
#     # 对于软件，它没有物理形体，因此无须关联一个资产对象；
#     sof_sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="软件类型")
#     sof_license_num = models.IntegerField(default=1, verbose_name="授权数量")
#     sof_version = models.CharField(max_length=64, help_text='例如: RedHat release 7 (Final)',
#                                verbose_name='软件/系统版本')
#
#     def __str__(self):
#         return '%s--%s' % (self.get_sof_sub_asset_type_display(), self.sof_version)
#
#     class Meta:
#         verbose_name = '05-软件/系统'
#         verbose_name_plural = verbose_name


class BusinessUnit(models.Model):
    """业务线"""

    bus_parent_unit = models.ForeignKey('self', blank=True, null=True, related_name='parent_level',
                                    on_delete=models.SET_NULL)
    bus_name = models.CharField('业务线', max_length=64)
    bus_department_per = models.CharField(max_length=64, null=True, blank=True, verbose_name="业务负责人")
    bus_phone = models.CharField(max_length=64, null=True, blank=True, verbose_name="联系电话")
    bus_mail = models.EmailField(null=True, blank=True, verbose_name="联系邮箱")
    bus_memo = models.CharField('备注', max_length=64, blank=True, null=True)

    def __str__(self):
        return self.bus_name

    class Meta:
        verbose_name = '09-业务线'
        verbose_name_plural = verbose_name


class IDC(models.Model):
    """机房"""
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    idc_name = models.CharField(max_length=64, verbose_name="机房名称")
    idc_link = models.CharField(max_length=64, blank=True, verbose_name="链路信息")
    idc_cab = models.CharField(max_length=64, blank=True, verbose_name="机柜名称")
    idc_num = models.CharField(max_length=64, blank=True, verbose_name="编号信息")
    idc_memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.asset.name + ":   " + self.idc_name

    class Meta:
        verbose_name = '06-机房'
        verbose_name_plural = verbose_name


class Services(models.Model):
    """服务组件"""

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    serv_ser = models.CharField('服务', max_length=64, blank=True, null=True)
    serv_port = models.CharField('开放端口', max_length=128, blank=True, null=True)
    serv_visit = models.CharField('访问方式', max_length=64, blank=True, null=True)
    serv_memo = models.CharField('备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.asset.name + ":   " + self.serv_ser

    class Meta:
        verbose_name = '06-Services'
        verbose_name_plural = verbose_name


class Database(models.Model):
    """数据库组件"""

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    data_model = models.CharField('数据库类型', max_length=128, blank=True, null=True)
    data_version = models.CharField('数据库版本', max_length=64, blank=True, null=True)
    data_department_per = models.CharField(max_length=64, null=True, blank=True, verbose_name="数据库负责人")
    data_phone = models.CharField(max_length=64, null=True, blank=True, verbose_name="联系电话")
    data_mail = models.EmailField(null=True, blank=True, verbose_name="联系邮箱")
    data_memo = models.CharField('备注', max_length=64, blank=True, null=True)

    def __str__(self):
        return self.asset.name + ":   " + self.data_model

    class Meta:
        verbose_name = '07-Database'
        verbose_name_plural = verbose_name


class Middleware(models.Model):
    """中间件组件"""

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    mid_model = models.CharField('中间件类型', max_length=128, blank=True, null=True)
    mid_version = models.CharField('中间件版本', max_length=64, blank=True, null=True)
    mid_department_per = models.CharField(max_length=64, null=True, blank=True, verbose_name="中间件负责人")
    mid_phone = models.CharField(max_length=64, null=True, blank=True, verbose_name="联系电话")
    mid_mail = models.EmailField(null=True, blank=True, verbose_name="联系邮箱")
    mid_memo = models.CharField('备注', max_length=64, blank=True, null=True)
    def __str__(self):
        return self.asset.name + ":   " + self.mid_model

    class Meta:
        verbose_name = '08-Middleware'
        verbose_name_plural = verbose_name


class Manufacturer(models.Model):
    """服务商"""

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    man_name = models.CharField('服务商名称', max_length=64, null=True, blank=True)
    man_frame = models.CharField('开发框架', max_length=64, null=True, blank=True)
    man_language = models.CharField('开发语言', max_length=64, null=True, blank=True)
    man_version = models.CharField('版本信息', max_length=64, null=True, blank=True)
    man_department = models.CharField('负责部门', max_length=64, null=True, blank=True)
    man_department_per = models.CharField(max_length=64, null=True, blank=True, verbose_name="服务商负责人")
    man_phone = models.CharField(max_length=64, null=True, blank=True, verbose_name="联系电话")
    man_mail = models.EmailField(null=True, blank=True, verbose_name="联系邮箱")
    man_status = models.EmailField(null=True, blank=True, verbose_name="维保状态")
    man_stime = models.DateField(null=True, blank=True, verbose_name="开始时间")
    man_etime = models.DateField(null=True, blank=True, verbose_name="结束时间")
    man_memo = models.CharField('备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.asset.name + ":   " + self.man_name

    class Meta:
        verbose_name = '10-服务商'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """标签"""
    name = models.CharField('标签名', default='N/A', max_length=32, unique=True)
    c_day = models.DateField('创建日期', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class EventLog(models.Model):
    """
    日志.
    在关联对象被删除的时候，不能一并删除，需保留日志。
    因此，on_delete=models.SET_NULL
    """

    event_type_choice = (
        (0, '其它'),
        (1, '硬件变更'),
        (2, '新增配件'),
        (3, '设备下线'),
        (4, '设备上线'),
        (5, '定期维护'),
        (6, '业务上线\更新\变更'),
    )

    asset = models.ForeignKey('Asset', blank=True, null=True, on_delete=models.SET_NULL)  # 当资产审批成功时有这项数据
    log_name = models.CharField('事件名称', max_length=128)
    log_new_asset = models.ForeignKey('NewAssetApprovalZone', blank=True, null=True, on_delete=models.SET_NULL)
    log_event_type = models.SmallIntegerField('事件类型', choices=event_type_choice, default=4)
    log_component = models.CharField('事件子项', max_length=256, blank=True, null=True)
    log_detail = models.TextField('事件详情')
    log_date = models.DateTimeField('事件时间', auto_now_add=True)
    log_user = models.ForeignKey(User, blank=True, null=True, verbose_name='事件执行人', on_delete=models.SET_NULL)
    log_memo = models.TextField('备注', blank=True, null=True)

    def __str__(self):
        return self.log_name

    class Meta:
        verbose_name = '事件纪录'
        verbose_name_plural = verbose_name


class NewAssetApprovalZone(models.Model):
    """新资产待审批区"""
    asset_type_choice = (
        ('server', '服务器'),
        ('securitydevice', '安全设备'),
        ('networkdevice', '网络设备'),
        ('otherdevice', '其它设备'),
        # ('software', '软件资产'),
    )

    sub_asset_type_choice = (
        (0, '物理服务器'),
        (1, '虚拟机'),
        (2, '其它设备'),
    )

    sec_sub_asset_type_choice = (
        (0, '防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'),
        (4, '运维审计系统'),
        (5, '其它设备'),
    )

    asset_status = (
        (0, '在线'),
        (1, '下线'),
        (2, '未知'),
        (3, '故障'),
        (4, '备用'),
    )

    level_status = (
        (5, '非常高'),
        (4, '高'),
        (3, '中'),
        (2, '低'),
        (1, '可忽略'),
    )
    aud_approved = models.BooleanField('是否批准', default=True)
    aud_sn = models.CharField(max_length=128, unique=True, verbose_name="资产序列号")  # 不可重复
    aud_asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='server', verbose_name="资产类型")
    aud_name = models.CharField(max_length=64, default="未知", verbose_name="资产名称")  # 不可重复
    aud_manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP')
    aud_in_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='内网IP')  # Michael
    aud_out_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='公网IP')  # Michael
    aud_visit_url = models.CharField(max_length=64, null=True, blank=True, verbose_name='域名/URL')  # Michael
    aud_url_status = models.CharField(max_length=64, null=True, blank=True, verbose_name='域名状态')  # Michael
    # business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True, verbose_name='所属业务线',
    #                                   on_delete=models.SET_NULL)
    aud_business_style = models.CharField(max_length=64, null=True, blank=True, verbose_name="业务类型")
    aud_contract = models.CharField(max_length=64, null=True, blank=True, verbose_name='业务部门')
    # contract = models.ForeignKey('Contract', null=True, blank=True, verbose_name='业务部门', on_delete=models.SET_NULL)
    aud_department_per = models.CharField(max_length=64, null=True, blank=True, verbose_name="总负责人")
    aud_phone = models.CharField(max_length=64, null=True, blank=True, verbose_name="总负责人-电话")
    aud_mail = models.EmailField(null=True, blank=True, verbose_name="总负责人-邮箱")
    # idc = models.ForeignKey('IDC', null=True, blank=True, verbose_name='所在机房', on_delete=models.SET_NULL)
    aud_regional = models.CharField(max_length=64, null=True, blank=True, verbose_name="部署区域")
    aud_deployment = models.CharField(max_length=64, null=True, blank=True, verbose_name="部署方式")
    aud_status = models.SmallIntegerField(choices=asset_status, default=0, verbose_name='资产状态')
    aud_tags = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    aud_le_status = models.SmallIntegerField(choices=level_status, default=5, verbose_name='重要程度')
    aud_memo = models.TextField(null=True, blank=True, verbose_name='备注')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='录入日期')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')
    data = models.TextField('资产数据')    # 此字段必填

    ser_sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="服务器类型")
    ser_os_type = models.CharField('操作系统类型', max_length=64, blank=True, null=True)
    ser_os_release = models.CharField('操作系统版本', max_length=64, blank=True, null=True)
    ser_model = models.CharField(max_length=128, null=True, blank=True, verbose_name='内核信息')
    ser_department_per = models.CharField(max_length=64, null=True, blank=True, verbose_name="系统负责人")
    ser_phone = models.CharField(max_length=64, null=True, blank=True, verbose_name="系统负责人-电话")
    ser_mail = models.EmailField(null=True, blank=True, verbose_name="系统负责人-邮箱")
    ser_memo = models.CharField('服务器备注', max_length=64, blank=True, null=True)

    idc_name = models.CharField(max_length=64, default='未知', verbose_name="机房名称")
    idc_link = models.CharField(max_length=64, blank=True, verbose_name="链路信息")
    idc_cab = models.CharField(max_length=64, blank=True, verbose_name="机柜名称")
    idc_num = models.CharField(max_length=64, blank=True, verbose_name="编号信息")
    idc_memo = models.CharField('机房备注', max_length=64, blank=True, null=True)

    serv_ser = models.CharField('服务', max_length=64, blank=True, null=True)
    serv_port = models.CharField('开放端口', max_length=128, blank=True, null=True)
    serv_visit = models.CharField('访问方式', max_length=64, blank=True, null=True)
    serv_memo = models.CharField('服务备注', max_length=128, blank=True, null=True)

    data_model = models.CharField('数据库类型', max_length=128, blank=True, null=True)
    data_version = models.CharField('数据库版本', max_length=64, blank=True, null=True)
    data_department_per = models.CharField(max_length=64, null=True, blank=True, verbose_name="数据库负责人")
    data_phone = models.CharField(max_length=64, null=True, blank=True, verbose_name="联系电话")
    data_mail = models.EmailField(null=True, blank=True, verbose_name="联系邮箱")
    data_memo = models.CharField('数据库备注', max_length=64, blank=True, null=True)

    mid_model = models.CharField('中间件类型', max_length=128, blank=True, null=True)
    mid_version = models.CharField('中间件版本', max_length=64, blank=True, null=True)
    mid_department_per = models.CharField(max_length=64, null=True, blank=True, verbose_name="中间件负责人")
    mid_phone = models.CharField(max_length=64, null=True, blank=True, verbose_name="联系电话")
    mid_mail = models.EmailField(null=True, blank=True, verbose_name="联系邮箱")
    mid_memo = models.CharField('中间件备注', max_length=64, blank=True, null=True)

    man_name = models.CharField('服务商名称', max_length=64, null=True, blank=True)
    man_frame = models.CharField('开发框架', max_length=64, null=True, blank=True)
    man_language = models.CharField('开发语言', max_length=64, null=True, blank=True)
    man_version = models.CharField('版本信息', max_length=64, null=True, blank=True)
    man_department = models.CharField('负责部门', max_length=64, null=True, blank=True)
    man_department_per = models.CharField(max_length=64, null=True, blank=True, verbose_name="服务商负责人")
    man_phone = models.CharField(max_length=64, null=True, blank=True, verbose_name="联系电话")
    man_mail = models.EmailField(null=True, blank=True, verbose_name="联系邮箱")
    man_status = models.EmailField(null=True, blank=True, verbose_name="维保状态")
    man_stime = models.DateField(null=True, blank=True, verbose_name="开始时间")
    man_etime = models.DateField(null=True, blank=True, verbose_name="结束时间")
    man_memo = models.CharField('服务商备注', max_length=128, blank=True, null=True)

    sec_sub_asset_type = models.SmallIntegerField(choices=sec_sub_asset_type_choice, default=0, verbose_name="安全设备类型")
    sec_model = models.CharField(max_length=128, default='未知型号', verbose_name='设备型号')
    sec_version = models.CharField(max_length=64, default='未知版本', verbose_name='软件版本')
    sec_department = models.CharField(max_length=64, null=True, blank=True, verbose_name="运维部门")
    sec_department_per = models.CharField(max_length=64, null=True, blank=True, verbose_name="运维负责人")
    sec_phone = models.CharField(max_length=64, null=True, blank=True, verbose_name="联系电话")
    sec_mail = models.EmailField(null=True, blank=True, verbose_name="联系邮箱")
    sec_memo = models.CharField('安全设备备注', max_length=64, blank=True, null=True)

    def __str__(self):
        return self.aud_sn

    class Meta:
        verbose_name = '99-待审批资产'
        verbose_name_plural = verbose_name
        ordering = ['-c_time']
