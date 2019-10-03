import sys
import csv
import json
from pprint import pprint

class CEIM:
    def __init__(self, tec_class='', situation='', component_type='',
                component='', sub_component='', instance_id='',
                instance_value='', instanced_situation='', appl_id='',
                summary='', extended_attr = '', comments = '',
                slot = '', node =''):

        self.tec_class = tec_class                      #1
        self.situation = situation                      #1
        self.slot = slot                                #2
        self.node = node                                #3
        self.component_type = component_type            #4
        self.component = component                      #5
        self.sub_component = sub_component              #6
        self.instance_id = instance_id                  #7
        self.instance_value = instance_value            #8
        self.instanced_situation = instanced_situation  #9
        self.appl_id = appl_id                          #10
        self.summary = summary                          #11
        self.extended_attr = extended_attr              #12
        self.comments = comments                        #13

def ch_item(app_tup,opt):
    c_item=''
    while c_item not in app_tup:
        fmt = ''
        print('\n---------------------------------------------------')
        print('Please choose one of the choices below: \n')
        for item in range(0,len(app_tup)):
            fmt=('%s | %s' %(fmt,app_tup[item]))
        print(fmt + '\n')
        c_item=input(opt)
    return c_item

def writeTSV(FileName,obj):
    with open(FileName, 'a+', newline='') as tsv:
        spamwriter = csv.writer(tsv, dialect="excel-tab")
        add_list = []
        for i in range(0,14):
            add_list.append(getattr(obj, ceim_tuple[i]))
        spamwriter.writerow(add_list)

# Function to list contents from existing .tsv file
def list(FileName):
    count_entries = -1
    with open(FileName) as tsv:
        for line in csv.reader(tsv, dialect="excel-tab"):
            try: #to skip blanklines
                if line[0][0] != '#':
                    count_entries += 1
                    print ("\n-----------------------------------------------")
                    print ("Entry: %s\n" %(count_entries))
                    for i in range(0,14):
                        print(getattr(ceim_header, ceim_tuple[i]), line[i])
            except:
                pass # skip blank lines


def add_entry(FileName):
    new_entry = CEIM()

    #gett user input
    for i in range(0,14):
        if i in [4, 5, 6, 10]:
            var = ch_item(app_dict[i], getattr(ceim_header, ceim_tuple[i]))
        else:
            print('\n---------------------------------------------------')
            var = input('Please entry %s' %(getattr(ceim_header, ceim_tuple[i])))

        setattr(new_entry,ceim_tuple[i],var) # set value

    #confirm information
    print('\n----------------------------------------------')
    for i in range(0,14):
        print(getattr(ceim_header, ceim_tuple[i]),getattr(new_entry, ceim_tuple[i]))

    print('\n----------------------------------------------')

    yesno=False

    while not yesno in ['y', 'n']:
        yesno = input('are the information above right? (y/n): ')
    if yesno == 'y':
        writeTSV(FileName,new_entry)
        print('Added to %s' %(FileName))
    else:
        print ('aborting')

def help():
    print('\n----------------------------------------------')
    print('Usage:')
    print('<python3.6> ceim.py <tsv file> <opt>\n')
    print('opt:\n')
    print('list - list all entries in tsv file')
    print('add - add new entry to tsv file')
    print('\nJSON options:')
    print('<python3.6> ceim.py <tsv file> <opt> <json file>\n')
    print('json - creates tsv from json file')
    print('json-dump - creates json from tsv file')
    print('----------------------------------------------\n')



# Create new entry from json
def from_json(FileName,JsonFile):
    json_entry = CEIM()

    with open(JsonFile) as ceim_json:
        parsed_json = json.load(ceim_json)
        ceim_json.close()

    for i in range(len(parsed_json)):
        print('\n----------------------------------------------')
        for tup in range(0,14):
            setattr(json_entry,ceim_tuple[tup],parsed_json[i][ceim_tuple[tup]]) # set value
        writeTSV(FileName,json_entry)
        pprint(parsed_json[i])
        print('\nAdded to %s' %(FileName))


# JSON dump from TSV
def to_json(FileName,JsonFile):
    json_list=[]
    with open(FileName) as tsv:
        for line in csv.reader(tsv, dialect="excel-tab"):
            try: #to skip blanklines
                json_dict={}
                for i in range(0,14):
                    key=ceim_tuple[i]
                    json_dict[key]= line[i]
                json_list.append(json_dict)
            except:
                pass # skip blank lines

    with open(JsonFile, 'w+') as outfile:
        json.dump(json_list, outfile, indent=4, separators=(',', ': '))
        outfile.write('\n')
    print ('Json dumped to %s' %(JsonFile))


