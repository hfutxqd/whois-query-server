# whois-query-server
A whois query http server base on python3.7. It supports almost all domain.

Run server in system    
`python3.7 -m pip install -r requirements.txt`
`python3.7 server.py`    

Run server in docker    
`docker run -d -p8000:8000 imxqd/whois-query-server:latest`    

Example:    
`http://127.0.0.1:8000/json/cctv.cn`    
Return: 

	{
	  "domain_name": "cctv.cn",
	  "registrar": "易介集团北京有限公司",
	  "name": "中央电视台",
	  "creation_date": "1047299089",
	  "expiration_date": "1840010185",
	  "name_servers": [
	    "ns4.cctv.com.cn",
	    "ns3.cctv.com.cn",
	    "ns2.cctv.com.cn",
	    "ns1.cctv.com.cn"
	  ],
	  "status": [
	    "serverDeleteProhibited",
	    "serverUpdateProhibited",
	    "serverTransferProhibited"
	  ],
	  "emails": "cy@cctv.com",
	  "dnssec": "unsigned"
	}

or    
`http://127.0.0.1:8000/raw/cctv.cn`    
Return:      

	Domain Name: cctv.cn
	ROID: 20030310s10001s00022615-cn
	Domain Status: serverDeleteProhibited
	Domain Status: serverUpdateProhibited
	Domain Status: serverTransferProhibited
	Registrant ID: sfn8594304310599
	Registrant: 中央电视台
	Registrant Contact Email: cy@cctv.com
	Sponsoring Registrar: 易介集团北京有限公司
	Name Server: ns4.cctv.com.cn
	Name Server: ns3.cctv.com.cn
	Name Server: ns2.cctv.com.cn
	Name Server: ns1.cctv.com.cn
	Registration Time: 2003-03-10 20:24:49
	Expiration Time: 2028-04-22 17:56:25
	DNSSEC: unsigned
