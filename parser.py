"""

Parsing Verilog Netlist file and perform fault collapsing

"""

# Taking Filename input
verilogFile = input('Please enter the file name of the Verilog Netlist = ')

# Dictionary for levels for each gate
level_dict = {'0' : [] , '1' : []}
current_level = 0
all_gates_list = []
all_IOs_list =[]
equivalence_gates = []
same_wire = []
colList = []
ip1List = []
ip2List = []
unique_list = []
repeated_list = []

def get_output(in_word):
    #print(in_word)
    temp = in_word.split(",")
    temp1 = temp[0].split("Y")
    l1 = list(temp1[1])
    end_index = l1.index(')')
    out = ''.join(l1[1:end_index])
    return out

def get_input1(in_word):
    #print(in_word)
    temp = in_word.split(",")
    temp1 = temp[1].split("A")
    l1 = list(temp1[1])
    end_index = l1.index(')')
    out = ''.join(l1[1:end_index])
    return out

def get_input2(in_word):
    #print(in_word)
    temp = in_word.split(",")
    temp1 = temp[2].split("B")
    l1 = list(temp1[1])
    end_index = l1.index(')')
    out = ''.join(l1[1:end_index])
    return out

def get_input(in_word):
    #print(in_word)
    temp = in_word.split(",")
    temp1 = temp[0].split("A")
    l1 = list(temp1[1])
    end_index = l1.index(')')
    out = ''.join(l1[1:end_index])
    return out

def get_level(current_level, input1, input2, input_list):
    level1 = False
    level2 = False
    if input1 in input_list:
        level1 = True
    if input2 in input_list:
        level2 = True
    if level1 == True:
        if level2 == True:
            return 0
        else:
            return 1
    else:
        if level2 == True:
            return 1
        else:
            update_level = current_level + 1
            return update_level

def get_level_inv(current_level, input1, input_list):
    level1 = False
    level2 = False
    if input1 in input_list:
        level1 = True
    if level1 == True:
        return 0
    else:
        update_level = current_level + 1
        return update_level

# 0, 1, 2, and 3 are used as pointers for current remaining stuck-at faults for a wire
# 0 - both stuck-at-1 and stuck-at-0
# 1 - only stuck-at-1
# 2 - only stuck-at-0
# 3 - none
def equivalence_check(in_list):
    if 'NAND2X1' in in_list:
        if in_list[6] == 0:
            in_list[6] = 1
        elif in_list[6] == 1:
            pass
        elif in_list[6] == 2:
            in_list[6] = 3
        elif in_list[6] == 3:
            pass
        if in_list[7] == 0:
            in_list[7] = 1
        elif in_list[7] == 1:
            pass
        elif in_list[7] == 2:
            in_list[7] = 3
        elif in_list[7] == 3:
            pass
        return in_list
    if 'NOR2X1' in in_list:
        if in_list[6] == 0:
            in_list[6] = 2
        elif in_list[6] == 1:
            in_list[6] = 3
        elif in_list[6] == 2:
            pass
        elif in_list[6] == 3:
            pass
        if in_list[7] == 0:
            in_list[7] = 2
        elif in_list[7] == 1:
            in_list[7] =3
        elif in_list[7] == 2:
            pass
        elif in_list[7] == 3:
            pass
        return in_list
    if 'AND2X1' in in_list:
        if in_list[6] == 0:
            in_list[6] = 1
        elif in_list[6] == 1:
            pass
        elif in_list[6] == 2:
            in_list[6] = 3
        elif in_list[6] == 3:
            pass
        if in_list[7] == 0:
            in_list[7] = 1
        elif in_list[7] == 1:
            pass
        elif in_list[7] == 2:
            in_list[7] = 3
        elif in_list[7] == 3:
            pass
        return in_list
    if 'OR2X1' in in_list:
        if in_list[6] == 0:
            in_list[6] = 2
        elif in_list[6] == 1:
            in_list[6] = 3
        elif in_list[6] == 2:
            pass
        elif in_list[6] == 3:
            pass
        if in_list[7] == 0:
            in_list[7] = 2
        elif in_list[7] == 1:
            in_list[7] = 3
        elif in_list[7] == 2:
            pass
        elif in_list[7] == 3:
            pass
        return in_list
    if 'INVX1' in in_list:
        if in_list[4] == 0:
            in_list[4] = 1
        if in_list[5] == 0:
            in_list[5] = 1
        return in_list
    if 'BUFX1' in in_list:
        if in_list[4] == 0:
            in_list[4] = 3
        elif in_list[5] == 0:
            in_list[5] == 3
        elif in_list[4] == 1 or in_list[4] == 2:
            in_list[4] = 3
        elif in_list[5] == 1 or in_list[5] == 2:
            in_list[5] = 3

