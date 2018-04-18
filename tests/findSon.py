# encoding=utf-8

d = {
         '1': 0,
         '2':1,
         '3':2,
         '4':1,
         '5':2,
         '6':1,
         '7':6,
         '8':6,
         '9':0,
         '10':9,
     }

a=[]
j = 0

def getAllSon(i, dict_list):
    global a, j
    j += 1
    for key, value in dict_list.items():
        if value == int(i):
            a.append(key)
            getAllSon(key, dict_list)


def getAllSon2(i, dict_list):
    a=[]
    for key, value in dict_list.items():
        if value == int(i):
            a.append(key)
            getAllSon2(key, dict_list)
    return a


if __name__ == '__main__':
    print getAllSon2(1, d)
    print a,j
