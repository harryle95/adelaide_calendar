import { useState } from "react";
import HelpTooltip from "./HelpTooltip";
import { MagnifyingGlassIcon } from "@radix-ui/react-icons";
import AdvancedSearchDialog from "./AdvancedSearchDialog";
import axios from "axios";
import CourseDropdown from "./CourseDropdown";

// This is the mock/placeholder array for data coming from the backend API
// Create an array of objects
const courses = ["MATH101", "MATH102", "MATH103", "PHYS101", "PHYS102"];

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
    pagesize: "10",
  };

  const buildFullQueryUrl = (value) => {
    const fullQueryUrl = `${apiUrl}?target=${params.target}&virtual=${params.virtual}&year=${params.year}&subject=${value}&pagenbr=${params.pagenbr}&pagesize=${params.pagesize}`;
    return fullQueryUrl;
  };

  const handleInputChange = (e) => {
    const value = (e.target.value).toUpperCase();
    setInputValue(value);
    fetchData(value)
      .then((response) => {
        if (value && response && response.data) {
          setSearchedCourses(response.data.data.query.rows);
        } else {
          setSearchedCourses([{}]);
        }
        console.log(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const fetchData = async (value) => {
    // const response = await axios.get(buildFullQueryUrl(value));
    const response = await axios.get("https://courseplanner-api.adelaide.edu.au/api/course-planner-query/v1/?target=/system/COURSE_SEARCH/queryx&virtual=Y&year=2024&course_title=MATH&pagenbr=1&pagesize=5");
    return response;
  };

  return (
    <div className="flex flex-col w-1/5 ml-3 mt-3">
      <div className="border border-black rounded-md py-1.5">
        <div className="flex items-center ml-4 mb-1">
          <span className="mr-1 font-bold">Add courses</span> <HelpTooltip />
        </div>
        <div className="relative flex ml-4">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 transform text-black" />
          <input
            type="search"
            onChange={handleInputChange}
            placeholder="MATH3012..."
            className="rounded-md border border-black py-1 pl-10 pr-4 focus:outline-none focus:ring-2"
          />
          <div id="search-spinner" aria-hidden hidden={true} />
          <div className="sr-only" aria-live="polite"></div>
          <AdvancedSearchDialog />
        </div>
      </div>
      <div className="w-full mt-3">
        {inputValue ? (
          <CourseDropdown searchedCourses={searchedCourses} />
        ) : (
          <></>
        )}
      </div>
    </div>
  );
};

export default SearchBox;
