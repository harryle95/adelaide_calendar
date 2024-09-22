import { route as schedule } from "./schedule";
import { route as course } from "./course";
import { route as auth } from "./auth";
import { route as degree } from "./degree";
import { route as test } from "./test";

export const routes = [...schedule, ...course, ...auth, ...degree, ...test];
