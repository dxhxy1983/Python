int i,j;
int crc16;
int temp;

crc16=0xFFFF;
for ( i = 0; i < sizeOfDim(buf,0); i++)
{
    crc16^=buf[i];
    for (j = 0; j<8; j++)
    {
        temp=crc16&&0x0001;
        crc16>>=0x01;
        if (temp) crc16^=0xA001;
             
    }   
}