# Header
ceim_header=CEIM(tec_class = '#TEC CLASS: ',                       #0,
                situation = 'Pattern Match: ',                     #1,
                slot = 'Match Slot :',                             #2,
                node = 'Node  :',                                  #3,
                component_type = 'ComponentType: ',                #4,
                component = 'Component: ',                         #5,
                sub_component = 'SubComponent: ',                  #6,
                instance_id = 'InstanceId: ',                      #7,
                instance_value = 'InstanceValue: ',                #8,
                instanced_situation = 'InstanceSituation:',        #9,
                appl_id = 'ApplId: ',                              #10,
                summary = 'Summary: ',                             #11,
                extended_attr = 'ExtendedAttr: ',                  #12,
                comments = 'Comments ',                            #13
                )

ceim_tuple=(
            'tec_class', 'situation','slot','node','component_type','component',
            'sub_component','instance_id','instance_value','instanced_situation',
            'appl_id','summary','extended_attr','comments'
            )

app_dict={
            #component_type
            4:('Application', 'ComputerSystem', 'Database', 'Hardware', 'J2EE',
                'ManagementInfrastructure', 'Messaging', 'Network',
                'OperatingSystem', 'Security', 'Storage', 'WebServer',
                'Workload', 'Unknown', ),
            #component
            5:(
                'ActiveDirectory','AIX','AntiVirus','Apache','AS400',
                'BlackBerry','CICS','Citrix','Customer','DB2','Domino',
                'Generic','HMC','HPUX','HTTP','IBM','IIS','Impact',
                'IMS','Informix','Intel','IPlanet','IPM8Agent',
                'ITCAM','ITM5','ITM6','ITM6Agent','ITUAM','JBoss',
                'LDAP','LINUX','Lotus','Mongo','MQ','MSExchange',
                'mySAP','NetWare','Network','NodeAvail','OMNIbus',
                'Oracle','Ping','Probe','Ruby','SAP','ServerResourceManagement',
                'SharePoint','Siebel','Solaris','SQL','Sun','Sybase','TEC',
                'TivoliEndpoint','TivoliFramework','Tomcat','TPC','TSM',
                'Tuxedo','TWS','UNIX','Unknown','VitalSuite','VMwareESX',
                'VMwareVM','WebLogic','WebSphere','WebsphereInterchangeServer',
                'WebSphereMQ','WebSphereMQIntegrator','Windows','zOS'
                ),
            # sub_component
            6: (
                'Cluster','Configuration','CPU','Disk','Drive','FileSystem',
                'Group','Job','License','Listener','Log','Mail','Memory',
                'Network','NetworkInterface','Notification','Performance',
                'Ping','Process','Service','SPA','Status','Tape','TEMS','TEPS',
                'Ticketing','User','Version','WPA'
                ),
            #appl_id
            10: (
                'ACTIVEDIR','AIX','APACHE','APM','BES','BROADVISION','CHECKPOINT',
                'CISCO','CITRIX','COLDFUSION','COMMON','DB2','DCE','HTTPSERVER',
                'IIS','INFORMIX','IPLANET','ISM','ITM','ITUAM','J2EE','LDAP',
                'LINUX','METERING','MONGO','MQSERIES','MSEXCHANGE','MSSQL',
                'NET_AVAIL','NETSCAP','NETSERV_AVAIL','NOTES','OMNIBUS','ORACLE',
                'OS400','RTT','SAP','SHAREPOINT','SIEBEL','SPECTRUM','SRM',
                'SSLCERT','SYBASE','TDW','TSM','TWS','UNIX','VERITAS','VITALSUITE'
                ,'VMW','WEBSPHERE','WIN','XENAPP'
                )
            }



# main
if len(sys.argv) < 2: # if no arg is giving return message
    help()
elif len(sys.argv) == 3 and sys.argv[2] == 'list': #if list arg is giving runs list
    FileName=sys.argv[1]
    list(FileName)
elif len(sys.argv) == 3 and sys.argv[2] == 'add': #add Entry
    FileName=sys.argv[1]
    add_entry(FileName)
elif len(sys.argv) == 4 and sys.argv[2] == 'json': #add Entry
    FileName=sys.argv[1]
    JsonFile=sys.argv[3]
    from_json(FileName,JsonFile)
elif len(sys.argv) == 4 and sys.argv[2] == 'json-dump': #add Entry
    FileName=sys.argv[1]
    JsonFile=sys.argv[3]
    to_json(FileName,JsonFile)
else:
    help()
