from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils import six 
import os
import pickle
import cv2
import numpy as np
import shutil

from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
import re

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
img_files_path = 'static\\\\parse_recipes\\\\00_original_book_pics'
processed_files_path = 'static\\\\parse_recipes\\\\01_processed_recipes'
recipes_dict_folder = 'static\\\\parse_recipes\\\\02_recipe_dicts'
static_path = SITE_ROOT + '\\static\\parse_recipes\\'


img_disp_width, img_disp_height = 1000, 1333.333333


def get_img_list(img_files_path):
	SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
	img_list = next(os.walk(os.path.join(SITE_ROOT, img_files_path)))[2][:5]
	return img_list


def open_update_save_dict(static_path, img_list, img_index, trim_dict_):
	# If existing dict
	if os.path.isfile(static_path + 'trim_dict.pkl'):
		
		# Open
		with open(static_path + 'trim_dict.pkl', 'rb') as f: 
			trim_dict = pickle.load(f)
		
		# Update
		if img_list[img_index] in trim_dict.keys():
			trim_dict[img_list[img_index]].update(trim_dict_)
		else:
			trim_dict[img_list[img_index]] = trim_dict_
		
		# Save
		with open(static_path + 'trim_dict.pkl', 'wb') as f:
			pickle.dump(trim_dict, f, pickle.HIGHEST_PROTOCOL)

	# If not existing dict
	else:
		# Create dict
		trim_dict = {img_list[img_index]: trim_dict_}
		# Save
		with open(static_path + 'trim_dict.pkl', 'wb') as f:
			pickle.dump(trim_dict, f, pickle.HIGHEST_PROTOCOL)





def parse_ctrl(request):

	# Load list of files to trim
	SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
	img_files_path = 'static\\\\parse_recipes\\\\00_original_book_pics'
	img_list = next(os.walk(os.path.join(SITE_ROOT, img_files_path)))[2][:5]
	total_images_len = len(img_list)

	# Load 'trim_dict'
	static_path = SITE_ROOT + '\\static\\parse_recipes\\'
	# If existing dict
	if os.path.isfile(static_path + 'trim_dict.pkl'):
		# Open
		with open(static_path + 'trim_dict.pkl', 'rb') as f: 
			trim_dict = pickle.load(f)
	else:
		# Dict does not exist
		trim_dict = {}

	##### Check what is missing #####

	# Left edge
	if True:
		left_edge_imgs = []
		if len(trim_dict.keys()) > 0:
			for img in trim_dict.keys():
				if 'left_edge' in trim_dict[img].keys():
					left_edge_imgs.append(img)
			left_edge_missing = list(set(img_list) - set(left_edge_imgs))
		else:
			left_edge_missing = img_list
		left_edge_missing_len = len(left_edge_missing)
		left_edge_done_len = total_images_len - left_edge_missing_len

	# Right edge
	if True:
		right_edge_imgs = []
		if len(trim_dict.keys()) > 0:
			for img in trim_dict.keys():
				if 'right_edge' in trim_dict[img].keys():
					right_edge_imgs.append(img)
			right_edge_missing = list(set(img_list) - set(right_edge_imgs))
		else:
			right_edge_missing = img_list
		right_edge_missing_len = len(right_edge_missing)
		right_edge_done_len = total_images_len - right_edge_missing_len

	# Top edge
	if True:
		top_edge_imgs = []
		if len(trim_dict.keys()) > 0:
			for img in trim_dict.keys():
				if 'top_edge' in trim_dict[img].keys():
					top_edge_imgs.append(img)
			top_edge_missing = list(set(img_list) - set(top_edge_imgs))
		else:
			top_edge_missing = img_list
		top_edge_missing_len = len(top_edge_missing)
		top_edge_done_len = total_images_len - top_edge_missing_len

	# Bottom edge
	if True:
		bottom_edge_imgs = []
		if len(trim_dict.keys()) > 0:
			for img in trim_dict.keys():
				if 'bottom_edge' in trim_dict[img].keys():
					bottom_edge_imgs.append(img)
			bottom_edge_missing = list(set(img_list) - set(bottom_edge_imgs))
		else:
			bottom_edge_missing = img_list
		bottom_edge_missing_len = len(bottom_edge_missing)
		bottom_edge_done_len = total_images_len - bottom_edge_missing_len

	# Header edge
	if True:
		header_imgs = []
		if len(trim_dict.keys()) > 0:
			for img in trim_dict.keys():
				if 'header' in trim_dict[img].keys():
					header_imgs.append(img)
			header_missing = list(set(img_list) - set(header_imgs))
		else:
			header_missing = img_list
		header_missing_len = len(header_missing)
		header_done_len = total_images_len - header_missing_len

	# Footer edge
	if True:
		footer_imgs = []
		if len(trim_dict.keys()) > 0:
			for img in trim_dict.keys():
				if 'footer' in trim_dict[img].keys():
					footer_imgs.append(img)
			footer_missing = list(set(img_list) - set(footer_imgs))
		else:
			footer_missing = img_list
		footer_missing_len = len(footer_missing)
		footer_done_len = total_images_len - footer_missing_len

	# Vertical split
	if True:
		splt_vert_imgs = []
		if len(trim_dict.keys()) > 0:
			for img in trim_dict.keys():
				if 'split_vertical' in trim_dict[img].keys():
					splt_vert_imgs.append(img)
			splt_vert_missing = list(set(img_list) - set(splt_vert_imgs))
		else:
			splt_vert_missing = img_list
		splt_vert_missing_len = len(splt_vert_missing)
		splt_vert_done_len = total_images_len - splt_vert_missing_len

	# Trim recipes
	if True:
		trim_recipes_imgs = []
		if len(trim_dict.keys()) > 0:
			for img in trim_dict.keys():
				if 'trim_recipes' in trim_dict[img].keys():
					trim_recipes_imgs.append(img)
			trim_recipes_missing = list(set(img_list) - set(trim_recipes_imgs))
		else:
			trim_recipes_missing = img_list
		trim_recipes_missing_len = len(trim_recipes_missing)
		trim_recipes_done_len = total_images_len - trim_recipes_missing_len

	# Run OCR
	if True:
		rec_folder = SITE_ROOT + '\\' + processed_files_path
		ocr_flds = os.listdir(rec_folder)

		n_pages = len(list(set([x.split('rec')[0][:-1] for x in ocr_flds])))
		n_recipes = len(os.listdir(rec_folder))

	# Inspect
	if True:
		insp_folder = SITE_ROOT + '\\' + recipes_dict_folder
		inspected_flds = len(os.listdir(insp_folder))

	context = {
		'total_images_len': total_images_len,
		
		'left_edge_missing': left_edge_missing,
		'left_edge_missing_len': left_edge_missing_len,
		'left_edge_done_len': left_edge_done_len,

		'right_edge_missing': right_edge_missing,
		'right_edge_missing_len': right_edge_missing_len,
		'right_edge_done_len': right_edge_done_len,

		'top_edge_missing': top_edge_missing,
		'top_edge_missing_len': top_edge_missing_len,
		'top_edge_done_len': top_edge_done_len,

		'bottom_edge_missing': bottom_edge_missing,
		'bottom_edge_missing_len': bottom_edge_missing_len,
		'bottom_edge_done_len': bottom_edge_done_len,

		'header_missing': header_missing,
		'header_missing_len': header_missing_len,
		'header_done_len': header_done_len,

		'footer_missing': footer_missing,
		'footer_missing_len': footer_missing_len,
		'footer_done_len': footer_done_len,

		'splt_vert_missing': splt_vert_missing,
		'splt_vert_missing_len': splt_vert_missing_len,
		'splt_vert_done_len': splt_vert_done_len,

		'trim_recipes_missing': trim_recipes_missing,
		'trim_recipes_missing_len': trim_recipes_missing_len,
		'trim_recipes_done_len': trim_recipes_done_len,

		'ocr_processed_imgs': n_pages,
		'ocr_processed_recipes': n_recipes,

		'inspected_recipes': inspected_flds,

	}
	
	return render(request, 'parse_recipes/parse_ctrl.html', context)


