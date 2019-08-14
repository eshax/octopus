# !/usr/bin/python
# encoding:utf-8

import requests, json

rdb = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

class sms:

    @staticmethod
    def send(s, f, t, bp, sp, a):
        k = "%s.%s.%s" % (s, f, t)
        if rdb.get(k):
            return
        headers = {
            "Content-Type" : "application/json;charset=utf-8"
        }
        data = {
                   "appid" : "84ce75cc5c0f4920bbb4f9c864f56519",
                     "sid" : "9a802239b6f553f520df3ce22246b5d7",
                   "token" : "cae9415f5bd02c98c6c1986304bfb3c6",
              "templateid" : "493779",
                   "param" : "%s,%s,%s,%f,%f,%.2f" % (s, f, t, bp, sp, a),
                  "mobile" : "18600040475"
        }
        res = requests.post('https://open.ucpaas.com/ol/sms/sendsms', data=json.dumps(data), headers=headers)
        print(res.text)
        rdb.set(k, 1)
        rdb.expire(k, 60 * 60 * 24)

if __name__ == '__main__':
    sms.send("swtc/cnyt", "weidex", "coinw", 0.00512, 0.0053, 195000.00)
