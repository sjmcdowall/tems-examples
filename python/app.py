from flask import Flask, request, render_template
import json
import pprint
import threading
import time
from queue import Queue


'''
Author: Naman Shenoy
'''

app = Flask(__name__)

pp = pprint.PrettyPrinter(indent=4)
'''
ITEM QUEUE
'''
class QueueItem:
	def __init__(self, test_cell_id, key, value):
		self.test_cell_id = test_cell_id
		self.key = key
		self.value = value

message_queue = Queue()

'''
HELPER METHODS
'''

def log_info(header, values, logging=True):
	#if logging:
		#print(logging)
		#logfile = open('log.txt', 'a')
		#logfile.write('\n===============>  '+str(header)+'  <===============\n')

	print ('\n===============>  '+str(header)+'  <===============\n')
	#if logging:
			#logfile.write(str(values))
	for key,value in values.items():
		if key and value:
			print('Key =>  '+str(key))
			print('Value ==>  '+str(value))
			print('\n\n')


def log_sub_info(header, values,logging=True):
	#if logging:
		#print(logging)
		#logfile = open('log.txt', 'a')
		#logfile.write('\n\t\t=======>  '+str(header)+'  <=======\n')

	print ('\n\t\t=======>  '+str(header)+'  <=======\n')
	#if logging:
			#logfile.write(str(values))

	for key,value in values.items():
		if key and value:
			print('Key =>  '+str(key))
			print('Value ==>  '+str(value))
			print('\n\n')


'''
VIEW URLS
'''
@app.route('/')
def index():
	return 'Hi'

@app.route('/<test_cell_id>/')
def tester_view(test_cell_id):
	test_cell_id = test_cell_id.upper()
	return test_cell_id

'''
API ROUTING METHODS
'''
# INITIALIZATION API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/INITIALIZATION', methods=['GET','POST'])
def tcs_initialization(test_cell_id):
	try:
		test_cell_id = test_cell_id.upper()
		if request.method == 'GET':
			return json.dumps({"success":True}), 301, {'ContentType':'application/json'}
		if request.method == 'POST':
			log_info('START INITIALIZATION', {'test_cell_id':test_cell_id,})
			log_info('Request JSON',{})
			print (json.dumps(request.get_json(silent=True),indent=4,sort_keys=True))
			post_json = request.get_json(silent=True)

			log_info('END INITIALIZATION', {})

			return json.dumps({"success":True}), 200, {'ContentType':'application/json'}
	except KeyError as error:
		return json.dumps({"success":"Key Error"}), 404, {'ContentType':'application/json'}
	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

# STATUS API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/STATUS', methods=['GET', 'POST'])
def tcs_status(test_cell_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':

		log_info('BEFORE: START STATUS',{'test_cell_id':test_cell_id})

		post_json = request.get_json(silent=True)
		print(json.dumps(post_json, indent=4, sort_keys=True))

		print('AFTER: THREADS ACTIVE: '+str(threading.active_count()))
		log_info('END STATUS',{})

		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}
	return json.dumps({"success":False}), 200, {'ContentType':'application/json'}

# SHUTDOWN API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/SHUTDOWN', methods=['GET', 'POST'])
def tcs_shutdown(test_cell_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':
		log_info('START SHUTDOWN',{'test_cell_id' : test_cell_id})
		print(json.dumps(request.get_json(silent=True), indent=4, sort_keys=True))

		log_sub_info(test_cell_id+' Shutdown',{})

		log_info('END SHUTDOWN',{})
		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}

	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

# CONFIGURATION API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/CONFIGURATION', methods=['GET', 'POST'])
def tcs_configuration(test_cell_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':
		log_info('START CONFIGURATION',{'test_cell_id':test_cell_id})
		post_json = request.get_json(silent=True)
		if post_json:
			print(post_json.keys())
			print(json.dumps(post_json, indent=4, sort_keys=True))
			print(json.dumps(post_json['BOARD'], indent=4, sort_keys=True))
			save_json = {'board': post_json['BOARD'], 'timestamp': post_json['TIME_STAMP'], 'tester':test_cell_id}
			print(json.dumps(save_json, indent=4, sort_keys=True))
			return json.dumps({"success":True}), 200, {'ContentType':'application/json'}

		else:
			message_queue.put(QueueItem(test_cell_id, 'config_id', 'None'))
			print ('Config was null')
		log_info('END CONFIGURATION',{})

		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}
	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

