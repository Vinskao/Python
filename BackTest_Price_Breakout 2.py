# -*- coding: UTF-8 -*-

#取得歷史資料
Match_data = [ line.strip('\n').split(",") for line in open('i020.TXFA8') ][1:]

#取得歷史日期
Date_list = set([ i[0] for i in Match_data ])
Date_list=sorted(list(Date_list))

#宣告績效計算變數
ProfitList=[]
TotalProfit=0

#依據歷史日期每日進行回測
for DateNum in range(len(Date_list)):
	#取得回測當日資料
	C_I020 = [ i for i in Match_data if i[0]== Date_list[DateNum] ]
	
	print(C_I020[0][0],end=' ')
	
	#---------------------------------------策略開始-----------------------------------------
	
	#取得8:45至09:00的資料 價格當作策略突破區間
	I020a = [ int(line[3]) for line in C_I020 if int(line[1])>8450000 and int(line[1])<9000000 ]
	MaxPrice = max(I020a)
	MinPrice = min(I020a)
	Spread = MaxPrice - MinPrice
	SpreadRatio = 0.4
	
	#目前在倉Flag
	Index = 0
	
	#設定進場區間 取得9:00至13:00的資料
	I020b= [ line for line in C_I020 if int(line[1])>9000000 and int(line[1])<11000000 ]

	#判斷進場 突破上下區間 加上 價差
	for i in I020b:
		Price = int(i[3])
		if Price > MaxPrice + Spread * SpreadRatio:
			Index = 1
			OrderTime=int(i[1])  #下單時間紀錄
			OrderPrice=Price #下單價格紀錄
			break
		elif Price < MinPrice - Spread * SpreadRatio:
			Index = -1
			OrderTime=int(i[1])  #下單時間紀錄
			OrderPrice=Price #下單價格紀錄
			break

	#設定出場區間 取得進場至13:30的資料
	I020c= [ line for line in C_I020 if int(line[1])>OrderTime and int(line[1])<13300000 ]

	TakeProfit = 60
	StopLoss = 30
	
	#開始記錄進場後每一筆成交價，1.若觸及停損則出場，2.若時間到尚未觸及停損則出場
	if Index == 1 :
		for i in I020c:
			Price = int(i[3])
			if Price > OrderPrice + TakeProfit :
				CoverTime=int(i[1])  #下單時間紀錄
				CoverPrice=Price #下單價格紀錄
				Profit=CoverPrice-OrderPrice
				print("Buy OrderTime:",OrderTime," OrderPrice:",OrderPrice," CoverTime:",CoverTime," CoverPrice:",CoverPrice," Profit:",CoverPrice-OrderPrice)
				break
			elif Price <= OrderPrice - StopLoss:
				CoverTime=int(i[1])  #下單時間紀錄
				CoverPrice=Price #下單價格紀錄
				Profit=CoverPrice-OrderPrice
				print("Buy OrderTime:",OrderTime," OrderPrice:",OrderPrice," CoverTime:",CoverTime," CoverPrice:",CoverPrice," Profit:",CoverPrice-OrderPrice)
				break
			elif i[1] == I020c[-1][1]:
				CoverTime=int(i[1])  #下單時間紀錄
				CoverPrice=Price #下單價格紀錄
				Profit=CoverPrice-OrderPrice
				print("Buy OrderTime:",OrderTime," OrderPrice:",OrderPrice," CoverTime:",CoverTime," CoverPrice:",CoverPrice," Profit:",CoverPrice-OrderPrice)
				break
	elif Index == -1 : 
		for i in I020c:
			Price = int(i[3])
			if Price < OrderPrice - TakeProfit :
				CoverTime=int(i[1])  #下單時間紀錄
				CoverPrice=Price #下單價格紀錄
				Profit=OrderPrice-CoverPrice
				print("Sell OrderTime:",OrderTime," OrderPrice:",OrderPrice," CoverTime:",CoverTime," CoverPrice:",CoverPrice," Profit:",OrderPrice-CoverPrice)
				break
			elif Price >= OrderPrice + StopLoss:
				CoverTime=int(i[1])  #下單時間紀錄
				CoverPrice=Price #下單價格紀錄
				Profit=OrderPrice-CoverPrice
				print("Sell OrderTime:",OrderTime," OrderPrice:",OrderPrice," CoverTime:",CoverTime," CoverPrice:",CoverPrice," Profit:",OrderPrice-CoverPrice)
				break
			elif i[1] == I020c[-1][1]:
				CoverTime=int(i[1])  #下單時間紀錄
				CoverPrice=Price #下單價格紀錄
				Profit=OrderPrice-CoverPrice
				print("Sell OrderTime:",OrderTime," OrderPrice:",OrderPrice," CoverTime:",CoverTime," CoverPrice:",CoverPrice," Profit:",OrderPrice-CoverPrice)
				break
	else :
		continue
		
	#計算績效
	ProfitList.append(Profit)
	TotalProfit+=Profit
	
#策略回測完成後，計算當月總績效、最大連續虧損
LossList=[]
Loss=0
for pf in ProfitList:
	if pf<=0:
		Loss+=pf
		LossList.append(Loss)
	else:
		Loss=0
print('ToTal Profit:',TotalProfit,', Max Loss',min(LossList))