def trim_left(request, img_index):

	# List of files to trim
	SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
	img_files_path = 'static\\\\parse_recipes\\\\00_original_book_pics'
	img_list = next(os.walk(os.path.join(SITE_ROOT, img_files_path)))[2][:5]
	
	# POST
	if request.method == 'POST':

		static_path = SITE_ROOT + '\\static\\parse_recipes\\'
		trim_dict_ = {'left_edge': int(request.POST.get('x_trim_coord'))}

		# If existing dict
		if os.path.isfile(static_path + 'trim_dict.pkl'):
			# Open
			with open(static_path + 'trim_dict.pkl', 'rb') as f: 
				trim_dict = pickle.load(f)
			# Update
			if img_list[img_index] in trim_dict.keys():
				trim_dict[img_list[img_index]].update(trim_dict_)
			else:
				trim_dict[img_list[img_index]] = trim_dict_
			# Save
			with open(static_path + 'trim_dict.pkl', 'wb') as f:
				pickle.dump(trim_dict, f, pickle.HIGHEST_PROTOCOL)

		# If not existing dict
		else:
			# Create dict
			trim_dict = {img_list[img_index]: trim_dict_}
			# Save
			with open(static_path + 'trim_dict.pkl', 'wb') as f:
				pickle.dump(trim_dict, f, pickle.HIGHEST_PROTOCOL)


		# Go to next image
		img_index += 1
		if img_index < len(img_list):
			context = {
				'img_list_len': len(img_list),
				'img_index': img_index,
				'current_img_file': img_list[img_index],
				'current_img_path': '\\\\' + img_files_path + '\\\\' + img_list[img_index],
				'img_number': img_index + 1,
			}
			return render(request, 'parse_recipes/parse_left.html', context)
		
		else:
			html = "<html><body>End of images.</body></html>"
			return HttpResponse(html)
	
	# GET
	else:
		if img_index < len(img_list):
			context = {
				'img_list_len': len(img_list),
				'img_index': img_index,
				'current_img_file': img_list[img_index],
				'current_img_path': '\\\\' + img_files_path + '\\\\' + img_list[img_index],
				'img_number': img_index + 1,
			}
			return render(request, 'parse_recipes/parse_left.html', context)
		
		else:
			html = "<html><body>End of images.</body></html>"
			return HttpResponse(html)
	

def trim_right(request, img_index):

	# List of files to trim
	SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
	img_files_path = 'static\\\\parse_recipes\\\\00_original_book_pics'
	img_list = next(os.walk(os.path.join(SITE_ROOT, img_files_path)))[2][:5]
	
	# POST
	if request.method == 'POST':

		static_path = SITE_ROOT + '\\static\\parse_recipes\\'
		trim_dict_ = {'right_edge': int(request.POST.get('x_trim_coord'))}

		# If existing dict
		if os.path.isfile(static_path + 'trim_dict.pkl'):
			# Open
			with open(static_path + 'trim_dict.pkl', 'rb') as f: 
				trim_dict = pickle.load(f)
			# Update
			if img_list[img_index] in trim_dict.keys():
				trim_dict[img_list[img_index]].update(trim_dict_)
			else:
				trim_dict[img_list[img_index]] = trim_dict_
			# Save
			with open(static_path + 'trim_dict.pkl', 'wb') as f:
				pickle.dump(trim_dict, f, pickle.HIGHEST_PROTOCOL)

		# If not existing dict
		else:
			# Create dict
			trim_dict = {img_list[img_index]: trim_dict_}
			# Save
			with open(static_path + 'trim_dict.pkl', 'wb') as f:
				pickle.dump(trim_dict, f, pickle.HIGHEST_PROTOCOL)


		# Go to next image
		img_index += 1
		if img_index < len(img_list):
			context = {
				'img_list_len': len(img_list),
				'img_index': img_index,
				'current_img_file': img_list[img_index],
				'current_img_path': '\\\\' + img_files_path + '\\\\' + img_list[img_index],
				'img_number': img_index + 1,
			}
			return render(request, 'parse_recipes/parse_right.html', context)
		
		else:
			html = "<html><body>End of images.</body></html>"
			return HttpResponse(html)
	
	# GET
	else:
		if img_index < len(img_list):
			context = {
				'img_list_len': len(img_list),
				'img_index': img_index,
				'current_img_file': img_list[img_index],
				'current_img_path': '\\\\' + img_files_path + '\\\\' + img_list[img_index],
				'img_number': img_index + 1,
			}
			return render(request, 'parse_recipes/parse_right.html', context)
		
		else:
			html = "<html><body>End of images.</body></html>"
			return HttpResponse(html)


