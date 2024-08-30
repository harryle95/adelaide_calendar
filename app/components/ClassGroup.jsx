import { useState } from "react";
import ClassItem from "./ClassItem";

const ClassGroup = ({ parent_class_nbr, group }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isChecked, setChecked] = useState(false);
  const [numChecked, setNumChecked] = useState(0);

  const handleOpen = () => {
    setIsOpen(!isOpen);
  };

  const handleCheckboxChange = (e) => {
    setChecked(e.target.checked);
    setNumChecked(0);
  }

  return (
    <section>
      <div className="flex space-x-4 items-center">
        <button onClick={handleOpen}>{isOpen ? "▲" : "▼"}</button>
        <header> {group.type} </header>
        <input
          type="checkbox"
          checked={isChecked}
          onChange={handleCheckboxChange}
          disabled={!isChecked}
        />
      </div>
      <div className={`${isOpen ? "block ml-7" : "hidden"}`}>
        {group.classes.map((eachClass, index) => {
          return (
            <ClassItem
              key={index}
              parent_class_nbr={parent_class_nbr}
              class_nbr={eachClass.class_nbr}
              section={eachClass.section}
              component={eachClass.component}
              meetings={eachClass.meetings}
              isGroupChecked={isChecked}
              setGroupChecked={setChecked}
              numChecked={numChecked}
              setNumChecked={setNumChecked}
            />
          );
        })}
      </div>
    </section>
  );
};

export default ClassGroup;
