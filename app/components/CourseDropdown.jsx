import { useContext, useEffect } from "react";
import { CourseContext } from "../Contexts/CourseContext";
import axios from "axios";
import { CacheContext } from "../Contexts/CacheContext";

const CourseDropdown = ({ searchedCourses }) => {
  const { cache, setCache } = useContext(CacheContext);

  const { selectedCourses, setSelectedCourses } = useContext(CourseContext);

  const apiUrl = "/api/course-planner-query/v1/";

  const params = {
    target: "/system/COURSE_CLASS_LIST/queryx",
    virtual: "Y",
    offer: "1",
    session: "1",
  };

  const buildFullQueryUrl = (crseid, term) => {
    const fullQueryUrl = `${apiUrl}?target=${params.target}&virtual=${params.virtual}&crseid=${crseid}&offer=${params.offer}&term=${term}&session=${params.session}`;
    return fullQueryUrl;
  };

  const fetchData = async (crseid, term) => {
    const response = await axios.get(buildFullQueryUrl(crseid, term));
    return response;
  };

  const handleClick = (course) => {
    if (!selectedCourses[course.CLASS_NBR]) {
      if (cache[course.CLASS_NBR]) {
        console.log("Already in cache!");
        setSelectedCourses((prevCourses) => ({
          ...prevCourses,
          [course.CLASS_NBR]: cache[course.CLASS_NBR],
        }));
      } else {
        fetchData(course.COURSE_ID, course.TERM)
          .then((response) => {
            const newCache = { ...cache };
            newCache[course.CLASS_NBR] = {
              info: {
                class_nbr: course.CLASS_NBR,
                subject: course.SUBJECT,
                catalog_nbr: course.CATALOG_NBR,
                title: course.COURSE_TITLE,
                crseid: course.COURSE_ID,
                term: course.TERM,
              },
              groupList: [],
            };

            const groupsArray = response.data.data.query.rows[0].groups;
            groupsArray.forEach((group) => {
              newCache[course.CLASS_NBR].groupList.push(group);
            });

            setCache(newCache);
            setSelectedCourses((prevCourses) => ({
              ...prevCourses,
              [course.CLASS_NBR]: newCache[course.CLASS_NBR],
            }));

            console.log(
              "Data added to cache for class number:",
              course.CLASS_NBR
            );
            console.log(newCache[course.CLASS_NBR]);
          })
          .catch((error) => console.log(error));
      }
    }
  };

  return (
    <section className=" bg-white flex flex-col shadow-2xl max-h-40 overflow-y-scroll">
      {searchedCourses.map((course, index) => {
        return (
          <div key={index} className="hover:bg-slate-200 pl-5 pt-0.5">
            <button onClick={() => handleClick(course)}>
              {course.SUBJECT} {course.CATALOG_NBR} {course.CLASS_NBR}
            </button>
          </div>
        );
      })}
    </section>
  );
};

export default CourseDropdown;
