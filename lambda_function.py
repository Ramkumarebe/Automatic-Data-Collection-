import psycopg2
import requests
import json

# Make API request to retrieve data
def lambda_handler(event, context):
  try:
    response = requests.get('http://api.open-notify.org/iss-now.json')
  
    response.raise_for_status()
    print(response)
  except requests.exceptions.RequestException as e:
   flag = {"text": "Server is down!"}
   requests.post("https://hooks.slack.com/services/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", json=flag)
   print(e)
   return
   
  data = json.loads(response.text)

  latitude = data["iss_position"]["latitude"]
  longitude = data["iss_position"]["longitude"]
  timestamp = data["timestamp"]
  message = data["message"]
  print(data)

#Connect to RDS database
  conn = psycopg2.connect(
    host='database-1.ch67q9yb4zb7.ap-south-1.rds.amazonaws.com',
    database='postgres',
    user='postgres',
    password='',
    port=5432)
	              

# Define SQL query to insert data
  cur = conn.cursor()
  
  cur.execute("INSERT INTO issdata (latitude, longitude, timestamp, message) VALUES (%s, %s, %s, %s);", (latitude, longitude, timestamp, message))
  conn.commit() 
  cur.close()
  conn.close()

