import React from "react";

const menuMap: Record<string, string> = {
  Home: "/",
  Schedule: "/schedule",
  Courses: "/course",
  Degree: "/degree",
};

const NavigationMenu = React.memo(() => {
  return (
    <div className="flex h-16 w-full bg-slate-900 px-5">
      <div className="flex flex-grow items-center gap-x-4 text-lg font-bold text-white">
        {Object.entries(menuMap).map(([title, ref]) => (
          <div
            key={title}
            className="flex h-full items-center hover:bg-slate-600"
          >
            <a href={ref}>{title}</a>
          </div>
        ))}
      </div>
    </div>
  );
});

NavigationMenu.displayName = "NavigationMenu";

export { NavigationMenu };
