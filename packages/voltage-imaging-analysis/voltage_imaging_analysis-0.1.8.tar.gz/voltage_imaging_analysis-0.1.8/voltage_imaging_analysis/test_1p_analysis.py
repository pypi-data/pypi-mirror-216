from __future__ import division, print_function
import numpy as np
from voltage_imaging_analysis import voltage_imaging_analysis_fcts as voltage_imaging_fcts
import timeit
import tifffile
import scipy
import cv2
from matplotlib import pyplot as plt
import skimage
import math
from scipy import ndimage as ndi

def euclidean_distance(x1, y1, x2, y2):
    return math.hypot((x1 - x2), (y1 - y2))

# goal: identify points to target based on 1p analysis
# todo: case where no activity observed

# experimental protocol:
    # crop sensor area to region of holographic spots

#for n=1:no_acq_rates:
    # acquire 1p data at 500 hz
    # identify active cells
    # if no activity break and move region
    # else
    # target these cells with holographic spots
    # acquire data for acquisition rate all powers (should have calculated angles for same average powers different repetition rates)

# repeat 

blocksize_x1x2 = 10
blocksize_x3 = 10
no_pix_1khz = 200
border_pix = 10

fname = r"H:/1p_data_for_tests/1p_field_stim_no_stim_2/1p_field_stim_no_stim_2_MMStack_Pos0.ome.tif"

print("Loading " + fname + "...")

data = tifffile.imread(fname)

data_downsampled = skimage.measure.block_reduce(data, block_size=(blocksize_x3, blocksize_x1x2, blocksize_x1x2), func=np.mean, cval=0, func_kwargs=None)

no_tiles = np.ceil(np.divide(np.array(data.shape), np.array(data_downsampled.shape))).astype(int)

# use R_pca to estimate the degraded data as L + S, where L is low rank, and S is sparse
rpca = voltage_imaging_fcts.R_pca(data_downsampled.reshape(data_downsampled.shape[0], -1))
L, S = rpca.fit(max_iter=10000, iter_print=100)

S = S.reshape(data_downsampled.shape[0], data_downsampled.shape[1], data_downsampled.shape[2])

# S = skimage.measure.block_reduce(S, block_size=(5, 1, 1), func=np.mean, cval=0, func_kwargs=None)

# gaussian filter sparse components
S = scipy.ndimage.gaussian_filter(S, (3,1,1), order=0)

# JEDI = negative indicator --> multiply dataset by -1 and renormalize
S = -1*S
S = np.divide(S - np.min(S), np.max(S) - np.min(S))

putative_cell_coords_x1x2r = []

# in each frame, identify putative cells
for frame_idx in np.arange(S.shape[0]):
# for frame_idx in np.arange(0,2):
    blobs = skimage.feature.blob_log(S[frame_idx, :, :], min_sigma=1, max_sigma=3, threshold=.05)
    putative_cell_coords_x1x2r.append(blobs)

# putative_cell_coords_x1x2r = [item for sublist in putative_cell_coords_x1x2r for item in sublist]
putative_cell_coords_x1x2r = np.concatenate(putative_cell_coords_x1x2r)

# eliminate outright repeats
putative_cell_coords_x1x2r, counts = np.unique(putative_cell_coords_x1x2r, axis=0, return_counts=True)

# remove any overlapping "blobs"
putative_cell_coords_x1x2r = putative_cell_coords_x1x2r[np.argsort(counts)][::-1]
counts = counts[np.argsort(counts)]

circle_list = []

for coords_x1x2r in putative_cell_coords_x1x2r:
    if not any((x2, y2, r2) for x2, y2, r2 in circle_list if euclidean_distance(coords_x1x2r[0], coords_x1x2r[1], x2, y2) < coords_x1x2r[2] + r2):
        circle_list.append([coords_x1x2r[0], coords_x1x2r[1], coords_x1x2r[2]])  

coords_X1, coords_X2 = np.meshgrid(np.arange(data_downsampled.shape[1]), np.arange(data_downsampled.shape[2]), indexing='ij')

all_idxs = np.arange(np.size(data_downsampled[0, :, :])).reshape(data_downsampled.shape[1], data_downsampled.shape[2])

mask = np.zeros_like(all_idxs)

all_sets_coordinates = []

for coords_x1x2r in circle_list:

    spot_coords = (coords_X1 - coords_x1x2r[0])**2 + (coords_X2 - coords_x1x2r[1])**2 < coords_x1x2r[2]**2

    coords_unravelled = np.unravel_index(all_idxs[spot_coords], [data_downsampled.shape[1], data_downsampled.shape[2]])

    mask[coords_unravelled] = 1

# upsample mask
mask_upsampled = voltage_imaging_fcts.tile_array(mask, no_tiles[1], no_tiles[2])

# get rid of artefacts from "block_reduce"
pix_to_crop = np.array(mask_upsampled.shape) - np.array(data.shape[1:]) 

mask_upsampled = mask_upsampled[:-pix_to_crop[0], :-pix_to_crop[1]]

mask_upsampled = skimage.morphology.isotropic_erosion(mask_upsampled, no_tiles[1])

labeled_mask = skimage.measure.label(mask_upsampled)

all_spot_centroids_x1x2 = []

for region in skimage.measure.regionprops(labeled_mask):
    x1, x2 = region.centroid
    all_spot_centroids_x1x2.append([x1, x2])

all_spot_centroids_x1x2 = np.array(all_spot_centroids_x1x2)

indices = np.rint(all_spot_centroids_x1x2).astype(int)

indices = indices[indices[:, 0] < data.shape[1] - border_pix]
indices = indices[indices[:, 1] < data.shape[2] + border_pix]

centroid_array = np.zeros([data.shape[1], data.shape[2]])
centroid_array[indices[:, 0], indices[:, 1]] = 1

density = scipy.ndimage.convolve1d(centroid_array, np.ones([no_pix_1khz]), axis=0)

max_idx_x1 = np.argmax(np.sum(density, axis=1))

indices_within_region = indices[indices[:, 0] < max_idx_x1 + no_pix_1khz/2]
indices_within_region = indices_within_region[indices_within_region[:, 0] > max_idx_x1 - no_pix_1khz/2]

# find the indices within the region that are the furthest apart
p = 5

from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist

# Returned 420 points in testing
hull = ConvexHull(indices_within_region)

# Extract the points forming the hull
hullpoints = indices_within_region[hull.vertices,:]

# Naive way of finding the best pair in O(H^2) time if H is number of points on
# hull
hdist = cdist(hullpoints, hullpoints, metric='euclidean')

# Get the farthest apart points
bestpair = np.unravel_index(hdist.argmax(), hdist.shape)

points_to_target = np.array([hullpoints[bestpair[0]],hullpoints[bestpair[1]]])

# Now we have a problem
print("Finding optimal set...")
while len(points_to_target)<p:
  print("Number of points found = {0}".format(len(P)))
  distance_to_P        = cdist(indices_within_region, points_to_target)
  minimum_to_each_of_P = np.min(distance_to_P, axis=1)
  best_new_point_idx   = np.argmax(minimum_to_each_of_P)
  best_new_point = np.expand_dims(indices_within_region[best_new_point_idx,:],0)
  points_to_target = np.append(points_to_target, best_new_point,axis=0)

print(points_to_target)

# convert into coordinates of holographic spots

# start experiment