# USER_ACCOUNT API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/USER_ACCOUNT', methods=['GET', 'POST'])
def tcs_user_account(test_cell_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':
		log_info('START USER_ACCOUNT',{'test_cell_id':test_cell_id})
		post_json = request.get_json(silent=True)
		print(json.dumps(request.get_json(silent=True), indent=4, sort_keys=True))
		if "LOGIN" in post_json['USER_EVENT']:
			user_logged_in = post_json['USER_ID']
			log_sub_info('USER HAS LOGGED IN',{'user_id':user_logged_in})
		elif "LOGOUT" in post_json['USER_EVENT']:
			user_logged_out = post_json['USER_ID']
			log_sub_info('USER HAS LOGGED OUT',{})
		log_info('END USER_ACCOUNT',{})

		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}
	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

# TESTER_OS API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/TESTER_OS', methods=['GET', 'POST'])
def tcs_tester_os(test_cell_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':
		log_info('START TESTER_OS',{'test_cell_id':test_cell_id})
		post_json = request.get_json(silent=True)
		print(json.dumps(post_json, indent=4, sort_keys=True))
		igxl_version = post_json['VERSION']

		user_logged_in = post_json['USER_ID']

		log_info('END TESTER_OS',{})
		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}
	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

# TEST_PROGRAM_LOAD API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/TEST_PROGRAM_LOAD', methods=['GET', 'POST'])
def tcs_test_program_load(test_cell_id):
	test_cell_id = test_cell_id.upper()
	try:
		if request.method == 'POST':
			log_info('START TEST_PROGRAM_LOAD',{'test_cell_id':test_cell_id})
			post_json = request.get_json(silent=True)

			print(json.dumps(post_json, indent=4, sort_keys=True))

			log_info('END TEST_PROGRAM_LOAD',{})

			return json.dumps({"success":True}), 200, {'ContentType':'application/json'}
		return json.dumps({"success":False}), 404, {'ContentType':'application/json'}
	except KeyError as err:
		print (err)
		log_info('KEY ERROR DURING TEST_PROGRAM_LOAD',{})
		log_info('END TEST_PROGRAM_LOAD',{})

		return json.dumps({'error':'KeyError'}), 400, {'ContentType':'application/json'}
	except:
		return json.dumps({'error':'Unknown'}), 500, {'ContentType':'application/json'}


# LOT_START API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/LOT/<lot_id>/LOT_START', methods=['GET', 'POST'])
def tcs_test_lot_start(test_cell_id, lot_id):
	test_cell_id = test_cell_id.upper()

	if request.method == 'POST':
		log_info('START LOT_START',{'test_cell_id':test_cell_id})
		print(json.dumps(request.get_json(silent=True), indent=4, sort_keys=True))
		log_info('END LOT_START',{})
		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}
	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}


# LOT_END API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/LOT/<lot_id>/LOT_END', methods=['GET', 'POST'])
def tcs_test_lot_end(test_cell_id,lot_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':
		log_info('START LOT_END',{'test_cell_id':test_cell_id})
		print(json.dumps(request.get_json(silent=True), indent=4, sort_keys=True))
		log_info('END LOT_END',{})
		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}
	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}


# SUBLOT_START API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/LOT/<lot_id>/SUBLOT/<sublot_id>/SUBLOT_START', methods=['GET', 'POST'])
def tcs_sublot_start(test_cell_id, lot_id, sublot_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':
		log_info('START SUBLOT_START',{'test_cell_id':test_cell_id})
		print(json.dumps(request.get_json(silent=True), indent=4, sort_keys=True))
		log_info('END SUBLOT_START',{})
		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}
	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

# SUBLOT_END API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/LOT/<lot_id>/SUBLOT/<sublot_id>/SUBLOT_END', methods=['GET', 'POST'])
def tcs_sublot_end(test_cell_id, lot_id, sublot_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':
		log_info('START SUBLOT_END',{'test_cell_id':test_cell_id})
		print(json.dumps(request.get_json(silent=True), indent=4, sort_keys=True))
		log_info('END SUBLOT_END',{})
		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}
	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

# TEST_START API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/LOT/<lot_id>/SUBLOT/<sublot_id>/TEST_START', methods=['GET', 'POST'])
def tcs_test_start(test_cell_id, lot_id, sublot_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':
		log_info('START TEST_START',{'test_cell_id':test_cell_id})
		print(json.dumps(request.get_json(silent=True), indent=4, sort_keys=True))
		log_info('END TEST_START',{})
		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}
	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

# TEST_END API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/LOT/<lot_id>/SUBLOT/<sublot_id>/TEST_END', methods=['GET', 'POST'])
def tcs_test_end(test_cell_id, lot_id, sublot_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':
		log_info('START TEST_END',{'test_cell_id':test_cell_id})
		post_json = request.get_json(silent=True)
		print(json.dumps(post_json, indent=4, sort_keys=True))
		log_info('END TEST_END',{})
		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}
	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