def trim_top(request, img_index):

	# List of files to trim
	SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
	img_files_path = 'static\\\\parse_recipes\\\\00_original_book_pics'
	img_list = next(os.walk(os.path.join(SITE_ROOT, img_files_path)))[2][:5]
	
	# POST
	if request.method == 'POST':

		static_path = SITE_ROOT + '\\static\\parse_recipes\\'
		trim_dict_ = {'top_edge': int(request.POST.get('y_trim_coord'))}

		# If existing dict
		if os.path.isfile(static_path + 'trim_dict.pkl'):
			# Open
			with open(static_path + 'trim_dict.pkl', 'rb') as f: 
				trim_dict = pickle.load(f)
			# Update
			if img_list[img_index] in trim_dict.keys():
				trim_dict[img_list[img_index]].update(trim_dict_)
			else:
				trim_dict[img_list[img_index]] = trim_dict_
			# Save
			with open(static_path + 'trim_dict.pkl', 'wb') as f:
				pickle.dump(trim_dict, f, pickle.HIGHEST_PROTOCOL)

		# If not existing dict
		else:
			# Create dict
			trim_dict = {img_list[img_index]: trim_dict_}
			# Save
			with open(static_path + 'trim_dict.pkl', 'wb') as f:
				pickle.dump(trim_dict, f, pickle.HIGHEST_PROTOCOL)


		# Go to next image
		img_index += 1
		if img_index < len(img_list):
			context = {
				'img_list_len': len(img_list),
				'img_index': img_index,
				'current_img_file': img_list[img_index],
				'current_img_path': '\\\\' + img_files_path + '\\\\' + img_list[img_index],
				'img_number': img_index + 1,
			}
			return render(request, 'parse_recipes/parse_top.html', context)
		
		else:
			html = "<html><body>End of images.</body></html>"
			return HttpResponse(html)
	
	# GET
	else:
		if img_index < len(img_list):
			context = {
				'img_list_len': len(img_list),
				'img_index': img_index,
				'current_img_file': img_list[img_index],
				'current_img_path': '\\\\' + img_files_path + '\\\\' + img_list[img_index],
				'img_number': img_index + 1,
			}
			return render(request, 'parse_recipes/parse_top.html', context)
		
		else:
			html = "<html><body>End of images.</body></html>"
			return HttpResponse(html)
		

def trim_bottom(request, img_index):

	# List of files to trim
	SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
	img_files_path = 'static\\\\parse_recipes\\\\00_original_book_pics'
	img_list = next(os.walk(os.path.join(SITE_ROOT, img_files_path)))[2][:5]
	
	# POST
	if request.method == 'POST':

		static_path = SITE_ROOT + '\\static\\parse_recipes\\'
		trim_dict_ = {'bottom_edge': int(request.POST.get('y_trim_coord'))}

		# If existing dict
		if os.path.isfile(static_path + 'trim_dict.pkl'):
			# Open
			with open(static_path + 'trim_dict.pkl', 'rb') as f: 
				trim_dict = pickle.load(f)
			# Update
			if img_list[img_index] in trim_dict.keys():
				trim_dict[img_list[img_index]].update(trim_dict_)
			else:
				trim_dict[img_list[img_index]] = trim_dict_
			# Save
			with open(static_path + 'trim_dict.pkl', 'wb') as f:
				pickle.dump(trim_dict, f, pickle.HIGHEST_PROTOCOL)

		# If not existing dict
		else:
			# Create dict
			trim_dict = {img_list[img_index]: trim_dict_}
			# Save
			with open(static_path + 'trim_dict.pkl', 'wb') as f:
				pickle.dump(trim_dict, f, pickle.HIGHEST_PROTOCOL)


		# Go to next image
		img_index += 1
		if img_index < len(img_list):
			context = {
				'img_list_len': len(img_list),
				'img_index': img_index,
				'current_img_file': img_list[img_index],
				'current_img_path': '\\\\' + img_files_path + '\\\\' + img_list[img_index],
				'img_number': img_index + 1,
			}
			return render(request, 'parse_recipes/parse_bottom.html', context)
		
		else:
			html = "<html><body>End of images.</body></html>"
			return HttpResponse(html)
	
	# GET
	else:
		if img_index < len(img_list):
			context = {
				'img_list_len': len(img_list),
				'img_index': img_index,
				'current_img_file': img_list[img_index],
				'current_img_path': '\\\\' + img_files_path + '\\\\' + img_list[img_index],
				'img_number': img_index + 1,
			}
			return render(request, 'parse_recipes/parse_bottom.html', context)
		
		else:
			html = "<html><body>End of images.</body></html>"
			return HttpResponse(html)
		

