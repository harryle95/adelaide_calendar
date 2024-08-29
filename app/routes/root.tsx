import React from "react";
import { NavigationMenu } from "./navigation_menu";
import { Outlet, useLoaderData, Await } from "react-router-dom";
import type { SCHEMA, User } from "../service";
import { AuthProvider } from "../service";

function Root({ profile }: { profile: SCHEMA["User"] }) {
  const [user, setUser] = React.useState<User>(profile);
  React.useEffect(() => {
    if (user.id !== profile.id) {
      setUser(profile);
    }
  }, [profile.id]);
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

function IndexPage() {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const result = useLoaderData() as any;
  return (
    <React.Suspense>
      <Await resolve={result.user}>
        {(user: SCHEMA["User"]) => <Root profile={user} />}
      </Await>
    </React.Suspense>
  );
}

export default IndexPage;
