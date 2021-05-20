# compose_flask/app.py
from flask import Flask, jsonify, request
from redis import Redis
from connection import get_connection
import json

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/redis/user')
def redis_get_user():
	try:
		userId = request.args.get('userId', 0)
		key = "user"+str(userId)
		#redis.incr('hits')
		#data = redis.mget(['123', '456'])
		user = redis.get(key)	
		#return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')
		result = {
			"result": "ok",
			"message": "successful",
			"data": json.loads(user)
		}
	except Exception as e:
		result = {
			"result": "fail",
			"message": str(e),
			"data": None
		}
	return jsonify(result)

@app.route('/redis/user', methods=['POST, PUT'])
def redis_post_user():
	try:
		received_data = request.data
		received_data = received_data.decode('utf-8')
		data = json.loads(received_data)
		userId = data['userId']
		value = data['data']
		key = "user"+str(userId)
		redis.set(key, value)
		result = {
			"result": "ok",
			"message": "successful"
		}
	except Exception as e:
		result = {
			"result": "fail",
			"message": str(e)
		}
	return jsonify(result)

@app.route('/redis/user', methods=['DELETE'])
def redis_delete_user():
	try:
		received_data = request.data
		received_data = received_data.decode('utf-8')
		data = json.loads(received_data)
		userId = data['userId']
		key = "user"+str(userId)
		redis.delete(key)
		result = {
			"result": "ok",
			"message": "successful"
		}
	except Exception as e:
		print("err ",e)
		result = {
			"result": "fail",
			"message": str(e)
		}
	return jsonify(result)

@app.route('/mysql/user')
def get_mysql_users():
	try:
		conn = get_connection()
		cursor = conn.cursor()
		sql = "select * from tbl_users"
		cursor.execute(sql)
		data = cursor.fetchall()
		#do something
		result = {
			"result": "ok",
			"message": "successful",
			"data": data
		}

	except Exception as e:
		result = {
			"result": "fail",
			"message": str(e),
			"data": None
		}

	finally:
		conn.commit()
		cursor.close()

	return jsonify(result)

@app.route('/mysql/user', methods=['DELETE'])
def delete_mysql_user():
	try:
		conn = get_connection()
		cursor = conn.cursor()
		received_data = request.data
		received_data = received_data.decode('utf-8')
		data = json.loads(received_data)
		userId = data['userId']

		sql = "delete from tbl_users where id=%s"
		cursor.execute(sql,(userId,))

		result = {
			"result": "ok",
			"message": "successful"
		}

	except Exception as e:
		result = {
			"result": "fail",
			"message": str(e)
		}

	finally:
		conn.commit()
		cursor.close()

	return jsonify(result)

@app.route('/mysql/user', methods=['POST'])
def register_mysql_user():
	try:
		conn = get_connection()
		cursor = conn.cursor()
		received_data = request.data
		received_data = received_data.decode('utf-8')
		data = json.loads(received_data)

		userName = data['username']

		sql = "insert into tbl_users(username) values(%s)"
		cursor.execute(sql,(userName,))

		result = {
			"result": "ok",
			"message": "successful"
		}

	except Exception as e:
		result = {
			"result": "fail",
			"message": str(e)
		}
	finally:
		conn.commit()
		cursor.close()

	return jsonify(result)

@app.route('/mysql/user', methods=['PUT'])
def update_mysql_user():
	try:
		conn = get_connection()
		cursor = conn.cursor()
		received_data = request.data
		received_data = received_data.decode('utf-8')
		data = json.loads(received_data)
		userId = data['id']
		userName = data['username']

		sql = "update tbl_users set username = %s where id = %s"
		cursor.execute(sql,(userName,userId))

		result = {
			"result": "ok",
			"message": "successful"
		}

	except Exception as e:
		result = {
			"result": "fail",
			"message": str(e)
		}

	finally:
		conn.commit()
		cursor.close()

	return jsonify(result)


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True, port=5006)