from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from src.db.models.course import Course 
from src.db.models.group import Group 
from src.db.models.classinfo import ClassInfo
from src.db.models.meeting import Meeting
import json

# Helper function to convert course object into a dictionary
def course_to_dict(course):
    return {
        "course_id": course.course_id,
        "course_offer_nbr": course.course_offer_nbr,
        "year": course.year,
        "term": course.term,
        "term_descr": course.term_descr,
        "subject": course.subject,
        "catalogue_nbr": course.catalogue_nbr,
        "acad_career": course.acad_career,
        "acad_career_descr": course.acad_career_descr,
        "course_title": course.course_title,
        "units": course.units,
        "campus": course.campus,
        "class_nbr": course.class_nbr,
        "groups": [
            {
                "group_id": group.group_id,
                "group_type": group.group_type,
                "classes": [
                    {
                        "class_nbr": cls.class_nbr,
                        "section": cls.section,
                        "size": cls.size,
                        "enrolled": cls.enrolled,
                        "available": cls.available,
                        "institution": cls.institution,
                        "component": cls.component,
                        "meetings": [
                            {
                                "meeting_id": meeting.meeting_id,
                                "dates": meeting.dates,
                                "days": meeting.days,
                                "start_time": str(meeting.start_time),
                                "end_time": str(meeting.end_time),
                                "location": meeting.location
                            }
                            for meeting in cls.meetings
                        ]
                    }
                    for cls in group.classes
                ]
            }
            for group in course.groups
        ]
    }



# SEARCH
def search_course_by_id(engine, course_id: str):
    stmt = select(Course).options(
        joinedload(Course.groups)
        .joinedload(Group.classes)
        .joinedload(ClassInfo.meetings)
    ).where(Course.course_id == course_id)
    
    with Session(engine) as session:
        result = session.execute(stmt).scalars().first()
        if result:
            json_data = json.dumps(course_to_dict(result))
            return json_data
        else:
            return None

def search_course_by_title(engine, course_title: str):
    stmt = select(Course).options(
        joinedload(Course.groups)
        .joinedload(Group.classes)
        .joinedload(ClassInfo.meetings)
    ).where(Course.course_title == course_title)
    
    with Session(engine) as session:
        result = session.execute(stmt).scalars().first()
        if result:
            json_data = json.dumps(course_to_dict(result))
            return json_data
        else:
            return None

def search_course_by_number(engine, catalogue_nbr: str):
    stmt = select(Course).options(
        joinedload(Course.groups)
        .joinedload(Group.classes)
        .joinedload(ClassInfo.meetings)
    ).where(Course.catalogue_nbr == catalogue_nbr)
    
    with Session(engine) as session:
        result = session.execute(stmt).scalars().first()
        if result:
            json_data = json.dumps(course_to_dict(result))
            return json_data
        else:
            return None
        
# INSERT
def insert_course(engine, course_data: dict):
    new_course = Course(**course_data)
    with Session(engine) as session:
        session.add(new_course)
        session.commit()

def insert_group_for_course(engine, group_data: dict, course_id: str):
    with Session(engine) as session:
        # Find the course by its course_id
        course = session.query(Course).filter(Course.course_id == course_id).first()

        if course:
            existing_group = session.query(Group).filter(Group.course_id == course_id,
                                                         Group.group_type == group_data["group_type"]).first()
            if not existing_group:
                # Create a new Group object using dictionary unpacking
                new_group = Group(**group_data)
                # Associate the group with the course
                new_group.course = course
                session.add(new_group)
                session.commit()
                print("Group inserted successfully.")
            else:
                print("Groups for course ID exist already.")
        else:
            print(f"Course with id {course_id} not found.")
        
def insert_classinfo_for_group(engine, classinfo_data: dict, group_id: int):
    with Session(engine) as session:
        # Find the group by its group_id
        group = session.query(Group).filter(Group.group_id == group_id).first()

        if group:
            existing_class = session.query(ClassInfo).filter(
                ClassInfo.class_nbr == classinfo_data['class_nbr'],
                ClassInfo.group_id == group_id
            ).first()
            if not existing_class:
                # Create a new ClassInfo object using dictionary unpacking
                new_classinfo = ClassInfo(**classinfo_data)
                # Associate the classinfo with the group
                group.classes.append(new_classinfo)

                session.add(new_classinfo)
                session.commit()
                print("ClassInfo inserted successfully.")
            else:
                print("Class exists already.")
        else:
            print("Group not found.")


def insert_meeting_for_class(engine, meeting_data: dict, class_nbr: int):
    with Session(engine) as session:
        # Find the classinfo by its class_nbr
        classinfo = session.query(ClassInfo).filter(ClassInfo.class_nbr == class_nbr).first()

        if classinfo:
            # Create a new Meeting object using dictionary unpacking
            new_meeting = Meeting(**meeting_data)
            # Associate the meeting with the classinfo
            classinfo.meetings.append(new_meeting)

            session.add(new_meeting)
            session.commit()
            return "Meeting inserted successfully."
        else:
            return "ClassInfo not found."


# DELETE

def empty_groups_table(engine):
    with Session(engine) as session:
        # Delete all rows from the Groups table
        session.query(Group).delete()
        session.commit()
        print("Groups table emptied successfully.")

def empty_classInfo_table(engine):
    with Session(engine) as session:
        # Delete all rows from the Groups table
        session.query(ClassInfo).delete()
        session.commit()
        print("ClassInfo table emptied successfully.")