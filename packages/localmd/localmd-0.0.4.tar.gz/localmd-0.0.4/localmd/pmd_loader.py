import os
import pathlib
import sys
from sys import getsizeof
import math
import tifffile
from tqdm import tqdm
import time
import datetime


import numpy as np
import jax
import jax.numpy as jnp
from jax import jit, vmap
import functools
from functools import partial

##CAUTION: Experimental Imports..
from jax.experimental import sparse
from jax.experimental.sparse import BCOO

import torch
import torch.multiprocessing as multiprocessing

from localmd.preprocessing_utils import get_noise_estimate_vmap, center_and_get_noise_estimate, get_mean_and_noise
from localmd.dataset import PMDDataset

def display(msg):
    """
    Printing utility that logs time and flushes.
    """
    tag = '[' + datetime.datetime.today().strftime('%y-%m-%d %H:%M:%S') + ']: '
    sys.stdout.write(tag + msg + '\n')
    sys.stdout.flush()
   
def make_jax_random_key():
    ii32 = np.iinfo(np.int32)
    prng_input = np.random.randint(low=ii32.min, high=ii32.max,size=1, dtype=np.int32)[0]
    key = jax.random.PRNGKey(prng_input)
    
    return key

@partial(jit, static_argnums=(2,3))
def truncated_random_svd(input_matrix, key, rank, num_oversamples=10):
    '''
    Key: This function assumes that (1) rank + num_oversamples is less than all dimensions of the input_matrix and (2) num_oversmples >= 1
    
    '''
    d = input_matrix.shape[0]
    T = input_matrix.shape[1]
    random_data = jax.random.normal(key, (T, rank + num_oversamples))
    projected = jnp.matmul(input_matrix, random_data)
    Q, R = jnp.linalg.qr(projected)
    B = jnp.matmul(Q.T, input_matrix)
    U, s, V = jnp.linalg.svd(B, full_matrices=False)
    
    U_final = Q.dot(U)
    V = jnp.multiply(jnp.expand_dims(s, axis=1), V)
    
    #Final step: prune the rank 
    U_truncated = jax.lax.dynamic_slice(U_final, (0, 0), (U_final.shape[0], rank))
    V_truncated = jax.lax.dynamic_slice(V, (0, 0), (rank, V.shape[1]))
    return [U_truncated, V_truncated]


class FrameDataloader():
    def __init__(self, dataset, batch_size, frame_corrector=None, dtype="float32"):
        self.dataset = dataset
        self.chunks = math.ceil(self.shape[2]/batch_size)
        self.batch_size = batch_size
        self.frame_corrector = frame_corrector
        self.dtype=dtype
        
        
    def __len__(self):
        return max(1, self.chunks - 1)
    
    @property
    def shape(self):
        return self.dataset.shape
    
    def __getitem__(self, index):
        start_time = time.time()
        start = index * self.batch_size
        
        if index == max(0, self.chunks - 2):
            end = self.shape[2]
            #load rest of data here
            keys = [i for i in range(start, end)]
            data = self.dataset.get_frames(keys).astype(self.dtype)
        elif index < self.chunks - 2:
            end = start + self.batch_size
            keys = [i for i in range(start, end)]
            data = self.dataset.get_frames(keys).astype(self.dtype)
        else:
            raise ValueError
        if self.frame_corrector is not None:
            data = self.frame_corrector.register_frames(data.transpose(2, 0, 1)).transpose(1, 2, 0)
        else:
            data = data
        return data
    



