path_cellpose_env -m cellpose --dir %1 --chan 0 --pretrained_model path_model_Reelin_P40_advanced --diameter .0 --save_tif --no_npy --stitch_threshold 0.4 --use_gpu --anisotropy 4 --cellprob_threshold -2.0 --flow_threshold 0.5

