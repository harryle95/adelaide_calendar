import { useContext } from "react";
import { CourseContext } from "../Contexts/CourseContext";
import CourseCard from "./CourseCard";

const CourseSelectionPanel = () => {
  const { selectedCourses } = useContext(CourseContext);

  return (
    <div className="space-y-2">
      {Object.keys(selectedCourses).map((parentClassNbr, index) => {
        return (
          <CourseCard
            key={index}
            // class_nbr={selectedCourses[parentClassNbr].info.class_nbr}
            class_nbr={parentClassNbr}
            subject={selectedCourses[parentClassNbr].info.subject}
            catalog_nbr={selectedCourses[parentClassNbr].info.catalog_nbr}
            title={selectedCourses[parentClassNbr].info.title}
            crseid={selectedCourses[parentClassNbr].info.crseid}
            term={selectedCourses[parentClassNbr].info.term}
            groupList={selectedCourses[parentClassNbr].groupList}
          />
        );
      })}
    </div>
  );
};

export default CourseSelectionPanel;