with open (verilogFile) as fo:
    for itr in fo:
        words = itr.split()
        #print(words)
        previous_level = current_level
        #print(itr)
        if words == []:
            pass
        elif words[0] == "module":
            print('The name of the input module is {}\n'.format(words[1]))
        elif words[0] == "input":
            print('The input wires are {}'.format(words[1]))
            temp = words[1].split(';')
            input_list = temp[0].split(',')
        elif words[0] == "output":
            print('The output wires are {}'.format(words[1]))
        elif words[0] == "wire":
            print('The wires used in the design are {}'.format(words[1]))
        elif words[0] == "fanout2":
            pass
        elif words[0] == "NAND2X1":
            output1 = get_output(words[2])
            input1 = get_input1(words[2])
            input2 = get_input2(words[2])
            all_IOs_list.append([output1, input1, input2])
            all_gates_list.append([words[0], words[1], output1, input1, input2, 0, 0, 0])
            current_level = get_level(previous_level, input1, input2, input_list)
            if str(current_level) not in level_dict:
                level_dict[str(current_level)] = []
            value = level_dict[str(current_level)]
            value.append(words[1])
            level_dict[str(current_level)] = value
        elif words[0] == "NOR2X1":
            output1 = get_output(words[2])
            input1 = get_input1(words[2])
            input2 = get_input2(words[2])
            all_IOs_list.append([output1, input1, input2])
            all_gates_list.append([words[0], words[1], output1, input1, input2, 0, 0, 0])
            current_level = get_level(previous_level, input1, input2, input_list)
            if str(current_level) not in level_dict:
                level_dict[str(current_level)] = []
            value = level_dict[str(current_level)]
            value.append(words[1])
            level_dict[str(current_level)] = value
        elif words[0] == "AND2X1":
            output1 = get_output(words[2])
            input1 = get_input1(words[2])
            input2 = get_input2(words[2])
            all_IOs_list.append([output1, input1, input2])
            all_gates_list.append([words[0], words[1], output1, input1, input2, 0, 0, 0])
            current_level = get_level(previous_level, input1, input2, input_list)
            if str(current_level) not in level_dict:
                level_dict[str(current_level)] = []
            value = level_dict[str(current_level)]
            value.append(words[1])
            level_dict[str(current_level)] = value
        elif words[0] == "OR2X1":
            output1 = get_output(words[2])
            input1 = get_input1(words[2])
            input2 = get_input2(words[2])
            all_IOs_list.append([output1, input1, input2])
            all_gates_list.append([words[0], words[1], output1, input1, input2, 0, 0, 0])
            current_level = get_level(previous_level, input1, input2, input_list)
            if str(current_level) not in level_dict:
                level_dict[str(current_level)] = []
            value = level_dict[str(current_level)]
            value.append(words[1])
            level_dict[str(current_level)] = value
        elif words[0] == "XOR2X1":
            output1 = get_output(words[2])
            input1 = get_input1(words[2])
            input2 = get_input2(words[2])
            all_IOs_list.append([output1, input1, input2])
            all_gates_list.append([words[0], words[1], output1, input1, input2, 0, 0, 0])
            current_level = get_level(previous_level, input1, input2, input_list)
            if str(current_level) not in level_dict:
                level_dict[str(current_level)] = []
            value = level_dict[str(current_level)]
            value.append(words[1])
            level_dict[str(current_level)] = value
        elif words[0] == "XNOR2X1":
            output1 = get_output(words[2])
            input1 = get_input1(words[2])
            input2 = get_input2(words[2])
            all_IOs_list.append([output1, input1, input2])
            all_gates_list.append([words[0], words[1], output1, input1, input2, 0, 0, 0])
            current_level = get_level(previous_level, input1, input2, input_list)
            if str(current_level) not in level_dict:
                level_dict[str(current_level)] = []
            value = level_dict[str(current_level)]
            value.append(words[1])
            level_dict[str(current_level)] = value
        elif words[0] == "INVX1":
            output1 = get_output(words[2])
            input1 = get_input1(words[2])
            all_IOs_list.append([output1, input1, 0])
            all_gates_list.append([words[0], words[1], output1, input1, 0, 0])
            current_level = get_level_inv(previous_level, input1, input_list)
            #level_dict_inv[words[1]] = current_level
            if str(current_level) not in level_dict:
                level_dict[str(current_level)] = []
            value = level_dict[str(current_level)]
            value.append(words[1])
            level_dict[str(current_level)] = value
        elif words[0] == "BUFX1":
            output1 = get_output(words[2])
            input1 = get_input1(words[2])
            all_IOs_list.append([output1, input1, 0])
            all_gates_list.append([words[0], words[1], output1, input1, 0, 0])
            if str(current_level) not in level_dict:
                level_dict[str(current_level)] = []
            value = level_dict[str(current_level)]
            value.append(words[1])
            level_dict[str(current_level)] = value
    # Finding and Printing total number of Single Stuck-at-Faults
    for i in range(0,all_IOs_list.__len__()):
        for j in range(0,3):
            if all_IOs_list[i][j] in unique_list:
                repeated_list.append(all_IOs_list[i][j])
            else:
                unique_list.append(all_IOs_list[i][j])
    for k in range(0,input_list.__len__()):
        if input_list[k] in unique_list:
            repeated_list.append(input_list[k])
        else:
            unique_list.append(input_list[k])