def trim_header(request, img_index):

	# List of files to trim
	SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
	img_files_path = 'static\\\\parse_recipes\\\\00_original_book_pics'
	img_list = next(os.walk(os.path.join(SITE_ROOT, img_files_path)))[2][:5]
	
	# POST
	if request.method == 'POST':

		static_path = SITE_ROOT + '\\static\\parse_recipes\\'
		trim_dict_ = {'header': int(request.POST.get('y_trim_coord'))}

		# If existing dict
		if os.path.isfile(static_path + 'trim_dict.pkl'):
			# Open
			with open(static_path + 'trim_dict.pkl', 'rb') as f: 
				trim_dict = pickle.load(f)
			# Update
			if img_list[img_index] in trim_dict.keys():
				trim_dict[img_list[img_index]].update(trim_dict_)
			else:
				trim_dict[img_list[img_index]] = trim_dict_
			# Save
			with open(static_path + 'trim_dict.pkl', 'wb') as f:
				pickle.dump(trim_dict, f, pickle.HIGHEST_PROTOCOL)

		# If not existing dict
		else:
			# Create dict
			trim_dict = {img_list[img_index]: trim_dict_}
			# Save
			with open(static_path + 'trim_dict.pkl', 'wb') as f:
				pickle.dump(trim_dict, f, pickle.HIGHEST_PROTOCOL)


		# Go to next image
		img_index += 1
		if img_index < len(img_list):
			context = {
				'img_list_len': len(img_list),
				'img_index': img_index,
				'current_img_file': img_list[img_index],
				'current_img_path': '\\\\' + img_files_path + '\\\\' + img_list[img_index],
				'img_number': img_index + 1,
			}
			return render(request, 'parse_recipes/parse_header.html', context)
		
		else:
			html = "<html><body>End of images.</body></html>"
			return HttpResponse(html)
	
	# GET
	else:
		if img_index < len(img_list):
			context = {
				'img_list_len': len(img_list),
				'img_index': img_index,
				'current_img_file': img_list[img_index],
				'current_img_path': '\\\\' + img_files_path + '\\\\' + img_list[img_index],
				'img_number': img_index + 1,
			}
			return render(request, 'parse_recipes/parse_header.html', context)
		
		else:
			html = "<html><body>End of images.</body></html>"
			return HttpResponse(html)


def trim_footer(request, img_index):

	# List of files to trim
	SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
	img_files_path = 'static\\\\parse_recipes\\\\00_original_book_pics'
	img_list = next(os.walk(os.path.join(SITE_ROOT, img_files_path)))[2][:5]
	
	# POST
	if request.method == 'POST':

		static_path = SITE_ROOT + '\\static\\parse_recipes\\'
		trim_dict_ = {'footer': int(request.POST.get('y_trim_coord'))}

		# If existing dict
		if os.path.isfile(static_path + 'trim_dict.pkl'):
			# Open
			with open(static_path + 'trim_dict.pkl', 'rb') as f: 
				trim_dict = pickle.load(f)
			# Update
			if img_list[img_index] in trim_dict.keys():
				trim_dict[img_list[img_index]].update(trim_dict_)
			else:
				trim_dict[img_list[img_index]] = trim_dict_
			# Save
			with open(static_path + 'trim_dict.pkl', 'wb') as f:
				pickle.dump(trim_dict, f, pickle.HIGHEST_PROTOCOL)

		# If not existing dict
		else:
			# Create dict
			trim_dict = {img_list[img_index]: trim_dict_}
			# Save
			with open(static_path + 'trim_dict.pkl', 'wb') as f:
				pickle.dump(trim_dict, f, pickle.HIGHEST_PROTOCOL)


		# Go to next image
		img_index += 1
		if img_index < len(img_list):
			context = {
				'img_list_len': len(img_list),
				'img_index': img_index,
				'current_img_file': img_list[img_index],
				'current_img_path': '\\\\' + img_files_path + '\\\\' + img_list[img_index],
				'img_number': img_index + 1,
			}
			return render(request, 'parse_recipes/parse_footer.html', context)
		
		else:
			html = "<html><body>End of images.</body></html>"
			return HttpResponse(html)
	
	# GET
	else:
		if img_index < len(img_list):
			context = {
				'img_list_len': len(img_list),
				'img_index': img_index,
				'current_img_file': img_list[img_index],
				'current_img_path': '\\\\' + img_files_path + '\\\\' + img_list[img_index],
				'img_number': img_index + 1,
			}
			return render(request, 'parse_recipes/parse_footer.html', context)
		
		else:
			html = "<html><body>End of images.</body></html>"
			return HttpResponse(html)


def split_recipe_vertical(request, img_index):

	# List of files to trim
	SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
	img_files_path = 'static\\\\parse_recipes\\\\00_original_book_pics'
	img_list = next(os.walk(os.path.join(SITE_ROOT, img_files_path)))[2][:5]
	
	# POST
	if request.method == 'POST':

		static_path = SITE_ROOT + '\\static\\parse_recipes\\'
		trim_dict_ = {'split_vertical': [
			int(request.POST.get('x_split_coord_1')), 
			int(request.POST.get('x_split_coord_2')), 
			request.POST.get('rec_side'), 
		]}

		# If existing dict
		if os.path.isfile(static_path + 'trim_dict.pkl'):
			# Open
			with open(static_path + 'trim_dict.pkl', 'rb') as f: 
				trim_dict = pickle.load(f)
			# Update
			if img_list[img_index] in trim_dict.keys():
				trim_dict[img_list[img_index]].update(trim_dict_)
			else:
				trim_dict[img_list[img_index]] = trim_dict_
			# Save
			with open(static_path + 'trim_dict.pkl', 'wb') as f:
				pickle.dump(trim_dict, f, pickle.HIGHEST_PROTOCOL)

		# If not existing dict
		else:
			# Create dict
			trim_dict = {img_list[img_index]: trim_dict_}
			# Save
			with open(static_path + 'trim_dict.pkl', 'wb') as f:
				pickle.dump(trim_dict, f, pickle.HIGHEST_PROTOCOL)


		# Go to next image
		img_index += 1
		if img_index < len(img_list):
			context = {
				'img_list_len': len(img_list),
				'img_index': img_index,
				'current_img_file': img_list[img_index],
				'current_img_path': '\\\\' + img_files_path + '\\\\' + img_list[img_index],
				'img_number': img_index + 1,
			}
			return render(request, 'parse_recipes/split_vertical.html', context)
		
		else:
			html = "<html><body>End of images.</body></html>"
			return HttpResponse(html)
	
	# GET
	else:
		if img_index < len(img_list):
			context = {
				'img_list_len': len(img_list),
				'img_index': img_index,
				'current_img_file': img_list[img_index],
				'current_img_path': '\\\\' + img_files_path + '\\\\' + img_list[img_index],
				'img_number': img_index + 1,
			}
			return render(request, 'parse_recipes/split_vertical.html', context)
		
		else:
			html = "<html><body>End of images.</body></html>"
			return HttpResponse(html)


