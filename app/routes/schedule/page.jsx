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
    <CacheContext.Provider value={{ cache, setCache }}>
      <CourseContext.Provider value={{ selectedCourses, setSelectedCourses }}>
        <EventContext.Provider
          value={{ displayedEvents, modifyDisplayedEvents }}
        >
          <section>
            <div className="ml-4 mt-4 space-y-4">
              <SearchBox />
            </div>
            <div className="flex flex-wrap mx-4 mt-4 mb-32">
              <CourseSelectionPanel />
              <Calendar />
            </div>
          </section>
        </EventContext.Provider>
      </CourseContext.Provider>
    </CacheContext.Provider>
  );
}
