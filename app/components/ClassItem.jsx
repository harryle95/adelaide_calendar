import { useState, useContext, useEffect } from "react";
import moment from "moment";
import { EventContext } from "../Contexts/EventContext";

const ClassItem = ({
  parent_class_nbr,
  class_nbr,
  section,
  component,
  meetings,
  isGroupChecked,
  setGroupChecked,
  numChecked,
  setNumChecked,
}) => {
  const [isChecked, setChecked] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const { modifyDisplayedEvents } = useContext(EventContext);

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
    if (numChecked === 0) {
      setGroupChecked(false);
    }
  }, [numChecked]);

  const handleOpen = () => {
    setIsOpen(!isOpen);
  };

  const handleCheckboxChange = (e) => {
    setChecked(e.target.checked);

    if (e.target.checked) {
      // modify the check state of parent component: ClassGroup
      setGroupChecked(true);
      setNumChecked((prevNumChecked) => prevNumChecked + 1);
      console.log("added 1 numcheck", numChecked);

      meetings.forEach((meeting) => {
        const [startDate, endDate] = meeting.dates.split(" - ");
        const newEvent = {
          id: class_nbr,
          groupId: parent_class_nbr,
          title: `${section} ${component}`,
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
        prevEvents.filter((event) => event.id !== class_nbr)
      );
      // modify the check state of parent component: ClassGroup
      setNumChecked((prevNumChecked) => prevNumChecked - 1);
      console.log("remove 1 numcheck", numChecked);
    }
  };
  return (
    <section>
      <div className="flex space-x-4 items-center">
        <button onClick={handleOpen}>{isOpen ? "▲" : "▼"}</button>
        <h1>Child class number: {class_nbr}</h1>
        <input
          type="checkbox"
          checked={isChecked}
          onChange={handleCheckboxChange}
        />
      </div>
      <div className={`${isOpen ? "block ml-7" : "hidden"}`}>
        {meetings.map((meeting, index) => {
          return (
            <h2 key={index}>
              {meeting.days} {meeting.start_time}-{meeting.end_time}{" "}
              {meeting.location} {meeting.dates}
            </h2>
          );
        })}
      </div>
    </section>
  );
};

export default ClassItem;
