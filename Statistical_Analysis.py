#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      patri
#
# Created:     30/01/2019
# Copyright:   (c) patri 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

def Normalized_Data():

    from dtw import dtw
    import numpy as np
    import matplotlib.pyplot as plt
    import csv
    import itertools
    import numpy.core.defchararray as np_f

    x_normalized = []
    y_normalized = []

    Data1 = []
    Data2 = []
    Data3 = []

    List = []
    List2 = []
    List3 = []

    DTW_Sat = []
    DTW_Week = []

    FID = []
    Longitude = []
    Latitude = []

    count1 = 0
    count2 = 0


    Regular_Sat_Location = r'C:\Users\patri\Desktop\Thesis_Final\Data_From_Extraction\M05_D07_HL_Edit_Regular_Sat.csv'
    Regular_Weekday_Location = r'C:\Users\patri\Desktop\Thesis_Final\Data_From_Extraction\M05_D25_HL_Edit_Regular_Weekday.csv'
    Memorial_Day_Location = r'C:\Users\patri\Desktop\Thesis_Final\Data_From_Extraction\M05_D28_HL_Edit_Memorial_Day_Sat.csv'

    with open(Regular_Sat_Location) as file:
        reader = csv.reader(file, delimiter=',')

        for column in reader:

            Data1.append(column[2])

            FID.append(column[0])

            Longitude.append(column[5])

            Latitude.append(column[4])

    FID.remove(FID[0])
    Longitude.remove(Longitude[0])
    Latitude.remove(Latitude[0])
    Data1.remove(Data1[0])

    with open(Regular_Weekday_Location) as file:
            reader = csv.reader(file, delimiter=',')

            for column in reader:

                Data2.append(column[2])

    Data2.remove(Data2[0])

    with open(Memorial_Day_Location) as file:
        reader = csv.reader(file, delimiter=',')

        for column in reader:

            Data3.append(column[2])

    Data3.remove(Data3[0])


    for day in Data1:

        result = [i.strip() for i in day.split(',')]
        List.append(result)

    Reg_Sat_List = list(itertools.chain.from_iterable(List))

    for day2 in Data2:

        result2 = [i2.strip() for i2 in day2.split(',')]
        List2.append(result2)

    Reg_Weekday_List = list(itertools.chain.from_iterable(List2))

    for day3 in Data3:

        result3 = [i3.strip() for i3 in day3.split(',')]
        List3.append(result3)

    Memorial_Day_List = list(itertools.chain.from_iterable(List3))


    x_with_string = np.array(Reg_Sat_List).reshape(-1, 1)
    findx = np_f.replace(x_with_string, 'NA', '0')
    Reg_Sat_Input = np.array(findx, dtype=int).reshape(-1,1)

    Reg_Sat_Input_split = np.split(Reg_Sat_Input,24)

    y_with_string = np.array(Reg_Weekday_List).reshape(-1, 1)
    findy = np_f.replace(y_with_string, 'NA', '0')
    Reg_Weekday_Input = np.array(findy, dtype=int).reshape(-1,1)

    Reg_Weekday_Input_split = np.split(Reg_Weekday_Input,24)

    x_with_string = np.array(Memorial_Day_List).reshape(-1, 1)
    findx = np_f.replace(x_with_string, 'NA', '0')
    Memorial_Day_List_Input = np.array(findx, dtype=int).reshape(-1,1)

    Memorial_Day_List_Input_split = np.split(Memorial_Day_List_Input,24)


    for x_hour_frequency in Memorial_Day_List_Input_split:

        for y_hour_frequency in Reg_Sat_Input_split:


            max = np.amax(x_hour_frequency)
            x_normalized_weeks = np.true_divide(x_hour_frequency,max)

            max2 = np.amax(y_hour_frequency)
            y_normalized_weeks = np.true_divide(y_hour_frequency,max2)

            l2_norm = lambda x_normalized_weeks, y_normalized_weeks: (x_normalized_weeks - y_normalized_weeks) ** 2

            dist = dtw(x_normalized_weeks, y_normalized_weeks, dist=l2_norm)

            DTW_Sat.append(dist[0])

            count1 += 1

            count2 += 1

    for x_hour_frequency in Memorial_Day_List_Input_split:

        for y_hour_frequency in Reg_Weekday_Input_split:


            max = np.amax(x_hour_frequency)
            x_normalized_weeks = np.true_divide(x_hour_frequency,max)

            max2 = np.amax(y_hour_frequency)
            y_normalized_weeks = np.true_divide(y_hour_frequency,max2)

            l2_norm = lambda x_normalized_weeks, y_normalized_weeks: (x_normalized_weeks - y_normalized_weeks) ** 2

            dist = dtw(x_normalized_weeks, y_normalized_weeks, dist=l2_norm)

            DTW_Week.append(dist[0])

            count1 += 1

            count2 += 1

    """
    #l2_norm = lambda Test_List_x, Test_List_y: (Test_List_x - Test_List_y) ** 2

    #dist, cost_matrix, acc_cost_matrix, path = dtw(Test_List_x, Test_List_y, dist=l2_norm)

    #print(dist)

    #For the dynamic time warping distance, the smaller the distance, the more
    #similar they are. The larger the distance, the less similar they are.

    plt.imshow(acc_cost_matrix.T, origin='lower', cmap='gray', interpolation='nearest')
    plt.plot(path[0], path[1], 'w')
    plt.show()
    """

    Big_File_Sat = zip(FID,Latitude,Longitude,DTW_Sat)

    Big_File_Week = zip(FID,Latitude,Longitude,DTW_Week)

    Sat_CSV = r"C:\Users\patri\Desktop\Thesis_Final\Results\Sat_CSV.csv"

    Weekday_CSV = r"C:\Users\patri\Desktop\Thesis_Final\Results\Weekday_CSV.csv"

    with open(Sat_CSV, 'w') as file2:

        csv_writer = csv.writer(file2, delimiter=',')

        file2.write('FID,Latitude,Longitude,DTW_Distance'+'\n')

        for line in Big_File_Sat:

            file2.write(''.join(str(line[0]))+','+''.join(str(line[1]))+','+''.join(str(line[2]))+','+''.join(str(line[3]))+','+'\n')


    with open(Weekday_CSV, 'w') as file3:

        csv_writer = csv.writer(file3, delimiter=',')

        file3.write('FID,Latitude,Longitude,DTW_Distance'+'\n')

        for line in Big_File_Week:

            file3.write(''.join(str(line[0]))+','+''.join(str(line[1]))+','+''.join(str(line[2]))+','+''.join(str(line[3]))+','+'\n')


if __name__ == '__main__':
    main()
    Normalized_Data()


