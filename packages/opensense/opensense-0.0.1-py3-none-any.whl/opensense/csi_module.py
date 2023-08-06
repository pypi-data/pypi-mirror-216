import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import tsmoothie
from utils import *
import time

class CSIData:
    def __init__(self, csi_data=None) -> None:
        '''
        Read one CSI sample in a time duration
        Useful for model inference / real-time demo
        csi_data format: (num_antenna_pair, num_subcarrier, time_length)
        '''
        assert len(csi_data.shape) == 3, "Error: the data dimension should follow (num_antenna_pair, num_subcarrier, time_length)"
        self.num_antenna_pair, self.num_subcarrier, self.time_length = csi_data.shape
        self.csi_data = csi_data
        # log_info('CSI data loaded with the size', self.csi_data.shape)

    def denoise(self, denoise_method: str="kalman"):
        '''
        The denoising method for CSI data:
        method -> "", "", ""
        '''
        # log_split()
        # log_info('Start denoising with', method_name)

        smoother = denoise_dict[denoise_method]
        smoothed_data = np.zeros(self.csi_data.shape)

        for antenna in range(self.num_antenna_pair):
            smoother.smooth(self.csi_data[antenna])

            smoothed_data[antenna, :, :] = smoother.smooth_data
            # log_info('Antenna', antenna+1, 'is finished.')

        self.csi_data = smoothed_data
        # log_info('Denoise is finished.')
        # log_split()

    def remove_inf_nan(self):
        '''
        Eliminate the inf and NaN value in the CSI data
        '''
        self.csi_data = interpolate_nan_inf(self.csi_data)
        # log_info('Preprocessing (removing Inf/NaN) is finished.')

    def customized_denoise(self):
        '''
        Implement customized denoising approach here
        '''
        pass

class CSIDataset(Dataset):
    def __init__(self, data=None):
        '''
        Input: data [numpy.array] size (num_sample, num_pair_antennas, num_subcarrier, time_length)
        '''
        self.data = data
        if data:
            self.num_sample, self.num_antenna_pair, self.num_subcarrier, self.time_length = self.data.shape
            log_info("Dataset is loaded with the size of", self.data.shape)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data[idx]
        return torch.from_numpy(sample)
    
    def read_from_npy(self, root="sample_data.npy"):
        self.data = np.load(root)
        self.num_sample, self.num_antenna_pair, self.num_subcarrier, self.time_length = self.data.shape
        log_info("Dataset is loaded with the size of", self.data.shape)

    def preprocess(self, denoise_method="kalman"):
        '''
        Remove inf/nan and denoise the dataset
        '''
        assert len(self.data) > 1, "Please load the dataset first"

        for i in range(len(self.data)):
            csi = CSIData(self.data[i])
            csi.remove_inf_nan()
            csi.denoise()
            self.data[i,:,:,:] = csi.csi_data

        log_info("Preprocessing is finished.")

def csi_dataset_preprocessing(root="sample_data.npy", save_root="processed_data.npy"):
    '''
    Input: data [numpy.array] size (num_sample, num_pair_antennas, num_subcarrier, time_length)
    '''
    data = np.load(root)
    assert len(data) > 1, "The dataset is none."
    for i in range(len(data)):
        csi = CSIData(data[i])
        csi.remove_inf_nan()
        csi.denoise()
        data[i,:,:,:] = csi.csi_data

    np.save("", save_root)
    log_info("Preprocessed is finished, which is saved to", save_root)

# Testing functions
# if __name__ == "__main__":
    ## For CSIData testing
    # from tsmoothie.utils_func import sim_randomwalk
    # one_antenna = sim_randomwalk(n_series=114, timesteps=500, 
    #                     process_noise=10, measure_noise=30)
    # data = np.array([one_antenna, one_antenna, one_antenna, one_antenna])
    # csi = CSIData(data)
    # csi.remove_inf_nan()
    # csi.denoise()

    ## For CSIDataset testing
    # dataset = CSIDataset()
    # dataset.read_from_npy(root="sample_data.npy")
    # dataset.preprocess()
    # dataloader = DataLoader(dataset, batch_size=3, shuffle=True)

    # for batch in dataloader:
    #     pass

    ## Test function
    # csi_dataset_preprocessing()