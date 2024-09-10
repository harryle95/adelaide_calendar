import React, { useContext, useEffect, useState } from "react";
import { formatDate } from "@fullcalendar/core";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import rrulePlugin from "@fullcalendar/rrule";
import { EventContext } from "../Contexts/EventContext";

const Calendar = () => {
  const [weekendsVisible, setWeekendsVisible] = useState(true);
  // const [currentEvents, setCurrentEvents] = useState([]);
  const { displayedEvents } = useContext(EventContext);

  function handleWeekendsToggle() {
    setWeekendsVisible(!weekendsVisible);
  }

  // useEffect(() => {
  //   if (events) {
  //     setCurrentEvents(events);
  //   }
  // }, [events]);

  return (
    <div className="w-7/12 ml-auto border border-black rounded-md p-4">
      {/* <Sidebar
        weekendsVisible={weekendsVisible}
        handleWeekendsToggle={handleWeekendsToggle}
        currentEvents={currentEvents}
      /> */}
      <div className="demo-app-main">
        <FullCalendar
          plugins={[
            dayGridPlugin,
            timeGridPlugin,
            interactionPlugin,
            rrulePlugin,
          ]}
          headerToolbar={{
            left: "prev,next today",
            center: "title",
            right: "dayGridMonth,timeGridWeek,timeGridDay",
          }}
          initialView="timeGridWeek"
          editable={true}
          selectable={true}
          selectMirror={true}
          dayMaxEvents={true}
          weekends={!weekendsVisible}
          events={displayedEvents}
        />
      </div>
    </div>
  );
};

// function Sidebar({ weekendsVisible, handleWeekendsToggle, currentEvents }) {
//   return (
//     <div className="demo-app-sidebar">
//       <div className="demo-app-sidebar-section">
//         <label>
//           <input
//             type="checkbox"
//             checked={weekendsVisible}
//             onChange={handleWeekendsToggle}
//           ></input>
//           toggle weekends
//         </label>
//       </div>
//     </div>
//   );
// }

export default Calendar;
