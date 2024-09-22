import { useState, useContext, useEffect } from "react";
import moment from "moment";
import { EventContext } from "../Contexts/EventContext";
import { CourseContext } from "../Contexts/CourseContext";

const ClassItem = ({
  parent_class_nbr,
  class_nbr,
  section,
  component,
  meetings,
  isGroupChecked,
  modifyGroupChecked,
  numOfItemsChecked,
  modifyNumOfItemsChecked,
}) => {
  const [isChecked, setChecked] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const { modifyDisplayedEvents } = useContext(EventContext);
  const { selectedCourses } = useContext(CourseContext);

  const dayDict = {
    Monday: "mo",
    Tuesday: "tu",
    Wednesday: "we",
    Thursday: "th",
    Friday: "fr",
  };

  useEffect(() => {
    if (!isGroupChecked) {
      setChecked(false);
    }
  }, [isGroupChecked]);

  useEffect(() => {
    if (numOfItemsChecked === 0) {
      modifyGroupChecked(false);
    }
  }, [numOfItemsChecked]);

  const handleOpen = () => {
    setIsOpen(!isOpen);
  };

  const handleCheckboxChange = (e) => {
    setChecked(e.target.checked);

    if (e.target.checked) {
      // modify the check state of parent component: ClassGroup
      modifyGroupChecked(true);
      modifyNumOfItemsChecked((prev) => prev + 1);
      // modify the check state of parent component: ClassGroup

      meetings.forEach((meeting) => {
        const [startDate, endDate] = meeting.dates.split(" - ");

        // create a newEvent object to add to calendar
        const newEvent = {
          id: class_nbr,
          groupId: parent_class_nbr,
          title: `${selectedCourses[parent_class_nbr].info.subject}
          ${selectedCourses[parent_class_nbr].info.catalog_nbr}
          ${section} ${class_nbr} ${component}`,
          rrule: {
            freq: "weekly",
            byweekday: dayDict[meeting.days],
            dtstart:
              moment(startDate, "DD MMM").year(2024).format("YYYY-MM-DD") +
              "T12:00:00",
            until: moment(endDate, "DD MMM").year(2024).format("YYYY-MM-DD"),
          },
          startTime: moment(meeting.start_time, "hA").format("HH:mm:ss"),
          endTime: moment(meeting.end_time, "hA").format("HH:mm:ss"),
          description: meeting.location,
        };
        modifyDisplayedEvents((prevEvents) => [...prevEvents, newEvent]);
      });
    } else {
      // if unchecked, remove the corresponding event from the list
      modifyDisplayedEvents((prevEvents) =>
        prevEvents.filter((prevEvent) => prevEvent.id !== class_nbr)
      );
      // modify the check state of parent component: ClassGroup
      modifyNumOfItemsChecked((prev) => prev - 1);
    }
  };

  return (
    <section className="space-y-2">
      <div className="flex items-center pl-6 bg-slate-200">
        <button onClick={handleOpen}>{isOpen ? "▲" : "▼"}</button>
        <header className="ml-2">Child class number: {class_nbr}</header>
        <input className="ml-auto"
          type="checkbox"
          checked={isChecked}
          onChange={handleCheckboxChange}
        />
      </div>
      <div className={`${isOpen ? "block px-12 space-y-4" : "hidden"}`}>
        {meetings.map((meeting, index) => {
          return (
            <p className="bg-slate-200" key={index}>
              {meeting.days} {meeting.start_time}-{meeting.end_time}{" "}
              {meeting.location} {meeting.dates}
            </p>
          );
        })}
      </div>
    </section>
  );
};

export default ClassItem;
