//#include "led.h"
#include "delay.h"
#include "key.h"
#include "sys.h"
#include "usart.h"
#include "global.h"
#include "var.h"
#include "time.h"
#include "stmflash.h"
#include "math.h"
#include "lcd.h"


void RebuildParameter_lcd(struct RUNparameter DP[6][6],u16 g,u32 addr1,u32 addr2)
{
	char temp8[250];
	u16 temp16[200],a;
	memcpy(temp8,DP,g);   //
	a=CalcCrc(temp8,g);       //����У��ֵ
	temp8[g]=a&0xFF;
	temp8[g+1]=a>>8;
	memcpy(temp16,temp8,g+2);   //
	//����д��flash
	FLASH_Unlock();						//����
	FLASH_ErasePage(addr1);   //����ҳ����Χ����addr2
	STMFLASH_Write_NoCheck(addr1,temp16,g/2+1);
	STMFLASH_Write_NoCheck(addr2,temp16,g/2+1);
	FLASH_Lock();//����
}

void RebuildParameter(struct DEVICEPARAMETER DP,u32 addr1,u32 addr2)
{
	char temp8[60];
	u16 temp16[30];
	memcpy(temp8,&DP,(sizeof(DP)-2));   //
	DP.Crc16=CalcCrc(temp8,(sizeof(DP)-2));    //����У��ֵ
	memcpy(temp16,&DP,sizeof(DP));   //
	//����д��flash
	FLASH_Unlock();						//����
	FLASH_ErasePage(addr1);   //����ҳ����Χ����addr2
	STMFLASH_Write_NoCheck(addr1,temp16,sizeof(DP)/2);
	STMFLASH_Write_NoCheck(addr2,temp16,sizeof(DP)/2);
	FLASH_Lock();//����
}


 int main(void)
 {
	char x=0;
	u8 DeviceAddress=0x01;
	u16 buflong=sizeof(runparameter);	 
	char BPbuf[255];
	u16  t,test;      
	u32 usartbound1=BOUND1;
	u32 usartbound2=BOUND2;
//	char speed_n=0;     //��ǰ�ٶ��ۼƼ���
//	u16  speed_s=0;     //��ǰ�ٶ��ۼ�ֵ
	char erro_count=0;  //
	u16  startwork=0;  //��ָͣ��
	char S_formula=1;  //��ʾ�䷽���
	u16  erroNO;       //������
	 
	delay_init();	    	 //��ʱ������ʼ��	
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2); //����NVIC�жϷ���2:2λ��ռ���ȼ���2λ��Ӧ���ȼ�

// 	LED_Init();			     //LED�˿ڳ�ʼ��
//	KEY_Init();          //��ʼ���밴�����ӵ�Ӳ���ӿ�
	time_conf();
	DIR1_Init();           //PA.8 ����ͣ���usart1-485���ڽ���״̬
	DIR2_Init();           //PA.1 ����ͣ���usart2-485���ڽ���״̬
	
	
//�����ò���
	DeviceParameter=*(struct DEVICEPARAMETER*)ParameterAddr3;
	memcpy(BPbuf,&DeviceParameter,(sizeof(DeviceParameter)-2));   //
//У��
  t=CalcCrc(BPbuf,(sizeof(DeviceParameter)-2));    //����У��ֵ
	if(t==DeviceParameter.Crc16)
	{
		DeviceAddress=DeviceParameter.Addr;
		usartbound1=DeviceParameter.Bound1;
    usartbound2=DeviceParameter.Bound2;  
	}else
	{
		DeviceParameter=*(struct DEVICEPARAMETER*)ParameterAddr4;
	  memcpy(BPbuf,&DeviceParameter,(sizeof(DeviceParameter)-2));   //
//У��
   t=CalcCrc(BPbuf,(sizeof(DeviceParameter)-2));    //����У��ֵ
	 if(t==DeviceParameter.Crc16)
	  {
		  DeviceAddress=DeviceParameter.Addr;
		  usartbound1=DeviceParameter.Bound1;
			usartbound2=DeviceParameter.Bound2;
//			if(DeviceParameter.Addr>0&&DeviceParameter.Bound1>0&&DeviceParameter.Bound2>0)
      RebuildParameter(DeviceParameter,ParameterAddr3,ParameterAddr4);  //����д��flash
	  }else
		     {
		       usartbound1=BOUND1;
					 usartbound2=BOUND2;
					 DeviceParameter.Addr=DeviceAddress;
					 DeviceParameter.Bound1=BOUND1;
					 DeviceParameter.Bound2=BOUND2; 
					 DeviceParameter.even_odd=0;
					 DeviceParameter.stop_bit=1;
					 DeviceParameter.Crc16=0;
				 }
   }	
	
	 
//��ʼ��ϵͳĬ�ϲ���
   runparameter[0][1].acc=1000;  //���ٶ�
	 runparameter[0][1].speed=1;  //����    1.����   2.Ӣ��
	 runparameter[0][1].time=2;   //������  1.��     2.��

//�����ò���
	memcpy(BPbuf,(char*)ParameterAddr1,(buflong+2));   //
//У��
  t=CalcCrc(BPbuf,buflong);    //����У��ֵ
	if(t==BPbuf[buflong+1]*256+BPbuf[buflong])
	{
		memcpy(runparameter,BPbuf,buflong); 
	}else
	{
	 memcpy(BPbuf,(char*)ParameterAddr2,(buflong+2));  //
//У��
   t=CalcCrc(BPbuf,buflong);    //����У��ֵ
	 if(t==BPbuf[buflong+1]*256+BPbuf[buflong])
	  {
			memcpy(runparameter,BPbuf,buflong); 
      RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
	  }
   }

	 
	 //��ʼ���̶�����
	runparameter[0][0].speed=120;
	runparameter[0][0].time=20;
	runparameter[0][0].acc=1000;
	 
	for(x=1;x<6;x++)
	 {
		runparameter[x][5].speed=120;
		runparameter[x][5].time=40;
		runparameter[x][5].acc=1000;
	 }
	 
	delay_ms(2);
	uart_init(usartbound1);	 //���ڳ�ʼ��
	uart2_init(usartbound2);

//	LCD_Init();


//------------------------------- 
	 