class PMDLoader():
    def __init__(self, dataset, dtype='float32', center=True, normalize=True, background_rank=15, batch_size=2000, order="F", num_workers = None, pixel_batch_size=5000, frame_corrector_obj = None, num_samples = 8):
        '''
        Inputs: 
            dataset: <INSERT TYPE> object. This is a basic reader which allows us to read frames of the input data. 
            dtype: np.dtype. intended format of data
            center: bool. whether or not to center the data before denoising
            normalize: bool. whether or not noise normalize the data
            background_rank: int. we run an approximate truncated svd on the full FOV of the data, of rank 'background_rank'. We subtract this from the data before running the core matrix decomposition compression method
            batch_size: max number of frames to load into memory (CPU and GPU) at a time
            order: the order (either "C" or "F") in which we reshape 2D data into 3D videos and vice versa
            num_workers: int, keep it at 0 for now. Number of workers used in pytorch dataloading. Experimental and best kept at 0. 
            pixel_batch_size: int. maximum number of pixels of data we load onto GPU at any point in time
            frame_corrector_obj: jnormcorre frame corrector object. This is used to register loaded data on the fly. So in a complete pipeline, like the maskNMF pipeline, we can load data, correct it on the fly, and compress it. Avoids the need to explicitly rewrite the data onto disk during registration. 
            num_samples: int. when we estimate mean and noise variance, we take 8 samples of the data, each sample has 'batch_size' number of continuous frames. If there are fewer than num_samples * batch_size frames in the dataset, we just sequentially load the entire dataset to get these estimates. 
        
        
        '''
        self.order = order
        self.dataset = dataset
        self.dtype = dtype
        
        assert isinstance(dataset, PMDDataset), "Dataset object does not conform to PMDDataset API requirements" 
        self.shape = self.dataset.shape
        self._estimate_batch_size(frame_const=batch_size)
        self.pixel_batch_size=pixel_batch_size
        self.frame_corrector = frame_corrector_obj
        self.num_samples = num_samples
        
        def regular_collate(batch):
            return batch[0]
        self.curr_dataloader = FrameDataloader(self.dataset, self.batch_size, frame_corrector = self.frame_corrector, dtype=self.dtype)
        self.curr_dataloader_vanilla = FrameDataloader(self.dataset, self.batch_size, frame_corrector = None, dtype=self.dtype)
        if num_workers is None:
            num_cpu = multiprocessing.cpu_count()
            num_workers = min(num_cpu - 1, len(self.tiff_dataobj))
            num_workers = max(num_workers, 0)
        display("num workers for each dataloader is {}".format(num_workers))
        
        self.loader = torch.utils.data.DataLoader(self.curr_dataloader, batch_size=1,
                                             shuffle=False, num_workers=num_workers, collate_fn=regular_collate, timeout=0)
        self.loader_vanilla = torch.utils.data.DataLoader(self.curr_dataloader_vanilla, batch_size=1,
                                             shuffle=False, num_workers=num_workers, collate_fn=regular_collate, timeout=0)
        
        self.center = center
        self.normalize=normalize
        self.background_rank = background_rank
        self.frame_constant = 1024
        self._initialize_all_normalizers()
        self._initialize_all_background()
    
    
    def _get_size_in_GB(self, obj_to_measure):
        val = getsizeof(obj_to_measure)
        return val/(1024**3)
    
    def _estimate_batch_size_heuristic(self, desired_size_in_GB=50, num_frames_to_sim=10):
        test = np.zeros((self.shape[0], self.shape[1], num_frames_to_sim), dtype=self.dtype)
        gb_size = self._get_size_in_GB(test)
        
        multiplier = math.ceil(desired_size_in_GB/gb_size)
        return multiplier * num_frames_to_sim  #To be safe
        

    
    def _estimate_batch_size(self, frame_const = 2000):
        est_1 = self._estimate_batch_size_heuristic()
        self.batch_size = min(frame_const, est_1)
        display("The batch size used is {}".format(self.batch_size))

    def temporal_crop(self, frames):
        '''
        Input: 
            frames: a list of frame values (for e.g. [1,5,2,7,8]) 
        Returns: 
            A (potentially motion-corrected) array containing these frames from the tiff dataset with shape (d1, d2, T) where d1, d2 are FOV dimensions, T is 
            number of frames selected
        '''
        if self.frame_corrector is not None:
            frame_length = len(frames) 
            result = np.zeros((self.shape[0], self.shape[1], frame_length))
            
            value_points = list(range(0, frame_length, self.batch_size))
            if value_points[-1] > frame_length - self.batch_size and frame_length > self.batch_size:
                value_points[-1] = frame_length - self.batch_size
            for k in value_points:
                start_point = k
                end_point = min(k + self.batch_size, frame_length)
                curr_frames = frames[start_point:end_point]
                x = self.dataset.get_frames(curr_frames).astype(self.dtype).transpose(2,0,1)
                result[:, :, start_point:end_point] = np.array(self.frame_corrector.register_frames(x)).transpose(1,2,0)
            return result
        else:
            return self.dataset.get_frames(frames).astype(self.dtype)

        
        
    def _initialize_all_normalizers(self):
        '''
        Constructs mean image and normalization image
        '''
        display("Computing Video Statistics")
        if self.center and self.normalize:
            
            if self.shape[2] > self.frame_constant * self.num_samples:
                results = self._calculate_mean_and_normalizer_sampling()
            else:
                results = self._calculate_mean_and_normalizer()
            self.mean_img = results[0]
            self.std_img = results[1]
        else:
            raise ValueError("Method now requires normalization and centering")
        return self.mean_img, self.std_img
    
    def _initialize_all_background(self):
        self.spatial_basis = self._calculate_background_filter()
    
    def _calculate_mean_and_normalizer_sampling(self):
        '''
        This function uses sampling procedures to accurately estimate the noise variance and mean of every pixel of the dataset
        '''
        display("Calculating mean and noise variance via sampling")
        overall_mean = np.zeros((self.shape[0], self.shape[1]))
        overall_normalizer = np.zeros((self.shape[0], self.shape[1]), dtype=self.dtype)
        num_frames = self.shape[2]
        
        divisor = math.ceil(math.sqrt(self.pixel_batch_size))
        if self.shape[0] - divisor <= 0:
            dim1_range_start_pts = np.arange(1)
        else:
            dim1_range_start_pts = np.arange(0, self.shape[0] - divisor, divisor)
            dim1_range_start_pts = np.concatenate([dim1_range_start_pts, [self.shape[0] - divisor]], axis = 0)
        if self.shape[1] - divisor <= 0:
            dim2_range_start_pts = np.arange(1)
        else:
            dim2_range_start_pts = np.arange(0, self.shape[1] - divisor, divisor)
            dim2_range_start_pts = np.concatenate([dim2_range_start_pts, [self.shape[1] - divisor]], axis = 0)
        
        if self.shape[2] - self.frame_constant <= 0:
            elts_to_sample = [0]
        else:
            elts_to_sample = list(range(0, self.shape[2] - self.frame_constant, self.frame_constant))
            elts_to_sample.append(self.shape[2] - self.frame_constant)
        elts_used = np.random.choice(elts_to_sample, min(self.num_samples, len(elts_to_sample)), replace=False)
        frames_actually_used = 0
        for i in elts_used:
            start_pt_frame = i
            end_pt_frame = min(i + self.frame_constant, self.shape[2])
            frames_actually_used += end_pt_frame - start_pt_frame
            
            data = np.array(self.temporal_crop([i for i in range(start_pt_frame, end_pt_frame)]))
            mean_value_net = np.zeros((self.shape[0], self.shape[1]))
            normalizer_net = np.zeros((self.shape[0], self.shape[1]))
            for step1 in dim1_range_start_pts:
                for step2 in dim2_range_start_pts:
                    crop_data = data[step1:step1+divisor, step2:step2+divisor, :]
                    mean_value, noise_est_2d = get_mean_and_noise(crop_data, crop_data.shape[2])
                    mean_value_net[step1:step1+divisor, step2:step2+divisor] = np.array(mean_value)
                    normalizer_net[step1:step1+divisor, step2:step2+divisor] = np.array(noise_est_2d)
                    
            overall_mean += (mean_value_net / len(elts_used))
            overall_normalizer += (normalizer_net / len(elts_used))
        overall_normalizer[overall_normalizer==0] = 1
        display("Finished mean and noise variance")
        return overall_mean.astype(self.dtype), overall_normalizer

    
    def _calculate_mean_and_normalizer(self):
        '''
        This function takes a full pass through the dataset and calculates the mean and noise variance at the 
        same time
        '''
        display("Calculating mean and noise variance")
        overall_mean = np.zeros((self.shape[0], self.shape[1]))
        overall_normalizer = np.zeros((self.shape[0], self.shape[1]), dtype=self.dtype)
        num_frames = self.shape[2]
        
        divisor = math.ceil(math.sqrt(self.pixel_batch_size))
        if self.shape[0] - divisor <= 0:
            dim1_range_start_pts = np.arange(1) 
        else:
            dim1_range_start_pts = np.arange(0, self.shape[0] - divisor, divisor)
            dim1_range_start_pts = np.concatenate([dim1_range_start_pts, [self.shape[0] - divisor]], axis = 0)
        
        if self.shape[1] - divisor <= 0:
            dim2_range_start_pts = np.arange(1)
        else:
            dim2_range_start_pts = np.arange(0, self.shape[1] - divisor, divisor)
            dim2_range_start_pts = np.concatenate([dim2_range_start_pts, [self.shape[1] - divisor]], axis = 0)
        
        if self.shape[2] - self.frame_constant <= 0:
            elts_used = [0]
        else:
            elts_used = list(range(0, self.shape[2] - self.frame_constant, self.frame_constant))
            elts_used.append(self.shape[2] - self.frame_constant)
        elts_used = list(range(0, self.shape[2], self.frame_constant))
        if elts_used[-1] > self.shape[2] - self.frame_constant and elts_used[-1] > 0:
            elts_used[-1] = self.shape[2] - self.frame_constant
        

        for i in elts_used:
            start_pt_frame = i
            end_pt_frame = min(i + self.frame_constant, self.shape[2])
            data = np.array(self.temporal_crop([i for i in range(start_pt_frame, end_pt_frame)]))

            data = np.array(data) 
            mean_value_net = np.zeros((self.shape[0], self.shape[1]))
            normalizer_net = np.zeros((self.shape[0], self.shape[1]))
            for step1 in dim1_range_start_pts:
                for step2 in dim2_range_start_pts:
                    crop_data = data[step1:step1+divisor, step2:step2+divisor, :]
                    mean_value, noise_est_2d = get_mean_and_noise(crop_data, crop_data.shape[2])
                    mean_value_net[step1:step1+divisor, step2:step2+divisor] = np.array(mean_value)
                    normalizer_net[step1:step1+divisor, step2:step2+divisor] = np.array(noise_est_2d)
                    
            overall_mean += (mean_value_net/len(elts_used))
            overall_normalizer += (normalizer_net/len(elts_used))
        overall_normalizer[overall_normalizer==0] = 1
        display("Finished mean and noise variance")
        return overall_mean.astype(self.dtype), overall_normalizer
    
    def temporal_crop_standardized(self, frames):
        crop_data = self.temporal_crop(frames)
        crop_data -= self.mean_img[:, :, None]
        crop_data /= self.std_img[:, :, None]
        
        return crop_data.astype(self.dtype)

    def _calculate_background_filter(self, n_samples = 1000):
        if self.background_rank <= 0:
            return np.zeros((self.shape[0]*self.shape[1], 1)).astype(self.dtype)
        sample_list = [i for i in range(0, self.shape[2])]
        random_data = np.random.choice(sample_list,replace=False, size=min(n_samples, self.shape[2]))
        crop_data = self.temporal_crop_standardized(random_data)
        key = make_jax_random_key()
        spatial_basis, _ = truncated_random_svd(crop_data.reshape((-1, crop_data.shape[-1]), order=self.order), key, self.background_rank)
        return np.array(spatial_basis).astype(self.dtype)
            
    def V_projection(self, M):
            '''
            This function projects the standardized data onto U (via multiplication by the matrices contained in the list-like object M. Here we use JAX just-in-time compilation capabilities 
                to fuse the motion correction and projection steps. 
            
            Given some data, D, the projection is computing by calculating M[1]*M[0]*D, where * denotes matrix multiplication
            
            Assumption: M has a small number of rows (and many columns). It is R x d, where R is the
            rank of the decomposition and d is the number of pixels in the movie
            Here we compute M(D - mean)/stdv. We break the computation into temporal subsets, so if the dataset is T frames, we compute this product T' frames at a time (where T' usually around 1 or 2K) 
            R = Rank of PMD Decomposition
            d = number of pixels in dataset
            T = number of frames in dataset
            T' = number of frames we load at a time in the below for loop

            M: Projection matrix given as input: it is R x T'
            D: The loaded dataset: dimensions d x T'
            mean = mean of data (from self.mean_image -- it is reshaped to d x 1 here
            stdv = noise variance of data (from self.std_img)
            '''
            sparse_projection_term = BCOO.from_scipy_sparse(M[0])
            inv_term = M[1]

            result = np.zeros((inv_term.shape[0], self.shape[2]), dtype=self.dtype)
            mean_img_r = self.mean_img.reshape((-1, 1), order=self.order)
            std_img_r = self.std_img.reshape((-1, 1), order=self.order)
            start = 0

            if self.frame_corrector is not None:
                registration_method = self.frame_corrector.register_frames
            else:
                def return_identity(frames):
                    return frames
                registration_method = return_identity
            def full_V_projection_routine_jax(order, register_func, inv_term, sparse_project_term, data, mean_img_r, std_img_r):
                new_data = register_func(data)
                return V_projection_routine_jax(self.order, inv_term, sparse_project_term, new_data, mean_img_r, std_img_r)

            full_V_projection_routine = jit(full_V_projection_routine_jax, static_argnums=(0, 1))

            start = 0
            result_list = []
            for i, data in enumerate(tqdm(self.loader_vanilla), 0):
                output = full_V_projection_routine(self.order, registration_method, inv_term, sparse_projection_term, data, mean_img_r, std_img_r)
                num_frames_chunk = output.shape[1]

                endpt = min(self.shape[2], start+num_frames_chunk)
                result_list.append(output)
                start = endpt
            result = np.array(jnp.concatenate(result_list, axis = 1))

            return result  
    
    ##TODO: Compose all operations so this pipeline executes end-to-end on accelerator
    def temporal_crop_with_filter(self, frames):
        crop_data = self.temporal_crop(frames)
        spatial_basis_r = self.spatial_basis.reshape((self.shape[0], self.shape[1], -1), order = self.order)
        
        output_matrix = np.zeros((crop_data.shape[0], crop_data.shape[1], crop_data.shape[2]))
        temporal_basis = np.zeros((spatial_basis_r.shape[2], crop_data.shape[2]))
        num_iters = math.ceil(output_matrix.shape[2]/self.batch_size)
        start = 0
        for k in range(num_iters):
            end_pt = min(crop_data.shape[2], start + self.batch_size)
            crop_data_subset = crop_data[:, :, start:end_pt]
            filter_data, temporal_basis_crop = standardize_and_filter(crop_data_subset, self.mean_img, self.std_img, spatial_basis_r)
            filter_data = np.array(filter_data)
            temporal_basis_crop = np.array(temporal_basis_crop)
            output_matrix[:, :, start:end_pt] = filter_data
            temporal_basis[:, start:end_pt] = temporal_basis_crop
            start += self.batch_size
        return output_matrix, temporal_basis
        
        

