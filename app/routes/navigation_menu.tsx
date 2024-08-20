import React from "react";
import { NavLink } from "react-router-dom";

const menuMap: Record<string, string> = {
  Home: "/",
  Schedule: "/schedule",
  Courses: "/course",
  Degree: "/degree",
};

const NavigationMenu = React.memo(() => {
  const linkClassName = ({ isActive }: { isActive: boolean }) =>
    isActive
      ? "flex h-full items-center bg-slate-600 px-4"
      : "flex h-full items-center hover:bg-slate-600 px-4";
  return (
    <div className="flex h-16 w-full bg-slate-900 px-5 text-lg font-bold text-white">
      <div className="flex flex-grow items-center">
        <img
          src="/vite.svg"
          alt="Adelaide University Logo"
          loading="lazy"
          className="h-full w-auto p-2"
        />
        {Object.entries(menuMap).map(([title, ref]) => (
          <NavLink to={ref} key={title} className={linkClassName}>
            {title}
          </NavLink>
        ))}
      </div>
      <div>
        <NavLink to="/auth" className={linkClassName}>
          Login
        </NavLink>
      </div>
    </div>
  );
});

NavigationMenu.displayName = "NavigationMenu";

export { NavigationMenu };