def trim_recipes(request, img_index):

	dict_key_name = 'trim_recipes'
	html_to_render = 'parse_recipes/trim_recipes.html'

	# List of files to trim
	img_list = get_img_list(img_files_path)
	
	# POST
	if request.method == 'POST':

		# Extract form fields with y coords (we need the loop because we
		# dont know how many recipes we will have)
		y_coords = []
		for y_key in [k for k in request.POST.keys() if k[:6] == 'y_trim']:
			y_coords.append(int(request.POST.get(y_key)))

		trim_dict_ = {dict_key_name: y_coords}
		open_update_save_dict(static_path, img_list, img_index, trim_dict_)

		# Go to next image
		img_index += 1
		if img_index < len(img_list):
			context = {
				'img_list_len': len(img_list),
				'img_index': img_index,
				'current_img_file': img_list[img_index],
				'current_img_path': '\\\\' + img_files_path + '\\\\' + img_list[img_index],
				'img_number': img_index + 1,
			}
			return render(request, html_to_render, context)
		
		else:
			return HttpResponse('<html><body>End of images.</body></html>')
	
	# GET
	else:
		if img_index < len(img_list):
			context = {
				'img_list_len': len(img_list),
				'img_index': img_index,
				'current_img_file': img_list[img_index],
				'current_img_path': '\\\\' + img_files_path + '\\\\' + img_list[img_index],
				'img_number': img_index + 1,
			}
			return render(request, html_to_render, context)
		
		else:
			return HttpResponse('<html><body>End of images.</body></html>')





def ocr_on_header(header_img):

	# Apply OCR
	gray = cv2.cvtColor(header_img, cv2.COLOR_BGR2GRAY)
	gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	#gray = cv2.medianBlur(gray, 3)
	temp_img = SITE_ROOT + '\\' + img_files_path + '\\' + 'temp_img.jpg'
	cv2.imwrite(temp_img, gray)
	text = pytesseract.image_to_string(Image.open(temp_img))

	with open(temp_img, 'rb') as f: page_img = f.read()   
	os.remove(temp_img)
    
	return text


def ocr_on_pg_number(footer_img):

	# Apply OCR
	gray = cv2.cvtColor(footer_img, cv2.COLOR_BGR2GRAY)
	gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	#gray = cv2.medianBlur(gray, 3)
	temp_img = SITE_ROOT + '\\' + img_files_path + '\\' + 'temp_img.jpg'
	cv2.imwrite(temp_img, gray)
	text = pytesseract.image_to_string(Image.open(temp_img))

	with open(temp_img, 'rb') as f: page_img = f.read()   
	os.remove(temp_img)
    
	return text


def ocr_on_procedure(proc_img):

	# Apply OCR
	gray = cv2.cvtColor(proc_img, cv2.COLOR_BGR2GRAY)
	gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	gray = cv2.medianBlur(gray, 3)
	temp_img = SITE_ROOT + '\\' + img_files_path + '\\' + 'temp_img.jpg'
	cv2.imwrite(temp_img, gray)
	text = pytesseract.image_to_string(Image.open(temp_img))
    
    # Delete temp img
	with open(temp_img, 'rb') as f: procedure_img = f.read()   
	os.remove(temp_img)

	# Process text
	text = text.split('\n')
	recipe_name, procedure = [], []
	for t in text:
		if t.isupper():
			recipe_name.append(t)
		else:
			procedure.append(t)
	recipe_name = ' '.join(' '.join(recipe_name).split()).lower()
	procedure = ' '.join(' '.join(procedure).split())
	procedure = procedure.split('.')
	procedure = [x.lstrip() for x in procedure]
	procedure = '.\n\n'.join(procedure)
	
	return recipe_name, procedure


def ocr_on_ingredients(ingr_img):
    
    # Apply OCR
	gray = cv2.cvtColor(ingr_img, cv2.COLOR_BGR2GRAY)
	gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #gray = cv2.medianBlur(gray, 3)
	temp_img = SITE_ROOT + '\\' + img_files_path + '\\' + 'temp_img.jpg'
	cv2.imwrite(temp_img, gray)
	text = pytesseract.image_to_string(Image.open(temp_img))
    
	with open(temp_img, 'rb') as f: ingredients_img = f.read()
    #os.remove(temp_img)
    
    # Remove double breaks
	t = text.splitlines()
	text_out = []
	for tx in t:
		if len(tx) > 0:
			text_out.append(tx)
    
	# Recipe name italian
	rec_name_ita = text_out[0].lower()
	
	# Recipe yield
	rec_yield = text_out[1]
	rec_yield = rec_yield.replace('Serves ', '')
	
	# Ingredients
	ingr_txt = text_out[2:]

	return rec_name_ita, rec_yield, ingr_txt