# TEST_DATA_SETUP API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/LOT/<lot_id>/TEST_DATA_SETUP', methods=['GET', 'POST'])
def tcs_test_data_setup(test_cell_id, lot_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':
		log_info('START TEST_DATA_SETUP',{'test_cell_id':test_cell_id})
		print(json.dumps(request.get_json(silent=True), indent=4, sort_keys=True))
		log_info('END TEST_DATA_SETUP',{})
		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}

	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

# TEST_DATA API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/LOT/<lot_id>/SUBLOT/<sublot_id>/TEST_DATA', methods=['GET', 'POST'])
def tcs_test_data(test_cell_id, lot_id, sublot_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':
		log_info('START TEST_DATA',{'test_cell_id':test_cell_id})
		print(json.dumps(request.get_json(silent=True), indent=4, sort_keys=True))
		log_info('END TEST_DATA',{})
		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}

	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

# HALT API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/HALT', methods=['GET', 'POST'])
def tcs_halt(test_cell_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':
		log_info('START HALT',{'test_cell_id':test_cell_id})
		print(json.dumps(request.get_json(silent=True), indent=4, sort_keys=True))
		log_info('END HALT',{})
		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}

	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

# EXTERNAL API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/EXTERNAL', methods=['GET', 'POST'])
def tcs_external(test_cell_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':
		log_info('START EXTERNAL',{'test_cell_id':test_cell_id})
		print(json.dumps(request.get_json(silent=True), indent=4, sort_keys=True))
		log_info('END EXTERNAL',{})
		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}

	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

# PERIPHERAL_MESSAGE API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/PERIPHERAL_MESSAGE', methods=['GET', 'POST'])
def tcs_peripheral_message(test_cell_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':
		log_info('START PERIPHERAL_MESSAGE',{'test_cell_id':test_cell_id})
		print(json.dumps(request.get_json(silent=True), indent=4, sort_keys=True))
		log_info('END PERIPHERAL_MESSAGE',{})
		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}
	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

#MAINTENANCE API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/MAINTENANCE', methods=['GET', 'POST'])
def tcs_maintenance(test_cell_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':
		log_info('START MAINTENANCE',{'test_cell_id':test_cell_id})
		print(json.dumps(request.get_json(silent=True), indent=4, sort_keys=True))
		log_info('END MAINTENANCE',{})
		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}
	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

# maintenance_MESSAGE API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/MAINTENANCE_MESSAGE', methods=['GET', 'POST'])
def tcs_maintenance_message(test_cell_id):
	test_cell_id = test_cell_id.upper()
	print ('MAINTENANCE_MESSAGE')
	if request.method == 'POST':
		log_info('START MAINTENANCE_MESSAGE',{'test_cell_id':test_cell_id})
		post_json = json.dumps(request.get_json(silent=True))
		if 'null' in post_json:
			print ("NO SILENT JSON")
			post_json = json.loads(request.data.decode('utf-8'))
			print (post_json['RAM'])
		print(json.dumps(post_json, indent=4, sort_keys=True))
		log_info('END MAINTENANCE_MESSAGE',{})
		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}
	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

# maintenance_DATA API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/MAINTENANCE_DATA', methods=['GET', 'POST'])
def tcs_maintenance_data(test_cell_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':
		log_info('START MAINTENANCE_DATA',{'test_cell_id':test_cell_id})

		print(json.dumps(request.get_json(silent=True), indent=4, sort_keys=True))
		redis.hmset(test_cell_id+'_TEST',post_json)
		log_info('END MAINTENANCE_DATA',{})
		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}
	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

# TODO: Implement Test Cell Control Message

# GENERIC API Endpoint
@app.route('/TEST_CELL/<test_cell_id>/GENERIC', methods=['GET', 'POST'])
def tcs_generic(test_cell_id):
	test_cell_id = test_cell_id.upper()
	if request.method == 'POST':
		log_info('START GENERIC',{'test_cell_id':test_cell_id})
		print(json.dumps(request.get_json(silent=True), indent=4, sort_keys=True))
		log_info('END GENERIC',{})
		redis.hmset(test_cell_id+'_TEST',post_json)
		return json.dumps({"success":True}), 200, {'ContentType':'application/json'}
	return json.dumps({"success":False}), 404, {'ContentType':'application/json'}

if __name__ == '__main__':
	app.run(debug=True, host= '0.0.0.0')
