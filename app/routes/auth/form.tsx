import React from "react";
import { FormProps, Link } from "react-router-dom";
import { Form } from "react-router-dom";

type RootProps = React.ComponentPropsWithoutRef<"div">;
interface HeaderProps extends React.ComponentPropsWithoutRef<"h1"> {
  title: string;
}
interface FooterProps {
  children: React.ReactNode;
}
interface InputProps
  extends Omit<React.ComponentPropsWithoutRef<"input">, "name" | "id"> {
  name: string;
  labelClassName: string;
  inputClassName: string;
}

interface InputWithLinkProps extends InputProps {
  linkTo: string;
  linkTitle: string;
  linkClassName: string;
}

const Root = (props: RootProps) => {
  return <div {...props} />;
};

const Header = (props: HeaderProps) => {
  const { title, ...other } = props;
  return <h1 {...other}>{title}</h1>;
};

const Body = (props: FormProps) => {
  return <Form {...props} />;
};

const Footer = (props: FooterProps) => {
  return (
    <>
      <hr />
      {props.children}
    </>
  );
};

const InputGroup = (props: InputProps) => {
  const { labelClassName, inputClassName, name, ...rest } = props;
  const isRequired = props.required ? "*" : "";
  return (
    <>
      <label htmlFor={name} className={labelClassName}>
        {name.charAt(0).toUpperCase() + name.slice(1) + isRequired}
      </label>
      <input
        id={name}
        placeholder={`Enter ${name}`}
        name={name}
        {...rest}
        className={inputClassName}
      />
    </>
  );
};

const InputGroupWithLink = (props: InputWithLinkProps) => {
  const {
    linkTo,
    linkTitle,
    linkClassName,
    className,
    labelClassName,
    inputClassName,
    name,
    ...rest
  } = props;
  const isRequired = props.required ? "*" : "";
  return (
    <>
      <div className={className}>
        <label htmlFor={name} className={labelClassName}>
          {name.charAt(0).toUpperCase() + name.slice(1) + isRequired}
        </label>
        <Link to={linkTo} className={linkClassName}>
          {linkTitle}
        </Link>
      </div>
      <input
        id={name}
        placeholder={`Enter ${name}`}
        name={name}
        {...rest}
        className={inputClassName}
      />
    </>
  );
};

export { Root, Header, Body, Footer, InputGroup, InputGroupWithLink };
export type {
  InputProps,
  InputWithLinkProps,
  RootProps,
  HeaderProps,
  FooterProps,
};
