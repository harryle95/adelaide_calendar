import { useState } from "react";
import HelpTooltip from "./HelpTooltip";
import { MagnifyingGlassIcon } from "@radix-ui/react-icons";
import AdvancedSearchDialog from "./AdvancedSearchDialog";
import axios from "axios";
import CourseDropdown from "./CourseDropdown";

const SearchBox = () => {
  const [searchedCourses, setSearchedCourses] = useState([{}]);

  // Create "local" useState
  const [inputValue, setInputValue] = useState("");

  const apiUrl = "/api/course-planner-query/v1/";

  const params = {
    target: "/system/COURSE_SEARCH/queryx",
    virtual: "Y",
    year: "2024",
    subject: "CHEM",
    pagenbr: "1",
    pagesize: "25",
  };

  const buildFullQueryUrl = (value) => {
    const fullQueryUrl = `${apiUrl}?target=${params.target}&virtual=${params.virtual}&year=${params.year}&subject=${value}&pagenbr=${params.pagenbr}&pagesize=${params.pagesize}`;
    return fullQueryUrl;
  };

  const handleInputChange = (e) => {
    const value = e.target.value.toUpperCase();
    setInputValue(value);
    fetchData(value)
      .then((response) => {
        if (value && response && response.data) {
          const courseList = response.data.data.query.rows;
          setSearchedCourses(courseList);
        } else {
          setSearchedCourses([{}]);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const fetchData = async (value) => {
    const response = await axios.get(buildFullQueryUrl(value));
    // const response = await axios.get("https://courseplanner-api.adelaide.edu.au/api/course-planner-query/v1/?target=/system/COURSE_SEARCH/queryx&virtual=Y&year=2024&course_title=MATH&pagenbr=1&pagesize=5");
    return response;
  };

  return (
    <section className="flex flex-col w-1/5">
      <div className="border border-black rounded-md py-2 pl-4">
        <div className="flex items-center mb-1">
          <header className="mr-1 font-bold">Add courses</header>{" "}
          <HelpTooltip />
        </div>
        <div className="relative flex">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 transform text-black" />
          {/* Implement loader here */}
          <form>
            <input
              type="text"
              onChange={handleInputChange}
              placeholder="MATH3012..."
              className="rounded-md border border-black py-1 pl-10 pr-4 focus:outline-none focus:ring-2"
            />
          </form>
          <AdvancedSearchDialog />
        </div>
      </div>
      {inputValue && <CourseDropdown searchedCourses={searchedCourses} />}
    </section>
  );
};

export default SearchBox;
