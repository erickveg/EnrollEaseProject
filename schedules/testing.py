# #%%
# data =  [['BUS100_01',   'BUS100_05', 'ED444_02', 'CHILD210_01'],
#          ['CHILD210_08', 'CHILD210_12' ],
#          ['BUS100_03',   'CSE382_01', 'CHILD210_03'],
#          ['CHILD210_06'],
#          ['CHILD210_02'],
#          ['CHILD210_11']]

# master_combinations = []
# combinations = []

# def same_code_in_list(string, list):
#     for i in list:
#         if string.split("_")[0] in i.split("_")[0]:
#             return True
#     return False

# def combination_has_course_from_same_sublist(combination, sublist):
#     for course in combination:
#         if course in sublist:
#             return True
#     return False

# for i in range(len(data)):
#     for j in range(len(data[i])):
#         primary_course = data[i][j]
#         combinations.append([primary_course])

#         for k in range(len(data[i+1:])): # iterate through the rest of the lists
#             for l in range(len(data[i+1:][k])):
#                 secondary_course = data[i+1+k][l]
                
#                 combinations_length = len(combinations)
#                 for c in range(combinations_length):
#                     combination = combinations[c]

#                     # if the secondary_course code is not in the list of combinations AND
#                     # if the seconday_course is not in the same list sub-list
#                     if not same_code_in_list(secondary_course, combination) and not combination_has_course_from_same_sublist(combination, data[i+1+k]):   
#                         temp_comb = combination[:]
#                         temp_comb.append(secondary_course)
#                         combinations.append(temp_comb)

#         master_combinations.append(combinations)
#         combinations = []

# for m in master_combinations:
#     print(len(m))

# print()
# print()


#%%
class Section:
    def __init__(self, section_code, time, days):
        self.section_code = section_code
        self.time = time
        self.days = [d for d in days if d.isalpha()]

    def __str__(self):
        days_str = "".join(self.days)
        return f"{self.section_code} {self.time} {days_str}"
    
    def __repr__(self):
        days_str = "".join(self.days)
        return f"{self.section_code} {self.time} {days_str}"
    

master_combinations = []
combinations = []

# '1015-1115': ['BUS100_01',   'BUS100_05', 'ED444_02', 'CHILD210_01'],
# '1130-1230': ['CHILD210_08', 'CHILD210_12' ],
# '1245-1345': ['BUS100_03',   'CSE382_01', 'CHILD210_03'],
# '1315-1445': ['CHILD210_06'],
# '1400-1500': ['CHILD210_02'],
# '1515-1645': ['CHILD210_11']}   

# T: 12:45AM-01:45PM  : BUS100_02           # T: 10:15-11:15AM  : ED444_01

 
    
sections = [   
    Section("BUS100_01", "1015-1115", "MWF"),
    Section("BUS100_05", "1015-1115", "MWF"),
    Section("ED444_02", "1015-1115", "MWF"),
    Section("CHILD210_01", "1015-1115", "MWF"),
    Section("CHILD210_08", "1130-1230", "MWF"),
    Section("CHILD210_12", "1130-1230", "MWF"),
    Section("BUS100_03", "1245-1345", "MWF"),
    Section("CSE382_01", "1245-1345", "MWF"),
    Section("CHILD210_03", "1245-1345", "MWF"),
    Section("CHILD210_06", "1315-1445", "MWF"),
    Section("CHILD210_02", "1400-1500", "MWF"),
    Section("CHILD210_11", "1515-1645", "MWF"),
    Section("TEST101_01", "1015-1115", "M"),
    Section("TEST101_02", "1130-1230", "M"),
    Section("BUS100_02", "1245-1345", "T"),
    Section("ED444_01", "1015-1115", "T")
    ]

def same_code_in_combination(section, combination):
    for s in combination:
        if section.section_code.split("_")[0] in s.section_code.split("_")[0]:
            return True
    return False

def same_time_in_combination(section, combination):
    for s in combination:
        if section.time == s.time:
            return True
    return False

def same_days_in_combination(section, combination):
    for s in combination:
        return any(item in s.days for item in section.days)

for i in range(len(sections)):
    primary_course = sections[i]
    combinations.append([primary_course])

    for k in range(len(sections[i+1:])): # iterate through the rest of the lists
        secondary_course = sections[i+1+k]
        
        combinations_length = len(combinations)
        for c in range(combinations_length):
            combination = combinations[c]

            # if the secondary_course code is not in the list of combinations AND
            # if the seconday_course is not in the same list sub-list
            if not same_code_in_combination(secondary_course, combination) and\
              (not same_time_in_combination(secondary_course, combination) or\
                (same_time_in_combination(secondary_course, combination) and not same_days_in_combination(secondary_course, combination))):   
                temp_comb = combination[:]
                temp_comb.append(secondary_course)
                combinations.append(temp_comb)

    master_combinations.append(combinations)
    combinations = []

for m2_ in master_combinations:
    print(len(m2_))
    print()

