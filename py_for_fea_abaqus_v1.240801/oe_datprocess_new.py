import os

# [INSTRUCTION]
# [File name] + [rf2_OL] + [sum of nodes] + [number of nodes] + [number of thickness values] + [sum of the thickness values] + [sum of reaction force] + [displacement] + [strain] + [stress]
# (continued) + [rf1_OL] + [sum of nodes] + [number of nodes] + [number of thickness values] + [sum of the thickness values] + [sum of reaction force] + [displacement] + [strain] + [stress]
# check the sum of nodes,etc are like below. If not, something is wrong
# (for rf2_OL) 154684.0 99 99 0.9188000000000004
# (for rf1_OT) 214439.0 125 125 0.9446000000000006

# Examples:
# OL_regio_C10_3.0_D_0_01_k1_060_k2_05_kr_1_disp_0_0012.dat rf2_OL 154684.0 99 99 0.9188000000000004 0.00017762970159 0.001200000000000003 0.2140407325020294 0.010000000000000024 rf1_OT 214439.0 125 125 0.9446000000000006 0.0 -0.00019831781903999998 0.0 -0.0022035313226666667
# OL_regio_C10_3.0_D_0_01_k1_060_k2_05_kr_1_disp_0_0036.dat rf2_OL 154684.0 99 99 0.9188000000000004 0.0005429853697999999 0.003599999999999996 0.6518290182413644 0.029999999999999968 rf1_OT 214439.0 125 125 0.9446000000000006 0.0 -0.004509189790399999 0.0 -0.05010210878222222
# OL_regio_C10_3.0_D_0_01_k1_060_k2_05_kr_1_disp_0_006.dat rf2_OL 154684.0 99 99 0.9188000000000004 0.0009296611116999999 0.0060000000000000045 1.1124528935572933 0.05000000000000004 rf1_OT 214439.0 125 125 0.9446000000000006 0.0 -0.0023275110215999996 0.0 -0.02586123357333333

dat_files = [file for file in os.listdir() if file.endswith('.dat')]    # all .dat files in the current directory

combined_result_data = []

for file_name in dat_files:
    with open(file_name, 'r') as file:
        data = file.read()

