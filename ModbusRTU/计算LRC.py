def calculate_lrc(data):
    """
    Calculate the Longitudinal Redundancy Check (LRC) of a given byte string.

    Args:
        data (bytes): The byte string to calculate LRC for.

    Returns:
        int: The LRC value.
    """
    # lrc = 0
    # for byte in data:
    #     lrc ^= byte   # XOR each byte with lrc
    # lrc ^= 0xFF      # Invert all bits
    # lrc += 1         # Add 1
    # lrc &= 0xFF      # Modulo 256
    # return lrc
    lrc=0
    for i in range(len(data)):
        lrc=lrc+int(data[i])
    lrc=lrc
    lrc=~lrc+1
    lrc=lrc.to_bytes(1, byteorder='little',signed=True)
    # print(hex(lrc))
    return (lrc)

if __name__ == "__main__":
    # data = b'0x3a0x300x310x300x330x300x300x300x310x300x300x300x36'

    address=1
    
    
    for i in range(0,25):
        data = [3,1,6]
        address=address+1
        data.insert(0, address)
        # for j in range(len(data)):
        #     data[j]=data[j].to_bytes(1,byteorder="little")
        lrc = calculate_lrc(data)
        data.append(lrc)
    # print(hex(lrc))   # Output: 0x54
        for i in range(len(data)):
            data[i]=bin(data[i])
        print(data)
    # data[0]=hex(data[0])
    # for i in range(0,50):
        
    #     data[0]=hex(data[0])+0x1
        
    #     print(data) 
