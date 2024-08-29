import React from "react";
import { Link, NavLink } from "react-router-dom";
import * as PrimitiveAvatar from "@radix-ui/react-avatar";
import { useAuthContext, type SCHEMA } from "../service";
import "./navigation_style.css";
import "./drop_down_style.css";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import { ExitIcon, PersonIcon } from "@radix-ui/react-icons";

const menuMap: Record<string, string> = {
  Home: "/",
  Schedule: "/schedule",
  Courses: "/course",
  Degree: "/degree",
};

const getInitials = (name?: string) => {
  if (name) {
    const nameSplit = name.split(" ");
    if (nameSplit.length === 1) {
      const nameStr = nameSplit[0];
      return nameStr.length === 1 ? nameStr[0] : nameStr[0] + nameStr[1];
    }
    const firstInitial = nameSplit[0][0].toUpperCase();
    const lastInitial = nameSplit[nameSplit.length - 1][0].toUpperCase();
    return firstInitial + lastInitial;
  }
  return "JD";
};

const Avatar = ({ user }: { user: SCHEMA["User"] }) => {
  return (
    <PrimitiveAvatar.Root className="AvatarRoot">
      <PrimitiveAvatar.Image
        className="AvatarImage"
        src={user.avatarUrl!}
        alt={user.name!}
      />
      <PrimitiveAvatar.Fallback className="AvatarFallback" delayMs={600}>
        {getInitials(user.name!)}
      </PrimitiveAvatar.Fallback>
    </PrimitiveAvatar.Root>
  );
};

const ProfileButton = ({ user }: { user: SCHEMA["User"] }) => {
  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button type="button">
          <Avatar user={user} />
        </button>
      </DropdownMenu.Trigger>
      <DropdownMenu.Portal>
        <DropdownMenu.Content className="DropdownMenuContent" sideOffset={5}>
          <DropdownMenu.Item className="DropdownMenuItem">
            <PersonIcon />
            <Link to="/auth/me">Profile</Link>
          </DropdownMenu.Item>
          <DropdownMenu.Item className="DropdownMenuItem">
            <ExitIcon />
            <Link to="/auth/logout">Logout</Link>
          </DropdownMenu.Item>
          <DropdownMenu.Arrow className="DropdownMenuArrow" />
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
        <img src="/vite.svg" alt="Vite Logo" className="h-full w-auto p-2" />
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
