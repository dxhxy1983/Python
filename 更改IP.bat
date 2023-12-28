@echo off
cls
color 0A
set NAME1="本地连接"
set NAME2="无线网络连接"
@echo off
echo.
echo. ===修改ip地址===
echo.
echo. 1:有线自动获取
echo.
echo. 2:重设有线ip地址为192.168.0.201
echo. 
echo. 21:重设有线IP地址为192.168.0.251 子网掩码255.255.254.0
echo.
echo. 3:重设有线ip地址为10.28.213.10
echo.
echo. 4:重设有线ip地址为192.168.1.201
echo.
echo. 5:无线自动获取
echo.
echo. 6:重设无线ip为192.168.0.252
echo.
echo. 61:重设无线ip为192.168.0.252 子网掩码255.255.254.0
echo.
echo. 7:重设无线ip为10.28.213.11
echo. 
echo  8:重设无线ip为192.168.1.210
echo.
set/p sel=请选择修改方式：
if "%sel%"=="1" goto auto1
if "%sel%"=="2" goto jt1
if "%sel%"=="21" goto jt11
if "%sel%"=="3" goto jt2
if "%sel%"=="4" goto jt3
if "%sel%"=="5" goto auto2
if "%sel%"=="6" goto jt4
if "%sel%"=="61" goto jt41
if "%sel%"=="7" goto jt5
if "%sel%"=="8" goto jt6

echo 您没有选择修改方式。
goto end
 
:auto1
netsh interface ip set address name=%NAME1% source=dhcp
netsh interface ip delete dns %NAME1% all
ipconfig /flushdns
//ipconfig /all
goto end

:auto2
netsh interface ip set address name=%NAME2% source=dhcp
netsh interface ip delete dns %NAME2% all
ipconfig /flushdns
//ipconfig /all
goto end
 
 
:jt1
echo 正在更改IP地址，请稍等......
netsh interface ip set address name=%NAME1% source=static addr=192.168.0.201 mask=255.255.255.0 gateway=192.168.0.1 gwmetric=1
netsh interface ip set dns name=%NAME1% source=static addr=192.168.0.1
netsh interface ip add dns name=%NAME1% addr=8.8.8.8 index=2 
ipconfig /flushdns
//ipconfig /all
echo 更改IP地址完成！
goto end

 
:jt11
echo 正在更改IP地址，请稍等......
netsh interface ip set address name=%NAME1% source=static addr=192.168.0.251 mask=255.255.254.0 gateway=192.168.0.1 gwmetric=1
netsh interface ip set dns name=%NAME1% source=static addr=192.168.0.1
netsh interface ip add dns name=%NAME1% addr=8.8.8.8 index=2 
ipconfig /flushdns
//ipconfig /all
echo 更改IP地址完成！
goto end

:jt2
echo 正在更改IP地址，请稍等......
netsh interface ip set address name=%NAME1% source=static addr=10.28.213.10 mask=255.255.255.0 gateway=10.28.213.254 gwmetric=1
netsh interface ip set dns name=%NAME1% source=static addr=10.8.0.107
netsh interface ip add dns name=%NAME1% addr=8.8.8.8 index=2 
ipconfig /flushdns
//ipconfig /all
echo 更改IP地址完成！
goto end



:jt3
echo 正在更改IP地址，请稍等......
netsh interface ip set address name=%NAME1% source=static addr=192.168.1.201 mask=255.255.255.0 gateway=192.168.1.1 gwmetric=1
netsh interface ip set dns name=%NAME1% source=static addr=10.8.0.107
netsh interface ip add dns name=%NAME1% addr=8.8.8.8 index=2 
ipconfig /flushdns
//ipconfig /all
echo 更改IP地址完成！
goto end


:jt4
echo 正在更改IP地址，请稍等......
netsh interface ip set address name=%NAME2% source=static addr=192.168.0.252 mask=255.255.255.0 gateway=192.168.0.1 gwmetric=1
netsh interface ip set dns name=%NAME2% source=static addr=10.8.0.107
netsh interface ip add dns name=%NAME2% addr=8.8.8.8 index=2 
ipconfig /flushdns
//ipconfig /all
echo 更改IP地址完成！
goto end

:jt41
echo 正在更改IP地址，请稍等......
netsh interface ip set address name=%NAME2% source=static addr=192.168.0.252 mask=255.255.254.0 gateway=192.168.0.1 gwmetric=1
netsh interface ip set dns name=%NAME2% source=static addr=10.8.0.107
netsh interface ip add dns name=%NAME2% addr=8.8.8.8 index=2 
ipconfig /flushdns
//ipconfig /all
echo 更改IP地址完成！
goto end

:jt5
echo 正在更改IP地址，请稍等......
netsh interface ip set address name=%NAME2% source=static addr=10.28.213.11 mask=255.255.255.0 gateway=10.28.213.254 gwmetric=1
netsh interface ip set dns name=%NAME1% source=static addr=10.8.0.107
netsh interface ip add dns name=%NAME1% addr=8.8.8.8 index=2 
ipconfig /flushdns
//ipconfig /all
echo 更改IP地址完成！
goto end


:jt6
echo 正在更改IP地址，请稍等......
netsh interface ip set address name=%NAME2% source=static addr=192.168.1.210 mask=255.255.255.0 gateway=192.168.1.1 gwmetric=1
netsh interface ip set dns name=%NAME2% source=static addr=10.8.0.107
netsh interface ip add dns name=%NAME2% addr=8.8.8.8 index=2 
ipconfig /flushdns
//ipconfig /all
echo 更改IP地址完成！
goto end

:end
//pause