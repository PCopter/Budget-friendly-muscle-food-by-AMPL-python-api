from amplpy import AMPL
import pandas as pd

def information():
    print("----------Please fill in information----------")
    age = input("Enter your age: ")
    weigth = input("Enter your weigth: ")
    high = input("Enter your high: ")
    while True:
        gender = input("Enter your gender (male/female): ")
        if gender.lower() == "male":
            break
        elif gender.lower() == "female":
            break
        else:
            print("Please select the correct gender. (male/female)")
    while True:
        Goal = input("Enter your Goal (Maintenance/Cutting/Bulking): ")
        if Goal.lower() == "cutting":
            break
        elif Goal.lower() == "bulking":
            break
        elif Goal.lower() == "maintenance":
            break
        else:
            print("Please select the correct Goal. (Maintenance/Cutting/Bulking)")
    return age,weigth,high,gender,Goal

def BMRGen(gender,high,weigth,age):
    userhigh = int(high)
    userweigth = int(weigth)
    userage = int(age)
    BMR = 0
    if gender.lower() == "male":
        BMR = 66 + (13.7*userweigth)+(5*userhigh)-(6.8*userage)
    elif gender.lower()  == "female" : 
        BMR = 665 + (9.6*userweigth)+(1.8*userhigh)-(4.7*userage)
    return BMR

def BulkOrCut(BMR,Goal):
    if Goal.lower() == "bulking":
        BMR += 500
    if Goal.lower() == "cutting":
        BMR -= 500
    return BMR

def divide_values(BMR):
    # 30% protein, 35% fats, 35% carbs
    max_Protein = round(((BMR * 0.30)/4),2)
    max_fats = round(((BMR * 0.35)/9),2)
    max_Crabs = round(((BMR * 0.35)/4),2)
    
    return max_Protein, max_fats, max_Crabs

