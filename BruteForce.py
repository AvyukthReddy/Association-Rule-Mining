import pandas as pd
import time
from itertools import combinations
import math

db1 = pd.read_csv('d:/1.csv', header=None)
print("Database 1:")
print(db1)
print()

db1_l = db1.values.tolist()  # Converting CSV to List
db1_list = []
for i in db1_l:
    l = []
    for j in i:
        if type(j) == str:  # Removing Nan values (Not A Number) from Transactions
            j = j.strip()
            l.append(j)
    db1_list.append(l)

print("Transactions After Removing Redundancy:")
for i in db1_list:
    print(i)
print()

total_transactions = len(db1_list)  # Total No. of. Transactions

min_support = float(input("Minimum Support (In %): "))
min_confidence = float(input("Minimum Confidence (In %): "))

# Stores particular instance of time immediately after triggering the program
start_time = time.time()

# Converting min_support from percentage to float
s = total_transactions * (min_support / 100)
size = 0
ans = []
flist = []
items = []
association_rules = {}


def freq(list_l):  # Function to calculate frequency
    f = {}
    if size == 0:
        for i in list_l:
            for j in i:
                if j not in f.keys():
                    f[j] = 1
                    items.append(j)
                else:
                    f[j] = f[j] + 1
    elif size > 0:
        for i in list_l:
            if i not in f.keys():
                f[i] = 1
            else:
                f[i] += 1
    flist.append(f)


def checkminsup(list_l):
    l = []
    freq(list_l)
    for i in flist[size].keys():
        l.append(i)
    ans.append(l)


def unique_items(list_1):  # Function to return all the unique items
    l = []
    if size == 1:
        l = list_1
    else:
        for i in list_1:
            for j in i:
                if j not in l:
                    l.append(j)
    return l


def calc_sup(count_itemset, count_total):  # Function that computes support
    temp_s = 100 * (count_itemset / count_total)
    return temp_s


def calc_conf(count_LHSRHS, count_LHS):  # Function that computes confidence
    temp_c = 100 * (count_LHSRHS / count_LHS)
    return temp_c


def fact(a, b):  # Return Factorial for Total No of Combinations
    return math.factorial(a)/math.factorial(b)


def calc_confidence():  # Stores all the subsets of frequent itemsets to calculate confidence
    for item in fans:
        if (len(item)) < 2:  # Confidence cannot be computed for Itemsets of size 1
            continue
        for i in range(1, len(item)):
            LHS = []  # Stores LHS part of the Association Rule
            RHS = []  # Stores RHS part of the Association Rule
            idx = []  # Stores the position of index in the LHS part

            for j in range(i):
                idx.append(j)

            for j in idx:
                LHS.append(item[j])

            for j in range(len(item)):
                if j not in idx:
                    RHS.append(item[j])

            total_count = 0  # Total No. of. Transactions in the Database
            LHS_count = 0  # Total No. of. Occurences of the item in the LHS part
            for ITEM in range(len(db1_list)):
                if (all(x in db1_list[ITEM] for x in LHS)):
                    LHS_count += 1
                    if (all(x in db1_list[ITEM] for x in RHS)):
                        total_count += 1

            temp_c = calc_conf(calc_sup(total_count, total_transactions), calc_sup(
                LHS_count, total_transactions))
            if temp_c >= min_confidence:  # Eliminates Association Rules if confidence < min_confidence
                key = ""
                val = ""

                for j in LHS:
                    key += " " + j
                key = key.strip()

                for j in RHS:
                    val += " " + j
                val = val.strip()

                if key in association_rules.keys():
                    association_rules[key].append([val, round(temp_c, 2)])

                else:
                    l = []
                    l.append([val, round(temp_c, 2)])
                    association_rules[key] = l

            last_idx = len(idx) - 1
            total_combinations = fact(len(item), i)

            while total_combinations:
                LHS = []  # Emptying LHS
                RHS = []  # Emptying RHS

                for j in range(i-1, -1, -1):
                    if (idx[j] < (len(item)-(last_idx-j)-1)):
                        t_idx = idx[j] + 1

                        for k in range(j, i):
                            idx[k] = t_idx
                            t_idx += 1
                        break
                    else:
                        continue

                for j in idx:  # Stores LHS
                    LHS.append(item[j])

                for j in range(len(item)):  # Stores RHS
                    if j not in idx:
                        RHS.append(item[j])

                total_count = 0  # Total No. of. Transactions in the Database
                LHS_count = 0  # Total No. of. Occurences of the item in the LHS part
                for ITEM in range(len(db1_list)):
                    if (all(x in db1_list[ITEM] for x in LHS)):
                        LHS_count += 1
                        if (all(x in db1_list[ITEM] for x in RHS)):
                            total_count += 1

                temp_c = calc_conf(calc_sup(total_count, total_transactions), calc_sup(
                    LHS_count, total_transactions))
                if temp_c < min_confidence:
                    total_combinations -= 1
                    continue

                key = ""  # Ignores Association Rules if confidence < min_confidence
                val = ""
                for j in LHS:
                    key += " " + j
                key = key.strip()
                for j in RHS:
                    val += " " + j
                val = val.strip()

                if key in association_rules.keys():
                    if (val not in [item[0] for item in association_rules[key]]):
                        association_rules[key].append([val, round(temp_c, 2)])
                else:
                    temp = []
                    temp.append([val, round(temp_c, 2)])
                    association_rules[key] = temp
                total_combinations -= 1


if size == 0:
    checkminsup(db1_list)  # Helps in identifying Frequent Itemsets of size 1
    size += 1

while len(ans[-1]) > 0:  # Helps in identifying Frequent Itemsets of size > 1
    newl1 = unique_items(ans[size-1])
    newl1 = combinations(newl1, size+1)
    newl1 = list(newl1)
    fl = []
    for i in newl1:
        for j in db1_list:
            condition = set(i).issubset(set(j))
            if condition:
                fl.append(frozenset(i))
    checkminsup(fl)
    size += 1

for i in range(len(ans)-1):  # Printing all the possible Frequent Itemsets
    print("\nFrequent Itemset", end="")
    if len(ans[i]) > 1:
        print("s", end="")
    print(" of Size", i+1, "Satisfying Minimum Support Condition", end=":\n")
    if i == 0:
        for j in ans[i]:
            fval = flist[i][j]
            print("{", end="")
            print(j, end="")
            print("}:", fval)
    else:
        for j in ans[i]:
            fval = flist[i][j]
            k = list(j)
            print("{", end="")
            for l in k[:-1]:
                print(l, end=", ")
            print(k[-1], end="}: ")
            print(fval)

fans = []
for i in range(len(ans)):
    if i == 0:
        for j in ans[i]:
            fans.append([j])
    else:
        for j in ans[i]:
            k = list(j)
            fans.append(k)

if (ans[1] != []):  # Calculating confidence of all the possible itemsets
    calc_confidence()
    print("\nConfidence of all the Possible Association Rules:")
    for key in association_rules:
        for value in association_rules[key]:
            print("{", end="")
            for j in key:
                if j == " ":
                    print(", ", end="")
                else:
                    print(j, end="")
            print("} -> {", end="")
            for j in range(len(value[0])):
                if value[0][j] == " ":
                    if j == 0:
                        continue
                    else:
                        print(end=", ")
                else:
                    print(value[0][j], end="")
            print("} <=> Confidence: " + str(value[1]) + "%")

total_time = time.time()-start_time
print("\nTotal Time taken for Computation using Brute Force:", total_time)