//���ó�ʼ״̬  ����	 
	 play_flag=0;      //�����б�־��0:δ���У�1�������У�2ͣ����
	 set_flag=false;   //������
	 modeNo=1;         ////0��ϵͳ���� 1������  2���ಽ 3.����
	 formula=0,step=0; //�䷽���0��������0
	 
	 readmotorflag=true;          //��ʼͨ��
	 readmotortime=READMOTORTIME;
	 
	 
 	while(1)
	{
		#ifdef IWDG_START
        IWDG_ReloadCounter();
    #endif
				

//		if(flish_time==0)
//		{
//			flish_time=FLISHTIME; //��˸ʱ����
//			shadow=(shadow+1)&0x01;//��
//			Showsetsite(setsite,shadow);
//		}
		
		if(readmotortime==0)
		{
			if(modeNo!=3)                   //0��ϵͳ���� 1������  2���ಽ 3.����
			{
				readmotorflag=false;          //��ͣ���ڶ�motor����
				readmotortime=READMOTORTIME;
				
				//����ʱ��=0
				if(PVtime==0&&play_flag==1)   //play_flag�����б�־��0:δ���У�1�������У�2ͣ����
				{
					if(modeNo==1)
					{
						stopmotor();  //ͣ��  �������
						//if(runstep1==6) process=3;  //�ж�δ����
					}
					else if(modeNo==2)
					{
						if(step==5)
						{
							stopmotor();  //ͣ��  �������
							//if(runstep2==8) process=3;  //�ж�δ����
						}
						else
						{
							step++;
							if(runparameter[formula][step].time!=0&&runparameter[formula][step].acc!=0&&runparameter[formula][step].speed!=0) 
							{
								writeplanbuf();
								SVspeed=runparameter[formula][step].speed;
							}
							else sendresdmotor(); //ѭ�������״̬  �������
						}
					}
				}
				
				//����ʱ�� !=0
				else
				{
					sendresdmotor(); //ѭ�������״̬   �������
				
				}
				
				
				
		  }
			else 
			{
				stopmotor();  //ͣ��   �������
				readmotorflag=true;            //���ڶ�motor����
				readmotortime=READMOTORTIME;
			}
	  }
		
		//ģʽһ���� 0��δ����  1������˨����  2����˨��ʱ2��   3�����������������    4���ȴ��ٶȴ��   5������˨����   6���ȴ�����   7��������ʱ��ͣ��
		//ģʽ������ 0��δ����  1��������������  2����������ʱ3��   3������˨����  4����˨��ʱ2��   5�����������������    6��step5�ȴ��ٶȴ��   7������˨����   8���ȴ�����   9��������ʱ��ͣ��  10��������������
		if(modeNo==1)
		{
			if(runstep1==2&&bolttime==0)
			{
				runstep1=3;
				neworder=true;
				airflag=true;
				airtime=500;
			}
		}
		else if(modeNo==2)
		{
			if(runstep2==2&&pumptime==0)
			{
				runstep2=3;
				neworder=true;
			}
			else if(runstep2==4&&bolttime==0)
			{
				runstep2=5;
				neworder=true;
				airflag=true;
				airtime=500;
			}
		}
		
		
		if(neworder)
		{
			neworder=false;
			if(startwork==0)           //play_flag�����б�־��0:δ���У�1�������У�2ͣ����     startwork ��ָͣ��
			{
				if(play_flag==1)
				{
					PVtime=0;					
					if(modeNo==2) step=5;   // modeNo  0��ϵͳ���� 1������  2���ಽ 3.����
					plansteplong=7;
					readmotorflag=true;                   //���ڶ�motor����
					readmotortime=READMOTORTIME;
				}
				else if((play_flag==0)&&(modeNo==2)&&(runstep2==10))
				{
					readmotorflag=false;                   //��ͣ���ڶ�motor����
					readmotortime=READMOTORTIME;
					delay_ms(150);
					memset(usart2_recebuf,0,wordsize2_rece); //������2
					buf2mumber=0;
					Usart2_overtime=RECEovertime2; 
					usart2_rec=stop;
					
					pumporder=0x00;
					writepumpbuf(pumporder);
				}
			}
			
			else if((startwork==0xFF)&&(runstep1||runstep2))
			{
				readmotorflag=false;                   //��ͣ���ڶ�motor����
				readmotortime=READMOTORTIME;
				delay_ms(150);
				memset(usart2_recebuf,0,wordsize2_rece); //������2
				buf2mumber=0;
				Usart2_overtime=RECEovertime2; 
				usart2_rec=stop;
				
				if(modeNo==1)
				{
					switch(runstep1)  //ģʽһ���� 0��δ����  1������˨����  2����˨��ʱ2��   3�����������������    4���ȴ��ٶȴ��   5������˨����   6���ȴ�����   7��������ʱ��ͣ��
					{
						case 1:	boltorder=0x00;  //boltorder=0xFF;
						        writeboltbuf(boltorder);
										break;
						
						case 3:	formula=0,step=0;  //�䷽��ţ������� 
										SVspeed=runparameter[formula][step].speed;
										SVtime=runparameter[formula][step].time;
										
										writeplanbuf();    //�������ݲ����͵�һ������
										break;
						
						case 5:	boltorder=0xFF;  //boltorder=0x00;
										bolt_speedtime=300;
										writeboltbuf(boltorder);
										break;
						
						case 7:	PVtime=0x00;
										readmotorflag=true;
										break;
					}
				}
				
				
				else if(modeNo==2)
				{
					switch(runstep2) //ģʽ������ 0��δ����  1��������������  2����������ʱ3��   3������˨����  4����˨��ʱ2��   5�����������������    6��step5�ȴ��ٶȴ��   7������˨����   8���ȴ�����   9��������ʱ��ͣ��  10��������������
					{
						case 1:	pumporder=0xFF;
										writepumpbuf(pumporder);
										break;
						
						case 3:	boltorder=0x00;  //boltorder=0xFF;
										writeboltbuf(boltorder);
										break;
						
						case 5:	formula=S_formula;
										step=1;
										SVspeed=runparameter[formula][step].speed;
										SVtime=runparameter[formula][step].time;
						
										writeplanbuf();    //�������ݲ����͵�һ������
										break;
						
						case 7:	boltorder=0xFF;  //boltorder=0x00;
										bolt_speedtime=300;
										writeboltbuf(boltorder);
										break;
						
						case 9:	PVtime=0x00;
										readmotorflag=true;
										break;
										
						case 10:pumporder=0x00;
										writepumpbuf(pumporder);
										break;
					}
				}
			}
			else readmotorflag=true;            //���ڶ�motor����
		}


		//У�鴮��1�յ��� *MODBUS-RTU�����ʽ* ������
				if((usart1check==stop)&&(usart1_rec==succeed))
		{
			u16 test;
			u16 StartAddress,RegisterNumber,NuAddress;
			
			usart1check=start;
      usart1check=stop;                        //����1��������У��
			buf1mumber=0;                            //����1����buf�����
			usart1_rec=stop;                         //����1����״̬	
			
			usart1_recebuf[0]=DeviceAddress;         //���뱾����ַһͬУ��
			test=CalcCrc(usart1_recebuf,(wordsize1_rece-2));    //����У��ֵ
			//-------������ַ-------			
			if((usart1_recebuf[wordsize1_rece-2]+usart1_recebuf[wordsize1_rece-1]*256)==test)   //У����ȷ&&������ַ��ȷ
			{
				delay_ms(2);
				
				if(usart1_recebuf[1]!=0x10)
				{
					memcpy(&ModbusRtu_order,usart1_recebuf,wordsize1_rece);   //������1�յ�������װ������ṹ��
				  StartAddress=ModbusRtu_order.StartAddressH*256+ModbusRtu_order.StartAddressL;		      //�ϲ���ʼ��ַ	
				  RegisterNumber=ModbusRtu_order.RegisterNumberH*256+ModbusRtu_order.RegisterNumberL;   //�ϲ����Ĵ�������/д�������
				
					if(ModbusRtu_order.FunctionCode==0x03)
					{
						char i,n;
						usart1_sendbuf[0]=DeviceAddress;
						usart1_sendbuf[1]=0x03;
						usart1_sendbuf[2]=2*RegisterNumber;
						n=2;
						for(i=0;i<RegisterNumber;i++)
						{
						 switch (StartAddress)         //ѭ����ӼĴ�������   V_power,I_hot,L_vacuum,I_motor
						 {
//               case 0x0000:usart1_sendbuf[n+1]=DeviceAddress>>8;
//												   usart1_sendbuf[n+2]=DeviceAddress&0x00FF;
//											     break;	
//							 case 0x0001:usart1_sendbuf[n+1]=0;
//						             if(usartbound1==9600)        usart1_sendbuf[n+2]=1;
//												 else if(usartbound1==19200)  usart1_sendbuf[n+2]=2;
//						             else if(usartbound1==38400)  usart1_sendbuf[n+2]=3;
//						             else if(usartbound1==115200) usart1_sendbuf[n+2]=4;
//											   break;
							 
							 case 0x0100:usart1_sendbuf[n+1]=runparameter[0][1].acc>>8;      //ϵͳ���ٶ�
													 usart1_sendbuf[n+2]=runparameter[0][1].acc&0x00FF;
													 break;
							 case 0x0101:usart1_sendbuf[n+1]=startwork>>8;      //��ָͣ��
													 usart1_sendbuf[n+2]=startwork&0x00FF;
													 break;
							 case 0x0102:usart1_sendbuf[n+1]=modeNo>>8;         //����ģʽ 0��ϵͳ���� 1������  2���ಽ 3.����
													 usart1_sendbuf[n+2]=modeNo&0x00FF;
													 break;
							 case 0x0103:usart1_sendbuf[n+1]=S_formula>>8;      //�䷽���
													 usart1_sendbuf[n+2]=S_formula&0x00FF;
													 break;
						   case 0x0104:usart1_sendbuf[n+1]=step>>8;           //������
													 usart1_sendbuf[n+2]=step&0x00FF;
													 break;
							 case 0x0105:usart1_sendbuf[n+1]=play_flag>>8;      //�����б�־��0:δ���У�1�������У�2ͣ����
													 usart1_sendbuf[n+2]=play_flag&0x00FF;
													 break;
							 case 0x0106:usart1_sendbuf[n+1]=PVspeed>>8;        //��ǰ�ٶ�
													 usart1_sendbuf[n+2]=PVspeed&0x00FF;
													 break;
							 case 0x0107:usart1_sendbuf[n+1]=PVtime>>8;         //ʣ��ʱ��
													 usart1_sendbuf[n+2]=PVtime&0x00FF;
													 break;
							 case 0x0108:usart1_sendbuf[n+1]=erroNO>>8;         //������
													 usart1_sendbuf[n+2]=erroNO&0x00FF;
													 break;
							 case 0x0109:usart1_sendbuf[n+1]=process>>8;         //����
													 usart1_sendbuf[n+2]=process&0x00FF;
													 break;
							 case 0x010A:usart1_sendbuf[n+1]=runstep1>>8;        //��ʼ������
													 usart1_sendbuf[n+2]=runstep1&0x00FF;
													 break;
							 case 0x010B:usart1_sendbuf[n+1]=runstep2>>8;        //�Ƚ�����
													 usart1_sendbuf[n+2]=runstep2&0x00FF;
													 break; 
							 case 0x1000:usart1_sendbuf[n+1]=runparameter[0][0].speed>>8;        //ת��
													 usart1_sendbuf[n+2]=runparameter[0][0].speed&0x00FF;
													 break;
							 case 0x1001:usart1_sendbuf[n+1]=runparameter[0][0].time>>8;         //��תʱ��
													 usart1_sendbuf[n+2]=runparameter[0][0].time&0x00FF;
													 break;
							 case 0x1002:usart1_sendbuf[n+1]=runparameter[0][0].acc>>8;         //���ٶ�
													 usart1_sendbuf[n+2]=runparameter[0][0].acc&0x00FF;
													 break;
													 
			        
							//A�䷽:�� 5��
							//��һ����
							case 0x1100://ת��
													usart1_sendbuf[n+1]=runparameter[1][1].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[1][1].speed&0x00FF;
													break;
							case 0x1101://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[1][1].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[1][1].time&0x00FF;
													break;
							case 0x1102://���ٶ�
													usart1_sendbuf[n+1]=runparameter[1][1].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[1][1].acc&0x00FF;
													break;
								
							//�ڶ�����
							case 0x1103://ת��
													usart1_sendbuf[n+1]=runparameter[1][2].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[1][2].speed&0x00FF;
													break;
							case 0x1104://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[1][2].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[1][2].time&0x00FF;
													break;
							case 0x1105://���ٶ�
													usart1_sendbuf[n+1]=runparameter[1][2].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[1][2].acc&0x00FF;
													break;
							//��������
							case 0x1106://ת��
													usart1_sendbuf[n+1]=runparameter[1][3].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[1][3].speed&0x00FF;
													break;
							case 0x1107://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[1][3].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[1][3].time&0x00FF;
													break;
							case 0x1108://���ٶ�
								          usart1_sendbuf[n+1]=runparameter[1][3].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[1][3].acc&0x00FF;
													break;
							//���Ĳ���
							case 0x1109://ת��
													usart1_sendbuf[n+1]=runparameter[1][4].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[1][4].speed&0x00FF;
													break;
							case 0x110A://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[1][4].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[1][4].time&0x00FF;
													break;
							case 0x110B://���ٶ�
													usart1_sendbuf[n+1]=runparameter[1][4].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[1][4].acc&0x00FF;
													break;
							//���岽��
							case 0x110C://ת��
													usart1_sendbuf[n+1]=runparameter[1][5].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[1][5].speed&0x00FF;
													break;
							case 0x110D://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[1][5].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[1][5].time&0x00FF;
													break;
							case 0x110E://���ٶ�										 
													usart1_sendbuf[n+1]=runparameter[1][5].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[1][5].acc&0x00FF;
													break;
							
							//B�䷽:�� 5��
							//��һ����
							case 0x1200://ת��
													usart1_sendbuf[n+1]=runparameter[2][1].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[2][1].speed&0x00FF;
													break;
							case 0x1201://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[2][1].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[2][1].time&0x00FF;
													break;
							case 0x1202://���ٶ�
													usart1_sendbuf[n+1]=runparameter[2][1].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[2][1].acc&0x00FF;
													break;
								
							//�ڶ�����
							case 0x1203://ת��
													usart1_sendbuf[n+1]=runparameter[2][2].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[2][2].speed&0x00FF;
													break;
							case 0x1204://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[2][2].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[2][2].time&0x00FF;
													break;
							case 0x1205://���ٶ�
													usart1_sendbuf[n+1]=runparameter[2][2].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[2][2].acc&0x00FF;
													break;
							//��������
							case 0x1206://ת��
													usart1_sendbuf[n+1]=runparameter[2][3].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[2][3].speed&0x00FF;
													break;
							case 0x1207://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[2][3].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[2][3].time&0x00FF;
													break;
							case 0x1208://���ٶ�
								          usart1_sendbuf[n+1]=runparameter[2][3].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[2][3].acc&0x00FF;
													break;
							//���Ĳ���
							case 0x1209://ת��
													usart1_sendbuf[n+1]=runparameter[2][4].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[2][4].speed&0x00FF;
													break;
							case 0x120A://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[2][4].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[2][4].time&0x00FF;
													break;
							case 0x120B://���ٶ�
													usart1_sendbuf[n+1]=runparameter[2][4].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[2][4].acc&0x00FF;
													break;
							//���岽��
							case 0x120C://ת��
													usart1_sendbuf[n+1]=runparameter[2][5].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[2][5].speed&0x00FF;
													break;
							case 0x120D://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[2][5].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[2][5].time&0x00FF;
													break;
							case 0x120E://���ٶ�										 
													usart1_sendbuf[n+1]=runparameter[2][5].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[2][5].acc&0x00FF;
													break;
	
							//C�䷽:�� 5��
							//��һ����
							case 0x1300://ת��
													usart1_sendbuf[n+1]=runparameter[3][1].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[3][1].speed&0x00FF;
													break;
							case 0x1301://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[3][1].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[3][1].time&0x00FF;
													break;
							case 0x1302://���ٶ�
													usart1_sendbuf[n+1]=runparameter[3][1].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[3][1].acc&0x00FF;
													break;
								
							//�ڶ�����
							case 0x1303://ת��
													usart1_sendbuf[n+1]=runparameter[3][2].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[3][2].speed&0x00FF;
													break;
							case 0x1304://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[3][2].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[3][2].time&0x00FF;
													break;
							case 0x1305://���ٶ�
													usart1_sendbuf[n+1]=runparameter[3][2].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[3][2].acc&0x00FF;
													break;
							//��������
							case 0x1306://ת��
													usart1_sendbuf[n+1]=runparameter[3][3].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[3][3].speed&0x00FF;
													break;
							case 0x1307://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[3][3].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[3][3].time&0x00FF;
													break;
							case 0x1308://���ٶ�
								          usart1_sendbuf[n+1]=runparameter[3][3].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[3][3].acc&0x00FF;
													break;
							//���Ĳ���
							case 0x1309://ת��
													usart1_sendbuf[n+1]=runparameter[3][4].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[3][4].speed&0x00FF;
													break;
							case 0x130A://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[3][4].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[3][4].time&0x00FF;
													break;
							case 0x130B://���ٶ�
													usart1_sendbuf[n+1]=runparameter[3][4].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[3][4].acc&0x00FF;
													break;
							//���岽��
							case 0x130C://ת��
													usart1_sendbuf[n+1]=runparameter[3][5].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[3][5].speed&0x00FF;
													break;
							case 0x130D://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[3][5].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[3][5].time&0x00FF;
													break;
							case 0x130E://���ٶ�										 
													usart1_sendbuf[n+1]=runparameter[3][5].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[3][5].acc&0x00FF;
													break;
							
							//D�䷽:�� 5��
							//��һ����
							case 0x1400://ת��
													usart1_sendbuf[n+1]=runparameter[4][1].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[4][1].speed&0x00FF;
													break;
							case 0x1401://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[4][1].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[4][1].time&0x00FF;
													break;
							case 0x1402://���ٶ�
													usart1_sendbuf[n+1]=runparameter[4][1].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[4][1].acc&0x00FF;
													break;
								
							//�ڶ�����
							case 0x1403://ת��
													usart1_sendbuf[n+1]=runparameter[4][2].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[4][2].speed&0x00FF;
													break;
							case 0x1404://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[4][2].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[4][2].time&0x00FF;
													break;
							case 0x1405://���ٶ�
													usart1_sendbuf[n+1]=runparameter[4][2].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[4][2].acc&0x00FF;
													break;
							//��������
							case 0x1406://ת��
													usart1_sendbuf[n+1]=runparameter[4][3].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[4][3].speed&0x00FF;
													break;
							case 0x1407://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[4][3].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[4][3].time&0x00FF;
													break;
							case 0x1408://���ٶ�
								          usart1_sendbuf[n+1]=runparameter[4][3].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[4][3].acc&0x00FF;
													break;
							//���Ĳ���
							case 0x1409://ת��
													usart1_sendbuf[n+1]=runparameter[4][4].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[4][4].speed&0x00FF;
													break;
							case 0x140A://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[4][4].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[4][4].time&0x00FF;
													break;
							case 0x140B://���ٶ�
													usart1_sendbuf[n+1]=runparameter[4][4].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[4][4].acc&0x00FF;
													break;
							//���岽��
							case 0x140C://ת��
													usart1_sendbuf[n+1]=runparameter[4][5].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[4][5].speed&0x00FF;
													break;
							case 0x140D://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[4][5].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[4][5].time&0x00FF;
													break;
							case 0x140E://���ٶ�										 
													usart1_sendbuf[n+1]=runparameter[4][5].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[4][5].acc&0x00FF;
													break;
							
							//E�䷽:�� 5��
							//��һ����
							case 0x1500://ת��
													usart1_sendbuf[n+1]=runparameter[5][1].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[5][1].speed&0x00FF;
													break;
							case 0x1501://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[5][1].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[5][1].time&0x00FF;
													break;
							case 0x1502://���ٶ�
													usart1_sendbuf[n+1]=runparameter[5][1].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[5][1].acc&0x00FF;
													break;
								
							//�ڶ�����
							case 0x1503://ת��
													usart1_sendbuf[n+1]=runparameter[5][2].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[5][2].speed&0x00FF;
													break;
							case 0x1504://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[5][2].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[5][2].time&0x00FF;
													break;
							case 0x1505://���ٶ�
													usart1_sendbuf[n+1]=runparameter[5][2].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[5][2].acc&0x00FF;
													break;
							//��������
							case 0x1506://ת��
													usart1_sendbuf[n+1]=runparameter[5][3].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[5][3].speed&0x00FF;
													break;
							case 0x1507://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[5][3].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[5][3].time&0x00FF;
													break;
							case 0x1508://���ٶ�
								          usart1_sendbuf[n+1]=runparameter[5][3].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[5][3].acc&0x00FF;
													break;
							//���Ĳ���
							case 0x1509://ת��
													usart1_sendbuf[n+1]=runparameter[5][4].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[5][4].speed&0x00FF;
													break;
							case 0x150A://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[5][4].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[5][4].time&0x00FF;
													break;
							case 0x150B://���ٶ�
													usart1_sendbuf[n+1]=runparameter[5][4].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[5][4].acc&0x00FF;
													break;
							//���岽��
							case 0x150C://ת��
													usart1_sendbuf[n+1]=runparameter[5][5].speed>>8;        //ת��
													usart1_sendbuf[n+2]=runparameter[5][5].speed&0x00FF;
													break;
							case 0x150D://��תʱ�����룩
													usart1_sendbuf[n+1]=runparameter[5][5].time>>8;         //��תʱ��
													usart1_sendbuf[n+2]=runparameter[5][5].time&0x00FF;
													break;
							case 0x150E://���ٶ�										 
													usart1_sendbuf[n+1]=runparameter[5][5].acc>>8;         //���ٶ�
													usart1_sendbuf[n+2]=runparameter[5][5].acc&0x00FF;
													break;
							
							 default: usart1_sendbuf[n+1]=0x00;
												usart1_sendbuf[n+2]=0x00;
											 break;
						 }
						 StartAddress++;
						 n=n+2;
						}
						test=CalcCrc(usart1_sendbuf,n+1);    //����У��ֵ
						usart1_sendbuf[n+1]=test&0x00FF;
						usart1_sendbuf[n+2]=test>>8;
						
						//�ظ���λ��
						USART1_SendBuf485(usart1_sendbuf,n+3);   //RS-485  

					 }

						else if(ModbusRtu_order.FunctionCode==0x06)
						{
							
							switch (StartAddress)
							{
//								case 0x0000:    //���ı�����ַ
//														if(RegisterNumber<255&&RegisterNumber>0)
//														{	
//															DeviceParameter.Addr=RegisterNumber;
//															DeviceAddress=RegisterNumber;
//															//��Ӧ��λ��
//															memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//															USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//															//����д��flash
//															if(DeviceParameter.Addr>0&&DeviceParameter.Bound1>0&&DeviceParameter.Bound2>0)
//															RebuildParameter(DeviceParameter,ParameterAddr3,ParameterAddr4);  //����д��flash
//														}
//														break;
//								
//								case 0x0001:   //���Ĵ��ڲ�����
//														if(1==RegisterNumber) DeviceParameter.Bound=9600;
//														else if(2==RegisterNumber) DeviceParameter.Bound=19200;
//														else if(3==RegisterNumber) DeviceParameter.Bound=38400;
//														else if(4==RegisterNumber) DeviceParameter.Bound=115200;
//														else break;
//														usartbound1=DeviceParameter.Bound;
//														//��Ӧ��λ��
//														memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//														USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//														//����д��flash
//														if(DeviceParameter.Addr>0&&DeviceParameter.Bound1>0&&DeviceParameter.Bound2>0)
//														RebuildParameter(DeviceParameter,ParameterAddr3,ParameterAddr4);  //����д��flash
//														uart_init(usartbound1);	 //���ڳ�ʼ��
//														break;
								
								case 0x0100:   //���ٶ�
														runparameter[0][1].acc=RegisterNumber;
														//����д��flash
														RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
														//��Ӧ��λ��
														memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
														USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
														break;
							  case 0x0101:   //��ͣ
														if(RegisterNumber==0||RegisterNumber==0xFF)
														{
														  startwork=RegisterNumber;
															neworder=true;
															if(startwork&&(play_flag==0)&&(PVspeed<2))  // if(startwork&&(runstep1==0)&&(runstep2==0))
															{
																if(modeNo==1) runstep1=1;
																else if(modeNo==2) runstep2=1;
																process=1;  //���̱�ʶ   0��������ʼ״̬   1���յ���ʼ�����������    2����������   3����;�յ�ֹͣ����    4����;ֹͣ
															}
															if(play_flag==0&&startwork==0&&PVspeed>2)  play_flag=1;
															if(play_flag&&startwork==0)  process=3;   //���̱�ʶ   0��������ʼ״̬   1���յ���ʼ�����������    2����������   3����;�յ�ֹͣ����    4����;ֹͣ
															if(process==1&&play_flag==0&&startwork==0)
															{
																if(modeNo==1)
																{
																	PVtime_flag=false;
																	PVtime=0;
																	runstep1=0;
																	process=4;
																	neworder=false;
																}
																else if(modeNo==2)
																{
																	runstep2=10;
																	PVtime_flag=false;
																	PVtime=0;
																	step=5;
																	process=3;
																}
															}
															if((process==0||process==2||process==4)&&startwork==0)  neworder=false;
														}
														//��Ӧ��λ��
														memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
														USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
														break;
								case 0x0102:   //����ģʽ��1��������2���ಽ��3������0��ϵͳ����
														if(play_flag==0) modeNo=RegisterNumber;
														//��Ӧ��λ��
														memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
														USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
														break;															
								case 0x0103:   //�䷽���
														S_formula=RegisterNumber;
														//��Ӧ��λ��
														memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
														USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
														break;
//								case 0x1000:   //����ת��
//														runparameter[0][0].speed=RegisterNumber;
//														//��Ӧ��λ��
//														memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//														USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//														break;
//								case 0x1001:   //������תʱ��
//														runparameter[0][0].time=RegisterNumber;
//														//��Ӧ��λ��
//														memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//														USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//														break;
//								case 0x1002:   //�������ٶ�
//														runparameter[0][0].acc=RegisterNumber;
//														RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
//														//��Ӧ��λ��
//														memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//														USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//														break;
								
								
							//A�䷽:�� 5��
							//��һ����
							case 0x1100://ת��
													runparameter[1][1].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
							            break;
							case 0x1101://��תʱ�����룩
													runparameter[1][1].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1102://���ٶ�
													runparameter[1][1].acc=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
								          break;
							//�ڶ�����
							case 0x1103://ת��
													runparameter[1][2].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1104://��תʱ�����룩
													runparameter[1][2].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1105://���ٶ�
													runparameter[1][2].acc=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//��������
							case 0x1106://ת��
													runparameter[1][3].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1107://��תʱ�����룩
													runparameter[1][3].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1108://���ٶ�
								          runparameter[1][3].acc=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//���Ĳ���
							case 0x1109://ת��
													runparameter[1][4].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x110A://��תʱ�����룩
													runparameter[1][4].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x110B://���ٶ�
													runparameter[1][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
//							//���岽��
//							case 0x110C://ת��
//													runparameter[1][5].speed=RegisterNumber;
//													//��Ӧ��λ��
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x110D://��תʱ�����룩
//													runparameter[1][5].time=RegisterNumber;
//													//��Ӧ��λ��
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x110E://���ٶ�										 
//													runparameter[1][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
//													//��Ӧ��λ��
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
								
							//B�䷽:�� 5��
							//��һ����
							case 0x1200://ת��
													runparameter[2][1].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
							            break;
							case 0x1201://��תʱ�����룩
													runparameter[2][1].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1202://���ٶ�
													runparameter[2][1].acc=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
								          break;
							//�ڶ�����
							case 0x1203://ת��
													runparameter[2][2].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1204://��תʱ�����룩
													runparameter[2][2].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1205://���ٶ�
													runparameter[2][2].acc=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//��������
							case 0x1206://ת��
													runparameter[2][3].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1207://��תʱ�����룩
													runparameter[2][3].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1208://���ٶ�
								          runparameter[2][3].acc=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//���Ĳ���
							case 0x1209://ת��
													runparameter[2][4].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x120A://��תʱ�����룩
													runparameter[2][4].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x120B://���ٶ�
													runparameter[2][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
//							//���岽��
//							case 0x120C://ת��
//													runparameter[2][5].speed=RegisterNumber;
//													//��Ӧ��λ��
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x120D://��תʱ�����룩
//													runparameter[2][5].time=RegisterNumber;
//													//��Ӧ��λ��
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x120E://���ٶ�										 
//													runparameter[2][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
//													//��Ӧ��λ��
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
							
							//C�䷽:�� 5��
							//��һ����
							case 0x1300://ת��
													runparameter[3][1].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
							            break;
							case 0x1301://��תʱ�����룩
													runparameter[3][1].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1302://���ٶ�
													runparameter[3][1].acc=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
								          break;
							//�ڶ�����
							case 0x1303://ת��
													runparameter[3][2].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1304://��תʱ�����룩
													runparameter[3][2].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1305://���ٶ�
													runparameter[3][2].acc=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//��������
							case 0x1306://ת��
													runparameter[3][3].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1307://��תʱ�����룩
													runparameter[3][3].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1308://���ٶ�
								          runparameter[3][3].acc=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//���Ĳ���
							case 0x1309://ת��
													runparameter[3][4].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x130A://��תʱ�����룩
													runparameter[3][4].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x130B://���ٶ�
													runparameter[3][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
//							//���岽��
//							case 0x130C://ת��
//													runparameter[3][5].speed=RegisterNumber;
//													//��Ӧ��λ��
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x130D://��תʱ�����룩
//													runparameter[3][5].time=RegisterNumber;
//													//��Ӧ��λ��
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x130E://���ٶ�										 
//													runparameter[3][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
//													//��Ӧ��λ��
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
							
							//D�䷽:�� 5��
							//��һ����
							case 0x1400://ת��
													runparameter[4][1].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
							            break;
							case 0x1401://��תʱ�����룩
													runparameter[4][1].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1402://���ٶ�
													runparameter[4][1].acc=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
								          break;
							//�ڶ�����
							case 0x1403://ת��
													runparameter[4][2].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1404://��תʱ�����룩
													runparameter[4][2].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1405://���ٶ�
													runparameter[4][2].acc=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//��������
							case 0x1406://ת��
													runparameter[4][3].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1407://��תʱ�����룩
													runparameter[4][3].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1408://���ٶ�
								          runparameter[4][3].acc=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//���Ĳ���
							case 0x1409://ת��
													runparameter[4][4].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x140A://��תʱ�����룩
													runparameter[4][4].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x140B://���ٶ�
													runparameter[4][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
//							//���岽��
//							case 0x140C://ת��
//													runparameter[4][5].speed=RegisterNumber;
//													//��Ӧ��λ��
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x140D://��תʱ�����룩
//													runparameter[4][5].time=RegisterNumber;
//													//��Ӧ��λ��
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x140E://���ٶ�										 
//													runparameter[4][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
//													//��Ӧ��λ��
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
							
							//E�䷽:�� 5��
							//��һ����
							case 0x1500://ת��
													runparameter[5][1].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
							            break;
							case 0x1501://��תʱ�����룩
													runparameter[5][1].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1502://���ٶ�
													runparameter[5][1].acc=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
								          break;
							//�ڶ�����
							case 0x1503://ת��
													runparameter[5][2].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1504://��תʱ�����룩
													runparameter[5][2].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1505://���ٶ�
													runparameter[5][2].acc=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//��������
							case 0x1506://ת��
													runparameter[5][3].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1507://��תʱ�����룩
													runparameter[5][3].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1508://���ٶ�
								          runparameter[5][3].acc=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//���Ĳ���
							case 0x1509://ת��
													runparameter[5][4].speed=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x150A://��תʱ�����룩
													runparameter[5][4].time=RegisterNumber;
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x150B://���ٶ�
													runparameter[5][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
													//��Ӧ��λ��
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
//							//���岽��
//							case 0x150C://ת��
//													runparameter[5][5].speed=RegisterNumber;
//													//��Ӧ��λ��
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x150D://��תʱ�����룩
//													runparameter[5][5].time=RegisterNumber;
//													//��Ӧ��λ��
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x150E://���ٶ�										 
//													runparameter[5][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
//													//��Ӧ��λ��
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
							
								default: break;
							}
						}
					 }
				
			 
				 else if(usart1_recebuf[1]==0x10)   //�����������  ��λ����Ӧ06����   0x10Э�����
				 {
					 	char i,n=7;
			  
						StartAddress=usart1_recebuf[2]*256+usart1_recebuf[3];		  //�ϲ���ʼ��ַ	
						NuAddress=usart1_recebuf[5]+usart1_recebuf[4]*256;	          //�Ĵ�������
						n=7;
					
						for(i=0;i<NuAddress;i++)
						{
							switch (StartAddress)
							{
								case 0x0100:   //���ٶ�
														runparameter[0][1].acc=RegisterNumber;
														//����д��flash
														RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
										        break;
								case 0x0101:   //��ͣ
														if(RegisterNumber==0||RegisterNumber==0xFF)
														{
														  startwork=RegisterNumber;
															neworder=true;
															if(startwork&&(runstep1==0)&&(runstep2==0))
															{
																if(modeNo==1) runstep1=1;
																else if(modeNo==2) runstep2=1;
																process=1;   //���̱�ʶ   0��������ʼ״̬   1���յ���ʼ�����������    2����������   3����;�յ�ֹͣ����    4����;ֹͣ
															}
															if(play_flag==0&&startwork==0&&PVspeed>2)  play_flag=1;
															if(play_flag&&startwork==0)  process=3;   //���̱�ʶ   0��������ʼ״̬   1���յ���ʼ�����������    2����������   3����;�յ�ֹͣ����    4����;ֹͣ
															if(process==1&&play_flag==0&&startwork==0)
															{
																if(modeNo==1)
																{
																	PVtime_flag=false;
																	PVtime=0;
																	runstep1=0;
																	process=4;
																	neworder=false;
																}
																else if(modeNo==2)
																{
																	runstep2=10;
																	PVtime_flag=false;
																	PVtime=0;
																	step=5;
																	process=3;
																}
															}
															if((process==0||process==2||process==4)&&startwork==0)  neworder=false;
														}
										        break;								
							  case 0x0102:   //����ģʽ��1��������2���ಽ��3������0��ϵͳ����
														if(play_flag==0)  modeNo=RegisterNumber;
										        break;
							  case 0x0103:   //�䷽���
														S_formula=RegisterNumber;
										        break;
//								case 0x1000:   //����ת��
//														runparameter[0][0].speed=RegisterNumber;
//										        break;								
//							  case 0x1001:   //������תʱ��
//														runparameter[0][0].time=RegisterNumber;
//										        break;
//							  case 0x1002:   //�������ٶ�
//														runparameter[0][0].acc=RegisterNumber;
//														RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
//										        break;
								
							//A�䷽:�� 5��
							//��һ����
							case 0x1100://ת��
													runparameter[1][1].speed=RegisterNumber;
							            break;
							case 0x1101://��תʱ�����룩
													runparameter[1][1].time=RegisterNumber;
													break;
							case 0x1102://���ٶ�
													runparameter[1][1].acc=RegisterNumber;
								          break;
							//�ڶ�����
							case 0x1103://ת��
													runparameter[1][2].speed=RegisterNumber;
													break;
							case 0x1104://��תʱ�����룩
													runparameter[1][2].time=RegisterNumber;
													break;
							case 0x1105://���ٶ�
													runparameter[1][2].acc=RegisterNumber;
													break;
							//��������
							case 0x1106://ת��
													runparameter[1][3].speed=RegisterNumber;
													break;
							case 0x1107://��תʱ�����룩
													runparameter[1][3].time=RegisterNumber;
													break;
							case 0x1108://���ٶ�
								          runparameter[1][3].acc=RegisterNumber;
													break;
							//���Ĳ���
							case 0x1109://ת��
													runparameter[1][4].speed=RegisterNumber;
													break;
							case 0x110A://��תʱ�����룩
													runparameter[1][4].time=RegisterNumber;
													break;
							case 0x110B://���ٶ�
													runparameter[1][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
													break;
//							//���岽��
//							case 0x110C://ת��
//													runparameter[1][5].speed=RegisterNumber;
//													break;
//							case 0x110D://��תʱ�����룩
//													runparameter[1][5].time=RegisterNumber;
//													break;
//							case 0x110E://���ٶ�										 
//													runparameter[1][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
//													break;
							
							//B�䷽:�� 5��
							//��һ����
							case 0x1200://ת��
													runparameter[2][1].speed=RegisterNumber;
							            break;
							case 0x1201://��תʱ�����룩
													runparameter[2][1].time=RegisterNumber;
													break;
							case 0x1202://���ٶ�
													runparameter[2][1].acc=RegisterNumber;
								          break;
							//�ڶ�����
							case 0x1203://ת��
													runparameter[2][2].speed=RegisterNumber;
													break;
							case 0x1204://��תʱ�����룩
													runparameter[2][2].time=RegisterNumber;
													break;
							case 0x1205://���ٶ�
													runparameter[2][2].acc=RegisterNumber;
													break;
							//��������
							case 0x1206://ת��
													runparameter[2][3].speed=RegisterNumber;
													break;
							case 0x1207://��תʱ�����룩
													runparameter[2][3].time=RegisterNumber;
													break;
							case 0x1208://���ٶ�
								          runparameter[2][3].acc=RegisterNumber;
													break;
							//���Ĳ���
							case 0x1209://ת��
													runparameter[2][4].speed=RegisterNumber;
													break;
							case 0x120A://��תʱ�����룩
													runparameter[2][4].time=RegisterNumber;
													break;
							case 0x120B://���ٶ�
													runparameter[2][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
													break;
//							//���岽��
//							case 0x120C://ת��
//													runparameter[2][5].speed=RegisterNumber;
//													break;
//							case 0x120D://��תʱ�����룩
//													runparameter[2][5].time=RegisterNumber;
//													break;
//							case 0x120E://���ٶ�										 
//													runparameter[2][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
//													break;
							
							//C�䷽:�� 5��
							//��һ����
							case 0x1300://ת��
													runparameter[3][1].speed=RegisterNumber;
							            break;
							case 0x1301://��תʱ�����룩
													runparameter[3][1].time=RegisterNumber;
													break;
							case 0x1302://���ٶ�
													runparameter[3][1].acc=RegisterNumber;
								          break;
							//�ڶ�����
							case 0x1303://ת��
													runparameter[3][2].speed=RegisterNumber;
													break;
							case 0x1304://��תʱ�����룩
													runparameter[3][2].time=RegisterNumber;
													break;
							case 0x1305://���ٶ�
													runparameter[3][2].acc=RegisterNumber;
													break;
							//��������
							case 0x1306://ת��
													runparameter[3][3].speed=RegisterNumber;
													break;
							case 0x1307://��תʱ�����룩
													runparameter[3][3].time=RegisterNumber;
													break;
							case 0x1308://���ٶ�
								          runparameter[3][3].acc=RegisterNumber;
													break;
							//���Ĳ���
							case 0x1309://ת��
													runparameter[3][4].speed=RegisterNumber;
													break;
							case 0x130A://��תʱ�����룩
													runparameter[3][4].time=RegisterNumber;
													break;
							case 0x130B://���ٶ�
													runparameter[3][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
													break;
//							//���岽��
//							case 0x130C://ת��
//													runparameter[3][5].speed=RegisterNumber;
//													break;
//							case 0x130D://��תʱ�����룩
//													runparameter[3][5].time=RegisterNumber;
//													break;
//							case 0x130E://���ٶ�										 
//													runparameter[3][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
//													break;
							
							//D�䷽:�� 5��
							//��һ����
							case 0x1400://ת��
													runparameter[4][1].speed=RegisterNumber;
							            break;
							case 0x1401://��תʱ�����룩
													runparameter[4][1].time=RegisterNumber;
													break;
							case 0x1402://���ٶ�
													runparameter[4][1].acc=RegisterNumber;
								          break;
							//�ڶ�����
							case 0x1403://ת��
													runparameter[4][2].speed=RegisterNumber;
													break;
							case 0x1404://��תʱ�����룩
													runparameter[4][2].time=RegisterNumber;
													break;
							case 0x1405://���ٶ�
													runparameter[4][2].acc=RegisterNumber;
													break;
							//��������
							case 0x1406://ת��
													runparameter[4][3].speed=RegisterNumber;
													break;
							case 0x1407://��תʱ�����룩
													runparameter[4][3].time=RegisterNumber;
													break;
							case 0x1408://���ٶ�
								          runparameter[4][3].acc=RegisterNumber;
													break;
							//���Ĳ���
							case 0x1409://ת��
													runparameter[4][4].speed=RegisterNumber;
													break;
							case 0x140A://��תʱ�����룩
													runparameter[4][4].time=RegisterNumber;
													break;
							case 0x140B://���ٶ�
													runparameter[4][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
													break;
//							//���岽��
//							case 0x140C://ת��
//													runparameter[4][5].speed=RegisterNumber;
//													break;
//							case 0x140D://��תʱ�����룩
//													runparameter[4][5].time=RegisterNumber;
//													break;
//							case 0x140E://���ٶ�										 
//													runparameter[4][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
//													break;
							
							//E�䷽:�� 5��
							//��һ����
							case 0x1500://ת��
													runparameter[5][1].speed=RegisterNumber;
							            break;
							case 0x1501://��תʱ�����룩
													runparameter[5][1].time=RegisterNumber;
													break;
							case 0x1502://���ٶ�
													runparameter[5][1].acc=RegisterNumber;
								          break;
							//�ڶ�����
							case 0x1503://ת��
													runparameter[5][2].speed=RegisterNumber;
													break;
							case 0x1504://��תʱ�����룩
													runparameter[5][2].time=RegisterNumber;
													break;
							case 0x1505://���ٶ�
													runparameter[5][2].acc=RegisterNumber;
													break;
							//��������
							case 0x1506://ת��
													runparameter[5][3].speed=RegisterNumber;
													break;
							case 0x1507://��תʱ�����룩
													runparameter[5][3].time=RegisterNumber;
													break;
							case 0x1508://���ٶ�
								          runparameter[5][3].acc=RegisterNumber;
													break;
							//���Ĳ���
							case 0x1509://ת��
													runparameter[5][4].speed=RegisterNumber;
													break;
							case 0x150A://��תʱ�����룩
													runparameter[5][4].time=RegisterNumber;
													break;
							case 0x150B://���ٶ�
													runparameter[5][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
													break;
//							//���岽��
//							case 0x150C://ת��
//													runparameter[5][5].speed=RegisterNumber;
//													break;
//							case 0x150D://��תʱ�����룩
//													runparameter[5][5].time=RegisterNumber;
//													break;
//							case 0x150E://���ٶ�										 
//													runparameter[5][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //����д��flash
//													break;							
								
							}
							StartAddress++;
							n=n+2;	
						}
						
						memcpy(usart1_sendbuf,usart1_recebuf,6);
						test=CalcCrc(usart1_sendbuf,6);    //����У��ֵ
						usart1_sendbuf[6]=test&0x00FF;
						usart1_sendbuf[7]=test>>8;
						
						//�ظ���λ��
						USART1_SendBuf485(usart1_sendbuf,8);   //RS-485 
				 } //0x10 end	

			}//������ַ����
			
		//--------�㲥��ַ-----------------
	  else
		 {
			usart1_recebuf[0]=0x00;         //����㲥��ַһͬУ�� 
			test=CalcCrc(usart1_recebuf,(wordsize1_rece-2));    //����У��ֵ 
			if((usart1_recebuf[wordsize1_rece-2]+usart1_recebuf[wordsize1_rece-1]*256)==test) 
		  {
			 	memcpy(&ModbusRtu_order,usart1_recebuf,wordsize1_rece);   //������1�յ�������װ������ṹ��
				StartAddress=ModbusRtu_order.StartAddressH*256+ModbusRtu_order.StartAddressL;		      //�ϲ���ʼ��ַ	
				RegisterNumber=ModbusRtu_order.RegisterNumberH*256+ModbusRtu_order.RegisterNumberL;   //�ϲ����Ĵ�������/д�������
				if(ModbusRtu_order.FunctionCode==0x03)
				{
					char i,n;
					usart1_sendbuf[0]=0x00;
					usart1_sendbuf[1]=0x03;
					usart1_sendbuf[2]=2*RegisterNumber;
					n=2;
					for(i=0;i<RegisterNumber;i++)
					{
					 switch (StartAddress)         //ѭ����ӼĴ�������
					 {
						 
						 case 0x0000:usart1_sendbuf[n+1]=DeviceAddress>>8;        //�豸��ַ
												 usart1_sendbuf[n+2]=DeviceAddress&0x00FF;
											   break;	

						 case 0x0001:usart1_sendbuf[n+1]=0;
						             if(usartbound1==9600)        usart1_sendbuf[n+2]=1;
												 else if(usartbound1==19200)  usart1_sendbuf[n+2]=2;
						             else if(usartbound1==38400)  usart1_sendbuf[n+2]=3;
						             else if(usartbound1==115200) usart1_sendbuf[n+2]=4;
											   break;		
						 
							case 0x0002:usart1_sendbuf[n+1]=0;
						             if(usartbound2==9600)        usart1_sendbuf[n+2]=1;
												 else if(usartbound2==19200)  usart1_sendbuf[n+2]=2;
						             else if(usartbound2==38400)  usart1_sendbuf[n+2]=3;
						             else if(usartbound2==115200) usart1_sendbuf[n+2]=4;
											   break;
												 
						 default: usart1_sendbuf[n+1]=0x00;
											usart1_sendbuf[n+2]=0x00;
							       break;
					 }
					 StartAddress++;
					 n=n+2;
				  }
					test=CalcCrc(usart1_sendbuf,n+1);    //����У��ֵ
					usart1_sendbuf[n+1]=test&0x00FF;
					usart1_sendbuf[n+2]=test>>8;
					
					//�ظ���λ��
			    USART1_SendBuf485(usart1_sendbuf,n+3);   //RS-485  

				 }

				else if(ModbusRtu_order.FunctionCode==0x06)
				{
					switch (StartAddress)
					{
						case 0x0000:    //���ı�����ַ
							          if(RegisterNumber<255&&RegisterNumber>0)
												{	
							            DeviceParameter.Addr=RegisterNumber;
						              DeviceAddress=RegisterNumber;
											    //��Ӧ��λ��
						              memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
			                    USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
						              //����д��flash
													if(DeviceParameter.Addr>0&&DeviceParameter.Bound1>0&&DeviceParameter.Bound2>0)
                          RebuildParameter(DeviceParameter,ParameterAddr3,ParameterAddr4);  //����д��flash 
												}
						            break;
						
						case 0x0001:   //���Ĵ��ڲ�����
							          if(1==RegisterNumber) DeviceParameter.Bound1=9600;
							          else if(2==RegisterNumber) DeviceParameter.Bound1=19200;
						            else if(3==RegisterNumber) DeviceParameter.Bound1=38400;
						            else if(4==RegisterNumber) DeviceParameter.Bound1=115200;
						            else break;
						            usartbound1=DeviceParameter.Bound1;
											  //��Ӧ��λ��
						            memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
                        USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
									      //����д��flash
												if(DeviceParameter.Addr>0&&DeviceParameter.Bound1>0&&DeviceParameter.Bound2>0)
                        RebuildParameter(DeviceParameter,ParameterAddr3,ParameterAddr4);  //����д��flash
								        uart_init(usartbound1);	 //���ڳ�ʼ��
						            break;
						
						case 0x0002:   //���Ĵ��ڲ�����
							          if(1==RegisterNumber) DeviceParameter.Bound2=9600;
							          else if(2==RegisterNumber) DeviceParameter.Bound2=19200;
						            else if(3==RegisterNumber) DeviceParameter.Bound2=38400;
						            else if(4==RegisterNumber) DeviceParameter.Bound2=115200;
						            else break;
						            usartbound2=DeviceParameter.Bound2;
											  //��Ӧ��λ��
						            memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
                        USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
									      //����д��flash
						            if(DeviceParameter.Addr>0&&DeviceParameter.Bound1>0&&DeviceParameter.Bound2>0)
                        RebuildParameter(DeviceParameter,ParameterAddr3,ParameterAddr4);  //����д��flash
								        uart2_init(usartbound2);	 //���ڳ�ʼ��
						            break;
						
					  default: break;
					}
				}	
       clean_usart1();  //������1��״̬ 
       memset(usart1_sendbuf,0,100);	
		  }
		 }//�㲥��ַ����
			
			clean_usart1();  //������1��״̬ 
		 
    }				//����1����	

			
			
		//У�鴮��2�յ��� *MODBUS-RTU�����ʽ* ������
		if((usart2check==stop)&&(usart2_rec==succeed))
		{
			//char c;
			s16  temphz;
			usart2check=start; 
      usart2check=stop;                        //����2��������У��
			buf2mumber=0;                            //����2����buf�����
			usart2_rec=stop;                         //����2����״̬
			usart2_recebuf[0]=usart2_sendbuf[0];                     //�����豸��ַ�̶�1
			test=CalcCrc(usart2_recebuf,(wordsize2_rece-2));    //����У��ֵ

			if(test==usart2_recebuf[wordsize2_rece-2]+usart2_recebuf[wordsize2_rece-1]*256)
			{
				erro_count=0;
				switch(usart2_recebuf[1])
				{
					case 0x03:
										
					readmotorflag=true;
					if(set_flag==false&&modeNo!=0)   //�����б�־
					{
						//��ƽ���ٶ�
			//			speed_s=usart2_recebuf[5]*256+usart2_recebuf[6]+speed_s;
			//			speed_n++;
			//			if(speed_n==4)
			//			{
			//				PVspeed=speed_s/4;
			//				speed_n=0; speed_s=0;
			//			}
						temphz=usart2_recebuf[3]*256+usart2_recebuf[4];  //����Ƶ��
						if(temphz<0)   PVspeed=0;
						else           PVspeed=temphz*2/4;      //temphz*0.1*20/4
						
						if(plansteplong==8)           //�ڶ��μ���
						{
							if(PVspeed>SVspeed*0.3)
							{
								delay_ms(50);
								plansteplong=7;
								planstep=7;
								memcpy(usart2_sendbuf,plan[planstep],8);   //������ֱ��װ�봮��1�ķ���
								USART2_SendBuf485(usart2_sendbuf,8);       //Rs-485
								usart2_rec=start;                      //����Usart2
								Usart2_overtime=RECEovertime2;
								readmotorflag=false;                   //��ͣ���ڶ�motor����
								readmotortime=READMOTORTIME;
							}
						}
						else
						{
							if(PVspeed>SVspeed*0.7)    //��ʼ����
							{
								if(PVspeed<SVspeed*1.2) PVtime_flag=true;
								else                    PVtime_flag=false;
								if(modeNo==1&&play_flag==1&&runstep1==3&&PVspeed<SVspeed*1.1)  //ģʽһ���� 0��δ����  1������˨����  2����˨��ʱ2��   3�����������������    4���ȴ��ٶȴ��   5������˨����   6���ȴ�����   7��������ʱ��ͣ��
								{
									runstep1=5;
									neworder=true;
								}
								else if(modeNo==2&&play_flag==1&&step==5&&runstep2==5&&PVspeed<SVspeed*1.1) //ģʽ������ 0��δ����  1��������������  2����������ʱ3��   3������˨����  4����˨��ʱ2��   5�����������������    6��step5�ȴ��ٶȴ��   7������˨����   8���ȴ�����   9��������ʱ��ͣ��  10��������������
								{
									runstep2=7;
									neworder=true;
								}
							}
							else if(PVspeed==0&&play_flag==1&&bolt_speedtime==0)  //�ж�˨��
							{
								if(modeNo==1&&runstep1==6)  //if(modeNo==1&&runstep1==5)
								{
									runstep1=7;
									neworder=true;
								}
								
								if(modeNo==2&&step==5&&runstep2==8)
								{
									runstep2=9;
									neworder=true;
								}
							}
							else if(PVspeed<2&&play_flag==2)  //�ж�ͣ��
							{
								if(modeNo==1) //0��ϵͳ���� 1������  2���ಽ 3.����
								{
									play_flag=0;
									PVtime_flag=false;
									startwork=0;
									if(runstep1==6) process=4;  //�����ж�����δ����
									runstep1=0;
									process++;
								}
								else if(modeNo==2)
								{
									if(runstep2==8) process=4;  //�����ж�����δ����
									runstep2=10;
									neworder=true;
									play_flag=0;
									PVtime_flag=false;
								}
								
							}
						 }
					 }

											memset(usart2_recebuf,0,wordsize2_rece);
											Usart2_overtime=RECEovertime2; 
											readmotortime=READMOTORTIME;
										break;
										 
					case 0x05:if(memcmp(usart2_recebuf,usart2_sendbuf,wordsize2_rece)==0)  //�Ƚ��ڴ�
										{
											if(modeNo==1) //if(modeNo==1&&runstep1==1)ģʽһ���� 0��δ����  1������˨����  2����˨��ʱ2��   3�����������������    4���ȴ��ٶȴ��   5������˨����   6���ȴ�����   7��������ʱ��ͣ��
											{
												if(runstep1==1)
												{
													runstep1=2;
													bolttime=50;  //bolttime=200;
												}
												else if(runstep1==5) runstep1=6;
											}
											if(modeNo==2) //ģʽ������ 0��δ����  1��������������  2����������ʱ3��   3������˨����  4����˨��ʱ2��   5�����������������    6��step5�ȴ��ٶȴ��   7������˨����   8���ȴ�����   9��������ʱ��ͣ��  10��������������
											{
												if(runstep2==1)
												{
													runstep2=2;
													pumptime=10;//pumptime=300;
												}
												else if(runstep2==3)
												{
													runstep2=4;
													bolttime=50;  //bolttime=200;
												}
												else if(runstep2==7)
												{
													runstep2=8;
												}
												else if(runstep2==10)
												{
													runstep2=0;
													startwork=0;
													process++;
												}
											}
										}
										readmotorflag=true;
										readmotortime=READMOTORTIME;
										memset(usart2_recebuf,0,wordsize2_rece);
										break;
					
					case 0x06:
										if(memcmp(usart2_recebuf,usart2_sendbuf,wordsize2_rece)==0)  //�Ƚ��ڴ�
										{
											//������һ�����
											if(planstep<6)
											{
												if(planstep==5) delay_ms(150);
												else            delay_ms(50);
												planstep++;
												memcpy(usart2_sendbuf,plan[planstep],8);   //������ֱ��װ�봮��1�ķ���
												USART2_SendBuf485(usart2_sendbuf,8);       //Rs-485
												usart2_rec=start;                      //����Usart2
												Usart2_overtime=RECEovertime2;
												readmotorflag=false;                   //��ͣ���ڶ�motor����
												memset(usart2_recebuf,0,wordsize2_rece);
											}
											else if(planstep==6||planstep==7)
											{
												readmotorflag=true;
												readmotortime=READMOTORTIME;
												memset(usart2_recebuf,0,wordsize2_rece);
											}
										}
											
										break;
				}
			}else  //У��ʧ��
					{
						memset(usart2_recebuf,0,wordsize2_rece); //��δ��֤
						buf2mumber=0;
						Usart2_overtime=RECEovertime2; 
						
						usart2_rec=start;         //У��ʧ�ܣ�����Usart2��ʱ��ʱ
						if(usart2_sendbuf[1]==3)  //У��ʧ��  ����Ƕ���������ʱ�ٶ�
						{
							erro_count++;
							readmotorflag=true;
							readmotortime=READMOTORTIME;
						}
					}
		}	


		//����1���ճ�ʱ
		if(Usart1_overtime==0)
		{
			memset(usart1_recebuf,0,wordsize1_rece);
			buf1mumber=0;
			Usart1_overtime=RECEovertime1; 
//			usart1_rec=fail;             //��ʽ��Ҫ���볬ʱ����
			usart1_rec=stop; 	
		}
		
			//����2���ճ�ʱ
		if(Usart2_overtime==0)
		{
			erro_count++;
			memset(usart2_recebuf,0,wordsize2_rece);
			buf2mumber=0;
			Usart2_overtime=RECEovertime2; 
			usart2_rec=stop;
			if(erro_count<4)
			{
        USART2_SendBuf485(usart2_sendbuf,8);       //Rs-485
				usart2_rec=start;                          //����Usart2				
		  }
			else
			{

				erroNO=0xFFFF;
				readmotorflag=false;
				modeNo=3;
			}
		}

		
	}	 
 }