def prepare_data(result_BMR_withGoal,min_Protein,min_fats,min_Carb):
    food_df = pd.DataFrame(
            [
                ("ก๋วยเตี๋ยวเส้นใหญ่เนื้อสับ", 40, 616, 26.6,34.9,54.8),
                ("ข้าวมันไก่", 40, 765.3, 27.5,32.2,89.1),
                ("ข้าวผัดกะเพราหมูสับไข่ดาว", 50, 594.2 , 39.1 ,23.8,54.1),
                ("ข้าวผัดคะน้าหมูกรอบ", 55, 753.1, 11.7 ,50.4,61.7),
                ("ข้าวไข่เจียวหมูสับ", 45, 889.8 , 31.8,63.3,46.7),
                ("ข้าวผัดกะเพราอกไก่", 50, 466.4, 37.6, 11 ,52.7),
                ("ข้าวไก่ทอดกระเทียมพริกไท", 55, 773.6, 39.9,31.5,80.6),
                ("ก๋วยเตี๋ยวเส้นใหญ่เนื้อสับ", 40, 616, 26.6, 34.9, 54.8),
                ("ข้าวมันไก่", 40, 765.3, 27.5, 32.2, 89.1),
                ("ข้าวราดผัดผักบุ้งไฟแดง", 35, 738.1, 15.3, 75.6, 42.1),
                ("ข้าวราดหมูอบ", 45, 971.9, 56.9, 104.9, 33.7),
                ("ข้าวราดกุ้งทอดกระเทียม", 50, 539.5, 34.2, 60.2, 16.4),
                ("ข้าวราดหมูกระเทียมพริกไท", 40, 617.7, 28, 66.6, 25.3),
                ("ข้าวราดไก่ทอดกระเทียมพริกไท", 40, 773.6, 39.9, 80.6, 31.5),
                ("ข้าวราดผัดกะเพราหมูกรอบ", 45, 753.8, 14.3, 50.5, 54),
                ("ข้าวราดผัดพริกอ่อน", 40, 570.4, 18.6, 78, 19.6),
                ("ข้าวราดหมูผัดพริกใบมะกรูด", 45, 791.8, 38.8, 77.8, 38.7),
                ("ข้าวราดกะเพราหมูสับไข่ดาว", 45, 594.2, 39.1, 54.1, 23.8),
                ("ข้าวราดแพนงกุ้ง", 50, 665.4, 51.7, 58.2, 23),
                ("ข้าวราดคะน้าหมูกรอบ", 45, 753.1, 11.7, 61.7, 50.4),
                ("ข้าวราดผัดพริกแกงปลาดุกทอดกรอบ", 45, 508.7, 34.8, 63.2, 12.5),
                ("ข้าวราดผัดกะเพราอกไก่", 30, 466.4, 37.6, 52.7, 11),
                ("ข้าวราดหมูพะโล้ใส่ไข่", 45, 535, 25.1, 66.3, 18.8),
                ("ข้าวราดไข่ระเบิด", 35, 535.2, 20.4, 51.6, 26.6),
                ("ข้าวราดไข่เจียวหมูสับ", 30, 889.8, 31.8, 46.7, 63.3),
                ("ข้าวราดเนื้อผัดน้ำมันหอย", 45, 565, 31, 63.9, 21.3),
                ("ข้าวราดกุ้งผัดพริกเผา", 50, 462, 19.7, 56.9, 24.3),
                ("สลัดผัก3สีไข่ต้ม", 35, 130, 6, 11, 6),
                ("สเต็กหมู", 69, 488, 78.4, 0, 17.2),
                ("ก๋วยเตี๋ยวบะหมี่แห้งหมูมะนาว", 50, 946.6, 47.4, 80.5, 55),
                ("ก๋วยเตี๋ยววุ้นเส้นเย็นตาโฟ", 45, 420, 11.3, 63.1, 13.6),
                ("ก๋วยเตี๋ยวเส้นใหญ่เย็นตาโฟ", 45, 381, 17.5, 42, 15.9),
                ("ก๋วยเตี๋ยวเส้นใหญ่เนื้อสับ", 50, 616, 26.6, 54.8, 34.9),
                ("ก๋วยเตี๋ยวคั่วไก่", 45, 602.5, 55.2, 58.2, 18),
                ("ก๋วยเตี๋ยวผัดขี้เมาหมู", 45, 578.4, 22.9, 37.4, 39),
                ("ซาลาเปาหมูสับ", 25, 202, 4, 24, 10),
                ("ผัดซีอ๊วมาม่าหมู", 40, 983.3, 33.7, 61.8, 67.9),
                ("ข้าวผัดอเมริกัน", 50, 989.4, 42.6, 80.2, 54.7),
                ("ข้าวผัดกุนเชียง", 45, 597.3, 23.5, 59.7, 29.4),
                ("ผัดซีอิ้วเส้นใหญ่หมู", 40, 730.4, 38.6, 62.1, 35.2),
                ("ผัดขี้เมาบะหมี่กุ้ง", 45, 873.8, 39.9, 79.2, 45.2),
                ("ผัดขี้เมามะกะโรนีรวมมิตร", 50, 1086.4, 60.3, 62.9, 65.8),
                ("ข้าวผัดปู", 55, 511, 15.5, 68.8, 19.1),
                ("ต้มยำกุ้ง", 70, 873.7, 161.9, 52.5, 5.5),
                ("ต้มจับฉ่าย", 30, 61.4, 7.2, 5.2, 1.3),
                ("ข้าวผัดต้มยำอกไก่", 45, 355.3, 22.7, 37.5, 13),
                ("ต้มมะระผักกาดดองเต้าหู้", 40, 404, 15.7, 74.3, 5.8),
                ("ข้าวต้มหมูและผักต้ม", 35, 535.2, 20.4, 51.6, 26.6),
                ("ต้มจืดเต้าหู้อ่อนไก่สับ", 35, 315.1, 45.6, 17.9, 8.7),
                ("ต้มยำปลาทู", 45, 446.5, 45.3, 40.3, 14.4),
                ("ขนมจีนแกงเขียวหวานไก่", 35, 505.7, 23, 57.6, 19.6),
                ("แกงคั่วสับปะรดกุ้ง", 55, 394.9, 13.4, 25.5, 29.4),
                ("แกงเทโพหมูสามชั้น", 50, 790.8, 12.4, 56.5, 58.6),
                ("แกงมะเขือใส่ลูกชิ้น", 30, 248.5, 12.7, 11.5, 16.6),
                ("แกงจืดเต้าหู้หมูสับใส่ผัก", 35, 320, 43.8, 7.4, 14.2),
                ("แกงเห็ด", 30, 206.3, 15.3, 35.5, 3.7),
                ("แกงผักกาด", 30, 148.7, 11.9, 29.9, 1.5),
                ("แกงผักกาดลัวะ", 30, 171.7, 13.8, 24.9, 2),
                ("แกงไก่ลาหู่", 40, 1403.2, 100.8, 24.8, 102),
                ("แกงหมูใส่ฟักเขียว", 45, 1131.9, 109.9, 45.7, 57.4),
                ("แกงเหลืองหน่อไม้ดอง", 30, 149, 20.5, 12.5, 2),
                ("แกงจืดฟักใส่อกไก่", 30, 176, 33.1, 3.4, 3.7),
                ("น่องไก่ทอด", 30, 275.3, 18.3, 0.2, 22.5),
                ("กระเพาะปลา", 45, 682, 38.3, 0, 58.8),
                ("พะแนงไก่ทอด", 50, 1449.9, 42.5, 138.7, 79.6),
                ("ข้าวกระเพราหมูและไก่ทอด", 45, 594.2, 39.1, 54.1, 23.8),
                ("ปลาทอดน้ำปลา", 65, 393, 74.3, 6.9, 5.2),
                ("ปลาทูทอด", 30, 312, 49.8, 0, 12.5),
                ("ข้าวมันไก่ทอด", 40, 1199.9, 40.2, 132.7, 55.6),
                ("ข้าวหมกไก่", 45, 904.6, 55.7, 81.8, 38.4),
                ("หอยทอด", 50, 1290.7, 39.4, 149.3, 60.3),
                ("มันฝรั่งทอด 100g", 39, 323, 3.4, 42.6, 15.5),
                ("ข้าวขาหมูไม่ติดมัน", 45, 409, 20, 53, 13),
                ("ปลาจาระเม๊ดนึ่งบ๊วย", 65, 127, 13, 3, 7),
                ("ปลากระพงนึ่งซีอิ๊ว", 60, 201, 48, 0, 1),
                ("ปลานิลนึ่งตระไคร้", 60, 433.5, 81.2, 12.7, 7),
                ("ไข่ตุ๋นแม่ทำ", 45, 480, 31.1, 3.8, 37.7),
                ("ก๋วยเตี๋ยวเส้นใหญ่น่องไก่ตุ๋น", 45, 427, 30, 43, 15),
                ("ก๋วยเตี๋ยวเส้นใหญ่ลูกชิ้นหมูตุ๋น", 45, 360, 29, 34, 12),
                ("ก๋วยเตี๋ยวเส้นหมี่แห้งหมูตุ๋น", 45, 277, 16, 33, 9),
                ("เกาเหลาเนื้อตุ๋น", 45, 432.1, 20.4, 21.8, 30.5),
                ("มาม่าต้มใส่ไข่", 20, 291, 12.3, 42.4, 7.8),
                ("มาม่าแห้งกับผักบุ้งและอกไก่ลวก", 40, 314, 64.1, 0, 6.5),
                ("สุกี้ยากี้อกไก่", 40, 367, 25.3, 35.4, 13.9),
                ("สุกี้ยากี้น้ำหมู", 40, 273, 15.2, 48.4, 1.7),
                ("สุกี้หมู", 40, 466.9, 57.1, 14.4, 19.2),
                ("สุกี้หมูเส้นบุก", 45, 189.7, 12.1, 12.9, 9.9),
                ("สุกี้รวมมิตรน้ำ", 40, 228, 21, 18, 8),
                ("ปลาซาบะย่าง", 65, 410, 37.2, 0, 27.8),
                ("ไก่ย่างตะไคร้ 100g", 40, 124.8, 22.6, 1.2, 2.6),
                ("ข้าวอกไก่ย่าง", 40, 397.5, 28.4, 43.6, 11.8),
                ("ปลาทับทิมย่างเกลือ", 79, 96, 20.1, 0, 1.7),
                ("เบอร์เกอร์ สเต๊กไก่ย่างถ่าน 90g", 69, 210, 12, 27, 8),
                ("ยำไก่ย่าง", 45, 440, 37, 68, 2.5),
                ("ยำวุ้นเส้นทะเล", 50, 427.3, 40.9, 30.4, 17.2),
                ("ยำหมูยอ", 40, 125.2, 4.2, 14, 6.3),
                ("ยำขนมจีนปลาทูครึ่งตัว", 40, 281, 14, 36, 9),
                ("น้ำยาขนมจีนแกงหมู", 35, 820.3, 67.7, 36.2, 47.8),
                ("ขนมจีนน้ำเงี้ยว", 35, 308, 18.9, 45.6, 5.6),
                ("ขนมจีนน้ำยากะทิปลา", 35, 525.7, 31.1, 58, 18.4),
                ("ส้มตำไข่เค็ม", 45, 172.2, 12.3, 14.2, 6.9),
                ("ส้มตำมะม่วงปลาแห้ง", 40, 555, 65.6, 30, 19.2),
                ("แซนวิชแฮม", 40, 212.4, 10.1, 22.6, 8.9),
                ("แซนวิชหมูหยองครีมสลัดชิ้น", 40, 780, 36, 132, 12),
                ("แซนวิชมายองเนสไข่กุ้งไข่ไก่", 40, 302.3, 20.1, 12.2, 19.5),
                ("ห่อหมกปลา", 45, 507.5, 38.3, 19.4, 31.7),
                ("ห่อหมกไก่", 45, 218, 20.2, 0, 15.2),
                ("ข้าวซอยไก่", 40, 505.7, 23, 57.6, 19.6),
                # Add more items as needed 
            ],
            columns=["FOODS", "cost", "calories", "protein" , "carbs","fat"],
        ).set_index("FOODS")

    user_df = pd.DataFrame(
            [
                ("MinimumNUTR",result_BMR_withGoal, min_Protein,min_fats,min_Carb),
            ],
            columns=["NUTR", "min_calories","min_protein","min_carbs","min_fat"],
        ).set_index("NUTR")
    return food_df,user_df

