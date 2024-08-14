import React from "react";
import Image from "next/image";

const menuMap: Record<string, string> = {
  Home: "/",
  Schedule: "/schedule",
  Courses: "/course",
  Degree: "/degree",
};

const NavigationMenu = React.memo(() => {
  const linkClassName = "flex h-full items-center hover:bg-slate-600 px-2";
  return (
    <div className="flex h-16 w-full bg-slate-900 px-5 text-lg font-bold text-white">
      <div className="flex flex-grow items-center gap-x-4">
        <Image
          src="/adelaide_logo.png"
          width={50}
          height={50}
          alt="Adelaide University Logo"
        />
        {Object.entries(menuMap).map(([title, ref]) => (
          <a href={ref} key={title} className={linkClassName}>
            {title}
          </a>
        ))}
      </div>
      <div>
        <a href="#" className={linkClassName}>
          Login
        </a>
      </div>
    </div>
  );
});

NavigationMenu.displayName = "NavigationMenu";

export { NavigationMenu };
