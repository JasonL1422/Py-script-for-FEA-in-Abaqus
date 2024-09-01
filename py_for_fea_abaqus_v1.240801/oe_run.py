"""
jongcheol1422@gmail.com
"""

"""
INSTRUCTIOIN
select the BC, geometry, etc.
adjust the [TIME] in the end.
"""

import subprocess
import time

abaqus_script_path = "oe_model.inp"  

kratio = 1  #F properties are divided by this. kratio between the edge and face

"BC select"
bc_settings = ["OL","oe.bottom,2,2", "OE.aTOP, 2, 2, paradisp"] #[for OL]
#bc_settings = ["OT","oe.left,1,1", "OE.aRIGHT, 1, 1, paradisp"] #[for OT]

"Geometry select"
#parameter_values_kap = ["regio", 0.33, 0.3, 0.2, 0.1] #[for_Regio-specific]
parameter_values_kap = ["homog", 0.33, 0.33, 0.33, 0.33] #[for_Homogeneous]

parameter_values_C10 = [2.2, 2.6, 3.0]
parameter_values_D = [0.01]
parameter_values_k1 = [80, 100, 120]
parameter_values_k2 = [30, 60, 90]

parameter_values_disp = [0.0012, 0.0036, 0.0060, 0.0084, 0.0108, 0.0132, 0.0156, 0.0180] #[for OL]
#parameter_values_disp = [0.0009, 0.0027, 0.0045, 0.0063, 0.0081, 0.0099, 0.0117, 0.0135, 0.0153] #[for OT]

max_width_C10 = len(str(max(parameter_values_C10)))
max_width_D = max(len(str(d).replace('.', '_')) for d in parameter_values_D)
max_width_k1 = len(str(max(parameter_values_k1)))
max_width_k2 = len(str(max(parameter_values_k2)))

""" Storage
parameter_values_disp = [0.0012, 0.0036, 0.0060, 0.0084, 0.0108, 0.0132, 0.0156, 0.0180, 0.0204] #[for OL]
parameter_values_disp = [0.0009, 0.0027, 0.0045, 0.0063, 0.0081, 0.0099, 0.0117, 0.0135, 0.0153] #[for OT]
parameter_values_kap = ["regio", 0.33, 0.3, 0.2, 0.1] #[for_Regio-specific]
parameter_values_kap = ["homog", 0.33, 0.33, 0.33, 0.33] #[for_Homogeneous]
"""

for param_C10 in parameter_values_C10:
    for param_D in parameter_values_D:
        for param_k1 in parameter_values_k1:
            for param_k2 in parameter_values_k2:
                param_parakF1 = param_k1 / kratio
                param_parakF2 = param_k1 / kratio
                for param_disp in parameter_values_disp:
                    # ---------------------------------------------------------
                    #padded_C10 = str(param_C10).zfill(max_width_C10)
                    padded_C10 = "{:.1f}".format(param_C10)
                    padded_D = str(param_D).replace('.', '_').zfill(max_width_D)
                    padded_k1 = str(param_k1).zfill(max_width_k1)
                    padded_k2 = str(param_k2).zfill(max_width_k2)
    
                    input_filename = "model_{0}_{1}_C10_{2}_D_{3}_k1_{4}_k2_{5}_kr_{6}_disp_{7}.inp".format(
                        str(bc_settings[0]),
                        str(parameter_values_kap[0]),
                        padded_C10,
                        padded_D,
                        padded_k1,
                        padded_k2,
                        kratio,
                        str(param_disp).replace('.', '_')
                    )
                    # ---------------------------------------------------------
                    
                    with open(abaqus_script_path, 'r') as file:
                        abaqus_script = file.read()
                    #
                    modified_abaqus_script = abaqus_script.replace("BCini", str(bc_settings[1]))
                    modified_abaqus_script = modified_abaqus_script.replace("BCext", str(bc_settings[2]))
                    #
                    modified_abaqus_script = modified_abaqus_script.replace("paraKapF", str(parameter_values_kap[1]))
                    modified_abaqus_script = modified_abaqus_script.replace("paraKapE1", str(parameter_values_kap[2]))
                    modified_abaqus_script = modified_abaqus_script.replace("paraKapE2", str(parameter_values_kap[3]))
                    modified_abaqus_script = modified_abaqus_script.replace("paraKapE3", str(parameter_values_kap[4]))
                    #
                    modified_abaqus_script = modified_abaqus_script.replace("paraC10", str(param_C10))
                    modified_abaqus_script = modified_abaqus_script.replace("paraD", str(param_D))
                    modified_abaqus_script = modified_abaqus_script.replace("parak1", str(param_k1))
                    modified_abaqus_script = modified_abaqus_script.replace("parak2", str(param_k2))
                    modified_abaqus_script = modified_abaqus_script.replace("paradisp", str(param_disp))
                    #
                    modified_abaqus_script = modified_abaqus_script.replace("parakF1", str(param_parakF1))
                    modified_abaqus_script = modified_abaqus_script.replace("parakF2", str(param_parakF2))

                    with open(input_filename, 'w') as file:
                        file.write(modified_abaqus_script)

                    abaqus_cmd = "abaqus job={0}_{1}_C10_{2}_D_{3}_k1_{4}_k2_{5}_kr_{6}_disp_{7} input={8}".format(
                        str(bc_settings[0]),
                        str(parameter_values_kap[0]),
                        padded_C10,
                        padded_D,
                        padded_k1,
                        padded_k2,
                        kratio,
                        str(param_disp).replace('.', '_'),
                        input_filename
                        )

                    print(abaqus_cmd)
                    process = subprocess.Popen(abaqus_cmd, shell=True)
                    process.wait()  
                    time.sleep(60)  # Adjust this
