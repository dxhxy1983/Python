height,weight=eval(input('请输入身高（CM）/体重（kg）（逗号隔开）：'))
BMI=weight/pow(height,2)
print('BMI指数为：{:.2f}'.format(BMI))
who,cho='',''

if  BMI<18.5:
    who,cho="偏瘦",'偏瘦'
elif 18.5<=BMI<24:
    who,cho="正常",'正常'
elif 24<=BMI<25:
    who,cho="正常",'偏胖'
elif 25<=BMI<28:
    who,cho="偏胖",'偏胖'
else:
    who,cho="肥胖",'肥胖'
print('世卫BMI标准为:{}，国标BMI标准为：{}'.format(who,cho))