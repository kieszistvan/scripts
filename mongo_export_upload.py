# Include the Dropbox SDK
import dropbox
import time
from subprocess import call

generated_access_token = 'generate one on Dropbox page'

exportFileName = 'export_' + time.strftime('%Y%m%d') + '.csv'
host = 'db_host:db_port'
db = 'db_name'
collection = 'collection_name'
fields = 'field_names'

# export from Mongo
call(['mongoexport', '--host', host, '--db', db, '--collection', collection, '--csv', '--out', exportFileName, '--fields', fields])

# upload to Dropbox
f = open(exportFileName, 'rb')
response = client.put_file(exportFileName, f)
client = dropbox.client.DropboxClient(generated_access_token)
print 'linked account: ', client.account_info()
print 'uploaded: ', response
