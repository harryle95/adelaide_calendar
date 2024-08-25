import { NavigationMenu } from "./navigation_menu";
import { Outlet } from "react-router-dom";

function Root() {
  return (
    <main className="h-screen w-screen flex flex-col">
      <NavigationMenu />
      <div className="grow shrink-0">
        <Outlet />
      </div>
    </main>
  );
}

export default Root;
