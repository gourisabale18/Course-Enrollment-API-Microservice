import boto3
from boto3.dynamodb.conditions import Key
import datetime
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Header, Response
from share.enrollment.enrollments import Item as Enrollment
from share.enrollment.waitlist import (
    addWaitlists, checkWaitlistPosition, checkWaitlistSize, removeWaitlist, removeAndAddWaitlist, checkNumberOfWaitlistEnrollments, createWaitlist, getLastModifiedDate, updateAllLastModifiedForIdsGreaterThan, deleteLastModified
)
from share.enrollment.enrollment_count import (
    addSectionEnrollment, checkCurrentSectionSize
)

from api.services.enrollment.main import (
    get_db, validate_student_id, validate_section_id
)

from share.notification.subscriptions import getSubscription
from share.notification.rabbitmq.sender import RabbitManager

router = APIRouter()

# List all classes
@router.get("/student/classes")
def list_classes(
    id: int = Depends(validate_student_id),
    db: boto3.session.Session = Depends(get_db)
):
    sections = db.Table("sections").scan()["Items"]
    return {"sections": sections}

# List all of a students enrollments
@router.get("/student/enrollments")
def list_classes(
    id: int = Depends(validate_student_id),
    db: boto3.session.Session = Depends(get_db)
):

    # Scan the "enrollments" table to get all items for the given student_id
    result = db.Table("enrollments").scan(
        FilterExpression=Key('student_id').eq(id)
    )

    # Return the result, you may want to format this based on your needs
    return {"enrollments": result.get('Items', [])}


@router.get("/student/check_waitlist")
def check_waitlist(
    section_id: int,
    id: int = Depends(validate_student_id),
    if_last_modified: str = Header(None, alias="If-Modified-Since"),
):
    try:
        # Get the current last modification date
        current_last_date = getLastModifiedDate(section_id, id)

        # Check if the resource has been modified since the specified date
        if if_last_modified and current_last_date and if_last_modified == current_last_date:
            return JSONResponse(content={}, status_code=304)

        # Replace this with your actual logic to fetch data or check waitlist position
        waitlist_position = checkWaitlistPosition(section_id, id)

        if waitlist_position is None:
            waitlist_position = 0

        # Set the response content
        response_data = {
            "Student of ID #: ": str(id),
            "waitlisted in section #: ": str(section_id),
            "with position": str(waitlist_position),
        }

        if current_last_date:
            return JSONResponse(content=response_data, headers={"Last-Modified": current_last_date})

        return JSONResponse(content=response_data)

    except LookupError:
        raise HTTPException(status_code=404, detail="Student is not in this Waitlisted Class")


# # # Enroll student into section or into section's waitlist
@router.post("/student/enroll")
def enroll_student(
    section_id: int,
    id: int = Depends(validate_student_id), 
    db: boto3.session.Session = Depends(get_db)
    ):
    
    section_id = validate_section_id(section_id, db)

    # Check if student with given id is not enrolled already
    result = db.Table("enrollments").query(
        KeyConditionExpression=Key('section_id').eq(section_id) & Key('student_id').eq(id)
    )

    if len(result["Items"]) > 0 and result["Items"][0]["is_dropped"] != 1:
        raise HTTPException(status_code=400, detail="Student is already enrolled in this class")
    

    # Gets current capacity of students; actively in the class
    current_capacity = checkCurrentSectionSize(section_id)

    # If current_capacity is None, then there are no students in the class
    if current_capacity == None:
        current_capacity = 0
    else:
        current_capacity = int(current_capacity)
    
    max_capacity = db.Table("sections").query(
        KeyConditionExpression=Key("id").eq(section_id),
    )

    max_capacity = max_capacity["Items"][0]["max_capacity"]
    max_capacity = int(max_capacity)

    # If current_capacity == max_capacity, then class is full.
    if current_capacity >= max_capacity:

        # Creates the waitlist if it does not exist
        createWaitlist(section_id)
        
        # get Waitlisted Count
        waitlist_count = checkWaitlistSize(section_id)

        # Check if waitlist is ful;
        if waitlist_count >= 15:
            raise HTTPException (status_code=400,detail="Waitlist is full. There are 15 students already waitlisted.")

        # get amount of classes student is waitlisted in
        num_waitlisted = checkNumberOfWaitlistEnrollments(id)
        # Raise Error if Student is Already Waitlisted in 3 Classes
        if num_waitlisted == 3:
            raise HTTPException (status_code=400,detail="Student is already waitlisted in 3 classes.")

        # Enroll Student into the class as waitlisted
        addWaitlists(section_id, id)
        position = checkWaitlistPosition(section_id, id)
        if position == None:
            position = 0
  
        return {"details": f"The class is currently full you are waitlisted at number {position}"}

    # Inserts the student into enrollments table if there is space in the class
    else:
        try:
            # Add Student to Enrollments Table
            db.Table("enrollments").put_item(
                Item=Enrollment(id, section_id, datetime.datetime.now().strftime("%m/%d/%Y"), 0).__dict__
            )
            # Increment Section Enrollment Counter
            addSectionEnrollment(section_id)

            return {"details": "Student of id " + str(id) + " sucessfully enrolled"}
        
        # Check if enroll was successful
        except:
            raise HTTPException(status_code=400,detail="Student was unable to be enrolled in section_id: " + str(section_id))
        

