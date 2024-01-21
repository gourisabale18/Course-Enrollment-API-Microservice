import redis
from datetime import datetime

redis_connection_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

waitlists = "Waitlists"
r = redis.Redis(connection_pool=redis_connection_pool)

# Creates a Waitlist for a Section - Registar API Call
def createWaitlist(section_id):   
    r.sadd(waitlists, str(section_id))

# Adds a Student to the Waitlist and Creates Waitlist if None Exists for that Class - Student API Call
def addWaitlists(class_waitlist, id):
        if r.sismember(waitlists, class_waitlist) == 1:
            position = r.zcard(class_waitlist) + 1
            r.zadd(class_waitlist, {id: position})   # Adds Student to Waitlist with Position Number in order to Track Users By Position 'Score' - Not Used to Track actual position (use rank instead)

            update_last_modified(class_waitlist, id)

def update_last_modified(class_waitlist, id):
    redis_key = f"last-modified:{class_waitlist}:{id}"
    date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    r.set(redis_key, date)

def deleteLastModified(class_waitlist, id):
    redis_key = f"last-modified:{class_waitlist}:{id}"
    r.delete(redis_key)

def getLastModifiedDate(class_waitlist, id):
    redis_key = f"last-modified:{class_waitlist}:{id}" # Generate the key for the last modification dates
    date = r.get(redis_key) # Get all members (dates) from the set associated with the key
    return date.decode('utf-8')

# Prints the Waitlist with the Positions of Each Student - Instructor API Call
def displayWaitlist(selected_waitlist):   
    selected_waitlist = str(selected_waitlist)
    if r.sismember(waitlists, selected_waitlist) == 1:    # Error Checks to See if Waitlist Exists
        return r.zrange(selected_waitlist, 0, -1)

# Checks the Waitlist Position of a Student - Student API Call
def checkWaitlistPosition(selected_waitlist, id):   
    if r.sismember(waitlists, str(selected_waitlist)) == 1:
        return r.zrank(str(selected_waitlist), id)          # Starts with '0' index; starting with '1' for normal users
        
# Checks the Waitlist Size to See if it is Full and Whether or Not a Student Can be Added - Student API Call
def checkWaitlistSize(selected_waitlist):   
    return r.zcard(selected_waitlist)

# Checks to See if a Student is Waitlisted in More than 3 Classes - Student API Call
def checkNumberOfWaitlistEnrollments(id):   
    class_waitlists = r.smembers(waitlists)
    count = 0 
    for waitlist in class_waitlists:
        if r.zscore(waitlist, id) is not None:
            count += 1
    return count

# Removes a Student From the Waitlist when Dropping or Being Dropped - Instructor or Student API Call
def removeWaitlist(selected_waitlist, id):
    score = r.zscore(selected_waitlist, id)
    r.zrem(selected_waitlist, id)
    return score


# Similar to removeWaitlist, but also pulls the student to be enrolled in the class - Student API Call
def removeAndAddWaitlist(selected_waitlist):   
    return r.zpopmin(selected_waitlist)
    
# Deletes a Waitlist - Registrar API Call
def deleteWaitlist(selected_waitlist):   
    r.srem(waitlists, selected_waitlist)
    r.zremrangebyrank(selected_waitlist, 0, -1)

def updateAllLastModifiedForIdsGreaterThan(section_id, user_score):
    members_with_scores = r.zrange(section_id, 0, -1, withscores=True)
    for item in members_with_scores:
        current_user_score = int(item[1])
        if current_user_score > user_score:
            update_last_modified(section_id, item[0].decode('utf-8'))

def print_values_for_class(class_waitlist):
    pattern = f"last-modified:{class_waitlist}:*"
    keys = r.keys(pattern)
    for key in keys:
        value = r.get(key)
        print(f"Values for key {key.decode('utf-8')}:", value)
    


if __name__ == "__main__":
    # print_values_for_class(4)
    # updateAllLastModifiedForIdsGreaterThan(4, 4)
    print_values_for_class(4)
    