"use client";
import React from "react";
import HelpTooltip from "./helptooltip";
import { MagnifyingGlassIcon } from "@radix-ui/react-icons";
import AdvancedSearchDialog from "./advanced-search-dialog";
import AdvancedSearchForm from "./advanced-search-form";

const SearchBox = () => {
  return (
    <div className="flex flex-col">
      <div className="flex items-center my-1">
        <span className="mr-1">Add courses</span> <HelpTooltip />
      </div>
      <div className="relative flex items-center">
        <MagnifyingGlassIcon className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 transform text-black" />
        <input
          type="text"
          placeholder="MATH3012..."
          className="rounded-md border border-black py-1 pl-10 pr-4 focus:outline-none focus:ring-2"
        />
        <AdvancedSearchDialog/>
      </div>
    </div>
  );
};

export default SearchBox;
