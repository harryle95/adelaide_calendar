import { useContext, useState } from "react";
import ClassItem from "./ClassItem";
import { EventContext } from "../Contexts/EventContext";

const ClassGroup = ({ parent_class_nbr, group }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isGroupChecked, setGroupChecked] = useState(false);
  const [numOfItemsChecked, setNumOfItemsChecked] = useState(0);
  const { modifyDisplayedEvents } = useContext(EventContext);

  const handleOpen = () => {
    setIsOpen(!isOpen);
  };

  const handleCheckboxChange = (e) => {
    setGroupChecked(e.target.checked);
    setNumOfItemsChecked(0);
    modifyDisplayedEvents((prevEvents) =>
      prevEvents.filter((prevEvent) => prevEvent.groupId !== parent_class_nbr)
    );
  };

  const modifyGroupChecked = setGroupChecked;

  const modifyNumOfItemsChecked = setNumOfItemsChecked;

  return (
    <section className="space-y-2 pl-6">
      <div className="flex items-center bg-slate-200">
        <button onClick={handleOpen}>{isOpen ? "▲" : "▼"}</button>
        <header className="ml-2 "> {group.type} </header>
        <input
          className="ml-auto"
          type="checkbox"
          checked={isGroupChecked}
          onChange={handleCheckboxChange}
          disabled={!isGroupChecked}
        />
      </div>
      <div className={`${isOpen ? "block space-y-2" : "hidden"}`}>
        {group.classes.map((eachClass, index) => {
          return (
            <div key={index}>
              <ClassItem
                parent_class_nbr={parent_class_nbr}
                class_nbr={eachClass.class_nbr}
                section={eachClass.section}
                component={eachClass.component}
                meetings={eachClass.meetings}
                isGroupChecked={isGroupChecked}
                modifyGroupChecked={modifyGroupChecked}
                numOfItemsChecked={numOfItemsChecked}
                modifyNumOfItemsChecked={modifyNumOfItemsChecked}
              />
            </div>
          );
        })}
      </div>
    </section>
  );
};

export default ClassGroup;
