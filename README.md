Automated Cryptocurrency Trading
=============

目录说明
-------------

```
.
├── config.py       配置文件
├── cron            定时任务脚本
│   └── otc.py      定时获取usdt, eth, btc, swtc, cnyt对人民币的充值和提现价格
├── engine          交易算法
│   ├── cebt.py     跨站双边
│   ├── cett.py     跨站三角（未实现）
│   ├── sebt.py     单站双边
│   ├── segt.py     单站网格或去头皮（未实现）
│   └── sett.py     单站三角
├── exchange        交易所SDK
│   ├── bitz.py     BITZ（未实现提币，撤单）
│   ├── coinbene.py 满币（未实现提币，撤单）
│   ├── coinw.py    币赢（未实现提币，撤单）
│   ├── huobi.py    火币（未实现提币，撤单）
│   └── weidex.py   威链（未实现提币，撤单）
├── README.md       说明
├── scanning.py     扫描各个交易所币对的深度，然后存入redis
├── tools           工具脚本
└── utils           工具类
    ├── db.py       对数据库类操作的封装Redis, Mysql
    ├── ex.py       对交易所的操作的封装
    ├── md5.py      MD5
    └── sku.py      对币的买卖操作再次封装，便于记录库存货币的成本
```