@partial(jit)
def standardize_and_filter(new_data, mean_img, std_img, spatial_basis):
    new_data -= jnp.expand_dims(mean_img, 2)
    new_data /= jnp.expand_dims(std_img, 2)
    
    d1, d2, T = new_data.shape

    new_data = jnp.reshape(new_data, (d1*d2, new_data.shape[2]), order="F")
    spatial_basis = jnp.reshape(spatial_basis, (d1*d2, spatial_basis.shape[2]), order="F")

    temporal_projection = jnp.matmul(spatial_basis.T, new_data) 
    new_data = new_data - jnp.matmul(spatial_basis, temporal_projection)

    return jnp.reshape(new_data, (d1, d2, T), order="F"), temporal_projection
                                       

@partial(jit)
def get_temporal_basis_jax(D, spatial_basis, mean_img_r, std_img_r):
    '''
    Get the relevant temporal component given the spatial basis: 
    
    Variables: 
        d (or (d1, d2) where d1*d2 = d): number of pixels of subchunk of data
        T: number of frames of subchunk of data
        K: rank of full FOV spatial basis
    Inputs: 
        - D: jnp.array, dimensions (d, T)
        - spatial_basis: shape (d, K). Key assumption: columns of spatial basis are orthonormal
        - mean_img_r: shape (d, 1)
        - std_img_r: shape (d, 1)
    NOTE: this method is faster than normalizing the matrix D first then multiplying by spatial_basis, since it immediately
    collapses everything to a d x K matrix. 
    '''

    spatial_basis_norm = jnp.divide(spatial_basis, std_img_r)
    spatialxdata = jnp.matmul(spatial_basis_norm.transpose(), D) 
    spatialxmean = jnp.matmul(spatial_basis_norm.transpose(), mean_img_r)
    diff = spatialxdata - spatialxmean
    
    return diff

# @partial(jit, static_argnums=(0))
def V_projection_routine_jax(order, inv_term, M, D, mean_img_r, std_img_r):
    # D = jnp.transpose(D, (1,2,0))
    D = jnp.reshape(D, (-1, D.shape[2]), order=order)
    D = D - mean_img_r
    D = D / std_img_r
    output = V_projection_inner_loop(inv_term, M, D)
    return output

# @sparse.sparsify
def V_projection_inner_loop(inv_term, M, D):
    '''
    Variables: 
        R: Current rank of decomposition 
        d (or (d1, d2) where d1*d2 = d): number of pixels of subchunk of data
        T: number of frames of subchunk of data
        K: rank of full FOV spatial basis
    Params: 
        - inv_term: shape (R, R)
        - M: shape (R, d)
        - mean_img_r: shape (d, 1)
        - std_img_r: shape (d, 1)
        
    '''
    output = M@D
    output = inv_term@output

    return output
  
@partial(jit)
def filter_components(data, spatial_r, temporal_basis):
    subt = jnp.tensordot(spatial_r, temporal_basis, axes=(2, 0))
    return data - subt