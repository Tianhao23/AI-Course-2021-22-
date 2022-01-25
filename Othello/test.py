d = {5: [5,6,7], 6:[7,8,9,9], 10:[23]}
for i in d:
    print(i)
#speed up: using bitboards
# for i in danger:
    #     if i in possibleSet:
    #         worstM.add(i)
    
    #         possibleSet.discard(i)
    # if 0 in possibleSet and pzl[1] == opposite: 
    #     for i in range(2, 7): 
    #         if pzl[i] == '.': return i
    # if 7 in possibleSet and pzl[6] == opposite:
    #     for i in range(5, 1, -1): 
    #         if pzl[i] == '.': return i
    # if 56 in possibleSet: return 56
    # if 63 in possibleSet: return 63
#  40  30  60  64  46  55  62  48  39  60
#  43  54  64  32  50  47  56  32  58  62
#  50  58  44  60  58  28  54  56  48  50
#  46  56  64  51  55  52  55  48  57  57
#  44  38  44  64  62  60  62  57  58  48
#  46  52  50  54  51  58  56  34  62  55
#  58  56  54  56  57  54  42  55  56  62
#  50  34  60  61  54  40  47  58  53  48
#  56  32  50  28  60  54  64  36  42  28
#  58  62  64  59  50  58  63  54  48  32
# My tokens: 5705; Total tokens: 6253
# Score: 91.2%
# NM/AB LIMIT: 14
# Game 26 as O => 28:
# 19184411_3_4_5201321_91710_024_22916_8221432_13426252338333746_743_61230414047394245315452516253486315566061595550584957
# Game 84 as O => 28:
# 4445265254386063311846342517414249243332_81062193755_2562940472050114857_9_043_116_3126158_4533930595123221415_7_6_51321
# Elasped time: 179.5s