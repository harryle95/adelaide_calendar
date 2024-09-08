import React, { useState } from "react";

interface FormValues {
  courseTitle: string;
  subjectArea: string;
}

const subjectAreas = [
  "Mathematics",
  "Computer Science",
  "Engineering",
  "Physics",
  "Chemistry",
  "Biology",
];

const AdvancedSearchForm = () => {
  const [formValues, setFormValues] = useState<FormValues>({
    courseTitle: "",
    subjectArea: subjectAreas[0], // Default value
  });

  const handleChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = event.target;
    setFormValues((prevValues) => ({
      ...prevValues,
      [name]: value,
    }));
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    console.log("Form submitted:", formValues);
    // You can handle form submission here, e.g., send data to an API
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="mx-auto max-w-lg rounded-md border p-4 shadow-md"
    >
      <div className="mb-4">
        <label
          htmlFor="courseTitle"
          className="block text-sm font-medium text-gray-700"
        >
          Course Title
        </label>
        <input
          type="text"
          id="courseTitle"
          name="courseTitle"
          value={formValues.courseTitle}
          onChange={handleChange}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
          required
        />
      </div>

      <div className="mb-4">
        <label
          htmlFor="subjectArea"
          className="block text-sm font-medium text-gray-700"
        >
          Subject Area
        </label>
        <select
          id="subjectArea"
          name="subjectArea"
          value={formValues.subjectArea}
          onChange={handleChange}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
          required
        >
          {subjectAreas.map((area, index) => (
            <option key={index} value={area}>
              {area}
            </option>
          ))}
        </select>
      </div>

      <div className="flex space-x-20">
        <button
          type="submit"
          className="w-full rounded-md bg-indigo-600 px-4 py-2 font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
          Search
        </button>
        <button
          type="submit"
          className="w-full rounded-md bg-indigo-600 px-4 py-2 font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
          Reset
        </button>
      </div>
    </form>
  );
};

export default AdvancedSearchForm;
