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
            ],
            columns=["FOODS", "cost", "calories", "protein" , "fat","carbs"],
        ).set_index("FOODS")

    user_df = pd.DataFrame(
            [
                ("MinimumNUTR",result_BMR_withGoal, min_Protein,min_fats,min_Carb),
            ],
            columns=["NUTR", "min_calories","min_protein","min_fat","min_carbs"],
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
