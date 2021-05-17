from django.shortcuts import render
from alipay import AliPay
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from DjangoV2Demo.settings import ALIPAY_APPID, APP_PRIVATE_KEY_PATH, ALIPAY_PUBLIC_KEY_PATH, ALIPAY_URL, ALIPAY_DEBUG
from demo.models import Order


def index(request):
    return render(request, 'index.html')


class AliPayView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        支付宝同步回调return_url
        方法：GET
        回调数据中不包含trade_status（订单状态）故不能作为最终付款成功的依据
        同步回调地址可展示成功后--想展示给用户的页面如首页（——index.html）
        异步回调地址需要内网穿透
        :param request:
        :return:
        """
        user = request.user
        data_dict = request.query_params.dict()
        o_sn = data_dict.pop('o_sn')

        # 1. 根据order_id, 验证订单对象是否存在
        try:
            order = Order.objects.get(order_sn=o_sn, user=user, pay_status='PAYING')
        except Order.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 2. 创建alipay对象, 生成order_string,拼接alipay的url
        app_private_key_string = open("apps/demo/keys/private_2048.txt").read()
        alipay_public_key_string = open("apps/demo/keys/ali_pay_key_2048.txt").read()

        ali_pay = AliPay(
            appid=ALIPAY_APPID,
            app_notify_url='http://127.0.0.1:8001/order/pay/',  # 默认回调url
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True,  # 默认False
        )

        subject = "测试订单"

        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = ali_pay.api_alipay_trade_page_pay(
            out_trade_no=o_sn,  # o_sn
            total_amount=str(order.order_mount),  # 订单总金额,需要转换成str类型,因为JSON不支持Decimal货币类型
            subject=subject,
            return_url='http://127.0.0.1:8001/index/',  # 成功回调地址
            notify_url="44028973accb.ngrok.io/order/pay/"  # 异步回调地址，需要内网穿透，不然接收不到通知
        )
        # 拼接url
        ali_pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
        print(ali_pay_url)
        return Response({'ali_pay_url': ali_pay_url})

    def post(self, request):
        """
        处理异步回调notify_url
        返回数据中支付状态为"TRADE_SUCCESS"或"TRADE_FINISHED"即为成功，此时修改订单状态及商品数据信息等
        :return:
        """
        data_dict = {}
        for key, value in request.POST.items():
            data_dict[key] = value

        app_private_key_string = open("apps/demo/keys/private_2048.txt").read()
        alipay_public_key_string = open("apps/demo/keys/ali_pay_key_2048.txt").read()

        ali_pay = AliPay(
            appid=ALIPAY_APPID,
            app_notify_url='http://127.0.0.1:8001/order/pay/',  # 默认回调url
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True,  # 默认False
        )

        signature = data_dict.pop("sign", None)
        success = ali_pay.verify(data_dict, signature)

        if success and data_dict["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            order_sn = data_dict.get('out_trade_no', None)  # 商户订单号
            trade_no = data_dict.get('trade_no', None)  # 交易编号
            trade_status = data_dict.get('trade_status', None)  # 订单状态
            pay_time = data_dict.get('gmt_payment', None)  # 支付时间
            # 如果支付成功,保存支付编号&订单号到数据表,修改订单的支付状态
            Order.objects.filter(order_sn=order_sn).update(pay_status=trade_status, trade_no=trade_no,
                                                           pay_time=pay_time)
            return Response({'trade_no': trade_no}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '订单支付失败'}, status=status.HTTP_400_BAD_REQUEST)
