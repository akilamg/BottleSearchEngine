import sys
import boto.ec2
import time

def terminate(connection):
	instances = sys.argv[1:]
	try:
		terminatelist=connection.terminate_instances(instance_ids=instances)
		message = "Success! Id(s) terminated: "+ " ".join(instances)
		return message
	except boto.exception.EC2ResponseError as e:
		raise e


aws_keys={}

if __name__ == "__main__":
	credentials = open("awskeys.conf","r")
	for line in credentials:
		key_id  = line.split(": ")[0]
		key_code = line.split(": ")[1]
		if "key_ID" in key_id or "access_key" in key_id:
			aws_keys[key_id] = key_code.split("\n")[0]
	connection = boto.ec2.connect_to_region('us-east-1',aws_access_key_id=aws_keys["key_ID"], aws_secret_access_key=aws_keys["access_key"]) #Region us-east-1
	print terminate(connection)