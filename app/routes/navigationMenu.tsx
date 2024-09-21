import React from "react";
import { Link, NavLink, useSubmit } from "react-router-dom";
import { Avatar } from "./components/avatar";
import { useAuthContext, type SCHEMA } from "../service";
import "./dropDownStyle.css";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import { ExitIcon, PersonIcon } from "@radix-ui/react-icons";

const BASE_URL = import.meta.env.BASE_URL;

const menuMap: Record<string, string> = {
  Home: "/",
  Schedule: "/schedule",
  Courses: "/course",
  Degree: "/degree",
};

const ProfileButton = ({ user }: { user: SCHEMA["User"] }) => {
  const submit = useSubmit();
  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button type="button">
          <Avatar user={user} />
        </button>
      </DropdownMenu.Trigger>
      <DropdownMenu.Portal>
        <DropdownMenu.Content sideOffset={5} asChild>
          <div className="DropdownMenuContent">
            <DropdownMenu.Item className="DropdownMenuItem">
              <PersonIcon />
              <Link to="/auth/me">Profile</Link>
            </DropdownMenu.Item>
            <DropdownMenu.Item className="DropdownMenuItem">
              <ExitIcon />
              <button
                onClick={() => {
                  submit({}, { method: "POST", action: "/auth/logout" });
                }}
              >
                Logout
              </button>
            </DropdownMenu.Item>
            <DropdownMenu.Arrow className="DropdownMenuArrow" />
          </div>
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
};

const NavigationMenu = React.memo(() => {
  const { user, isLoggedIn } = useAuthContext("Profile");
  const linkClassName = ({ isActive }: { isActive: boolean }) =>
    isActive
      ? "flex h-full items-center bg-slate-600 px-4"
      : "flex h-full items-center hover:bg-slate-600 px-4";
  return (
    <div className="flex flex-shrink-0 h-16 w-full bg-slate-900 px-5 text-lg font-bold text-white shadow-lg shadow-slate-400 pr-8">
      <div className="flex flex-grow items-center">
        <img
          src={`${BASE_URL}logo.png`}
          alt="UOA Logo"
          className="h-full w-auto p-2"
        />
        {Object.entries(menuMap).map(([title, ref]) => (
          <NavLink to={ref} key={title} className={linkClassName}>
            {title}
          </NavLink>
        ))}
      </div>
      {isLoggedIn ? (
        <ProfileButton user={user} />
      ) : (
        <div>
          <NavLink to="/auth" className={linkClassName}>
            Login
          </NavLink>
        </div>
      )}
    </div>
  );
});

NavigationMenu.displayName = "NavigationMenu";

export { NavigationMenu };