for i in range(0, all_IOs_list.__len__()):
    colList.append(all_IOs_list[i][0])
    ip1List.append(all_IOs_list[i][1])
    ip2List.append(all_IOs_list[i][2])

for i in range(0, all_IOs_list.__len__()):
    if colList[i] in ip1List:
        same_wire.append(colList[i])
    elif colList[i] in ip2List:
        same_wire.append(colList[i])

if 0 in unique_list:
    unique_list.remove(0)
unique_wires = len(unique_list)
total_faults = 2 * unique_wires
print('The total number of faults before collapsing are {}'.format(total_faults))

# Equivalence Fault Collapsing
for i in range(0, level_dict.__len__()):
    ext_list = level_dict[str(i)]
    for j in range(0, ext_list.__len__()):
        gate_check = ext_list[j]
        # find index of gate_check in all_gates_list as gate_index
        gate_index = [(m, gates.index(gate_check))
                      for m, gates in enumerate(all_gates_list)
                      if gate_check in gates]
        temp = gate_index[0]
        act_gate_index = temp[0]
        new_list = all_gates_list[act_gate_index] # gate_index goes here
        equi_gate = equivalence_check(new_list)
        all_gates_list[act_gate_index] = new_list

# Printing output to Text files
name = fo.name
split_name = name.split('.')
filename = split_name[0]
bp = open(filename + '_BF.txt','w')
for i in range(0,unique_list.__len__()):
    bp.write('sa1  {}\n'.format(unique_list[i]))
for i in range(0, unique_list.__len__()):
    bp.write('sa0  {}\n'.format(unique_list[i]))
bp.write('\n\nTotal Faults_BF={}\n'.format(total_faults))
bp.close()