def GenAMPL():
    # เอาไว้ test code โดยไม่ต้องเสียเวลากรอกข้อมูล
    result_BMR = BMRGen("male",180,80,21)
    result_BMR_withGoal = BulkOrCut(result_BMR,"bulking")

    # ใส่ข้อมูลของผู้ใช้
    age,weigth,high,gender,Goal = information()
    result_BMR = BMRGen(gender,high,weigth,age)
    result_BMR_withGoal = BulkOrCut(result_BMR,Goal)
    min_Protein, min_fats, min_Carbs = divide_values(result_BMR_withGoal)

    ampl = AMPL()
    ampl.set_option("solver", "cplex")

    ampl.eval(
        r"""
        set FOODS;
        set NUTR;

        param cost{FOODS} >= 0;
        param calories{FOODS} >= 0;
        param protein{FOODS} >= 0;
        param fat{FOODS} >= 0;
        param carbs{FOODS} >= 0;

        param min_calories{NUTR};
        param min_protein{NUTR};
        param min_fat{NUTR};
        param min_carbs{NUTR};
        
        
        var Quantity{FOODS} integer >= 0;
        var Calories_gained = sum{f in FOODS} calories[f] * Quantity[f]>= 0.00 within Reals;
        var Protein_gained = sum{f in FOODS} protein[f] * Quantity[f]>= 0.00 within Reals;
        var Fat_gained = sum{f in FOODS} fat[f] * Quantity[f]>= 0.00 within Reals;
        var Carbohydrates_gained = sum{f in FOODS} carbs[f] * Quantity[f]>= 0.00 within Reals;

        minimize TotalCost: sum{f in FOODS} (cost[f] * Quantity[f]);

        subject to MinCalories{i in NUTR}: sum{f in FOODS} (calories[f] * Quantity[f]) >= min_calories[i];
        subject to MinProtein{i in NUTR}: sum{f in FOODS} (protein[f] * Quantity[f]) >= min_protein[i];
        subject to MinFat{i in NUTR}: sum{f in FOODS} (fat[f] * Quantity[f]) >= min_fat[i];
        subject to MinCarbs{i in NUTR}: sum{f in FOODS} (carbs[f] * Quantity[f]) >= min_carbs[i];
        subject to SelectFoodOnce {f in FOODS}:Quantity[f] <= 1;

        
    """
    )
    food_df,user_df = prepare_data(result_BMR_withGoal,min_Protein,min_fats,min_Carbs)
    ampl.set_data(food_df, "FOODS")
    ampl.set_data(user_df,"NUTR")
    ampl.solve()

    totalcost = ampl.get_objective("TotalCost")
    print("\n\n\n\n----------Recommend---------- \nCalories per day: ", result_BMR_withGoal)
    print("Protein per day: ", min_Protein)
    print("fat per day: ", min_fats)
    print("Crab per day: ", min_Carbs)
    print("TotalCost is:", totalcost.value())
    df = ampl.get_variable("Quantity").get_values().to_pandas()
    df_filtered = df.loc[df['Quantity.val'] == 1]
    print("\n----------MENU SET----------")
    print(df_filtered)

    TotalCalories = ampl.get_variable("Calories_gained").get_values()
    TotalProtein = ampl.get_variable("Protein_gained").get_values()
    TotalFat = ampl.get_variable("Fat_gained").get_values()
    TotalCarbs = ampl.get_variable("Carbohydrates_gained").get_values()
    print("\n----------Total Nutrition----------\n" ,TotalCalories,TotalProtein,TotalFat,TotalCarbs)


    # รายการอาหารทั้งหมด
    print(food_df)


if __name__ == "__main__":
    try:
        GenAMPL()
    except Exception as e:
        print(e)
        raise
