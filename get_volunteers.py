import sys
import csv
import getopt
from bson.code import Code
from pymongo import MongoClient

def usage():
    print ("Error. Please try again.")

def main(argv):
    csv_file = 'volunteer_export.csv'
    db_host = 'localhost'
    db_port = 27017
    db_name = 'platform'

    try:
        opts, args = getopt.getopt(argv, "c:h:p:n:", ["csv-file=", "db-host=", "db-port=", "db-name="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-c", "--csv-file"):
            csv_file = arg
        elif opt in ("-h", "--db-host"):
            db_host = arg
        elif opt in ("-p", "--db-port"):
            db_port = int(arg)
        elif opt in ("-n", "--db-name"):
            db_name = arg

    print ('connected to {} on {}'.format(db_name, db_host + ':' + str(db_port)))

    client = MongoClient(db_host, db_port)
    db = client[db_name]

    reduce_coll_name = "volunteers"
    volunteer_coll_name = "volunteerdata"

    mapper = Code("""
                    function() {
                        this.team.members.forEach(function(member) { emit(member.shortId,  1 ); }),
                        this.team.waitlist.forEach(function(waiting) { emit(waiting.shortId, 1); })
                    }
                  """)

    reducer = Code("""
                    function(key, values) {
                        return values.length
                    }
                  """)

    query = { "$or": [ { "team.members": { "$not": { "$size": 0 } }},
                   { "team.waitlist": { "$not": { "$size": 0 } }}]}

    db.projects.map_reduce(mapper, reducer, reduce_coll_name, query)

    db.drop_collection(volunteer_coll_name)
    db.create_collection(volunteer_coll_name)

    for volunteer in db[reduce_coll_name].find():
        vid = volunteer["_id"]
        user = db.users.find_one({ "shortId": vid })

        if user is None:
            continue

        first_name = user["linkedin"]["firstName"]
        last_name = user["linkedin"]["lastName"]
        email = user["linkedin"]["email"]

        print (first_name, last_name, email, int(volunteer["value"]))

        result = db[volunteer_coll_name].insert_one( { "vid": vid,
            "firstName": first_name,
            "lastName": last_name,
            "email": email } )

    db.drop_collection(reduce_coll_name)

    cursor = db[volunteer_coll_name].find({},{"_id": 0})

    with open(csv_file, 'w', newline='') as outfile:
        fields = ["vid", "firstName", "lastName", "email"]
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        for x in cursor:
            writer.writerow(x)

if __name__ == "__main__":
    main(sys.argv[1:])