fp = open(filename + '_AF.txt','w')
total_faults_af = 0
for i in range(0,unique_list.__len__()):
    gate_index = [(m, gates.index(unique_list[i]))
                  for m, gates in enumerate(all_gates_list)
                  if unique_list[i] in gates]
    if gate_index == []:
        fp.write('sa1  {}\n'.format(unique_list[i]))
        total_faults_af += 1
    elif gate_index.__len__() == 1:
        temp = gate_index[0]
        act_gate_index = temp[0]
        gate_list = all_gates_list[act_gate_index]
        wire_index = gate_list.index(unique_list[i])
        if gate_list[0] in ['NAND2X1', 'NOR2X1','AND2X1','OR2X1','XOR2X1','XNOR2X1']:
            if wire_index == 2: # Means that the wire from gate list is an output of that gate
                if gate_list[wire_index] in same_wire:
                    pass
                else:
                    if gate_list[wire_index+3] == 0:
                        fp.write('sa1  {}\n'.format(gate_list[wire_index]))
                        total_faults_af += 1
                    elif gate_list[wire_index+3] == 1:
                        fp.write('sa1  {}\n'.format(gate_list[wire_index]))
                        total_faults_af += 1
            else:
                if gate_list[wire_index + 3] == 0:
                    fp.write('sa1  {}\n'.format(gate_list[wire_index]))
                    total_faults_af += 1
                elif gate_list[wire_index + 3] == 1:
                    fp.write('sa1  {}\n'.format(gate_list[wire_index]))
                    total_faults_af += 1
        else:
            if gate_list[0] == 'INVX1' or gate_list[0] == 'BUFX1':
                if wire_index == 2:  # Means that the wire from gate list is an output of that gate
                    if gate_list[wire_index] in same_wire:
                        pass
                    else:
                        if gate_list[wire_index + 2] == 0:
                            fp.write('sa1  {}\n'.format(gate_list[wire_index]))
                            total_faults_af += 1
                        elif gate_list[wire_index + 2] == 1:
                            fp.write('sa1  {}\n'.format(gate_list[wire_index]))
                            total_faults_af += 1
                else:
                    if gate_list[wire_index + 2] == 0:
                        fp.write('sa1  {}\n'.format(gate_list[wire_index]))
                        total_faults_af += 1
                    elif gate_list[wire_index + 2] == 1:
                        fp.write('sa1  {}\n'.format(gate_list[wire_index]))
                        total_faults_af += 1
    else:
        for j in range(0,gate_index.__len__()):
            temp = gate_index[j]
            act_gate_index = temp[0]
            gate_list = all_gates_list[act_gate_index]
            to_find = unique_list[i]
            wire_index = gate_list.index(unique_list[i])
            if gate_list[0] in ['NAND2X1', 'NOR2X1', 'AND2X1', 'OR2X1', 'XOR2X1', 'XNOR2X1']:
                if wire_index == 2:  # Means that the wire from gate list is an output of that gate
                    if gate_list[wire_index] in same_wire:
                        pass
                    else:
                        if gate_list[wire_index + 3] == 0:
                            fp.write('sa1  {}\n'.format(gate_list[wire_index]))
                            total_faults_af += 1
                        elif gate_list[wire_index + 3] == 1:
                            fp.write('sa1  {}\n'.format(gate_list[wire_index]))
                            total_faults_af += 1
                else:
                    if gate_list[wire_index + 3] == 0:
                        fp.write('sa1  {}\n'.format(gate_list[wire_index]))
                        total_faults_af += 1
                    elif gate_list[wire_index + 3] == 1:
                        fp.write('sa1  {}\n'.format(gate_list[wire_index]))
                        total_faults_af += 1
            else:
                if gate_list[0] in ['INVX1', 'BUFX1']:
                    if wire_index == 2:  # Means that the wire from gate list is an output of that gate
                        if gate_list[wire_index] in same_wire:
                            pass
                        else:
                            if gate_list[wire_index + 2] == 0:
                                fp.write('sa1  {}\n'.format(gate_list[wire_index]))
                                total_faults_af += 1
                            elif gate_list[wire_index + 2] == 1:
                                fp.write('sa1  {}\n'.format(gate_list[wire_index]))
                                total_faults_af += 1
                    else:
                        if gate_list[wire_index + 2] == 0:
                            fp.write('sa1  {}\n'.format(gate_list[wire_index]))
                            total_faults_af += 1
                        elif gate_list[wire_index + 2] == 1:
                            fp.write('sa1  {}\n'.format(gate_list[wire_index]))
                            total_faults_af += 1

