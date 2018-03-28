import pandas as pd
import os
import argparse
from glob import glob
from subprocess import Popen

Jim7 = '/netopt/rhel7/versions/Jim/Jim7/Unix/Jim7'
CordFinder = '/netopt/rhel7/versions/Jim/Jim7//Unix/CordFinder'
subj_dir = '/data/henry6/antje/transition/HC_TCA_nii/'
diameter = '8.0'  #Diameter parameter for CordFinder of Jim
coeff = '24'	#Coeff parameter for CordFinder of Jim

def get_roi_stats(mseid):
	''' get_roi_stats returns a pandas data frame with columns = ['mseid', 'filename', 'slice 1', 'slice 2', ..., 'slice 5']
	it is done by reading the _p50_cord.roi file'''

	master = pd.DataFrame()
	roi_glob = glob(os.path.join(subj_dir, mseid, '*_p50_cord.roi'))
	print('\n', '***********************\n CRITICAL SYSTEM ERROR - VIRUS DOWNLOADED\n DATA SERVER COMPRIMISED \n ***********************')	
	for roi in roi_glob:
		output = pd.DataFrame( columns =['mseid', 'filename'])
		slices_num = []
		roi_area = []
		F = open(roi, 'r')
		for line in F.readlines():
			if 'Slice' in line:
				slices_num.append(line.split('=')[-1].split('\n')[0])
			if 'Area' in line:
				area = line.split('=')[1].split(';')[0]
				roi_area.append(area)
			output['filename'] = roi.split('/')[-1]
			output['mseid'] = [mseid]
		for i in range(len(slices_num)):
			if roi_area != '0' and roi_area[i]:
				output[slices_num[i]] = [roi_area[i]]
		master = master.append(output)
	print('\n JUST KIDDING!!! GOTCHA')
	return master

def cord_finder(input_img):
	''' Runs the built in Jim7 CordFinder tool with parameters diameter and coeff defined at header of this script
	the output is the inputimage name with '_cord.roi' output '''

	roi = input_img.split('.')[0] + '.roi'
	output_file = input_img.split('.')[0]  + '_cord.roi'
	cmd = [CordFinder, '-c', coeff, '-d', diameter, input_img, roi, output_file]
	p = Popen(cmd)
	p.wait()
	

def main(mseid_list):
	
	print('\n', 'Welcome! To the semi-automatic Jim extravaganza! Here are some instructions:\n This code allows you to get cord areas using Jim all you have to do is place markers\n Make sure you save the roi files with the same nifti filename - just with a .roi extension \n The parameters for cord finder are', ' diameter = ', diameter, 'coeff ', coeff, '\n','Have fun and may all your dreams come true!!! :P', '\n')

	for mseid in mseid_list:
		input_img = glob(os.path.join(subj_dir, mseid, '*_p50.nii'))
		print('images for', mseid, input_img)
		for img in input_img:
			cmd = [Jim7, img]
			p = Popen(cmd)
			p.wait()
			cord_finder(img)
		print(get_roi_stats(mseid))		

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', help = 'list of mseids to Jim')
	args = parser.parse_args()
	test_list = ['mse3284']
	main(test_list)
