import { cn } from "@/lib/utils";
import { HTMLAttributes } from "react";

interface Props extends HTMLAttributes<HTMLHeadingElement> {}

const Title = ({ children, className }: Props) => {
  return <h1 className={cn("text-5xl font-bold", className)}>{children}</h1>;
};

export default Title;
