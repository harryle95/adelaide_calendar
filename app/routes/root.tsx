import React from "react";
import { NavigationMenu } from "./navigation_menu";
import { Outlet } from "react-router-dom";
import type { User } from "../service";
import { AuthProvider } from "../service";

function Root() {
  const [user, setUser] = React.useState<User | null>(null);

  return (
    <AuthProvider user={user} setUser={setUser}>
      <main className="h-screen w-screen flex flex-col">
        <NavigationMenu />
        <div className="grow shrink-0">
          <div className="bg-gradient-to-t from-indigo-500 via-purple-500 to-pink-500 h-full w-full">
            <Outlet />
          </div>
        </div>
      </main>
    </AuthProvider>
  );
}

export default Root;