def run_ocr_on_img(img_index):

	# List of files to trim
	img_list = get_img_list(img_files_path)
	
	if img_index < len(img_list):
		
		# Open img
		raw_img = cv2.imread(SITE_ROOT + '\\' + img_files_path + '\\' + img_list[img_index])
		img = raw_img.copy()

		# Load dict with trim infos
		with open(static_path + 'trim_dict.pkl', 'rb') as f: 
			trim_dict = pickle.load(f)
		dict_ = trim_dict[img_list[img_index]]

		# Correct for different dimentions
		x_prop = img.shape[1] / img_disp_width
		y_prop = img.shape[0] / img_disp_height

		# Get cuts
		left_edge = int(dict_['left_edge'] * x_prop)
		right_edge = int(dict_['right_edge'] * x_prop)
		top_edge = int(dict_['top_edge'] * y_prop)
		bottom_edge = int(dict_['bottom_edge'] * y_prop)
		header = int(dict_['header'] * y_prop)
		footer = int(dict_['footer'] * y_prop)
		split_vert_left = int(min(dict_['split_vertical'][:2]) * x_prop)
		split_vert_right = int(max(dict_['split_vertical'][:2]) * x_prop)
		procedure_side = dict_['split_vertical'][2]
		recipe_cuts = [int(x) for x in np.array(sorted(dict_['trim_recipes'])) * y_prop]
		recipe_cuts = recipe_cuts + [footer]

		# Header and footer imgs
		header_img = img[top_edge : header, left_edge : right_edge]
		header_txt = ocr_on_pg_number(header_img)
		footer_img = img[footer : bottom_edge, left_edge : right_edge]
		footer_txt = ocr_on_pg_number(footer_img)

		# For each recipe
		output_flds = []
		for i in range(len(recipe_cuts)-1):

			# Create folder to keep processed files
			rec_folder = SITE_ROOT + '\\' + processed_files_path + '\\' + img_list[img_index].split('.')[0] + '_rec' + str(i)
			output_flds.append(rec_folder)
			if not os.path.exists(rec_folder):
				os.mkdir(rec_folder)
			else:    
				shutil.rmtree(rec_folder)
				os.mkdir(rec_folder)

			# Run OCR for 'left'
			if procedure_side == 'left':
				proc_img = img[recipe_cuts[i]:recipe_cuts[i+1], left_edge:split_vert_left]
				ingr_img = img[recipe_cuts[i]:recipe_cuts[i+1], split_vert_right:right_edge]

			# Run OCR for 'right'
			else:
				proc_img = img[recipe_cuts[i]:recipe_cuts[i+1], split_vert_right:right_edge]
				ingr_img = img[recipe_cuts[i]:recipe_cuts[i+1], left_edge:split_vert_left]

			# Run OCR
			recipe_name, proc_txt = ocr_on_procedure(proc_img)
			rec_name_ita, rec_yield, ingr_txt = ocr_on_ingredients(ingr_img)

			# Store results
			cv2.imwrite(rec_folder + '\\' + 'header_img.jpg', header_img)
			cv2.imwrite(rec_folder + '\\' + 'footer_img.jpg', footer_img)
			cv2.imwrite(rec_folder + '\\' + 'proc_img.jpg', proc_img)
			cv2.imwrite(rec_folder + '\\' + 'ingr_img.jpg', ingr_img)
			txt_results = {
				'header_txt': header_txt,
				'footer_txt': footer_txt,
				'recipe_name': recipe_name,
				'proc_txt': proc_txt,
				'rec_name_ita': rec_name_ita,
				'rec_yield': rec_yield,
				'ingr_txt': ingr_txt,
			}
			with open(rec_folder + '\\' + 'ocr_dict.pkl', 'wb') as f:
				pickle.dump(txt_results, f, pickle.HIGHEST_PROTOCOL)		

		return output_flds


def run_ocr_all_imgs(request):

	img_list = next(os.walk(os.path.join(SITE_ROOT, img_files_path)))[2][:5]

	context = {'image_pg': {}}

	for img_index, img_file in enumerate(img_list):
		output_flds = run_ocr_on_img(img_index)
		output_flds = [x.split('\\')[-1] for x in output_flds]
		context['image_pg'].update({img_file: output_flds})

	return render(request, 'parse_recipes/ocr_results_all_imgs.html', context)





def look_at_index(text, index_list, gram_size):

	text = text.replace(',', '').replace('.', '').lower()
    
    # 1) Compute n-grams from 'text'
	unigram_items = text.split()
	
	if gram_size == 1:
		n_gram_items = unigram_items
	elif gram_size == 2:
		n_gram_items = [i + ' ' + j for i,j in zip(unigram_items[::1], unigram_items[1::1])]
	elif gram_size == 3:
		n_gram_items = [i+' '+j+' '+k for i,j,k in zip(unigram_items[::1], unigram_items[1::1], unigram_items[2::])]
	elif gram_size == 4:
		n_gram_items = [i+' '+j+' '+k+' '+l for i,j,k,l in zip(unigram_items[::1], unigram_items[1::1], unigram_items[2::], unigram_items[3::])]


    # 2) Plural to singular words
	plural_flag = [False] * len(n_gram_items)
	for i, n_gram in enumerate(n_gram_items):
		if n_gram[-1] == 's':
			n_gram_items[i] = n_gram[:-1]
			plural_flag[i] = True

	# 3) Search for n_gram at 'index_list'
	found_item = [n_gram for n_gram in n_gram_items if n_gram in index_list]
    
    # 4) remove from 'text' founded n_gram
	if len(found_item) > 0:
		found_item = found_item[0]
		found_index = n_gram_items.index(found_item)
		if plural_flag[found_index]:
			found_item += 's'
		out_text = text.replace(found_item, '').strip()
	else:
		found_item = ''
		out_text = text
    
	if len(found_item) > 0:
		if plural_flag[found_index]:
			found_item = found_item[:-1]
	
	
	# Remove leading space
	out_text = out_text.lstrip()

	# Remove double space
	out_text = re.sub(' +', ' ', out_text)

	return out_text, found_item


def search_amount(text):
    
	'''
	Input: text, readed ingredient line from ingredients image (w/ no recipe name and yield)
	Output: amount, int
    
	''' 
	text = text.replace(',', '').replace('.', '')
    
    # Ingredient with fraction amount
	if '/' in text:
		i = text.index('/')
        
        # Fraction amount (no integer part)
		if i == 0:
			pos_char = text[i+1]
			fraction_amt_str = '1/' + pos_char
            
		if i > 0:
			prev_char = text[i-1]
			pos_char = text[i+1]
			if prev_char == "'": 
				prev_char = '1'
				text = text.replace("'", '1')
			fraction_amt_str = prev_char + '/' + pos_char
            
        # Integer part: one previous position
		if i > 1:
			if text[i-2].isdigit(): 
				integer_amt_str_1 = text[i-2]
			else:
				integer_amt_str_1 = ''
		else:
			integer_amt_str_1 = ''
        
        # Integer part: two previous position
		if i > 2:
			if text[i-3].isdigit(): 
				integer_amt_str_2 = text[i-3]   
			else:
				integer_amt_str_2 = ''
		else:
			integer_amt_str_2 = ''
            
        # Introduce space if 'integer_amt_str_1' exists
		if len(integer_amt_str_1) > 0:
			text = text[:i-2+1] + ' ' + text[i-2+1:]
            
		amount_string = integer_amt_str_2 + integer_amt_str_1 + ' ' + fraction_amt_str
		amount_string = amount_string.lstrip()
    
    # Ingredient with only integer amount
	else:
		amount_string = ''
		last_found_digit = None
		for n, s in enumerate(text):
			if s.isdigit():
				amount_string += s
				last_found_digit = n
			elif (not s.isdigit()) & (last_found_digit == None):
				pass
			else:
				break
   
    # Output
	if amount_string == '':
		return {'text_strp': text, 'amount_string': amount_string}
	else:
		out_text = text.replace(amount_string, '').strip()
		return {'text_strp': out_text, 'amount_string': amount_string}


