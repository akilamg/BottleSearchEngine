import boto.ec2
import time
import os

def deploy():
	ec2 = boto.ec2.connect_to_region('us-east-1',aws_access_key_id='', aws_secret_access_key='')
	ec2_key_pair  = ec2.get_key_pair("key_pair")
	print ec2_key_pair
	if ec2_key_pair == None:
		ec2_key_pair  = ec2.create_key_pair("key_pair")
		ec2_key_pair.save(".")

	group = ec2.get_all_security_groups(filters={'group-name':'group'})
	if not group:
		group = ec2.create_security_group("csc326-groupg326-2-006","a group for ec2")
		group.authorize("icmp",-1,-1,"0.0.0.0/0")
		group.authorize("tcp",22,22,"0.0.0.0/0")
		group.authorize("tcp",80,80,"0.0.0.0/0")
		group.authorize('tcp', 8080, 8080, '0.0.0.0/0')
	else:
		group=group[0]

	instances = ec2.get_only_instances()
	runninginstances = [i for i in instances if i.state == 'running']
	instance = None
	if not instances or (instances and not runninginstances):
		instances = ec2.run_instances(image_id='ami-8caa1ce4',key_name='key_pair',security_groups=['csc326-groupg326-2-006'],instance_type='t1.micro')
		instances = instances.instances[0]
	else:
		instances=instances[0]
	instance = instances

	print "Waiting for instance to be ready to run.."
	while instance.update() != 'running':
		time.sleep(10)

	print "Instance is ready and running"

	os.system("ssh -i key_pair.pem ubuntu@%s sudo apt-get update" %(instance.ip_address))
	os.system("ssh -i key_pair.pem ubuntu@%s sudo apt-get install -y python-pip" %(instance.ip_address))
	os.system("ssh -i key_pair.pem ubuntu@%s sudo pip install bottle" %(instance.ip_address))
	os.system("ssh -i key_pair.pem ubuntu@%s sudo pip install beaker" %(instance.ip_address))
	os.system("ssh -i key_pair.pem ubuntu@%s sudo pip install google-api-python-client" %(instance.ip_address))
	os.system("ssh -i key_pair.pem ubuntu@%s sudo pip install oauth2client" %(instance.ip_address))
	os.system("ssh -i key_pair.pem ubuntu@%s sudo pip install BeautifulSoup4" %(instance.ip_address))
	os.system("ssh -i key_pair.pem ubuntu@%s sudo pip install BeautifulSoup4" %(instance.ip_address))
	os.system("ssh -i key_pair.pem ubuntu@%s mkdir app" %(instance.ip_address))
	os.system("scp -i key_pair.pem ~/RandomSearch/Lab2/* ubuntu@%s:~/app" %(instance.ip_address))
	os.system("ssh -i key_pair.pem ubuntu@%s sudo nohup python app/frontEnd.py" %(instance.ip_address))
	#elasticIPaddr = ec2.allocate_address()
	#elasticIPaddr.associate(instance.id)
	return instance.ip_address

if __name__ == "__main__":
	print(deploy())
