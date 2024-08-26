import { Outlet } from "react-router-dom";
import * as Form from "./form";
import { Link } from "react-router-dom";

const pageClass =
  "bg-gradient-to-t from-indigo-500 via-purple-500 to-pink-500 h-full w-full flex justify-center items-center";
const rootClass = "p-7 rounded-md flex flex-col bg-white";
const headerClass = "flex justify-center items-center font-bold text-3xl p-6";
const bodyClass = "flex flex-col gap-y-3";
const footerClass =
  "mt-3 flex items-center justify-center max-w-[300px] text-center";
const labelClass = "font-medium flex justify-between";
const inputClass = "px-2 py-1 rounded-md border-2 w-[300px]";
const buttonClass =
  "mt-3 rounded-2xl px-4 py-2 fond-extrabold bg-blue-500 text-white";
const linkClass = "text-blue-700 font-medium";

function SignUpForm() {
  return (
    <Form.Root className={rootClass}>
      <Form.Header className={headerClass} title="Sign-Up" />
      <Form.Body className={bodyClass} method="POST">
        <Form.InputGroup
          name="name"
          labelClassName={labelClass}
          inputClassName={inputClass}
          required
        />
        <Form.InputGroup
          name="password"
          type="password"
          labelClassName={labelClass}
          inputClassName={inputClass}
          required
        />
        <button type="submit" className={buttonClass}>
          Sign-up
        </button>
      </Form.Body>
    </Form.Root>
  );
}

function LoginForm() {
  return (
    <Form.Root className={rootClass}>
      <Form.Header className={headerClass} title="Login" />
      <Form.Body className={bodyClass} method="POST">
        <Form.InputGroup
          name="nameOrEmail"
          labelClassName={labelClass}
          inputClassName={inputClass}
          labelTitle="Username or Email"
          placeholder="Enter username or email address"
          required
        />
        <Form.InputGroupWithLink
          name="password"
          type="password"
          labelClassName={labelClass}
          inputClassName={inputClass}
          linkTo="./forgotPassword"
          linkTitle="ForgotPassword?"
          linkClassName={linkClass}
          className="flex justify-between"
          required
        />
        <button type="submit" className={buttonClass}>
          Login
        </button>
      </Form.Body>
      <Form.Footer>
        <div className={footerClass}>
          <div>
            Need an account?{" "}
            <Link to="./signup" className={linkClass}>
              Sign-up
            </Link>
          </div>
        </div>
      </Form.Footer>
    </Form.Root>
  );
}

function ForgotPasswordForm() {
  return (
    <Form.Root className={rootClass}>
      <Form.Header className={headerClass} title="Reset Password" />

      <Form.Body className={bodyClass}>
        <Form.InputGroup
          name="email"
          labelClassName={labelClass}
          inputClassName={inputClass}
          required
        />
        <button type="submit" className={buttonClass}>
          Submit
        </button>
      </Form.Body>
      <Form.Footer>
        <div className={footerClass}>
          A password reset email will be sent to your registered email.
        </div>
      </Form.Footer>
    </Form.Root>
  );
}

function ChangePasswordForm() {
  return (
    <Form.Root className={rootClass}>
      <Form.Header className={headerClass} title="Change Password" />

      <Form.Body className={bodyClass}>
        <Form.InputGroup
          name="oldPassword"
          labelClassName={labelClass}
          inputClassName={inputClass}
          labelTitle="Old Password"
          placeholder="Enter old password"
          required
        />
        <Form.InputGroup
          name="newPassword"
          labelClassName={labelClass}
          inputClassName={inputClass}
          labelTitle="New Password"
          placeholder="Enter new password"
          required
        />
        <button type="submit" className={buttonClass}>
          Submit
        </button>
      </Form.Body>
    </Form.Root>
  );
}

function Page() {
  return (
    <div className={pageClass}>
      <Outlet />
    </div>
  );
}

export default Page;
export { SignUpForm, LoginForm, ForgotPasswordForm, ChangePasswordForm };
