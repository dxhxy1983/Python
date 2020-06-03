#include <stdio.h>
#include <math.h>
#include <conio.h>
#include <string.h>
#include <stdlib.h>
#include <bios.h>
#include <dos.h>
//定义的常量//
#define 	F_01	40000	//第一层的脉冲数
#define 	F_02	40200 	//第二层的脉冲数
#define 	F_03	39800	//第三层的脉冲数
#define 	F_04	40100	//第四层的脉冲数
#define 	F_05	40000	//第五层的脉冲数
#define 	F_06	40300	//第六层的脉冲数
#define 	F_07	39900	//第七层的脉冲数
#define 	F_08	39700	//第八层的脉冲数
#define 	F_09	40200	//第九层的脉冲数
#define 	F_010	40100	//第十层的脉冲数

#define 	F_SUM_H	4		//十层楼总的脉冲数的高位
#define 	F_SUM_L	01200	//十层楼总的脉冲数的低位

#define     T  0.001 
unsigned short int f_pulse_num[10]={40000,40200,39800,40100,40000,40300,39900,39700,40200,40100};
int choose_floor();
void configue(float *h,float *a_max,float *v_max);
unsigned long int design_s_curve(int f_s,int f_d,float h,float a_max,float v_max,int *mem_v_matrix);//速度曲线规划,返回速度值
																					  //个数
void float_trans(float *f_in);
 

