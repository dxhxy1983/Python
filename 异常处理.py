def main():
    try :
        num1,num2= input("please input 2 numbers ,sepreated  by comma:")
        result=num1/num2
        # while (num2=0):
        #     ZeroDivisionErro=1
        
    except ZeroDivisionError:
        print("被除数为零！") 
    except :
        print('something wrong in the input!')
    else:
        print("商是：",result)
    finally:
        print("最终执行步")
main()
