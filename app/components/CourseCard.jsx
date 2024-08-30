import { useContext, useState, useRef } from "react";
import { CourseContext } from "../Contexts/CourseContext";
import { TrashIcon } from "@radix-ui/react-icons";
import ClassGroup from "./ClassGroup";
import { EventContext } from "../Contexts/EventContext";

const CourseCard = (props) => {
  const { class_nbr, subject, catalog_nbr, title, crseid, term, groupList } =
    props;
  const { setSelectedCourses } = useContext(CourseContext);
  const { modifyDisplayedEvents } = useContext(EventContext);
  const [isOpen, setIsOpen] = useState(false);

  const handleClick = () => {
    // remove from selectedCourses
    setSelectedCourses((prevCourses) => {
      const { [class_nbr]: _, ...rest } = prevCourses;
      return rest;
    });

    // remove from displayedEvents
    // when class_nbr === event.groupId
    modifyDisplayedEvents((prevEvents) =>
      prevEvents.filter((event) => event.groupId !== class_nbr)
    );
  };

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  // Not sure why this does not work
  //   const cache = useRef({});

  return (
    <section>
      <div className="flex space-x-4 items-center">
        <button onClick={handleToggle}>{isOpen ? "▲" : "▼"}</button>
        <header>
          {subject} {catalog_nbr} - {title} - Parent class number: {class_nbr}
        </header>
        <button
          onClick={handleClick}
          className="border border-black rounded-md p-0.5"
        >
          <TrashIcon />
        </button>
      </div>
      <div
        className={`${isOpen ? "block ml-7" : "hidden"}`}
      >
        {groupList.map((group, index) => (
          <ClassGroup key={index} parent_class_nbr={class_nbr} group={group} />
        ))}
      </div>
    </section>
  );
};

export default CourseCard;
