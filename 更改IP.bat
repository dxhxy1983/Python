@echo off
cls
color 0A
 
@echo off
echo.
echo. ===�޸�ip��ַ===
echo.
echo. 1:�����Զ���ȡ
echo.
echo. 2:��������ip��ַΪ192.168.0.201
echo. 
echo. 21:��������IP��ַΪ192168.0.251 ��������255.255.254.0
echo.
echo. 3:��������ip��ַΪ10.28.213.10
echo.
echo. 4:��������ip��ַΪ192.168.1.201
echo.
echo. 5:�����Զ���ȡ
echo.
echo. 6:��������ipΪ192.168.0.252
echo.
echo. 61:��������ipΪ192.168.0.252 ��������255.255.254.0
echo.
echo. 7:��������ipΪ10.28.213.11
echo. 
echo  8:��������ipΪ192.168.1.210
echo.
set/p sel=��ѡ���޸ķ�ʽ��
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

echo ��û��ѡ���޸ķ�ʽ��
goto end
 
:auto1
netsh interface ip set address name="��������" source=dhcp
netsh interface ip delete dns "��������" all
ipconfig /flushdns
//ipconfig /all
goto end

:auto2
netsh interface ip set address name="������������" source=dhcp
netsh interface ip delete dns "������������" all
ipconfig /flushdns
//ipconfig /all
goto end
 
 
:jt1
echo ���ڸ���IP��ַ�����Ե�......
netsh interface ip set address name="��������" source=static addr=192.168.0.201 mask=255.255.255.0 gateway=192.168.0.1 gwmetric=1
netsh interface ip set dns name="��������" source=static addr=192.168.0.1
netsh interface ip add dns name="��������" addr=8.8.8.8 index=2 
ipconfig /flushdns
//ipconfig /all
echo ����IP��ַ��ɣ�
goto end

 
:jt11
echo ���ڸ���IP��ַ�����Ե�......
netsh interface ip set address name="��������" source=static addr=192.168.0.251 mask=255.255.254.0 gateway=192.168.0.1 gwmetric=1
netsh interface ip set dns name="��������" source=static addr=192.168.0.1
netsh interface ip add dns name="��������" addr=8.8.8.8 index=2 
ipconfig /flushdns
//ipconfig /all
echo ����IP��ַ��ɣ�
goto end

:jt2
echo ���ڸ���IP��ַ�����Ե�......
netsh interface ip set address name="��������" source=static addr=10.28.213.10 mask=255.255.255.0 gateway=10.28.213.254 gwmetric=1
netsh interface ip set dns name="��������" source=static addr=10.8.0.107
netsh interface ip add dns name="��������" addr=8.8.8.8 index=2 
ipconfig /flushdns
//ipconfig /all
echo ����IP��ַ��ɣ�
goto end



:jt3
echo ���ڸ���IP��ַ�����Ե�......
netsh interface ip set address name="��������" source=static addr=192.168.1.201 mask=255.255.255.0 gateway=192.168.1.1 gwmetric=1
netsh interface ip set dns name="��������" source=static addr=10.8.0.107
netsh interface ip add dns name="��������" addr=8.8.8.8 index=2 
ipconfig /flushdns
//ipconfig /all
echo ����IP��ַ��ɣ�
goto end


:jt4
echo ���ڸ���IP��ַ�����Ե�......
netsh interface ip set address name="������������" source=static addr=192.168.0.252 mask=255.255.255.0 gateway=192.168.0.1 gwmetric=1
netsh interface ip set dns name="������������" source=static addr=10.8.0.107
netsh interface ip add dns name="������������" addr=8.8.8.8 index=2 
ipconfig /flushdns
//ipconfig /all
echo ����IP��ַ��ɣ�
goto end

:jt41
echo ���ڸ���IP��ַ�����Ե�......
netsh interface ip set address name="������������" source=static addr=192.168.0.252 mask=255.255.254.0 gateway=192.168.0.1 gwmetric=1
netsh interface ip set dns name="������������" source=static addr=10.8.0.107
netsh interface ip add dns name="������������" addr=8.8.8.8 index=2 
ipconfig /flushdns
//ipconfig /all
echo ����IP��ַ��ɣ�
goto end

:jt5
echo ���ڸ���IP��ַ�����Ե�......
netsh interface ip set address name="������������" source=static addr=10.28.213.11 mask=255.255.255.0 gateway=10.28.213.254 gwmetric=1
netsh interface ip set dns name="��������" source=static addr=10.8.0.107
netsh interface ip add dns name="��������" addr=8.8.8.8 index=2 
ipconfig /flushdns
//ipconfig /all
echo ����IP��ַ��ɣ�
goto end


:jt6
echo ���ڸ���IP��ַ�����Ե�......
netsh interface ip set address name="������������" source=static addr=192.168.1.210 mask=255.255.255.0 gateway=192.168.1.1 gwmetric=1
netsh interface ip set dns name="������������" source=static addr=10.8.0.107
netsh interface ip add dns name="������������" addr=8.8.8.8 index=2 
ipconfig /flushdns
//ipconfig /all
echo ����IP��ַ��ɣ�
goto end

:end
//pause