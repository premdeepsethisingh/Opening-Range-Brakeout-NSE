import logging
from kiteconnect import KiteTicker
from kiteconnect import KiteConnect
import datetime
import pdb
import math


api_key=''
api_secret=''
access_token=''


logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)
kws = KiteTicker(api_key,access_token)

lots = 0.2
mode = 1
bias = 0
offsetMultiplier = 1


name = [ 'AXISBANK','APOLLOTYRE','ASHOKLEY','BAJAJFINSV',
         'BAJFINANCE','BANKBARODA','CHOLAFIN','FEDERALBNK',
         'GRANULES','INDHOTEL','INDUSINDBK','MRPL',
         'NAUKRI','PRESTIGE','PVR','RBLBANK',
         'RELIANCE','SRTRANSFIN','TRENT','WOCKPHARMA' ]

Inst_token = [ 1510401,41729,54273,4268801,
               81153,1195009,175361,261889,
               3039233,387073,1346049,584449,
               3520257,5197313,3365633,4708097,
               738561,1102337,502785,1921537 ]

stocks={ 1510401:{'high':1,'low':1},41729:{'high':1,'low':1},
         54273:{'high':1,'low':1},4268801:{'high':1,'low':1},
         81153:{'high':1,'low':1},  1195009:{'high':1,'low':1},
         175361:{'high':1,'low':1},261889:{'high':1,'low':1},
         3039233:{'high':1,'low':1},387073:{'high':1,'low':1},
         1346049:{'high':1,'low':1},584449:{'high':1,'low':1},
         3520257:{'high':1,'low':1},5197313:{'high':1,'low':1},
         3365633:{'high':1,'low':1},4708097:{'high':1,'low':1},
         738561:{'high':1,'low':1},1102337:{'high':1,'low':1},
         502785:{'high':1,'low':1},1921537:{'high':1,'low':1} }

qty = [ 47,148,289,3,
        6,448,65,421,
        104,286,33,875,
        7,121,25,147,
        16,27,41,73 ]

mask = [ 1,1,1,1,
         1,1,1,1,
         1,1,1,1,
         1,1,1,1,
         1,1,1,1 ]

offset = [  1,0.2,0.2,5,
            2,0.1,0.5,0.1,
            0.3,0.1,2,0.05,
            2,0.2,1,0.2,
            1,1,1,0.5]






