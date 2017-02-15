data ="""
ab.ymatou.com.conf                  api.riskcontrol.ymatou.com.conf  im.app.ymatou.com.conf            ordersync.iapi.ymatou.com.conf           somaster.ymatou.com.conf
activity.app.ymatou.com.conf        api.seller.ymatou.com.conf       jk2.img.ymatou.com.conf           p4.img.ymatou.com.conf                   soslave.ymatou.com.conf
admin.messageroute.ymatou.com.conf  api.smsproxy.ymatou.com.conf     jk3.img.ymatou.com.conf           p5.img.ymatou.com.conf                   static.jyh.ymatou.com.conf
admin.timedtask.ymatou.cn.conf      api.social.ymatou.com.conf       jk4.img.ymatou.com.conf           paymentproxy.ymatou.com.conf             staticseller.ymatou.com.conf
api.accounting.i.ymatou.com.conf    app.ymatou.com.conf              jsapi.app.ymatou.com.conf         payproxy.xlobo.com.conf                  suggestbizer.ymatou.com.conf
api.appactivity.ymatou.com.conf     auth.open.xlobo.com.conf         jsapi.bf.ymatou.com.conf          payproxy.ymatou.com.conf                 suggestindexer.ymatou.com.conf
api.csim.i.ymatou.com.conf          bill.open.xlobo.com.conf         jsapi.sellerinfo.ymatou.com.conf  proymtlog.ymatou.cn.conf                 trade.app.ymatou.com.conf
api.cs.ymatou.com.conf              cat.iapi.ymatou.com.conf         jyh.ymatou.com.conf               proymtlog.ymatou.com.conf                traffic.app.ymatou.com.conf
api.event.push.ymatou.com.conf      comment.iapi.ymatou.com.conf     keyword.app.iapi.ymatou.com.conf  push2.iapi.ymatou.com.conf               user.app.ymatou.com.conf
api.evt.push.ymatou.com.conf        deliveryservice.ymatou.com.conf  list.promotion.ymatou.com.conf    rec.app.ymatou.com.conf                  userregister.ymatou.com.conf
api.img.ymatou.com.conf             disconfadmin.ymatou.cn.conf      livemanage.iapi.ymatou.com.conf   relation.app.ymatou.com.conf             webapi.app.ymatou.com.conf
api.im.ymatou.com.conf              disconf.iapi.ymatou.com.conf     liveproduct.iapi.ymatou.com.conf  seller.app.ymatou.com.conf               wms.xlobo.com.conf
api.messageroute.ymatou.com.conf    eventpush2.iapi.ymatou.com.conf  livequery.iapi.ymatou.com.conf    sellerorderbizer.iapi.ymatou.com.conf    www.ymatou.com.conf
api.mission.ymatou.com.conf         favorite.app.ymatou.com.conf     open.xlobo.com.conf               sellerorderindexer.iapi.ymatou.com.conf  ymtlog.ymatou.cn.conf
api.productitem.ymatou.com.conf     fp.ymatou.com.conf               op.trading.ymatou.cn.conf         sellerservice.ymatou.com.conf            ymtlog.ymatou.com.conf
api.push.ymatou.com.conf            im2.iapi.ymatou.com.conf         op.trading.ymatou.com.conf        seller.ymatou.com.conf

"""
dd = data.split()
sorted(dd)
for d in dd:
    print d.strip('.conf')