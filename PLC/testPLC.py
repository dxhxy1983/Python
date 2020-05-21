import struct
import time
import snap7

def plc_connect(ip, rack=0, slot=1):
    client = snap7.client.Client()

    client.connect(ip, rack, slot)

    return client


# """

# 连接初始化

# :param ip:

# :param rack: 通常为0

# :param slot: 根据plc安装，一般为0或1

# :return:

# """
    

def plc_con_close(client):
    client.disconnect()

# """

# 连接关闭

# :param client:

# :return:

# """



def test_mk10_1(client):
    area = snap7.snap7types.areas.DB
    dbnumber = 3
    amount = 1
    start = 0
    print(u'初始值')
    mk_data = client.read_area(area, dbnumber, start, 4)
    print(mk_data)
    # print(struct.unpack('!h', mk_data))
    print(u'置1')
    client.write_area(area, dbnumber, 3, struct.pack('b',15))
   
    print(u'当前值')
    mk_cur = client.read_area(area, dbnumber, start, 4)
    print(mk_cur)
    # print(struct.unpack('!h', mk_cur))
    # """

# 测试M10.1

# :return:

# """



def test_mk_w201(client):
    area = snap7.snap7types.areas.MK
    dbnumber = 0
    amount = 2
    start = 201
    print(u'初始值')
    mk_data = client.read_area(area, dbnumber, start, amount)
    print(struct.unpack('!h', mk_data))
    print(u'置12')
    client.write_area(area, dbnumber, start, b'')
    print(u'当前值')
    mk_cur = client.read_area(area, dbnumber, start, amount)
    print(struct.unpack('!h', mk_cur))
    time.sleep(3)
    print(u'置3')
    client.write_area(area, dbnumber, start, b'')
    print(u'当前值')
    mk_cur = client.read_area(area, dbnumber, start, amount)
    print(struct.unpack('!h', mk_cur))

# """

# 测试MW201,数据类型为word

# :param client:

# :return:

# """



if __name__ == "__main__":
    client_fd = plc_connect('192.168.0.2')
    test_mk10_1(client_fd)
    # test_mk10_1(client_fd)
    plc_con_close(client_fd)