def on_ticks(ws, ticks):
    flag = 0
    global stocks
    global name
    global lots
    global qty
    global mask
    global offset
    global Inst_token
    
    for single_company in ticks:    
        inst_of_single_company = single_company['instrument_token']
        high= single_company['ohlc']['high']
        low= single_company['ohlc']['low']
        stocks[inst_of_single_company]['high']= high
        stocks[inst_of_single_company]['low'] = low
        if(datetime.datetime.now().time().hour==9 and datetime.datetime.now().time().minute==45 and flag==0):
                if(bias==1):
                    for i in range(len(name)):
                            kite.place_order(
                                 tradingsymbol = name[i],
                                 variety = kite.VARIETY_REGULAR,
                                 exchange = kite.EXCHANGE_NSE,
                                 transaction_type = kite.TRANSACTION_TYPE_BUY,
                                 quantity = math.floor(qty[i]*mask[i]*lots)+1,
                                 order_type = kite.ORDER_TYPE_SLM,
                                 product = kite.PRODUCT_MIS,
                                 trigger_price = stocks[Inst_token[i]]['high'] + offset[i]
                                 )
                            kite.place_order(
                                 tradingsymbol = name[i],
                                 variety = kite.VARIETY_REGULAR,
                                 exchange = kite.EXCHANGE_NSE,
                                 transaction_type = kite.TRANSACTION_TYPE_BUY,
                                 quantity = math.floor(qty[i]*mask[i]*lots)+1,
                                 order_type = kite.ORDER_TYPE_LIMIT,
                                 product = kite.PRODUCT_MIS,
                                 price = stocks[Inst_token[i]]['low'] - offsetMultiplier*offset[i]
                                 )
                    flag = 1
                    pdb.set_trace()

                elif(bias==-1):
                    for i in range(len(name)):
                            kite.place_order(
                                 tradingsymbol = name[i],
                                 variety = kite.VARIETY_REGULAR,
                                 exchange = kite.EXCHANGE_NSE,
                                 transaction_type = kite.TRANSACTION_TYPE_SELL,
                                 quantity = math.floor(qty[i]*mask[i]*lots)+1,
                                 order_type = kite.ORDER_TYPE_LIMIT,
                                 product = kite.PRODUCT_MIS,
                                 price = stocks[Inst_token[i]]['high'] + offsetMultiplier*offset[i]
                                 )
                            kite.place_order(
                                 tradingsymbol = name[i],
                                 variety = kite.VARIETY_REGULAR,
                                 exchange = kite.EXCHANGE_NSE,
                                 transaction_type = kite.TRANSACTION_TYPE_SELL,
                                 quantity = math.floor(qty[i]*mask[i]*lots)+1,
                                 order_type = kite.ORDER_TYPE_SLM,
                                 product = kite.PRODUCT_MIS,
                                 trigger_price = stocks[Inst_token[i]]['low'] - offset[i]
                                 )
                    flag = 1
                    pdb.set_trace()

                elif(mode==1):
                    for i in range(len(name)):
                            kite.place_order(
                                 tradingsymbol = name[i],
                                 variety = kite.VARIETY_REGULAR,
                                 exchange = kite.EXCHANGE_NSE,
                                 transaction_type = kite.TRANSACTION_TYPE_BUY,
                                 quantity = math.floor(qty[i]*mask[i]*lots)+1,
                                 order_type = kite.ORDER_TYPE_SLM,
                                 product = kite.PRODUCT_MIS,
                                 trigger_price = stocks[Inst_token[i]]['high'] + offset[i]
                                 )
                            kite.place_order(
                                 tradingsymbol = name[i],
                                 variety = kite.VARIETY_REGULAR,
                                 exchange = kite.EXCHANGE_NSE,
                                 transaction_type = kite.TRANSACTION_TYPE_SELL,
                                 quantity = math.floor(qty[i]*mask[i]*lots)+1,
                                 order_type = kite.ORDER_TYPE_SLM,
                                 product = kite.PRODUCT_MIS,
                                 trigger_price = stocks[Inst_token[i]]['low'] - offset[i]
                                 )
                    flag = 1
                    pdb.set_trace()

                elif(mode==-1):
                    for i in range(len(name)):
                            kite.place_order(
                                 tradingsymbol = name[i],
                                 variety = kite.VARIETY_REGULAR,
                                 exchange = kite.EXCHANGE_NSE,
                                 transaction_type = kite.TRANSACTION_TYPE_SELL,
                                 quantity = math.floor(qty[i]*mask[i]*lots)+1,
                                 order_type = kite.ORDER_TYPE_LIMIT,
                                 product = kite.PRODUCT_MIS,
                                 price = stocks[Inst_token[i]]['high'] + offsetMultiplier*offset[i]
                                 )
                            kite.place_order(
                                 tradingsymbol = name[i],
                                 variety = kite.VARIETY_REGULAR,
                                 exchange = kite.EXCHANGE_NSE,
                                 transaction_type = kite.TRANSACTION_TYPE_BUY,
                                 quantity = math.floor(qty[i]*mask[i]*lots)+1,
                                 order_type = kite.ORDER_TYPE_LIMIT,
                                 product = kite.PRODUCT_MIS,
                                 price = stocks[Inst_token[i]]['low'] - offsetMultiplier*offset[i]
                                 )
                    flag = 1
                    pdb.set_trace()
                    
            
        

def on_connect(ws, response):
    ws.subscribe(Inst_token)
    ws.set_mode(ws.MODE_QUOTE,Inst_token)





kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.connect()









