import asyncio
from src.controller.proxy.services import ProxyQueryService
import json
from src.db.db_services import insert_course



if __name__ == "__main__":

    # GET ALL SUBJECTS
    subjects_data = asyncio.run(ProxyQueryService.subjects())
    print("TOTAL SUBJECTS: ", len(subjects_data))

    '''
    Searching for all courses by year (2024 for now) returns a list of 4765 courses.
    a page can have max 100 courses
    So max pages = 48
    '''
    course_list = []
    for page in range(1,48):
        t = asyncio.run(ProxyQueryService.course(subject_areas='ABORIG'))
        print("PAGE ", page)
        for search_bj in t:
            print(f"{search_bj.CATALOG_NBR} \t\t{search_bj.COURSE_TITLE} ") 
    # for page in range(1,3):
        # page_list = asyncio.run(ProxyQueryService.course(year=2024, page_number=page, page_size=100))
        # print(asyncio.run(ProxyQueryService.course(year=2024, subject_areas='ABORIG', page_number=page, page_size=100)))
        # print(f"Page {page} has {len(page_list)} courses")
        # course_list = course_list + page_list # type: ignore
    # print("COURSE_LIST SIZE: ", len(course_list))



    # print(asyncio.run(ProxyQueryService.course(subject_areas='GERM')))
    # GET ALL COURSES PER SUBJECT: match the course_title with SUBJECT (subject_area doesn't work)

        # course_list = asyncio.run(ProxyQueryService.course(subject_areas=subject.SUBJECT, page_size=25))
        # print(f"SUBJECT: {subject.SUBJECT} has \t\tCOURSES:  {len(course_list)} ")
        # for course in course_list:
        #     print(course)
        #     print('\n')
        #     pass
    




























''' 
    # course id for testing: 
    
    COURSE_ID = '111459'
    COURSE_OFFER_NUMBER = '1'
    TERM = '4420'

    # This provides extra info for a course - don't need it for the database
    course_details = asyncio.run(ProxyQueryService.course_detail(course_id=COURSE_ID, term=TERM, course_offer_number=COURSE_OFFER_NUMBER))
    print(crs)
    # print(course_details)

    # fetches the group which has a list of classes and each class has a list of meetings
    course_class_details = asyncio.run(ProxyQueryService.course_class_list(course_id=COURSE_ID, 
                                                                           course_offer_number=int(COURSE_OFFER_NUMBER),
                                                                           term=int(TERM),
                                                                           ))
    print("Classses:\n")
    # print(course_class_details)
    for group_obj in course_class_details:
        print("GROUP TYPE: ", group_obj.type)
        for crs_class_dict in group_obj.classes:
            print("\tCLASS")
            meetings = crs_class_dict["meetings"]
            # print(type(crs_class_dict))
            # del crs_class.meetings
            print(f"\t{json.dumps(crs_class_dict, indent=3)}")
            print("\t\tMEETINGS")
            for meeting in meetings:
                print(f"\t\t{json.dumps(meeting, indent=3)}")

'''


'''
 # get all camps provided by uni
    campus_data = asyncio.run(ProxyQueryService.campus())
    for camp in campus_data:
        # print(camp)
        # print()
        pass
        

    # Get all terms in uni (sems, trims, electives, summer, winter, teaching period,...)
    term_data = asyncio.run(ProxyQueryService.term())
    for term in term_data:
        # print(type(term))
        # print(term)
        # print()
        pass
        
   # get all academic careers provided by uni
    careers_data = asyncio.run(ProxyQueryService.academic_career())
    for career in careers_data:
        # print(career)
        pass

'''

# crs =     '''
#     CourseSearch(ACAD_CAREER='UGRD', 
#                 ACAD_CAREER_DESCR='Undergraduate', 
#                 CAMPUS='North Terrace', 
#                 CATALOG_NBR='1001', 
#                 CLASS_NBR=23781, 
#                 COURSE_ID='111459', 
#                 COURSE_OFFER_NBR=1, 
#                 COURSE_TITLE='Crafting Careers', 
#                 SUBJECT='ABLEINT', 
#                 YEAR='2024', 
#                 TERM='4420', 
#                 TERM_DESCR='Semester 2', 
#                 UNITS=3)
#     '''