void main()
{
	int f_source;//轿厢起始的楼层数
				 //有效数值范围为1~11;
	int f_de_buffer[3]={11,11,11};
					//轿厢的目的楼层数记录数组， 最多可以记录三个
					//轿厢每次都是从f_source的楼层运行到f_de_buffer[0]的楼层，
					//到达目的楼层后令f_source=f_de_buffer[0],f_de_buffer[0]=f_de_buffer[1],
					//默认f_de_buffer[0]=11时，给定速度应为0，轿厢保持原位。
					//f_de_buffer[2]中的每一个元素的有效值范围为1~11;
	int f_int_num=11;//如果运行过程中有截梯的中断信号，则保存在f_int_num中；
	float v_max=0;	//最大速度
	float a_max=0;	//最大速度
	float h=0;		//加加速度
	
	float s1,s2;
	unsigned  int mem_v_matrix[15000];//速度曲线存储矩阵；
	unsigned int s1_pulse_2,s2_pulse_2;
	int v_num_max=0;
	int i=0,j=0;
	double  went_pulse=0;
	long int int_pulse=0;
	int int_flag=0;
	char *mem_v_out;
	char ch;
	FILE *fp;
	/*配置电梯轿厢的初始状态，位于一层，并且设置v_max,a_max,h*/
	f_source=1;//默认初始时刻电梯的轿厢在第一层
	configue(&h,&a_max,&v_max);
	s1=(pow(v_max,2)*h+v_max*pow(a_max,2))/(2*a_max*h);
	s2= pow(a_max,3)/pow(h,2);
	float_trans(&s1);
	float_trans(&s2); 
	s2_pulse_2=(unsigned long  int)(s2*2*10000);
	s1_pulse_2=(unsigned long  int)(s1*2*10000);
	
	/*********************************************************/
	/*电梯位于初始状态时，电梯第一次接受运行到某一层的命令*/
	printf("\n now the elevator has arrived on the %d th floor \n ",f_source);
	f_de_buffer[0]=choose_floor(); 
	
	/*********************************************************/					 
	while(1)
	{
		if(f_de_buffer[0]==12)
		{
			break;
		}
		else if(f_de_buffer[0]>=1 && f_de_buffer[0]<=10)
		{
			v_num_max=design_s_curve(f_source,f_de_buffer[0],h,a_max,v_max,&mem_v_matrix[0]);
		}
		/*存储速度值，相当于电梯轿厢在按照规划出来的速度曲线运行*/
		if((fp=fopen("mem_v.txt","w+"))==NULL)
		{
			printf("con't open the file ");
			exit(0);
		}
		for(i=int_flag*i;i<v_num_max;i++)
		{	
			delay(1);
			if(i%1000==0)
			{
				printf("\n the time has gone : %d----the current v is :%f----went_pulse:%lf",(int)(i/1000),mem_v_matrix[i]/10000.0,went_pulse);
				
			}
			if(bioskey(1)!=0)
			{
				ch=bioskey(0);
				printf("\n the number you have pressed is %c ",ch);
				f_int_num=ch-0X30;//为了简便默认所有的截梯都是顺向的
				printf("\n the number you have pressed is %d ",f_int_num);
				//exit(0);
				if( (f_int_num>f_source && f_int_num<f_de_buffer[0]) ||(f_int_num<f_source && f_int_num>f_de_buffer[0]) )
				{
					if(f_source<f_int_num)
					{
						for(j=0;j<abs(f_source-f_int_num);j++)
						{
							int_pulse+=f_pulse_num[f_source+j+1];
						}
					}
					else if(f_source>f_int_num)
					{
						for(j=0;j<abs(f_source-f_int_num);j++)
						{
							int_pulse+=f_pulse_num[f_source-j-1];
						}
					}
					else
					{
						int_pulse=0;
					}
					if( (int_pulse-went_pulse)>s1_pulse_2)
					{
						break;
					}
					
				}
			}	
			went_pulse+=mem_v_matrix[i]/10000.0*10.0;
			itoa(mem_v_matrix[i],mem_v_out,10);
			strcat(mem_v_out,",");
			fwrite(mem_v_out,sizeof(char),strlen(mem_v_out),fp);
		}
		if(i<v_num_max)//截梯成功，调整电梯运行命令，还要保存当前的位置，即i的数值，然后需要重新规划速度曲线，
					   //但要从当前的位置，即i的数值处运行速度曲线
		{
			fclose(fp);
			f_de_buffer[2]=f_de_buffer[1];
			f_de_buffer[1]=f_de_buffer[0];
			f_de_buffer[0]=f_int_num;
			int_flag=1;
		}
		if(i==v_num_max)//电梯运行到f_de_buffer[0]所指示的楼层,后调整楼层运行命令
		{
			printf("\n the time has gone : %d----the current v is :%f----went_pulse:%lf",(int)(i/1000),mem_v_matrix[i]/10000.0,went_pulse);
			printf("\n now the elevator has arrived on the %d th floor \n ",f_de_buffer[0]);
			fclose(fp);
			f_source=f_de_buffer[0];
			f_de_buffer[0]=f_de_buffer[1];
			f_de_buffer[1]=f_de_buffer[2];
			f_de_buffer[2]=11;
			int_flag=0;
			if(f_de_buffer[0]==11)
			{
				f_de_buffer[0]=choose_floor();
			}
		}
			
	}
}
void float_trans(float *f_in)
{
	unsigned long int a;
	a=(unsigned long int)( (*f_in)*10000);
	*f_in=a/10000.0;
}
int choose_floor()
{
	int i=11;
	int floor;
	while(1)
	{
		printf("\n now the people inside can select the floor wanted from 1~10 ");
		printf("\n if none wanted,you can input '0' to skip this step  ");
		while(1)
		{
			printf("\n floor wanted by inside : ");
			scanf("%d",&floor);
			if(floor<=12 && floor>=0)
				break;
			else 
				printf("\n wrong ,please input the floor again \n ");
		}
		if(floor==0)
		{
			printf("\n now the people outside can select the floor wanted from 1~10 ");
			printf("\n if none wanted,you can input '0' to skip this step  ");
			while(1)
			{
				printf("\n floor wanted by inside : ");
				scanf("%d",&floor);
				if(floor<=12 && floor>=1)
					return;
				else if (floor==0)
					break;
				else 
					printf("\n wrong ,please input the floor again \n ");
			}
		}
		else if(floor<=12 && floor>=1)
			return floor;
			
	}
}
void configue(float *h,float *a_max,float *v_max)
{
	printf("now please configue the basic parameter of the elevator \n");
	printf("	   the parameter should meet the requirement	    \n");
	printf("	v_max<=4.000,a_max<=1.500,h<=1.300,v_max>a_max^2/h   \n ");
	while(1)
	{
		while(1)
		{
			printf("v_max=");
			scanf("%4f",v_max);
			if(*v_max<=4.000)
			{
				printf("\n");
				break;
			}
			else 
				printf("\n			WRONG,PLEASE INPUT v_max AGAIN			 \n");
		}
		while(1)
		{
			printf("a_max=");
			scanf("%4f",a_max);
			if(*a_max<=1.500)
			{
				printf("\n");
				break;
			}
			else 
				printf("\n			WRONG,PLEASE INPUT a_max AGAIN			 \n");
		}
		while(1)
		{
			printf("h=");
			scanf("%4f",h);
			if(*h<=1.500)
			{
				printf("\n");
				break;
			}
			else 
				printf("\n			  WRONG,PLEASE INPUT h AGAIN			  \n");
		}
		if(*v_max>( pow(*a_max,2)/(*h)))
		{
			printf("\n	  the parameter has been configued sucessfully	    \n");
			printf("\n	v_max=%4f	,	a_max=%4f	,	h=%4f \n",*v_max,*a_max,*h);
			break;
		}
		else
		{
				printf("\n	WRONG,PLEASE INPUT v_max a_max h  AGAIN			 \n");
		}
	}
}
unsigned long int design_s_curve(int f_s,int f_d,float h,float a_max,float v_max,int *mem_v_matrix )
{
	float s1;//六段式与七段式曲线的临界曲线加速上升的距离，与减速下降的距离相同
	float s2;//四段式与六段式曲线的临界曲线加速上升的距离，与减速下降的距离相同
	unsigned long int s1_pulse_2;
	unsigned long int s2_pulse_2;
	float t1,t2,t3,t4,t5,t6,t7;
	float t=0;
	float v=0,v_max_sub=0,a_max_sub=0;
	float s=0.0;
	int f_flag=2;//1表示电梯位于上升状态；0表示电梯位于下降状态；
	int i=0,i_max;
	long int sum_pulse=0;
	//long int mem_pulse=0;
	double mem_pulse=0.0;
	int mem_v=0;
	char *mem_v_out;
	FILE *fp;
	//unsigned  int mem_v_matrix[15000];
	 
	s1=(pow(v_max,2)*h+v_max*pow(a_max,2))/(2*a_max*h);
	s2= pow(a_max,3)/pow(h,2);
	float_trans(&s1);
	float_trans(&s2);
	s2_pulse_2=(unsigned long  int)(s2*2*10000);
	s1_pulse_2=(unsigned long  int)(s1*2*10000);
	printf("\n the journey of 6_curve to 7_curve %f\n ",s1*2);
	 
	printf("the corresponding pulse num is %ld",s1_pulse_2);
	printf("\n the journey of 4_curve to 6_curve %f\n ",s2*2);
	 
	printf("the corresponding pulse num is %ld",s2_pulse_2);
	getch();
	if(f_s<f_d)
	{
		f_flag=1;
		for(i=0;i<abs(f_s-f_d);i++)
		{
			sum_pulse+=f_pulse_num[f_s+i-1];
		}
	}
	else if (f_s>f_d)
	{
		f_flag=0;
		for(i=0;i<abs(f_s-f_d);i++)
		{
			sum_pulse+=f_pulse_num[f_s-i-1];
		}
	}
	else 
	{
		f_flag=2;
		sum_pulse=0;
	}
	printf("\n \n the sum_pulse is %ld",sum_pulse);
	
	if(sum_pulse>=s1_pulse_2)
	{
		t1= a_max/h;
		t2=(v_max-pow(a_max,2)/h)/a_max;
		
		float_trans(&t1);
		float_trans(&t2);
		
		t3=t1;
		
		t5=t3;
		t6=t2;
		t7=t1;
		t4=(sum_pulse/10000.0-s1*2)/v_max;
		float_trans(&t4);
		printf("\n t1=%f",t1);
		printf("\n t2=%f",t2);
		printf("\n t3=%f",t3);
		printf("\n t4=%f",t4);
		printf("\n t5=%f",t5);
		printf("\n t6=%f",t6);
		printf("\n t7=%f",t7);
		printf("\n \n");
		getch();
		
		for(i=0;;i++)
		{
			if(t<=t1)
			{
				v=h*pow(t,2)/2;
			}
			else if (t>t1 && t<=(t1+t2))
			{
				v=h*pow(t1,2)/2+a_max*(t-t1);
			}
			else if(t>(t1+t2) && t<=(t1+t2+t3) )
			{
                v=v_max-h*pow(t1+t2+t3-t,2)/2;
            }   
            else if(t>(t1+t2+t3) && t<=(t1+t2+t3+t4) ) 
			{
                v=v_max;
            }     
            else if(t>(t1+t2+t3+t4) && t<=(t1+t2+t3+t4+t5) )
			{
                v=v_max-h*pow(t-(t1+t2+t3+t4),2 )/2;
            }    
            else if(t>(t1+t2+t3+t4+t5) && t<=(t1+t2+t3+t4+t5+t6) )
			{
                v=v_max-h*pow(t5,2)/2-a_max*(t-(t1+t2+t3+t4+t5));
            }    
            else if(t>(t1+t2+t3+t4+t5+t6) && t<=(t1+t2+t3+t4+t5+t6+t7) ) 
			{
                v=h*pow( (t1+t2+t3+t4+t5+t6+t7-t),2)/2;
            }     
            else
			{
                v=0;
            }  
			//更新时间以及计算脉冲数
			t=0.001*i;
			float_trans(&v);
			mem_v=(int)(v*10000);
			mem_v_matrix[i]=mem_v;
			
			mem_pulse+=v*10.0;
			//printf("t= %f \n",t); 
			//printf(" 	%lf 	",mem_pulse);
			if(t>=t1+t2+t3+t4+t5+t6+t7)
				break;
		}
		i_max=i;
		printf("\n \n  mem_pulse= %f",mem_pulse);
		
		
	}
	else if (sum_pulse>=s2_pulse_2 && sum_pulse<s1_pulse_2)
	{
		s=sum_pulse/10000.0;
		v_max_sub=(-pow(a_max,2)+sqrt( pow(a_max,4)+4*pow(h,2)*s*a_max) )/(2*h);
		t1= a_max/h;
		t2=(v_max_sub-pow(a_max,2)/h)/a_max;
		
		float_trans(&t1);
		float_trans(&t2);
		
		t3=t1;
        
        t5=t3;
        t6=t2;
        t7=t1;
        
        t4=0;
		float_trans(&t4);
		printf("\n t1=%f",t1);
		printf("\n t2=%f",t2);
		printf("\n t3=%f",t3);
		printf("\n t4=%f",t4);
		printf("\n t5=%f",t5);
		printf("\n t6=%f",t6);
		printf("\n t7=%f",t7);
		printf("\n \n");
		getch();
		
		for(i=0;;i++)
		{
			if(t<=t1)
			{
				v=h*pow(t,2)/2;
			}
			else if (t>t1 && t<=(t1+t2))
			{
				v=h*pow(t1,2)/2+a_max*(t-t1);
			}
			else if(t>(t1+t2) && t<=(t1+t2+t3) )
			{
                v=v_max_sub-h*pow(t1+t2+t3-t,2)/2;
            }   
            else if(t>(t1+t2+t3) && t<=(t1+t2+t3+t4) ) 
			{
                v=v_max_sub;
            }     
            else if(t>(t1+t2+t3+t4) && t<=(t1+t2+t3+t4+t5) )
			{
                v=v_max_sub-h*pow(t-(t1+t2+t3+t4),2 )/2;
            }    
            else if(t>(t1+t2+t3+t4+t5) && t<=(t1+t2+t3+t4+t5+t6) )
			{
                v=v_max_sub-h*pow(t5,2)/2-a_max*(t-(t1+t2+t3+t4+t5));
            }    
            else if(t>(t1+t2+t3+t4+t5+t6) && t<=(t1+t2+t3+t4+t5+t6+t7) ) 
			{
                v=h*pow( (t1+t2+t3+t4+t5+t6+t7-t),2)/2;
            }     
            else
			{
                v=0;
            }  
			//更新时间以及计算脉冲数
			t=0.001*i;
			float_trans(&v);
			mem_v=(int)(v*10000);
			mem_v_matrix[i]=mem_v;
			
			mem_pulse+=v*10.0;
			//printf("t= %f \n",t); 
			//printf(" 	%lf 	",mem_pulse);
			
			if(t>=t1+t2+t3+t4+t5+t6+t7)
				break;
		}
		i_max=i;
		printf("\n \n  mem_pulse= %f",mem_pulse);
	
	}
	else if(sum_pulse<s2_pulse_2)
	{
		s=sum_pulse/10000.0;
		a_max_sub=pow( (s*pow(h,2)/2),1/3);
		
		t1= a_max_sub/h;
		t2=0;
		
		float_trans(&t1);
		float_trans(&t2);
		
		t3=t1;
        
        t5=t3;
        t6=0;
        t7=t1;
        
        t4=0;
		v_max_sub=h*pow(t1,2);
		float_trans(&t4);
		printf("\n t1=%f",t1);
		printf("\n t2=%f",t2);
		printf("\n t3=%f",t3);
		printf("\n t4=%f",t4);
		printf("\n t5=%f",t5);
		printf("\n t6=%f",t6);
		printf("\n t7=%f",t7);
		printf("\n \n");
		getch();
		
		for(i=0;;i++)
		{
			if(t<=t1)
			{
				v=h*pow(t,2)/2;
			}
			else if(t>(t1+t2) && t<=(t1+t2+t3) )
			{
                v=v_max_sub-h*pow(t1+t2+t3-t,2)/2;
            }     
            else if(t>(t1+t2+t3+t4) && t<=(t1+t2+t3+t4+t5) )
			{
                v=v_max_sub-h*pow(t-(t1+t2+t3+t4),2 )/2;
            }    
            else if(t>(t1+t2+t3+t4+t5+t6) && t<=(t1+t2+t3+t4+t5+t6+t7) ) 
			{
                v=h*pow( (t1+t2+t3+t4+t5+t6+t7-t),2)/2;
            }     
            else
			{
                v=0;
            }  
			//更新时间以及计算脉冲数
			t=0.001*i;
			float_trans(&v);
			mem_v=(int)(v*10000);
			mem_v_matrix[i]=mem_v;
			
			mem_pulse+=v*10.0;
			//printf("t= %f \n",t); 
			//printf(" 	%lf 	",mem_pulse);
			
			if(t>=t1+t2+t3+t4+t5+t6+t7)
				break;
		}
		i_max=i;
		printf("\n \n  mem_pulse= %f",mem_pulse);
	
	}
	else
	{
	
	}	
	return i_max;
}











