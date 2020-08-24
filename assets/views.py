from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json
from assets import models
from assets import asset_handler
from django.shortcuts import get_object_or_404


def index(request):
    """
    资产总表视图
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if "index/server" in request.path:
        assets = models.Asset.objects.filter(asset_type="server")
    elif "index/security" in request.path:
        assets = models.Asset.objects.filter(asset_type="securitydevice")
    elif "index/network" in request.path:
        assets = models.Asset.objects.filter(asset_type="networkdevice")
    elif "index/other" in request.path:
        assets = models.Asset.objects.filter(asset_type="otherdevice")
    else:
        assets = models.Asset.objects.all()
    return render(request, 'assets/index.html', locals())

#
# def indexserver(request):
#     if not request.session.get('is_login', None):
#         return redirect('/login/')
#     # assets = models.Asset.objects.all()
#     assets = models.Asset.objects.filter(asset_type="server")
#     return render(request, 'assets/indexserver.html', locals())
#
#
# def indexsafety(request):
#     if not request.session.get('is_login', None):
#         return redirect('/login/')
#     # assets = models.Asset.objects.all()
#     assets = models.Asset.objects.filter(asset_type="securitydevice")
#     return render(request, 'assets/indexsafety.html', locals())


# def index(request):
#     pass
#     return render(request, 'assets/index.html')

def dashboard(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    total = models.Asset.objects.count()
    upline = models.Asset.objects.filter(status=0).count()
    offline = models.Asset.objects.filter(status=1).count()
    unknown = models.Asset.objects.filter(status=2).count()
    breakdown = models.Asset.objects.filter(status=3).count()
    backup = models.Asset.objects.filter(status=4).count()

    up_rate = round(upline/total*100)
    o_rate = round(offline / total * 100)
    un_rate = round(unknown / total * 100)
    bd_rate = round(breakdown / total * 100)
    bu_rate = round(backup / total * 100)

    server_number = models.Server.objects.count()
    securitydevice_number = models.SecurityDevice.objects.count()
    networkdevice_number = models.NetworkDevice.objects.count()
    otherdevice_number = models.OtherDevice.objects.count()
    # software_number = models.Software.objects.count()

    return render(request, 'assets/dashboard.html', locals())


def detail(request, asset_id):
    """
    以显示服务器类型资产详细为例，安全设备、存储设备、网络设备等参照此例。
    :param request:
    :param asset_id:
    :return:
    """
    if not request.session.get('is_login', None):
        return redirect('/login/')
    asset = get_object_or_404(models.Asset, id=asset_id)
    if asset.asset_type == "securitydevice":
        return render(request, 'assets/detail_safety.html', locals())
    elif asset.asset_type == "networkdevice":
        return render(request, 'assets/detail_network.html', locals())
    elif asset.asset_type == "otherdevice":
        return render(request, 'assets/detail_other.html', locals())
    else:
        return render(request, 'assets/detail.html', locals())


@csrf_exempt
def report(request):
    if request.method == 'POST':
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)
        if not data:
            return HttpResponse('没有数据！')
        if not issubclass(dict, type(data)):
            return HttpResponse('数据必须为字典格式！')
        # 你的检测代码

        aud_sn = data.get('aud_sn', None)
        aud_asset_type = data.get('aud_asset_type', None)

        if aud_sn:
            asset_obj = models.Asset.objects.filter(sn=aud_sn)  # [obj]
            # print("++++++++++++")
            if asset_obj:
                update_asset = asset_handler.UpdateAsset(request, asset_obj[0], data)
                return HttpResponse('资产数据已经更新。')
            else:
                # print("------------")
                obj = asset_handler.NewAsset(request, data)
                res = obj.add_to_new_assets_zone()
                if aud_asset_type == "server":
                    response = obj.add_to_new_assets_zone_server()
                elif aud_asset_type == "securitydevice":
                    response = obj.add_to_new_assets_zone_securitydevice()
                else:
                    response = "N--------------N"
                return HttpResponse(response)
        else:
            return HttpResponse('没有资产sn，请检查数据内容！')

    return HttpResponse('200 ok')