def clean_recipe(data):

	recipe_dict = {
		'recipe_id': data['recipe_id'][0],
		'header_txt': data['header_txt'][0],
		'pg_number': int(data['pg_number'][0]),
		'recipe_name': data['recipe_name'][0],
		'procedure': data['procedure'][0],
		'recipe_name_italian': data['recipe_name_italian'][0],
		'rec_yield': int(data['rec_yield'][0]),
		'ingrs': [],
		'brecs': [],
		'salt_flag': data['salt_flag'][0],
		'pepper_flag': data['pepper_flag'][0],
		'white_pepper_flag': data['white_pepper_flag'][0],
	}

	# Clean ingrs
	for k in data.keys():
		if (k[:5] == 'ingrs') & (len(''.join(data[k][:-1])) > 0):
			recipe_dict['ingrs'].append(data[k])
		if (k[:5] == 'brecs') & (len(''.join(data[k][:-1])) > 0):
			recipe_dict['brecs'].append(data[k])

	return recipe_dict


def ajax_request_view(request):
	
	data = request.POST
	data = dict(six.iterlists(data))
	recipe_dict = clean_recipe(data)

	# Discard blank 'ingrs' and update 'recipe_dict'
	ingrs_no_blanks = []
	for ingrs in recipe_dict['ingrs']:
		ingrs_txt = ''.join(ingrs[:5]) # am. / un. / qlt. / ingr. / msenp.
		if len(ingrs_txt) > 0:
			ingrs_no_blanks.append(ingrs)
	recipe_dict['ingrs'] = ingrs_no_blanks

	# Discard blank 'brecs' and update 'recipe_dict'
	brecs_no_blanks = []
	for brecs in recipe_dict['brecs']:
		brecs_txt = ''.join(brecs[:5]) # am. / un. / qlt. / ingr. / msenp.
		if len(brecs_txt) > 0:
			brecs_no_blanks.append(brecs)
	recipe_dict['brecs'] = brecs_no_blanks

	# Load index_dict
	with open(SITE_ROOT + '\\static\\parse_recipes\\index_dict.pkl', 'rb') as f: 
		index_dict =  pickle.load(f)

	# Update index_dict['base_recipes']
	base_recipes = [x[3] for x in recipe_dict['brecs']]
	for base_recipe in base_recipes:
		if (len(base_recipe) > 0) & (base_recipe not in index_dict['base_recipes']):
			index_dict['base_recipes'].append(base_recipe)

	# Update index_dict['ingredients']
	ingredients = [x[3] for x in recipe_dict['ingrs']]
	for ingredient in ingredients:
		if (len(ingredient) > 0) & (ingredient not in index_dict['ingredients']):
			index_dict['ingredients'].append(ingredient)

	# Update index_dict['units']
	units = [x[1] for x in recipe_dict['ingrs']] + [x[1] for x in recipe_dict['brecs']]
	for unit in units:
		if (len(unit) > 0) & (unit not in index_dict['units']):
			index_dict['units'].append(unit)

	# Update index_dict['qualities']
	qualities = [x[2] for x in recipe_dict['ingrs']] + [x[2] for x in recipe_dict['brecs']]
	for quality in qualities:
		if (len(quality) > 0) & (quality not in index_dict['qualities']):
			index_dict['qualities'].append(quality)

	# Update index_dict['mises_en_plis']
	mises_en_plis = [x[4] for x in recipe_dict['ingrs']] + [x[4] for x in recipe_dict['brecs']]
	for mise_en_plis in mises_en_plis:
		if (len(mise_en_plis) > 0) & (mise_en_plis not in index_dict['mises_en_plis']):
			index_dict['mises_en_plis'].append(mise_en_plis)

	# Save index_dict
	with open(SITE_ROOT + '\\static\\parse_recipes\\index_dict.pkl', 'wb') as f: 
	    pickle.dump(index_dict, f, pickle.HIGHEST_PROTOCOL)


	assert False, recipe_dict
	




	# Save recipe dict
	with open(SITE_ROOT + '\\' + recipes_dict_folder + '\\' + recipe_dict['recipe_id'] + '.pkl', 'wb') as f: 
	 	pickle.dump(recipe_dict, f, pickle.HIGHEST_PROTOCOL)

	return HttpResponse("<html><body></body></html>")

# update index_dict
# save index dict

# http://127.0.0.1:8000/inspect_recipe/IMG_4405_rec1


