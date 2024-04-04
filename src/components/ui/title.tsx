import { cn } from "@/lib/utils";
import { HTMLAttributes } from "react";

interface Props extends HTMLAttributes<HTMLHeadingElement> {}

const Title = ({ children, className, ...rest }: Props) => {
  return (
    <h1 className={cn("sm:text-5xl text-4xl font-bold", className)} {...rest}>
      {children}
    </h1>
  );
};

export default Title;
