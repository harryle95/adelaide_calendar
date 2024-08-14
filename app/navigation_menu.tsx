"use client";
import React from "react";
import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";

const menuMap: Record<string, string> = {
  Home: "/",
  Schedule: "/schedule",
  Courses: "/course",
  Degree: "/degree",
};

const NavigationMenu = React.memo(() => {
  const pathName = usePathname();
  const linkClassName =
    "flex h-full items-center hover:bg-slate-600 px-2 data-[state=active]:bg-slate-600";
  return (
    <div className="flex h-16 w-full bg-slate-900 px-5 text-lg font-bold text-white">
      <div className="flex flex-grow items-center gap-x-4">
        <Image
          src="/adelaide_logo.png"
          width="0"
          height="0"
          sizes="100vh"
          alt="Adelaide University Logo"
          loading="lazy"
          className="h-full w-auto"
        />
        {Object.entries(menuMap).map(([title, ref]) => (
          <Link
            href={ref}
            key={title}
            className={linkClassName}
            data-state={
              pathName.split("/")[1] === ref.split("/")[1]
                ? "active"
                : "inactive"
            }
          >
            {title}
          </Link>
        ))}
      </div>
      <div>
        <Link
          href="/auth"
          className={linkClassName}
          data-state={pathName === "/auth" ? "active" : "inactive"}
        >
          Login
        </Link>
      </div>
    </div>
  );
});

NavigationMenu.displayName = "NavigationMenu";

export { NavigationMenu };