# Processing for each file------------------------------------------------------------------

        # Find the last 'SUMMARY'
        last_summary_index = data.rfind('SUMMARY')
        second_last_summary_index = data.rfind('SUMMARY', 0, last_summary_index)
    
        # Select data between the 2nd last and last 'SUMMARY'
        relevant_data = data[second_last_summary_index:last_summary_index]
    
        lines = relevant_data.split('\n')
        
        rf2_relevant_data = []
        rf1_relevant_data = []

        #----------------------------------------------------------

        start_collecting = False
        
        for line in lines:  # Find and store RF2 values
            if 'RF2' in line:
                start_collecting = True
            elif start_collecting and line.strip().startswith('MAXIMUM'):
                break
            elif start_collecting:
                rf2_relevant_data.append(line)

        rf2_relevant_data = rf2_relevant_data[2:-1] # Remove the first two and the last lines

        start_collecting = False
        for line in lines:  # Find and store RF1 values
            if 'RF1' in line:
                start_collecting = True
            elif start_collecting and line.strip().startswith('MAXIMUM'):
                break
            elif start_collecting:
                rf1_relevant_data.append(line)
        
        rf1_relevant_data = rf1_relevant_data[2:-1] # Remove the first two and the last lines
        #---------------------------------------------------------
        
        rf2_col1_values, rf2_col2_values, rf2_col3_values = [], [], []
        rf1_col1_values, rf1_col2_values, rf1_col3_values = [], [], []
    
        for line in rf2_relevant_data:
            elements = line.split()
            if len(elements) == 3:
                try:
                    rf2_col1_values.append(float(elements[0]))
                    rf2_col2_values.append(float(elements[1]))
                    rf2_col3_values.append(float(elements[2]))
                except ValueError:
                    pass
        
        # -------------------------------------------
    
        for line in rf1_relevant_data:
            elements = line.split()
            if len(elements) == 3:
                try:
                    rf1_col1_values.append(float(elements[0]))
                    rf1_col2_values.append(float(elements[1]))
                    rf1_col3_values.append(float(elements[2]))
                except ValueError:
                    pass

        if not rf2_col1_values or not rf2_col2_values or not rf2_col3_values or not rf1_col1_values or not rf1_col2_values or not rf1_col3_values:
            error_message = "Error: DivisionZero. No data in file {}".format(file_name)
            error_message2 = "Error:DivisionZero.Nodatainfile"
            print(error_message)
            combined_sum_data.append((file_name, error_message2))
            continue
        
        #-----------------------------------------------------------------------
        
        #Thickness at each nodes. rf2 (OL) has 99. rf1 (OT) has 125 nodes.
        rf2_thick_col4 = [0.0121,0.0121,0.0074,0.0074,0.01075,0.01075,0.0086,0.0086,0.007,0.007,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.0078,0.0078,0.0078,0.0078,0.0078,0.0078,0.0078,0.0094,0.0094,0.0094,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0094,0.0094,0.0094,0.0078,0.0078,0.0078,0.0078,0.0078,0.0078,0.0078,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007]
        rf1_thick_col4 = [0.007,0.0074,0.0086,0.01075,0.0121,0.01075,0.0086,0.0074,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.0078,0.0078,0.0078,0.0078,0.0078,0.0094,0.0094,0.0094,0.0121,0.0121,0.0121,0.0121,0.0121,0.0121,0.0094,0.0094,0.0094,0.0078,0.0078,0.0078,0.0078,0.0078,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007,0.007]
        
        rf2_len_thick = len(rf2_thick_col4) #To check # of thickness
        rf2_sum_thick = sum(rf2_thick_col4)
        rf1_len_thick = len(rf1_thick_col4) #To check # of thickness
        rf1_sum_thick = sum(rf1_thick_col4)
        
        # Initialize lists to store the reaction force divided by thickness
        rf2_force_per_thickness = []
        rf1_force_per_thickness = []

        # Calculate reaction force divided by thickness for RF2
        for i, (force, thickness) in enumerate(zip(rf2_col3_values, rf2_thick_col4)):
            if thickness != 0:  # Check to avoid division by zero
              rf2_force_per_thickness.append(force / thickness)
            else:
             rf2_force_per_thickness.append('Error: Thickness is zero at node {}'.format(rf2_col1_values[i]))

        # Calculate reaction force divided by thickness for RF1
        for i, (force, thickness) in enumerate(zip(rf1_col3_values, rf1_thick_col4)):
            if thickness != 0:  # Check to avoid division by zero
                rf1_force_per_thickness.append(force / thickness)
            else:
                rf1_force_per_thickness.append('Error: Thickness is zero at node {}'.format(rf1_col1_values[i]))

        #-----------------------------------------------------------------------
        #rf2_avg_col2 = sum(rf2_col2_values) / len(rf2_col2_values) #Avg RFs --> wrong
        #rf1_avg_col2 = sum(rf1_col2_values) / len(rf1_col2_values) #Avg RFs --> wrong
        
        
        # Calculate column sum_OL
        rf2_sum_col1 = sum(rf2_col1_values) #To check if correct nodes are considered.
        rf2_len_col1 = len(rf2_col1_values) #To check. The number of nodes
        
        rf2_sum_col3 = sum(rf2_col3_values) #Sum of RFs at all nodes
        rf2_avg_disp = sum(rf2_col2_values) / len(rf2_col2_values) #Avg of displacement
        
        rf2_stress = sum(rf2_force_per_thickness)/0.09 #Stress. Normalized by thickness and the length of the model
        rf2_strain = rf2_avg_disp / 0.12

        # Calculate column sum_OT
        rf1_sum_col1 = sum(rf1_col1_values) #To check if correct nodes are considered.
        rf1_len_col1 = len(rf1_col1_values) #To check. The number of nodes
        
        rf1_sum_col3 = sum(rf1_col3_values) #Sum of RFs at all nodes
        rf1_avg_disp = sum(rf1_col2_values) / len(rf1_col2_values) #Avg of displacement
        
        rf1_stress = sum(rf1_force_per_thickness)/0.12 #Stress. Normalized by thickness and the length of the model
        rf1_strain = rf1_avg_disp / 0.09
    
        #-----------------------------------------------------------------------
    
        # Create a line with the sum values
        rf2_result = ["rf2_OL", str(rf2_sum_col1), str(rf2_len_col1), str(rf2_len_thick), str(rf2_sum_thick), str(rf2_sum_col3), str(rf2_avg_disp), str(rf2_strain), str(rf2_stress)]
        rf2_result_line = ' '.join(rf2_result)
        rf1_result = ["rf1_OT", str(rf1_sum_col1), str(rf1_len_col1), str(rf1_len_thick), str(rf1_sum_thick), str(rf1_sum_col3), str(rf1_avg_disp), str(rf1_strain), str(rf1_stress)]
        rf1_result_line = ' '.join(rf1_result)
    
        # Combine sum of each file into a single list
        combined_result = rf2_result + rf1_result

# Data processing for one .dat file ends here-----------------------------------

        # Append the combined sum for this file to the list
        combined_result_data.append((file_name, combined_result))

# Save all combined sum into a single file
master_combined_result_file = 'master_combined_result.txt'
with open(master_combined_result_file, 'w') as master_file:
    for file_result in combined_result_data:
        file_name, sum = file_result
        master_file.write(file_name + ' ' + ' '.join(map(str, sum)) + '\n')
        
        
