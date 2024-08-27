import { NavigationMenu } from "./navigation_menu";
import { Outlet } from "react-router-dom";

function Root() {
  return (
    <main className="h-screen w-screen flex flex-col">
      <NavigationMenu />
      <div className="grow shrink-0">
        <div className="bg-gradient-to-t from-indigo-500 via-purple-500 to-pink-500 h-full w-full">
          <Outlet />
        </div>
      </div>
    </main>
  );
}

export default Root;
