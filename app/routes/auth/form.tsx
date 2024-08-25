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
  labelTitle?: string;
}

function capitalise(name: string): string {
  return name.charAt(0).toUpperCase() + name.slice(1);
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
  const {
    labelClassName,
    inputClassName,
    name,
    labelTitle,
    placeholder,
    ...rest
  } = props;
  const isRequired = props.required ? "*" : "";
  const formatedTitle = labelTitle
    ? labelTitle + isRequired
    : capitalise(name) + isRequired;
  const formatedPlaceholder = placeholder ? placeholder : "Enter " + name;
  return (
    <>
      <label htmlFor={name} className={labelClassName}>
        {formatedTitle}
      </label>
      <input
        id={name}
        placeholder={formatedPlaceholder}
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
    labelTitle,
    placeholder,
    name,
    ...rest
  } = props;
  const isRequired = props.required ? "*" : "";
  const formattedTitle = labelTitle
    ? labelTitle + isRequired
    : capitalise(name) + isRequired;
  const formatedPlaceholder = placeholder ? placeholder : "Enter " + name;
  return (
    <>
      <div className={className}>
        <label htmlFor={name} className={labelClassName}>
          {formattedTitle}
        </label>
        <Link to={linkTo} className={linkClassName}>
          {linkTitle}
        </Link>
      </div>
      <input
        id={name}
        placeholder={formatedPlaceholder}
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