# # Drop Student from a Class
@router.put("/student/drop")
def drop_class(
    section_id: int, 
    id: int = Depends(validate_student_id),
    db: boto3.session.Session = Depends(get_db)
    ):

    # Check if section exists
    section_id = validate_section_id(section_id, db)

    # Check whether or not a student is enrolled in the section
    result = db.Table("enrollments").query(
        KeyConditionExpression=Key('section_id').eq(section_id) & Key('student_id').eq(id)
    )


    # Confirms that student is not enrolled in the class and is not waitlisted in the class
    if len(result["Items"]) == 0 and checkWaitlistPosition(section_id, id) == None:
        raise HTTPException(status_code=400, detail="Student is not enrolled in this class")
    elif len(result["Items"]) > 0 and result["Items"][0]["is_dropped"] == 1:
        raise HTTPException(status_code=400, detail="Student is not enrolled in this class")
    elif checkWaitlistPosition(section_id, id) != None:
        score = removeWaitlist(section_id, id)
        updateAllLastModifiedForIdsGreaterThan(section_id, score)
        deleteLastModified(section_id, id)
        return {"details":"Student# " + str(id) + " dropped from waitlist"}
    else:
        # Switch Student From is_dropped FALSE (or UNSET) to TRUE in Enrollments Table also set is_waitlisted to FALSE
        db.Table("enrollments").update_item(
            Key={
                'section_id': section_id,
                'student_id': id
            },
            UpdateExpression="SET is_dropped = :r",
            ExpressionAttributeValues={
                ":r": 1
            },
            ReturnValues="UPDATED_NEW"                                   
        )
        addSectionEnrollment(section_id, -1)
        
        # If drop is successful We want to move the first person in waitlist to enrolled if they exist
        try:
            student_to_enroll = removeAndAddWaitlist(section_id)[0]
            student_id_to_enroll = student_to_enroll[0]
            student_score_to_enroll = int(student_to_enroll[1])
            student_id_to_enroll = int(student_id_to_enroll)

            updateAllLastModifiedForIdsGreaterThan(section_id, student_score_to_enroll)
            deleteLastModified(section_id, student_id_to_enroll)

            # Add Student to Enrollments Table
            db.Table("enrollments").put_item(
                Item=Enrollment(student_id_to_enroll, section_id, datetime.datetime.now().strftime("%m/%d/%Y"), 0).__dict__
            )
            # Icrement Section Enrollment Counter
            addSectionEnrollment(section_id)

            # Get subscription of student who was just enrolled from waitlist
            subscription = getSubscription(student_id_to_enroll, str(section_id))

            if subscription:
                # Notify student that they have been enrolled in the class and are no longer on waitlist
                rabbit_manager = RabbitManager()
                callback_url = subscription.get("callback_url")
                email = subscription.get("email")
                
                if callback_url: 
                    rabbit_manager.publish_notification(subscription)

                if email:
                    rabbit_manager.publish_email(subscription)

            return {"details": "Student of id " + str(id) + " sucessfully dropped and student of id " + str(student_id_to_enroll) + " enrolled"}
        
        except:
            return {"details":"Student# " + str(id) + " dropped from " + str(section_id)}

    
    