import { useState } from "react";
import SearchBox from "../../components/SearchBox";
import CourseSelectionPanel from "../../components/CourseSelectionPanel";
import Calendar from "../../components/Calendar";
import { CourseContext } from "../../Contexts/CourseContext";

export default function Page() {
  const [selectedCourses, setSelectedCourses] = useState([{}]);
  const [displayedCourses, setDisplayedCourses] = useState([{}]);
  return (
    <CourseContext.Provider value={{ selectedCourses, setSelectedCourses }}>
      <div className="space-x-1">
        <div>
          <SearchBox />
          <CourseSelectionPanel setDisplayedCourses={setDisplayedCourses} />
        </div>
        <div className="mt-5 w-6/12 ">
          <Calendar />
        </div>
      </div>
    </CourseContext.Provider>
  );
}
