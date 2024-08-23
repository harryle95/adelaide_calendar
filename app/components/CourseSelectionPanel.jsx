import { useContext } from "react";
import { CourseContext } from "../Contexts/CourseContext";

const CourseSelectionPanel = (props) => {
  const { setDisplayedCourses } = props;
  const { selectedCourses, setSelectedCourses } = useContext(CourseContext);
  return (
    <div>
      {selectedCourses.map((course, index) => {
        return (
          <div key={index}>
            {course.SUBJECT} {course.CATALOG_NBR} {course.CLASS_NBR} {course.COURSE_TITLE}
          </div>
        );
      })}
    </div>
  );
};

export default CourseSelectionPanel;
