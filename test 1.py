guancha = {}
geli = {}
while True:
    id=input('请输入身份证号，取消请直接回车。')
    if id=='':
        break
    elif (len(id)!=18) and (len(id)!=15):
        print('身份证号码错误！')
        continue
    wuhanren=(id[0:4]=='4201')

    temp=input('请输入体温，取消请直接回车。')
    if temp=='':
        break
    elif not temp.isdigit():
        print('体温输入错误！')
        continue
    fever=(float(temp)>=37.3)
    
    if not fever and wuhanren:
        guancha[id]=temp
        print('您是武汉籍人员，无发烧症状，请居家观察！')
    elif fever and not wuhanren:
        guancha[id]=temp
        print('您不是武汉籍人员 ，但有发烧症状，请居家观察！')
    elif fever and wuhanren:
        geli[id]=temp
        print('您是武汉籍人员且有发烧症状，系统已上报，请配合隔离！')
    else:
        print('恭喜您，没有中奖，可以走了！')
        
print('居家观察名单：',guancha)
file=open('居家观察名单.txt','w+')
file.writelines('居家观察名单\n      身份证号      体温\n')
for key in guancha.keys():
    file.writelines(key+' '+str(guancha[key])+'\n')
file.close()

print('隔离上报名单：',geli)
file=open('隔离上报名单.txt','w+')
file.writelines('隔离上报名单\n      身份证号      体温\n')
for key in geli.keys():
    file.writelines(key+' '+str(geli[key])+'\n')
file.close()
