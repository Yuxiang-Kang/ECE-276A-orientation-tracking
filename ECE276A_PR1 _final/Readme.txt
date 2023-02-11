Folder "data" contains cam, imu, vicon data
Folder "code" contains all the code and data created in the optimization and drawing process:
    1. "parameters.py" defines which dataset are used in all programs.
    2. "load_data.py" reads data from Folder "data".
    3. "Funcs.py" defines the motion and observation model needed in optimization.
    4. "main.py" and "main_no_vicon.py" creates the original estimated orientation sequence, and save them as ".npy" files.
    5. "Optimization.py" reads the data from "main.py", and conduct optimization, and save the resualt as ".npy" files.
    6. "Panorama.py" transforms a sphere coordiniate in camera frame to a cylinder coordinate.
    7. "Panorama_paint.py" draws a panorama photo based on the data from "Panorama.py".
    8. "plot_optimized.py" and "plot_optimized_testset.py" plots the pitch, roll, yaw curve of orientations from vicon, estimated and optimized orientations.
    9. "Quaternion_calculation.py" contains basic quaternion calculation functions

To use this program set:
    1. set "dataset" in "parameters.py"
    2. run "main.py" (or "main_no_vicon.py" for test sets)
    3. run "Optimization.py"
    4. run "plot_optimized.py" (or "plot_optimized_testset.py"  for test sets)
    5. run "Panorama.py"
    6. "Panorama_paint.py"