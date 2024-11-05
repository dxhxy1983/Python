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
	a=CalcCrc(temp8,g);       //计算校验值
	temp8[g]=a&0xFF;
	temp8[g+1]=a>>8;
	memcpy(temp16,temp8,g+2);   //
	//从新写入flash
	FLASH_Unlock();						//解锁
	FLASH_ErasePage(addr1);   //擦除页，范围包含addr2
	STMFLASH_Write_NoCheck(addr1,temp16,g/2+1);
	STMFLASH_Write_NoCheck(addr2,temp16,g/2+1);
	FLASH_Lock();//上锁
}

void RebuildParameter(struct DEVICEPARAMETER DP,u32 addr1,u32 addr2)
{
	char temp8[60];
	u16 temp16[30];
	memcpy(temp8,&DP,(sizeof(DP)-2));   //
	DP.Crc16=CalcCrc(temp8,(sizeof(DP)-2));    //计算校验值
	memcpy(temp16,&DP,sizeof(DP));   //
	//从新写入flash
	FLASH_Unlock();						//解锁
	FLASH_ErasePage(addr1);   //擦除页，范围包含addr2
	STMFLASH_Write_NoCheck(addr1,temp16,sizeof(DP)/2);
	STMFLASH_Write_NoCheck(addr2,temp16,sizeof(DP)/2);
	FLASH_Lock();//上锁
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
//	char speed_n=0;     //当前速度累计计数
//	u16  speed_s=0;     //当前速度累计值
	char erro_count=0;  //
	u16  startwork=0;  //启停指令
	char S_formula=1;  //显示配方编号
	u16  erroNO;       //错误编号
	 
	delay_init();	    	 //延时函数初始化	
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2); //设置NVIC中断分组2:2位抢占优先级，2位响应优先级

// 	LED_Init();			     //LED端口初始化
//	KEY_Init();          //初始化与按键连接的硬件接口
	time_conf();
	DIR1_Init();           //PA.8 输出低，令usart1-485处于接收状态
	DIR2_Init();           //PA.1 输出低，令usart2-485处于接收状态
	
	
//读配置参数
	DeviceParameter=*(struct DEVICEPARAMETER*)ParameterAddr3;
	memcpy(BPbuf,&DeviceParameter,(sizeof(DeviceParameter)-2));   //
