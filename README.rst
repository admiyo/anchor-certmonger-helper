# anchor-certmonger-helper


Helper program that enables Certmonger to communicate with an OpenStack Anchor CA 


1.      Set up Anchor according to its readme, with stand user ‘myusername’ and password ‘simplepassword’
2.      Add ‘anchor’ to ~/.config/certmonger/cas/

 

cat /home/gyee/.config/certmonger/cas/anchor

id=anchor

ca_is_default=0

ca_type=EXTERNAL

ca_external_helper=/home/gyee/projects/certmonger/anchor_ca_cert_helper.py --url http://0.0.0.0:5061/v1/sign/default --user myusername --secret simplepassword

 

