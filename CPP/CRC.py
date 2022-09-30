def crc16_cal(data):
    if data==0x00:
        return 0x0000
    test_crc=0xFFFF                 #预置1个16位的寄存器为十六进制FFFF（即全为1），称此寄存器为CRC寄存器；
    poly=0xa001
    # poly=0x8005
    while(1):
        test_crc=(data&0xFF)^test_crc   #把第一个8位二进制数据（既通讯信息帧的第一个字节）与16位的CRC寄存器的低8位相异或，把结果放于CRC寄存器，高八位数据不变；
        """
        （3）、把CRC寄存器的内容右移一位（朝低位）用0填补最高位，并检查右移后的移出位；
        （4）、如果移出位为0：重复第3步（再次右移一位）；如果移出位为1，CRC寄存器与多
            项式A001（1010 0000 0000 0001）进行异或；
        """
        #右移动
        for bit in range(8):
            if(test_crc&0x1)!=0:
                test_crc>>=1
                test_crc^=poly
            else:
                test_crc>>=1
        print(hex(test_crc))
        data>>=8
        if data==0x00:
            return test_crc
        print(hex(data))
if ( __name__ == '__main__' ):
    # data=input()
    # data_int=data.encode().hex()
    # crc16_cal(eval(data_int))
    d=0x010601001770
    crc16_cal(0x2D)