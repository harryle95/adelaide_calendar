import { useContext } from "react";
import { CourseContext } from "../Contexts/CourseContext";

const CourseDropdown = (props) => {
  const { searchedCourses } = props;

  const { selectedCourses, setSelectedCourses } = useContext(CourseContext);

  return (
    <section className=" bg-white flex flex-col shadow-2xl max-h-40 overflow-y-scroll">
      {searchedCourses.map((course, index) => {
        return (
          <div key={index} className="hover:bg-slate-200 pl-5 pt-0.5">
            <button
              onClick={() => {
                const newCourse = course;
                const isCourseAlreadySelected = selectedCourses.some(
                  (aCourse) => aCourse.CLASS_NBR === newCourse.CLASS_NBR
                );
                if (!isCourseAlreadySelected) {
                  setSelectedCourses((prevCourseList) => [
                    ...prevCourseList,
                    newCourse,
                  ]);
                }
              }}
            >
              {course.SUBJECT} {course.CATALOG_NBR} {course.CLASS_NBR}
            </button>
          </div>
        );
      })}
    </section>
  );
};

export default CourseDropdown;
