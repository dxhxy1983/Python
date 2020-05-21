import snap7
import time
def mk(client):
    area = snap7.snap7types.areas.PA
    dbnumber = 0
    amount = 1
    start = 0
    mk_data = client.read_area(area, dbnumber, start, amount)
    mk_data[0]=0b1
    client.write_area(area, dbnumber, start, mk_data)
    for i in range(5):
        
        client.write_area(area,dbnumber,start,mk_data)
        print(bin(mk_data[0]))
        mk_data[0]=mk_data[0]*2
        time.sleep(2)


    # mk_data = client.read_area(area, dbnumber, start, amount)
    print(bin(mk_data[0]))
    mk_data[0]=0b0
    print(u'复位')
    client.write_area(area, dbnumber, start, mk_data)



def plc_connect(ip, rack=0, slot=1):
    client = snap7.client.Client()
    client.connect(ip, rack, slot)
    return client  

def plc_con_close(client):
    client.disconnect()

if __name__ == "__main__":
    client_fd = plc_connect('192.168.0.2')
    mk(client_fd)
    plc_con_close(client_fd)