for i in range(0,unique_list.__len__()):
    gate_index = [(m, gates.index(unique_list[i]))
                  for m, gates in enumerate(all_gates_list)
                  if unique_list[i] in gates]
    if gate_index == []:
        fp.write('sa0  {}\n'.format(unique_list[i]))
        total_faults_af += 1
    elif gate_index.__len__() == 1:
        temp = gate_index[0]
        act_gate_index = temp[0]
        gate_list = all_gates_list[act_gate_index]
        wire_index = gate_list.index(unique_list[i])
        if gate_list[0] in ['NAND2X1', 'NOR2X1', 'AND2X1', 'OR2X1', 'XOR2X1', 'XNOR2X1']:
            if wire_index == 2: # Means that the wire from gate list is an output of that gate
                if gate_list[wire_index] in same_wire:
                    pass
                else:
                    if gate_list[wire_index+3] == 0:
                        fp.write('sa0  {}\n'.format(gate_list[wire_index]))
                        total_faults_af += 1
                    elif gate_list[wire_index+3] == 2:
                        fp.write('sa0  {}\n'.format(gate_list[wire_index]))
                        total_faults_af += 1
            else:
                if gate_list[wire_index + 3] == 0:
                    fp.write('sa0  {}\n'.format(gate_list[wire_index]))
                    total_faults_af += 1
                elif gate_list[wire_index + 3] == 2:
                    fp.write('sa0  {}\n'.format(gate_list[wire_index]))
                    total_faults_af += 1
        else:
            if gate_list[0] == ['INVX1', 'BUFX1']:
                if wire_index == 2:  # Means that the wire from gate list is an output of that gate
                    if gate_list[wire_index] in same_wire:
                        pass
                    else:
                        if gate_list[wire_index + 3] == 0:
                            fp.write('sa0  {}\n'.format(gate_list[wire_index]))
                            total_faults_af += 1
                        elif gate_list[wire_index + 3] == 2:
                            fp.write('sa0  {}\n'.format(gate_list[wire_index]))
                            total_faults_af += 1
                else:
                    if gate_list[wire_index + 3] == 0:
                        fp.write('sa0  {}\n'.format(gate_list[wire_index]))
                        total_faults_af += 1
                    elif gate_list[wire_index + 3] == 2:
                        fp.write('sa0  {}\n'.format(gate_list[wire_index]))
                        total_faults_af += 1
    else:
        for j in range(0,gate_index.__len__()):
            temp = gate_index[j]
            act_gate_index = temp[0]
            gate_list = all_gates_list[act_gate_index]
            to_find2 = unique_list[i]
            wire_index = gate_list.index(unique_list[i])
            if gate_list[0] in ['NAND2X1', 'NOR2X1', 'AND2X1', 'OR2X1', 'XOR2X1', 'XNOR2X1']:
                if wire_index == 2:  # Means that the wire from gate list is an output of that gate
                    if gate_list[wire_index] in same_wire:
                        pass
                    else:
                        if gate_list[wire_index + 3] == 0:
                            fp.write('sa0  {}\n'.format(gate_list[wire_index]))
                            total_faults_af += 1
                        elif gate_list[wire_index + 3] == 2:
                            fp.write('sa0  {}\n'.format(gate_list[wire_index]))
                            total_faults_af += 1
                else:
                    if gate_list[wire_index + 3] == 0:
                        fp.write('sa0  {}\n'.format(gate_list[wire_index]))
                        total_faults_af += 1
                    elif gate_list[wire_index + 3] == 2:
                        fp.write('sa0  {}\n'.format(gate_list[wire_index]))
                        total_faults_af += 1
            else:
                if gate_list[0] in ['INVX1', 'BUFX1']:
                    if wire_index == 2:  # Means that the wire from gate list is an output of that gate
                        if gate_list[wire_index] in same_wire:
                            pass
                        else:
                            if gate_list[wire_index + 3] == 0:
                                fp.write('sa0  {}\n'.format(gate_list[wire_index]))
                                total_faults_af += 1
                            elif gate_list[wire_index + 3] == 2:
                                fp.write('sa0  {}\n'.format(gate_list[wire_index]))
                                total_faults_af += 1
                    else:
                        if gate_list[wire_index + 2] == 0:
                            fp.write('sa0  {}\n'.format(gate_list[wire_index]))
                            total_faults_af += 1
                        elif gate_list[wire_index + 2] == 2:
                            fp.write('sa0  {}\n'.format(gate_list[wire_index]))
                            total_faults_af += 1

fp.write('\nTotal Faults_AF={}\n'.format(total_faults_af))
fp.write('\nCollapse_ratio={}\n'.format(total_faults_af/total_faults))
fp.write('\nEquivalent Classes:\n')

for i in range(0, all_gates_list.__len__()):
    in_list = all_gates_list[i]
    if in_list[0] in ['NAND2X1', 'NOR2X1', 'AND2X1', 'OR2X1']:
        if in_list[5] == 0:
            if in_list[6] == 1:
                if in_list[7] == 1:
                    fp.write('sa0 {}, sa0 {}, sa1 {},\n'.format(in_list[3], in_list[4], in_list[2]))
            elif in_list[6] == 2:
                if in_list[7] == 2:
                    fp.write('sa1 {}, sa1 {}, sa0 {}\n'.format(in_list[3], in_list[4], in_list[2]))
    elif in_list[0] == 'INVX1':
        if in_list[4] == 1:
            if in_list[5] == 1:
                fp.write('sa1 {}, sa1 {}\n'.format(in_list[2], in_list[3]))
    elif in_list[0] == 'BUFX1':
        if in_list[4] == 3:
            if in_list[5] == 0:
                fp.write('sa1 {}, sa0 {}\n'.format(in_list[2], in_list[2]))
        elif in_list[5] == 3:
            if in_list[4]:
                fp.write('sa1 {}, sa0 {}\n'.format(in_list[3], in_list[3]))

fp.close()

print('The total number of faults after collapsing are {}'.format(total_faults_af))
print('Collapse Ratio is {}'.format(total_faults_af/total_faults))

print(all_gates_list)
print(unique_list)

print('Done with Equivalence Fault Collapsing !!!')
