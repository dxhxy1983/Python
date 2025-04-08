def crc16_x25(data):
    """
    此函数用于计算给定数据的 CRC - 16/X25 校验值。
    :param data: 待计算 CRC 的字节数据
    :return: 计算得到的 CRC - 16/X25 校验值
    """
    crc = 0xFFFF
    polynomial = 0x8408# 0x1021
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ polynomial
            else:
                crc >>= 1
    crc ^= 0xFFFF
    # return ((crc & 0xFF) << 8) | ((crc >> 8) & 0xFF)# 小端
    return crc# 大端

# 示例用法
if __name__ == "__main__":
    input_str = "RRS"
    ascii_data = input_str.encode('ascii')
    result = crc16_x25(ascii_data)
    print(f"CRC - 16/X25 结果: {result:04X}")