//校验
  t=CalcCrc(BPbuf,(sizeof(DeviceParameter)-2));    //计算校验值
	if(t==DeviceParameter.Crc16)
	{
		DeviceAddress=DeviceParameter.Addr;
		usartbound1=DeviceParameter.Bound1;
    usartbound2=DeviceParameter.Bound2;  
	}else
	{
		DeviceParameter=*(struct DEVICEPARAMETER*)ParameterAddr4;
	  memcpy(BPbuf,&DeviceParameter,(sizeof(DeviceParameter)-2));   //
//校验
   t=CalcCrc(BPbuf,(sizeof(DeviceParameter)-2));    //计算校验值
	 if(t==DeviceParameter.Crc16)
	  {
		  DeviceAddress=DeviceParameter.Addr;
		  usartbound1=DeviceParameter.Bound1;
			usartbound2=DeviceParameter.Bound2;
//			if(DeviceParameter.Addr>0&&DeviceParameter.Bound1>0&&DeviceParameter.Bound2>0)
      RebuildParameter(DeviceParameter,ParameterAddr3,ParameterAddr4);  //从新写入flash
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
	
	 
//初始化系统默认参数
   runparameter[0][1].acc=1000;  //减速度
	 runparameter[0][1].speed=1;  //语言    1.中文   2.英文
	 runparameter[0][1].time=2;   //蜂鸣器  1.开     2.关

//读配置参数
	memcpy(BPbuf,(char*)ParameterAddr1,(buflong+2));   //
//校验
  t=CalcCrc(BPbuf,buflong);    //计算校验值
	if(t==BPbuf[buflong+1]*256+BPbuf[buflong])
	{
		memcpy(runparameter,BPbuf,buflong); 
	}else
	{
	 memcpy(BPbuf,(char*)ParameterAddr2,(buflong+2));  //
//校验
   t=CalcCrc(BPbuf,buflong);    //计算校验值
	 if(t==BPbuf[buflong+1]*256+BPbuf[buflong])
	  {
			memcpy(runparameter,BPbuf,buflong); 
      RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
	  }
   }

	 
	 //初始化固定参数
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
	uart_init(usartbound1);	 //串口初始化
	uart2_init(usartbound2);

//	LCD_Init();


//------------------------------- 
	 
//设置初始状态  单步	 
	 play_flag=0;      //运行中标志，0:未运行，1：运行中，2停车中
	 set_flag=false;   //非设置
	 modeNo=1;         ////0：系统参数 1：单步  2：多步 3.报错
	 formula=0,step=0; //配方编号0，步骤编号0
	 
	 readmotorflag=true;          //开始通信
	 readmotortime=READMOTORTIME;
	 
	 
 	while(1)
	{
		#ifdef IWDG_START
        IWDG_ReloadCounter();
    #endif
				

//		if(flish_time==0)
//		{
//			flish_time=FLISHTIME; //闪烁时间间隔
//			shadow=(shadow+1)&0x01;//求反
//			Showsetsite(setsite,shadow);
//		}
		
		if(readmotortime==0)
		{
			if(modeNo!=3)                   //0：系统参数 1：单步  2：多步 3.报错
			{
				readmotorflag=false;          //暂停周期读motor操作
				readmotortime=READMOTORTIME;
				
				//运行时间=0
				if(PVtime==0&&play_flag==1)   //play_flag运行中标志，0:未运行，1：运行中，2停车中
				{
					if(modeNo==1)
					{
						stopmotor();  //停车  电机串口
						//if(runstep1==6) process=3;  //判断未锁定
					}
					else if(modeNo==2)
					{
						if(step==5)
						{
							stopmotor();  //停车  电机串口
							//if(runstep2==8) process=3;  //判断未锁定
						}
						else
						{
							step++;
							if(runparameter[formula][step].time!=0&&runparameter[formula][step].acc!=0&&runparameter[formula][step].speed!=0) 
							{
								writeplanbuf();
								SVspeed=runparameter[formula][step].speed;
							}
							else sendresdmotor(); //循环读电机状态  电机串口
						}
					}
				}
				
				//运行时间 !=0
				else
				{
					sendresdmotor(); //循环读电机状态   电机串口
				
				}
				
				
				
		  }
			else 
			{
				stopmotor();  //停车   电机串口
				readmotorflag=true;            //周期读motor操作
				readmotortime=READMOTORTIME;
			}
	  }
		
		//模式一步骤 0：未启动  1：发开栓命令  2：开栓延时2秒   3：发送启动电机命令    4：等待速度达标   5：发挂栓命令   6：等待降速   7：清运行时间停机
		//模式二步骤 0：未启动  1：发开气泵命令  2：开气泵延时3秒   3：发开栓命令  4：开栓延时2秒   5：发送启动电机命令    6：step5等待速度达标   7：发挂栓命令   8：等待降速   9：清运行时间停机  10：发关气泵命令
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
			if(startwork==0)           //play_flag运行中标志，0:未运行，1：运行中，2停车中     startwork 启停指令
			{
				if(play_flag==1)
				{
					PVtime=0;					
					if(modeNo==2) step=5;   // modeNo  0：系统参数 1：单步  2：多步 3.报错
					plansteplong=7;
					readmotorflag=true;                   //周期读motor操作
					readmotortime=READMOTORTIME;
				}
				else if((play_flag==0)&&(modeNo==2)&&(runstep2==10))
				{
					readmotorflag=false;                   //暂停周期读motor操作
					readmotortime=READMOTORTIME;
					delay_ms(150);
					memset(usart2_recebuf,0,wordsize2_rece); //清理串口2
					buf2mumber=0;
					Usart2_overtime=RECEovertime2; 
					usart2_rec=stop;
					
					pumporder=0x00;
					writepumpbuf(pumporder);
				}
			}
			
			else if((startwork==0xFF)&&(runstep1||runstep2))
			{
				readmotorflag=false;                   //暂停周期读motor操作
				readmotortime=READMOTORTIME;
				delay_ms(150);
				memset(usart2_recebuf,0,wordsize2_rece); //清理串口2
				buf2mumber=0;
				Usart2_overtime=RECEovertime2; 
				usart2_rec=stop;
				
				if(modeNo==1)
				{
					switch(runstep1)  //模式一步骤 0：未启动  1：发开栓命令  2：开栓延时2秒   3：发送启动电机命令    4：等待速度达标   5：发挂栓命令   6：等待降速   7：清运行时间停机
					{
						case 1:	boltorder=0x00;  //boltorder=0xFF;
						        writeboltbuf(boltorder);
										break;
						
						case 3:	formula=0,step=0;  //配方编号，步骤编号 
										SVspeed=runparameter[formula][step].speed;
										SVtime=runparameter[formula][step].time;
										
										writeplanbuf();    //加载数据并发送第一组数据
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
					switch(runstep2) //模式二步骤 0：未启动  1：发开气泵命令  2：开气泵延时3秒   3：发开栓命令  4：开栓延时2秒   5：发送启动电机命令    6：step5等待速度达标   7：发挂栓命令   8：等待降速   9：清运行时间停机  10：发关气泵命令
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
						
										writeplanbuf();    //加载数据并发送第一组数据
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
			else readmotorflag=true;            //周期读motor操作
		}


		//校验串口1收到的 *MODBUS-RTU命令格式* 的数据
				if((usart1check==stop)&&(usart1_rec==succeed))
		{
			u16 test;
			u16 StartAddress,RegisterNumber,NuAddress;
			
			usart1check=start;
      usart1check=stop;                        //串口1接收数据校验
			buf1mumber=0;                            //串口1接收buf数组计
			usart1_rec=stop;                         //串口1接收状态	
			
			usart1_recebuf[0]=DeviceAddress;         //加入本机地址一同校验
			test=CalcCrc(usart1_recebuf,(wordsize1_rece-2));    //计算校验值
			//-------本机地址-------			
			if((usart1_recebuf[wordsize1_rece-2]+usart1_recebuf[wordsize1_rece-1]*256)==test)   //校验正确&&本机地址正确
			{
				delay_ms(2);
				
				if(usart1_recebuf[1]!=0x10)
				{
					memcpy(&ModbusRtu_order,usart1_recebuf,wordsize1_rece);   //将串口1收到的数据装入解析结构体
				  StartAddress=ModbusRtu_order.StartAddressH*256+ModbusRtu_order.StartAddressL;		      //合并开始地址	
				  RegisterNumber=ModbusRtu_order.RegisterNumberH*256+ModbusRtu_order.RegisterNumberL;   //合并（寄存器数量/写入参数）
				
					if(ModbusRtu_order.FunctionCode==0x03)
					{
						char i,n;
						usart1_sendbuf[0]=DeviceAddress;
						usart1_sendbuf[1]=0x03;
						usart1_sendbuf[2]=2*RegisterNumber;
						n=2;
						for(i=0;i<RegisterNumber;i++)
						{
						 switch (StartAddress)         //循环添加寄存器数据   V_power,I_hot,L_vacuum,I_motor
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
							 
							 case 0x0100:usart1_sendbuf[n+1]=runparameter[0][1].acc>>8;      //系统减速度
													 usart1_sendbuf[n+2]=runparameter[0][1].acc&0x00FF;
													 break;
							 case 0x0101:usart1_sendbuf[n+1]=startwork>>8;      //启停指令
													 usart1_sendbuf[n+2]=startwork&0x00FF;
													 break;
							 case 0x0102:usart1_sendbuf[n+1]=modeNo>>8;         //运行模式 0：系统参数 1：单步  2：多步 3.报错
													 usart1_sendbuf[n+2]=modeNo&0x00FF;
													 break;
							 case 0x0103:usart1_sendbuf[n+1]=S_formula>>8;      //配方编号
													 usart1_sendbuf[n+2]=S_formula&0x00FF;
													 break;
						   case 0x0104:usart1_sendbuf[n+1]=step>>8;           //步骤编号
													 usart1_sendbuf[n+2]=step&0x00FF;
													 break;
							 case 0x0105:usart1_sendbuf[n+1]=play_flag>>8;      //运行中标志，0:未运行，1：运行中，2停车中
													 usart1_sendbuf[n+2]=play_flag&0x00FF;
													 break;
							 case 0x0106:usart1_sendbuf[n+1]=PVspeed>>8;        //当前速度
													 usart1_sendbuf[n+2]=PVspeed&0x00FF;
													 break;
							 case 0x0107:usart1_sendbuf[n+1]=PVtime>>8;         //剩余时长
													 usart1_sendbuf[n+2]=PVtime&0x00FF;
													 break;
							 case 0x0108:usart1_sendbuf[n+1]=erroNO>>8;         //错误编号
													 usart1_sendbuf[n+2]=erroNO&0x00FF;
													 break;
							 case 0x0109:usart1_sendbuf[n+1]=process>>8;         //流程
													 usart1_sendbuf[n+2]=process&0x00FF;
													 break;
							 case 0x010A:usart1_sendbuf[n+1]=runstep1>>8;        //初始化进程
													 usart1_sendbuf[n+2]=runstep1&0x00FF;
													 break;
							 case 0x010B:usart1_sendbuf[n+1]=runstep2>>8;        //匀胶进程
													 usart1_sendbuf[n+2]=runstep2&0x00FF;
													 break; 
							 case 0x1000:usart1_sendbuf[n+1]=runparameter[0][0].speed>>8;        //转速
													 usart1_sendbuf[n+2]=runparameter[0][0].speed&0x00FF;
													 break;
							 case 0x1001:usart1_sendbuf[n+1]=runparameter[0][0].time>>8;         //旋转时长
													 usart1_sendbuf[n+2]=runparameter[0][0].time&0x00FF;
													 break;
							 case 0x1002:usart1_sendbuf[n+1]=runparameter[0][0].acc>>8;         //加速度
													 usart1_sendbuf[n+2]=runparameter[0][0].acc&0x00FF;
													 break;
													 
			        
							//A配方:共 5步
							//第一步：
							case 0x1100://转速
													usart1_sendbuf[n+1]=runparameter[1][1].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[1][1].speed&0x00FF;
													break;
							case 0x1101://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[1][1].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[1][1].time&0x00FF;
													break;
							case 0x1102://加速度
													usart1_sendbuf[n+1]=runparameter[1][1].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[1][1].acc&0x00FF;
													break;
								
							//第二步：
							case 0x1103://转速
													usart1_sendbuf[n+1]=runparameter[1][2].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[1][2].speed&0x00FF;
													break;
							case 0x1104://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[1][2].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[1][2].time&0x00FF;
													break;
							case 0x1105://加速度
													usart1_sendbuf[n+1]=runparameter[1][2].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[1][2].acc&0x00FF;
													break;
							//第三步：
							case 0x1106://转速
													usart1_sendbuf[n+1]=runparameter[1][3].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[1][3].speed&0x00FF;
													break;
							case 0x1107://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[1][3].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[1][3].time&0x00FF;
													break;
							case 0x1108://加速度
								          usart1_sendbuf[n+1]=runparameter[1][3].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[1][3].acc&0x00FF;
													break;
							//第四步：
							case 0x1109://转速
													usart1_sendbuf[n+1]=runparameter[1][4].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[1][4].speed&0x00FF;
													break;
							case 0x110A://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[1][4].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[1][4].time&0x00FF;
													break;
							case 0x110B://加速度
													usart1_sendbuf[n+1]=runparameter[1][4].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[1][4].acc&0x00FF;
													break;
							//第五步：
							case 0x110C://转速
													usart1_sendbuf[n+1]=runparameter[1][5].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[1][5].speed&0x00FF;
													break;
							case 0x110D://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[1][5].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[1][5].time&0x00FF;
													break;
							case 0x110E://加速度										 
													usart1_sendbuf[n+1]=runparameter[1][5].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[1][5].acc&0x00FF;
													break;
							
							//B配方:共 5步
							//第一步：
							case 0x1200://转速
													usart1_sendbuf[n+1]=runparameter[2][1].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[2][1].speed&0x00FF;
													break;
							case 0x1201://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[2][1].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[2][1].time&0x00FF;
													break;
							case 0x1202://加速度
													usart1_sendbuf[n+1]=runparameter[2][1].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[2][1].acc&0x00FF;
													break;
								
							//第二步：
							case 0x1203://转速
													usart1_sendbuf[n+1]=runparameter[2][2].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[2][2].speed&0x00FF;
													break;
							case 0x1204://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[2][2].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[2][2].time&0x00FF;
													break;
							case 0x1205://加速度
													usart1_sendbuf[n+1]=runparameter[2][2].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[2][2].acc&0x00FF;
													break;
							//第三步：
							case 0x1206://转速
													usart1_sendbuf[n+1]=runparameter[2][3].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[2][3].speed&0x00FF;
													break;
							case 0x1207://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[2][3].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[2][3].time&0x00FF;
													break;
							case 0x1208://加速度
								          usart1_sendbuf[n+1]=runparameter[2][3].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[2][3].acc&0x00FF;
													break;
							//第四步：
							case 0x1209://转速
													usart1_sendbuf[n+1]=runparameter[2][4].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[2][4].speed&0x00FF;
													break;
							case 0x120A://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[2][4].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[2][4].time&0x00FF;
													break;
							case 0x120B://加速度
													usart1_sendbuf[n+1]=runparameter[2][4].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[2][4].acc&0x00FF;
													break;
							//第五步：
							case 0x120C://转速
													usart1_sendbuf[n+1]=runparameter[2][5].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[2][5].speed&0x00FF;
													break;
							case 0x120D://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[2][5].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[2][5].time&0x00FF;
													break;
							case 0x120E://加速度										 
													usart1_sendbuf[n+1]=runparameter[2][5].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[2][5].acc&0x00FF;
													break;
	
							//C配方:共 5步
							//第一步：
							case 0x1300://转速
													usart1_sendbuf[n+1]=runparameter[3][1].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[3][1].speed&0x00FF;
													break;
							case 0x1301://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[3][1].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[3][1].time&0x00FF;
													break;
							case 0x1302://加速度
													usart1_sendbuf[n+1]=runparameter[3][1].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[3][1].acc&0x00FF;
													break;
								
							//第二步：
							case 0x1303://转速
													usart1_sendbuf[n+1]=runparameter[3][2].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[3][2].speed&0x00FF;
													break;
							case 0x1304://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[3][2].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[3][2].time&0x00FF;
													break;
							case 0x1305://加速度
													usart1_sendbuf[n+1]=runparameter[3][2].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[3][2].acc&0x00FF;
													break;
							//第三步：
							case 0x1306://转速
													usart1_sendbuf[n+1]=runparameter[3][3].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[3][3].speed&0x00FF;
													break;
							case 0x1307://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[3][3].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[3][3].time&0x00FF;
													break;
							case 0x1308://加速度
								          usart1_sendbuf[n+1]=runparameter[3][3].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[3][3].acc&0x00FF;
													break;
							//第四步：
							case 0x1309://转速
													usart1_sendbuf[n+1]=runparameter[3][4].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[3][4].speed&0x00FF;
													break;
							case 0x130A://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[3][4].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[3][4].time&0x00FF;
													break;
							case 0x130B://加速度
													usart1_sendbuf[n+1]=runparameter[3][4].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[3][4].acc&0x00FF;
													break;
							//第五步：
							case 0x130C://转速
													usart1_sendbuf[n+1]=runparameter[3][5].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[3][5].speed&0x00FF;
													break;
							case 0x130D://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[3][5].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[3][5].time&0x00FF;
													break;
							case 0x130E://加速度										 
													usart1_sendbuf[n+1]=runparameter[3][5].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[3][5].acc&0x00FF;
													break;
							
							//D配方:共 5步
							//第一步：
							case 0x1400://转速
													usart1_sendbuf[n+1]=runparameter[4][1].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[4][1].speed&0x00FF;
													break;
							case 0x1401://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[4][1].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[4][1].time&0x00FF;
													break;
							case 0x1402://加速度
													usart1_sendbuf[n+1]=runparameter[4][1].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[4][1].acc&0x00FF;
													break;
								
							//第二步：
							case 0x1403://转速
													usart1_sendbuf[n+1]=runparameter[4][2].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[4][2].speed&0x00FF;
													break;
							case 0x1404://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[4][2].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[4][2].time&0x00FF;
													break;
							case 0x1405://加速度
													usart1_sendbuf[n+1]=runparameter[4][2].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[4][2].acc&0x00FF;
													break;
							//第三步：
							case 0x1406://转速
													usart1_sendbuf[n+1]=runparameter[4][3].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[4][3].speed&0x00FF;
													break;
							case 0x1407://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[4][3].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[4][3].time&0x00FF;
													break;
							case 0x1408://加速度
								          usart1_sendbuf[n+1]=runparameter[4][3].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[4][3].acc&0x00FF;
													break;
							//第四步：
							case 0x1409://转速
													usart1_sendbuf[n+1]=runparameter[4][4].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[4][4].speed&0x00FF;
													break;
							case 0x140A://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[4][4].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[4][4].time&0x00FF;
													break;
							case 0x140B://加速度
													usart1_sendbuf[n+1]=runparameter[4][4].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[4][4].acc&0x00FF;
													break;
							//第五步：
							case 0x140C://转速
													usart1_sendbuf[n+1]=runparameter[4][5].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[4][5].speed&0x00FF;
													break;
							case 0x140D://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[4][5].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[4][5].time&0x00FF;
													break;
							case 0x140E://加速度										 
													usart1_sendbuf[n+1]=runparameter[4][5].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[4][5].acc&0x00FF;
													break;
							
							//E配方:共 5步
							//第一步：
							case 0x1500://转速
													usart1_sendbuf[n+1]=runparameter[5][1].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[5][1].speed&0x00FF;
													break;
							case 0x1501://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[5][1].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[5][1].time&0x00FF;
													break;
							case 0x1502://加速度
													usart1_sendbuf[n+1]=runparameter[5][1].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[5][1].acc&0x00FF;
													break;
								
							//第二步：
							case 0x1503://转速
													usart1_sendbuf[n+1]=runparameter[5][2].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[5][2].speed&0x00FF;
													break;
							case 0x1504://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[5][2].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[5][2].time&0x00FF;
													break;
							case 0x1505://加速度
													usart1_sendbuf[n+1]=runparameter[5][2].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[5][2].acc&0x00FF;
													break;
							//第三步：
							case 0x1506://转速
													usart1_sendbuf[n+1]=runparameter[5][3].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[5][3].speed&0x00FF;
													break;
							case 0x1507://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[5][3].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[5][3].time&0x00FF;
													break;
							case 0x1508://加速度
								          usart1_sendbuf[n+1]=runparameter[5][3].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[5][3].acc&0x00FF;
													break;
							//第四步：
							case 0x1509://转速
													usart1_sendbuf[n+1]=runparameter[5][4].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[5][4].speed&0x00FF;
													break;
							case 0x150A://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[5][4].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[5][4].time&0x00FF;
													break;
							case 0x150B://加速度
													usart1_sendbuf[n+1]=runparameter[5][4].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[5][4].acc&0x00FF;
													break;
							//第五步：
							case 0x150C://转速
													usart1_sendbuf[n+1]=runparameter[5][5].speed>>8;        //转速
													usart1_sendbuf[n+2]=runparameter[5][5].speed&0x00FF;
													break;
							case 0x150D://旋转时长（秒）
													usart1_sendbuf[n+1]=runparameter[5][5].time>>8;         //旋转时长
													usart1_sendbuf[n+2]=runparameter[5][5].time&0x00FF;
													break;
							case 0x150E://加速度										 
													usart1_sendbuf[n+1]=runparameter[5][5].acc>>8;         //加速度
													usart1_sendbuf[n+2]=runparameter[5][5].acc&0x00FF;
													break;
							
							 default: usart1_sendbuf[n+1]=0x00;
												usart1_sendbuf[n+2]=0x00;
											 break;
						 }
						 StartAddress++;
						 n=n+2;
						}
						test=CalcCrc(usart1_sendbuf,n+1);    //计算校验值
						usart1_sendbuf[n+1]=test&0x00FF;
						usart1_sendbuf[n+2]=test>>8;
						
						//回复上位机
						USART1_SendBuf485(usart1_sendbuf,n+3);   //RS-485  

					 }

						else if(ModbusRtu_order.FunctionCode==0x06)
						{
							
							switch (StartAddress)
							{
//								case 0x0000:    //更改本机地址
//														if(RegisterNumber<255&&RegisterNumber>0)
//														{	
//															DeviceParameter.Addr=RegisterNumber;
//															DeviceAddress=RegisterNumber;
//															//回应上位机
//															memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//															USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//															//从新写入flash
//															if(DeviceParameter.Addr>0&&DeviceParameter.Bound1>0&&DeviceParameter.Bound2>0)
//															RebuildParameter(DeviceParameter,ParameterAddr3,ParameterAddr4);  //从新写入flash
//														}
//														break;
//								
//								case 0x0001:   //更改串口波特率
//														if(1==RegisterNumber) DeviceParameter.Bound=9600;
//														else if(2==RegisterNumber) DeviceParameter.Bound=19200;
//														else if(3==RegisterNumber) DeviceParameter.Bound=38400;
//														else if(4==RegisterNumber) DeviceParameter.Bound=115200;
//														else break;
//														usartbound1=DeviceParameter.Bound;
//														//回应上位机
//														memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//														USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//														//从新写入flash
//														if(DeviceParameter.Addr>0&&DeviceParameter.Bound1>0&&DeviceParameter.Bound2>0)
//														RebuildParameter(DeviceParameter,ParameterAddr3,ParameterAddr4);  //从新写入flash
//														uart_init(usartbound1);	 //串口初始化
//														break;
								
								case 0x0100:   //减速度
														runparameter[0][1].acc=RegisterNumber;
														//从新写入flash
														RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
														//回应上位机
														memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
														USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
														break;
							  case 0x0101:   //启停
														if(RegisterNumber==0||RegisterNumber==0xFF)
														{
														  startwork=RegisterNumber;
															neworder=true;
															if(startwork&&(play_flag==0)&&(PVspeed<2))  // if(startwork&&(runstep1==0)&&(runstep2==0))
															{
																if(modeNo==1) runstep1=1;
																else if(modeNo==2) runstep2=1;
																process=1;  //流程标识   0：开机初始状态   1：收到开始命令进入流程    2：正常结束   3：中途收到停止命令    4：中途停止
															}
															if(play_flag==0&&startwork==0&&PVspeed>2)  play_flag=1;
															if(play_flag&&startwork==0)  process=3;   //流程标识   0：开机初始状态   1：收到开始命令进入流程    2：正常结束   3：中途收到停止命令    4：中途停止
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
														//回应上位机
														memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
														USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
														break;
								case 0x0102:   //工作模式：1：单步，2：多步，3：报错，0：系统参数
														if(play_flag==0) modeNo=RegisterNumber;
														//回应上位机
														memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
														USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
														break;															
								case 0x0103:   //配方编号
														S_formula=RegisterNumber;
														//回应上位机
														memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
														USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
														break;
//								case 0x1000:   //单步转速
//														runparameter[0][0].speed=RegisterNumber;
//														//回应上位机
//														memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//														USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//														break;
//								case 0x1001:   //单步旋转时长
//														runparameter[0][0].time=RegisterNumber;
//														//回应上位机
//														memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//														USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//														break;
//								case 0x1002:   //单步加速度
//														runparameter[0][0].acc=RegisterNumber;
//														RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
//														//回应上位机
//														memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//														USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//														break;
								
								
							//A配方:共 5步
							//第一步：
							case 0x1100://转速
													runparameter[1][1].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
							            break;
							case 0x1101://旋转时长（秒）
													runparameter[1][1].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1102://加速度
													runparameter[1][1].acc=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
								          break;
							//第二步：
							case 0x1103://转速
													runparameter[1][2].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1104://旋转时长（秒）
													runparameter[1][2].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1105://加速度
													runparameter[1][2].acc=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//第三步：
							case 0x1106://转速
													runparameter[1][3].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1107://旋转时长（秒）
													runparameter[1][3].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1108://加速度
								          runparameter[1][3].acc=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//第四步：
							case 0x1109://转速
													runparameter[1][4].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x110A://旋转时长（秒）
													runparameter[1][4].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x110B://加速度
													runparameter[1][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
//							//第五步：
//							case 0x110C://转速
//													runparameter[1][5].speed=RegisterNumber;
//													//回应上位机
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x110D://旋转时长（秒）
//													runparameter[1][5].time=RegisterNumber;
//													//回应上位机
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x110E://加速度										 
//													runparameter[1][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
//													//回应上位机
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
								
							//B配方:共 5步
							//第一步：
							case 0x1200://转速
													runparameter[2][1].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
							            break;
							case 0x1201://旋转时长（秒）
													runparameter[2][1].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1202://加速度
													runparameter[2][1].acc=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
								          break;
							//第二步：
							case 0x1203://转速
													runparameter[2][2].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1204://旋转时长（秒）
													runparameter[2][2].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1205://加速度
													runparameter[2][2].acc=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//第三步：
							case 0x1206://转速
													runparameter[2][3].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1207://旋转时长（秒）
													runparameter[2][3].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1208://加速度
								          runparameter[2][3].acc=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//第四步：
							case 0x1209://转速
													runparameter[2][4].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x120A://旋转时长（秒）
													runparameter[2][4].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x120B://加速度
													runparameter[2][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
//							//第五步：
//							case 0x120C://转速
//													runparameter[2][5].speed=RegisterNumber;
//													//回应上位机
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x120D://旋转时长（秒）
//													runparameter[2][5].time=RegisterNumber;
//													//回应上位机
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x120E://加速度										 
//													runparameter[2][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
//													//回应上位机
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
							
							//C配方:共 5步
							//第一步：
							case 0x1300://转速
													runparameter[3][1].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
							            break;
							case 0x1301://旋转时长（秒）
													runparameter[3][1].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1302://加速度
													runparameter[3][1].acc=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
								          break;
							//第二步：
							case 0x1303://转速
													runparameter[3][2].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1304://旋转时长（秒）
													runparameter[3][2].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1305://加速度
													runparameter[3][2].acc=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//第三步：
							case 0x1306://转速
													runparameter[3][3].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1307://旋转时长（秒）
													runparameter[3][3].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1308://加速度
								          runparameter[3][3].acc=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//第四步：
							case 0x1309://转速
													runparameter[3][4].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x130A://旋转时长（秒）
													runparameter[3][4].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x130B://加速度
													runparameter[3][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
//							//第五步：
//							case 0x130C://转速
//													runparameter[3][5].speed=RegisterNumber;
//													//回应上位机
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x130D://旋转时长（秒）
//													runparameter[3][5].time=RegisterNumber;
//													//回应上位机
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x130E://加速度										 
//													runparameter[3][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
//													//回应上位机
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
							
							//D配方:共 5步
							//第一步：
							case 0x1400://转速
													runparameter[4][1].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
							            break;
							case 0x1401://旋转时长（秒）
													runparameter[4][1].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1402://加速度
													runparameter[4][1].acc=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
								          break;
							//第二步：
							case 0x1403://转速
													runparameter[4][2].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1404://旋转时长（秒）
													runparameter[4][2].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1405://加速度
													runparameter[4][2].acc=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//第三步：
							case 0x1406://转速
													runparameter[4][3].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1407://旋转时长（秒）
													runparameter[4][3].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1408://加速度
								          runparameter[4][3].acc=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//第四步：
							case 0x1409://转速
													runparameter[4][4].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x140A://旋转时长（秒）
													runparameter[4][4].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x140B://加速度
													runparameter[4][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
//							//第五步：
//							case 0x140C://转速
//													runparameter[4][5].speed=RegisterNumber;
//													//回应上位机
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x140D://旋转时长（秒）
//													runparameter[4][5].time=RegisterNumber;
//													//回应上位机
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x140E://加速度										 
//													runparameter[4][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
//													//回应上位机
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
							
							//E配方:共 5步
							//第一步：
							case 0x1500://转速
													runparameter[5][1].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
							            break;
							case 0x1501://旋转时长（秒）
													runparameter[5][1].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1502://加速度
													runparameter[5][1].acc=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
								          break;
							//第二步：
							case 0x1503://转速
													runparameter[5][2].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1504://旋转时长（秒）
													runparameter[5][2].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1505://加速度
													runparameter[5][2].acc=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//第三步：
							case 0x1506://转速
													runparameter[5][3].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1507://旋转时长（秒）
													runparameter[5][3].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x1508://加速度
								          runparameter[5][3].acc=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							//第四步：
							case 0x1509://转速
													runparameter[5][4].speed=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x150A://旋转时长（秒）
													runparameter[5][4].time=RegisterNumber;
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
							case 0x150B://加速度
													runparameter[5][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
													//回应上位机
													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
													break;
//							//第五步：
//							case 0x150C://转速
//													runparameter[5][5].speed=RegisterNumber;
//													//回应上位机
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x150D://旋转时长（秒）
//													runparameter[5][5].time=RegisterNumber;
//													//回应上位机
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
//							case 0x150E://加速度										 
//													runparameter[5][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
//													//回应上位机
//													memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
//													USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
//													break;
							
								default: break;
							}
						}
					 }
				
			 
				 else if(usart1_recebuf[1]==0x10)   //多个数据设置  下位机对应06命令   0x10协议解析
				 {
					 	char i,n=7;
			  
						StartAddress=usart1_recebuf[2]*256+usart1_recebuf[3];		  //合并开始地址	
						NuAddress=usart1_recebuf[5]+usart1_recebuf[4]*256;	          //寄存器数量
						n=7;
					
						for(i=0;i<NuAddress;i++)
						{
							switch (StartAddress)
							{
								case 0x0100:   //减速度
														runparameter[0][1].acc=RegisterNumber;
														//从新写入flash
														RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
										        break;
								case 0x0101:   //启停
														if(RegisterNumber==0||RegisterNumber==0xFF)
														{
														  startwork=RegisterNumber;
															neworder=true;
															if(startwork&&(runstep1==0)&&(runstep2==0))
															{
																if(modeNo==1) runstep1=1;
																else if(modeNo==2) runstep2=1;
																process=1;   //流程标识   0：开机初始状态   1：收到开始命令进入流程    2：正常结束   3：中途收到停止命令    4：中途停止
															}
															if(play_flag==0&&startwork==0&&PVspeed>2)  play_flag=1;
															if(play_flag&&startwork==0)  process=3;   //流程标识   0：开机初始状态   1：收到开始命令进入流程    2：正常结束   3：中途收到停止命令    4：中途停止
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
							  case 0x0102:   //工作模式：1：单步，2：多步，3：报错，0：系统参数
														if(play_flag==0)  modeNo=RegisterNumber;
										        break;
							  case 0x0103:   //配方编号
														S_formula=RegisterNumber;
										        break;
//								case 0x1000:   //单步转速
//														runparameter[0][0].speed=RegisterNumber;
//										        break;								
//							  case 0x1001:   //单步旋转时长
//														runparameter[0][0].time=RegisterNumber;
//										        break;
//							  case 0x1002:   //单步加速度
//														runparameter[0][0].acc=RegisterNumber;
//														RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
//										        break;
								
							//A配方:共 5步
							//第一步：
							case 0x1100://转速
													runparameter[1][1].speed=RegisterNumber;
							            break;
							case 0x1101://旋转时长（秒）
													runparameter[1][1].time=RegisterNumber;
													break;
							case 0x1102://加速度
													runparameter[1][1].acc=RegisterNumber;
								          break;
							//第二步：
							case 0x1103://转速
													runparameter[1][2].speed=RegisterNumber;
													break;
							case 0x1104://旋转时长（秒）
													runparameter[1][2].time=RegisterNumber;
													break;
							case 0x1105://加速度
													runparameter[1][2].acc=RegisterNumber;
													break;
							//第三步：
							case 0x1106://转速
													runparameter[1][3].speed=RegisterNumber;
													break;
							case 0x1107://旋转时长（秒）
													runparameter[1][3].time=RegisterNumber;
													break;
							case 0x1108://加速度
								          runparameter[1][3].acc=RegisterNumber;
													break;
							//第四步：
							case 0x1109://转速
													runparameter[1][4].speed=RegisterNumber;
													break;
							case 0x110A://旋转时长（秒）
													runparameter[1][4].time=RegisterNumber;
													break;
							case 0x110B://加速度
													runparameter[1][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
													break;
//							//第五步：
//							case 0x110C://转速
//													runparameter[1][5].speed=RegisterNumber;
//													break;
//							case 0x110D://旋转时长（秒）
//													runparameter[1][5].time=RegisterNumber;
//													break;
//							case 0x110E://加速度										 
//													runparameter[1][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
//													break;
							
							//B配方:共 5步
							//第一步：
							case 0x1200://转速
													runparameter[2][1].speed=RegisterNumber;
							            break;
							case 0x1201://旋转时长（秒）
													runparameter[2][1].time=RegisterNumber;
													break;
							case 0x1202://加速度
													runparameter[2][1].acc=RegisterNumber;
								          break;
							//第二步：
							case 0x1203://转速
													runparameter[2][2].speed=RegisterNumber;
													break;
							case 0x1204://旋转时长（秒）
													runparameter[2][2].time=RegisterNumber;
													break;
							case 0x1205://加速度
													runparameter[2][2].acc=RegisterNumber;
													break;
							//第三步：
							case 0x1206://转速
													runparameter[2][3].speed=RegisterNumber;
													break;
							case 0x1207://旋转时长（秒）
													runparameter[2][3].time=RegisterNumber;
													break;
							case 0x1208://加速度
								          runparameter[2][3].acc=RegisterNumber;
													break;
							//第四步：
							case 0x1209://转速
													runparameter[2][4].speed=RegisterNumber;
													break;
							case 0x120A://旋转时长（秒）
													runparameter[2][4].time=RegisterNumber;
													break;
							case 0x120B://加速度
													runparameter[2][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
													break;
//							//第五步：
//							case 0x120C://转速
//													runparameter[2][5].speed=RegisterNumber;
//													break;
//							case 0x120D://旋转时长（秒）
//													runparameter[2][5].time=RegisterNumber;
//													break;
//							case 0x120E://加速度										 
//													runparameter[2][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
//													break;
							
							//C配方:共 5步
							//第一步：
							case 0x1300://转速
													runparameter[3][1].speed=RegisterNumber;
							            break;
							case 0x1301://旋转时长（秒）
													runparameter[3][1].time=RegisterNumber;
													break;
							case 0x1302://加速度
													runparameter[3][1].acc=RegisterNumber;
								          break;
							//第二步：
							case 0x1303://转速
													runparameter[3][2].speed=RegisterNumber;
													break;
							case 0x1304://旋转时长（秒）
													runparameter[3][2].time=RegisterNumber;
													break;
							case 0x1305://加速度
													runparameter[3][2].acc=RegisterNumber;
													break;
							//第三步：
							case 0x1306://转速
													runparameter[3][3].speed=RegisterNumber;
													break;
							case 0x1307://旋转时长（秒）
													runparameter[3][3].time=RegisterNumber;
													break;
							case 0x1308://加速度
								          runparameter[3][3].acc=RegisterNumber;
													break;
							//第四步：
							case 0x1309://转速
													runparameter[3][4].speed=RegisterNumber;
													break;
							case 0x130A://旋转时长（秒）
													runparameter[3][4].time=RegisterNumber;
													break;
							case 0x130B://加速度
													runparameter[3][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
													break;
//							//第五步：
//							case 0x130C://转速
//													runparameter[3][5].speed=RegisterNumber;
//													break;
//							case 0x130D://旋转时长（秒）
//													runparameter[3][5].time=RegisterNumber;
//													break;
//							case 0x130E://加速度										 
//													runparameter[3][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
//													break;
							
							//D配方:共 5步
							//第一步：
							case 0x1400://转速
													runparameter[4][1].speed=RegisterNumber;
							            break;
							case 0x1401://旋转时长（秒）
													runparameter[4][1].time=RegisterNumber;
													break;
							case 0x1402://加速度
													runparameter[4][1].acc=RegisterNumber;
								          break;
							//第二步：
							case 0x1403://转速
													runparameter[4][2].speed=RegisterNumber;
													break;
							case 0x1404://旋转时长（秒）
													runparameter[4][2].time=RegisterNumber;
													break;
							case 0x1405://加速度
													runparameter[4][2].acc=RegisterNumber;
													break;
							//第三步：
							case 0x1406://转速
													runparameter[4][3].speed=RegisterNumber;
													break;
							case 0x1407://旋转时长（秒）
													runparameter[4][3].time=RegisterNumber;
													break;
							case 0x1408://加速度
								          runparameter[4][3].acc=RegisterNumber;
													break;
							//第四步：
							case 0x1409://转速
													runparameter[4][4].speed=RegisterNumber;
													break;
							case 0x140A://旋转时长（秒）
													runparameter[4][4].time=RegisterNumber;
													break;
							case 0x140B://加速度
													runparameter[4][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
													break;
//							//第五步：
//							case 0x140C://转速
//													runparameter[4][5].speed=RegisterNumber;
//													break;
//							case 0x140D://旋转时长（秒）
//													runparameter[4][5].time=RegisterNumber;
//													break;
//							case 0x140E://加速度										 
//													runparameter[4][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
//													break;
							
							//E配方:共 5步
							//第一步：
							case 0x1500://转速
													runparameter[5][1].speed=RegisterNumber;
							            break;
							case 0x1501://旋转时长（秒）
													runparameter[5][1].time=RegisterNumber;
													break;
							case 0x1502://加速度
													runparameter[5][1].acc=RegisterNumber;
								          break;
							//第二步：
							case 0x1503://转速
													runparameter[5][2].speed=RegisterNumber;
													break;
							case 0x1504://旋转时长（秒）
													runparameter[5][2].time=RegisterNumber;
													break;
							case 0x1505://加速度
													runparameter[5][2].acc=RegisterNumber;
													break;
							//第三步：
							case 0x1506://转速
													runparameter[5][3].speed=RegisterNumber;
													break;
							case 0x1507://旋转时长（秒）
													runparameter[5][3].time=RegisterNumber;
													break;
							case 0x1508://加速度
								          runparameter[5][3].acc=RegisterNumber;
													break;
							//第四步：
							case 0x1509://转速
													runparameter[5][4].speed=RegisterNumber;
													break;
							case 0x150A://旋转时长（秒）
													runparameter[5][4].time=RegisterNumber;
													break;
							case 0x150B://加速度
													runparameter[5][4].acc=RegisterNumber;
													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
													break;
//							//第五步：
//							case 0x150C://转速
//													runparameter[5][5].speed=RegisterNumber;
//													break;
//							case 0x150D://旋转时长（秒）
//													runparameter[5][5].time=RegisterNumber;
//													break;
//							case 0x150E://加速度										 
//													runparameter[5][5].acc=RegisterNumber;
//													RebuildParameter_lcd(runparameter,buflong,ParameterAddr1,ParameterAddr2) ;  //从新写入flash
//													break;							
								
							}
							StartAddress++;
							n=n+2;	
						}
						
						memcpy(usart1_sendbuf,usart1_recebuf,6);
						test=CalcCrc(usart1_sendbuf,6);    //计算校验值
						usart1_sendbuf[6]=test&0x00FF;
						usart1_sendbuf[7]=test>>8;
						
						//回复上位机
						USART1_SendBuf485(usart1_sendbuf,8);   //RS-485 
				 } //0x10 end	

			}//本机地址结束
			
		//--------广播地址-----------------
	  else
		 {
			usart1_recebuf[0]=0x00;         //加入广播地址一同校验 
			test=CalcCrc(usart1_recebuf,(wordsize1_rece-2));    //计算校验值 
			if((usart1_recebuf[wordsize1_rece-2]+usart1_recebuf[wordsize1_rece-1]*256)==test) 
		  {
			 	memcpy(&ModbusRtu_order,usart1_recebuf,wordsize1_rece);   //将串口1收到的数据装入解析结构体
				StartAddress=ModbusRtu_order.StartAddressH*256+ModbusRtu_order.StartAddressL;		      //合并开始地址	
				RegisterNumber=ModbusRtu_order.RegisterNumberH*256+ModbusRtu_order.RegisterNumberL;   //合并（寄存器数量/写入参数）
				if(ModbusRtu_order.FunctionCode==0x03)
				{
					char i,n;
					usart1_sendbuf[0]=0x00;
					usart1_sendbuf[1]=0x03;
					usart1_sendbuf[2]=2*RegisterNumber;
					n=2;
					for(i=0;i<RegisterNumber;i++)
					{
					 switch (StartAddress)         //循环添加寄存器数据
					 {
						 
						 case 0x0000:usart1_sendbuf[n+1]=DeviceAddress>>8;        //设备地址
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
					test=CalcCrc(usart1_sendbuf,n+1);    //计算校验值
					usart1_sendbuf[n+1]=test&0x00FF;
					usart1_sendbuf[n+2]=test>>8;
					
					//回复上位机
			    USART1_SendBuf485(usart1_sendbuf,n+3);   //RS-485  

				 }

				else if(ModbusRtu_order.FunctionCode==0x06)
				{
					switch (StartAddress)
					{
						case 0x0000:    //更改本机地址
							          if(RegisterNumber<255&&RegisterNumber>0)
												{	
							            DeviceParameter.Addr=RegisterNumber;
						              DeviceAddress=RegisterNumber;
											    //回应上位机
						              memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
			                    USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
						              //从新写入flash
													if(DeviceParameter.Addr>0&&DeviceParameter.Bound1>0&&DeviceParameter.Bound2>0)
                          RebuildParameter(DeviceParameter,ParameterAddr3,ParameterAddr4);  //从新写入flash 
												}
						            break;
						
						case 0x0001:   //更改串口波特率
							          if(1==RegisterNumber) DeviceParameter.Bound1=9600;
							          else if(2==RegisterNumber) DeviceParameter.Bound1=19200;
						            else if(3==RegisterNumber) DeviceParameter.Bound1=38400;
						            else if(4==RegisterNumber) DeviceParameter.Bound1=115200;
						            else break;
						            usartbound1=DeviceParameter.Bound1;
											  //回应上位机
						            memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
                        USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
									      //从新写入flash
												if(DeviceParameter.Addr>0&&DeviceParameter.Bound1>0&&DeviceParameter.Bound2>0)
                        RebuildParameter(DeviceParameter,ParameterAddr3,ParameterAddr4);  //从新写入flash
								        uart_init(usartbound1);	 //串口初始化
						            break;
						
						case 0x0002:   //更改串口波特率
							          if(1==RegisterNumber) DeviceParameter.Bound2=9600;
							          else if(2==RegisterNumber) DeviceParameter.Bound2=19200;
						            else if(3==RegisterNumber) DeviceParameter.Bound2=38400;
						            else if(4==RegisterNumber) DeviceParameter.Bound2=115200;
						            else break;
						            usartbound2=DeviceParameter.Bound2;
											  //回应上位机
						            memcpy(usart1_sendbuf,&ModbusRtu_order,wordsize1_rece); 
                        USART1_SendBuf485(usart1_sendbuf,wordsize1_rece);                 //RS-485
									      //从新写入flash
						            if(DeviceParameter.Addr>0&&DeviceParameter.Bound1>0&&DeviceParameter.Bound2>0)
                        RebuildParameter(DeviceParameter,ParameterAddr3,ParameterAddr4);  //从新写入flash
								        uart2_init(usartbound2);	 //串口初始化
						            break;
						
					  default: break;
					}
				}	
       clean_usart1();  //清理串口1的状态 
       memset(usart1_sendbuf,0,100);	
		  }
		 }//广播地址结束
			
			clean_usart1();  //清理串口1的状态 
		 
    }				//串口1结束	

			
			
		//校验串口2收到的 *MODBUS-RTU命令格式* 的数据
		if((usart2check==stop)&&(usart2_rec==succeed))
		{
			//char c;
			s16  temphz;
			usart2check=start; 
      usart2check=stop;                        //串口2接收数据校验
			buf2mumber=0;                            //串口2接收buf数组计
			usart2_rec=stop;                         //串口2接收状态
			usart2_recebuf[0]=usart2_sendbuf[0];                     //下行设备地址固定1
			test=CalcCrc(usart2_recebuf,(wordsize2_rece-2));    //计算校验值

			if(test==usart2_recebuf[wordsize2_rece-2]+usart2_recebuf[wordsize2_rece-1]*256)
			{
				erro_count=0;
				switch(usart2_recebuf[1])
				{
					case 0x03:
										
					readmotorflag=true;
					if(set_flag==false&&modeNo!=0)   //设置中标志
					{
						//求平均速度
			//			speed_s=usart2_recebuf[5]*256+usart2_recebuf[6]+speed_s;
			//			speed_n++;
			//			if(speed_n==4)
			//			{
			//				PVspeed=speed_s/4;
			//				speed_n=0; speed_s=0;
			//			}
						temphz=usart2_recebuf[3]*256+usart2_recebuf[4];  //换向频率
						if(temphz<0)   PVspeed=0;
						else           PVspeed=temphz*2/4;      //temphz*0.1*20/4
						
						if(plansteplong==8)           //第二次加速
						{
							if(PVspeed>SVspeed*0.3)
							{
								delay_ms(50);
								plansteplong=7;
								planstep=7;
								memcpy(usart2_sendbuf,plan[planstep],8);   //将数据直接装入串口1的发送
								USART2_SendBuf485(usart2_sendbuf,8);       //Rs-485
								usart2_rec=start;                      //启动Usart2
								Usart2_overtime=RECEovertime2;
								readmotorflag=false;                   //暂停周期读motor操作
								readmotortime=READMOTORTIME;
							}
						}
						else
						{
							if(PVspeed>SVspeed*0.7)    //开始计数
							{
								if(PVspeed<SVspeed*1.2) PVtime_flag=true;
								else                    PVtime_flag=false;
								if(modeNo==1&&play_flag==1&&runstep1==3&&PVspeed<SVspeed*1.1)  //模式一步骤 0：未启动  1：发开栓命令  2：开栓延时2秒   3：发送启动电机命令    4：等待速度达标   5：发挂栓命令   6：等待降速   7：清运行时间停机
								{
									runstep1=5;
									neworder=true;
								}
								else if(modeNo==2&&play_flag==1&&step==5&&runstep2==5&&PVspeed<SVspeed*1.1) //模式二步骤 0：未启动  1：发开气泵命令  2：开气泵延时3秒   3：发开栓命令  4：开栓延时2秒   5：发送启动电机命令    6：step5等待速度达标   7：发挂栓命令   8：等待降速   9：清运行时间停机  10：发关气泵命令
								{
									runstep2=7;
									neworder=true;
								}
							}
							else if(PVspeed==0&&play_flag==1&&bolt_speedtime==0)  //判断栓塞
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
							else if(PVspeed<2&&play_flag==2)  //判断停车
							{
								if(modeNo==1) //0：系统参数 1：单步  2：多步 3.报错
								{
									play_flag=0;
									PVtime_flag=false;
									startwork=0;
									if(runstep1==6) process=4;  //新增判断销子未锁定
									runstep1=0;
									process++;
								}
								else if(modeNo==2)
								{
									if(runstep2==8) process=4;  //新增判断销子未锁定
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
										 
					case 0x05:if(memcmp(usart2_recebuf,usart2_sendbuf,wordsize2_rece)==0)  //比较内存
										{
											if(modeNo==1) //if(modeNo==1&&runstep1==1)模式一步骤 0：未启动  1：发开栓命令  2：开栓延时2秒   3：发送启动电机命令    4：等待速度达标   5：发挂栓命令   6：等待降速   7：清运行时间停机
											{
												if(runstep1==1)
												{
													runstep1=2;
													bolttime=50;  //bolttime=200;
												}
												else if(runstep1==5) runstep1=6;
											}
											if(modeNo==2) //模式二步骤 0：未启动  1：发开气泵命令  2：开气泵延时3秒   3：发开栓命令  4：开栓延时2秒   5：发送启动电机命令    6：step5等待速度达标   7：发挂栓命令   8：等待降速   9：清运行时间停机  10：发关气泵命令
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
										if(memcmp(usart2_recebuf,usart2_sendbuf,wordsize2_rece)==0)  //比较内存
										{
											//发送下一组参数
											if(planstep<6)
											{
												if(planstep==5) delay_ms(150);
												else            delay_ms(50);
												planstep++;
												memcpy(usart2_sendbuf,plan[planstep],8);   //将数据直接装入串口1的发送
												USART2_SendBuf485(usart2_sendbuf,8);       //Rs-485
												usart2_rec=start;                      //启动Usart2
												Usart2_overtime=RECEovertime2;
												readmotorflag=false;                   //暂停周期读motor操作
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
			}else  //校验失败
					{
						memset(usart2_recebuf,0,wordsize2_rece); //尚未验证
						buf2mumber=0;
						Usart2_overtime=RECEovertime2; 
						
						usart2_rec=start;         //校验失败，启动Usart2超时计时
						if(usart2_sendbuf[1]==3)  //校验失败  如果是读操作，延时再读
						{
							erro_count++;
							readmotorflag=true;
							readmotortime=READMOTORTIME;
						}
					}
		}	


		//串口1接收超时
		if(Usart1_overtime==0)
		{
			memset(usart1_recebuf,0,wordsize1_rece);
			buf1mumber=0;
			Usart1_overtime=RECEovertime1; 
//			usart1_rec=fail;             //正式版要加入超时处理
			usart1_rec=stop; 	
		}
		
			//串口2接收超时
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
				usart2_rec=start;                          //启动Usart2				
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