def inspect_recipe(request, recipe_id):

	
	# Define static path for view.py and html template
	proc_path_html = 'parse_recipes/01_processed_recipes/' + recipe_id
	proc_path_py = 'static\\parse_recipes\\01_processed_recipes\\' + recipe_id
	
	# Load imgs
	header_img = proc_path_html + '/header_img.jpg'
	footer_img = proc_path_html + '/footer_img.jpg'
	proc_img = proc_path_html + '/proc_img.jpg'
	ingr_img = proc_path_html + '/ingr_img.jpg'

	# Load processed txt dict
	with open(SITE_ROOT + '\\' + proc_path_py + '\\' + 'ocr_dict.pkl', 'rb') as f: 
		ocr_dict = pickle.load(f)

	context = {
		'recipe_id': recipe_id,
		'header_img': header_img,
		'footer_img': footer_img,
		'proc_img': proc_img,
		'ingr_img': ingr_img,
		'ocr_dict': ocr_dict,
		
		'white_pepper_flag': False,
		'salt_flag': False,
		'pepper_flag': False,

		'ingrs_strpd': [],
	}
			
	# Load index_dict
	with open(SITE_ROOT + '\\static\\parse_recipes\\index_dict.pkl', 'rb') as f: 
		index_dict =  pickle.load(f)

	# For each ingredient item:
	ingr_n, brec_n = 0, 0
	
	for ingr_item in context['ocr_dict']['ingr_txt']:
		
		# Seasoning

		# If ingr_item == 'salt and white pepper'
		if 'white pepper' in ingr_item: 
			context['white_pepper_flag'] = True
			ingr_item = ingr_item.replace('white pepper', '')

		# If ingr_item == 'salt'
		elif 'salt' in ingr_item: 
			context['salt_flag'] = True
			ingr_item = ingr_item.replace('salt', '')

		# If ingr_item == 'salt and pepper'
		elif 'pepper' in ingr_item: 
			context['pepper_flag'] = True
			ingr_item = ingr_item.replace('pepper', '')


		# Ingredient or base recipe
		else:

			ingr_flag = True # Ingredient, not base recipe

			# Search amount
			d_amt = search_amount(ingr_item)
			ingr_item_strpd, amount_str = d_amt['text_strp'], d_amt['amount_string']

			# Search n_grams at 'base_recipes'
			index_list = index_dict['base_recipes']
			for n_gram in reversed(range(1, 5)): # n_gramsn from 4 to 1
				ingr_item_strpd, found_brec = look_at_index(ingr_item_strpd, index_list, n_gram)
				if len(found_brec) > 0: 
					ingr_flag = False
					break

			# Search 'optional' ingredient
			if 'optional' in ingr_item_strpd:
				found_optional = True
				ingr_item_strpd = ingr_item_strpd.replace('optional', '')
			else:
				found_optional = False

			# Search n_grams at 'units'
			index_list = index_dict['units']
			for n_gram in reversed(range(1, 5)): # n_gramsn from 4 to 1
				ingr_item_strpd, found_unit = look_at_index(ingr_item_strpd, index_list, n_gram)
				if len(found_unit) > 0: break

			# Search n_grams at 'qualities'
			index_list = index_dict['qualities']
			for n_gram in reversed(range(1, 5)): # n_gramsn from 4 to 1
				ingr_item_strpd, found_quality = look_at_index(ingr_item_strpd, index_list, n_gram)
				if len(found_quality) > 0: break

			# Search n_grams at 'ingredients'
			index_list = index_dict['ingredients']
			for n_gram in reversed(range(1, 5)): # n_gramsn from 4 to 1
				ingr_item_strpd, found_item = look_at_index(ingr_item_strpd, index_list, n_gram)
				if len(found_item) > 0: break

			# Search n_grams at 'mises_en_plis'
			index_list = index_dict['mises_en_plis']
			for n_gram in reversed(range(1, 5)): # n_gramsn from 4 to 1
				ingr_item_strpd, found_msenp = look_at_index(ingr_item_strpd, index_list, n_gram)
				if len(found_msenp) > 0: break

			
			# Update context
			if ingr_flag:
				context['ingrs_strpd'].append({
					'ingr_flag': ingr_flag, 
					'amount_string_id': 'inpt_amt_' + str(ingr_n), 'amount_string': amount_str, 
					'found_unit_id': 'inpt_unit_' + str(ingr_n),	'found_unit': found_unit, 
					'found_quality_id': 'inpt_qlt_' + str(ingr_n), 'found_quality': found_quality, 
					'found_item_id': 'inpt_ingr_' + str(ingr_n),	'found_item': found_item, 
					'found_msenp_id': 'inpt_msenp_' + str(ingr_n), 'found_msenp': found_msenp, 
					'ingr_item_strpd_id': 'inpt_strpd_' + str(ingr_n), 'ingr_item_strpd': ingr_item_strpd,
					'found_optional_id': 'found_optional_' + str(ingr_n), 'found_optional': found_optional,
				})
				ingr_n += 1
				
			else:
				context['ingrs_strpd'].append({
					'ingr_flag': ingr_flag, 
					'amount_string_id': 'br_inpt_amt_' + str(brec_n), 'amount_string': amount_str, 
					'found_unit_id': 'br_inpt_unit_' + str(brec_n),	'found_unit': found_unit, 
					'found_quality_id': 'br_inpt_qlt_' + str(brec_n), 'found_quality': found_quality, 
					'found_item_id': 'br_inpt_ingr_' + str(brec_n),	'found_item': found_brec, 
					'found_msenp_id': 'br_inpt_msenp_' + str(brec_n), 'found_msenp': found_msenp, 
					'ingr_item_strpd_id': 'br_inpt_strpd_' + str(brec_n), 'ingr_item_strpd': ingr_item_strpd,
					'found_optional_id': 'found_optional_' + str(ingr_n), 'found_optional': found_optional,
				})
				brec_n += 1
	
	return render(request, 'parse_recipes/inspect_recipe.html', context)


def inspect_all_recipes(request):

	# Compare folders at '01_processed_recipes' and dicts at '02_recipe_dicts'
	# to check which recipes haven't been inspected yet
	all_recs_list_to_inspect = next(os.walk(os.path.join(SITE_ROOT, processed_files_path)))[1][:3]
	inspected_recs = next(os.walk(SITE_ROOT + '\\' + recipes_dict_folder))[2]
	inspected_recs = [x.split('.')[0] for x in inspected_recs]
	recs_to_inspect = list(set(all_recs_list_to_inspect) - set(inspected_recs))
	
	# Get the first recipe at 'recs_to_inspect' and run 'inspect_recipe' view
	# When the 'save' button at the inspection html is pressed, it calls the
	# 'ajax_request_view', that cleans the data comming from the ajax post and
	# save the recipe dict at '02_recipe_dicts'. Finally, the ajax post returns
	# to 'success' at the js script at 'inspect_recipe.html', which, by it's turn
	# calls 'inspect_all_recipes' view, and the process restart with the previous
	# lines comparisons.
	# When there is no more recipes to inspect, it returns 'Done!', and all the 
	# recipes dicts will be recoreded at '02_recipe_dicts'.
	if len(recs_to_inspect) > 0:
		return redirect('inspect_recipe_pg', recipe_id = recs_to_inspect[0])
	else:
		return HttpResponse("<html><body>Done!</body></html>")

	
	