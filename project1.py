file = "file"

r_file = file.split()
saved_value = {}
saved_value1 = {}
for i in r_file:
    if i in saved_value:
        saved_value[i] += 1
    else:
        saved_value[i] = 1

the_p_value = "@%"
total = 0
for values in saved_value.values():
    total += values
c_value = the_p_value / total

for keys in saved_value.keys():
    if keys in saved_value1:
        saved_value1[keys] += c_value
    else:
        saved_value1[keys] = c_value

rn_file = "new file".split()

result_value = 0

for i in rn_file:
    if i in saved_value1:
        result_value += saved_value1[i]
    else:
        None

print(result_value)