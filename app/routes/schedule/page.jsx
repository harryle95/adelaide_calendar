import { useState } from "react";
import SearchBox from "../../components/SearchBox";
import CourseSelectionPanel from "../../components/CourseSelectionPanel";
import Calendar from "../../components/Calendar";
import { CacheContext } from "../../Contexts/CacheContext";
import { CourseContext } from "../../Contexts/CourseContext";
import { EventContext } from "../../Contexts/EventContext";

export default function Page() {
  const [cache, setCache] = useState({});
  const [selectedCourses, setSelectedCourses] = useState({});
  const [displayedEvents, modifyDisplayedEvents] = useState([]);
  return (
    <CacheContext.Provider value={{cache, setCache}}>
      <CourseContext.Provider value={{selectedCourses, setSelectedCourses}}>
        <EventContext.Provider value={{displayedEvents, modifyDisplayedEvents}}>
      <section>
        <div className="ml-3 mt-3 space-y-4">
          <SearchBox />
          <CourseSelectionPanel />
        </div>
        <div className="mt-5 w-6/12 ">
          <Calendar />
        </div>
      </section>
      </EventContext.Provider>
      </CourseContext.Provider>
    </CacheContext.Provider>
  );
}
