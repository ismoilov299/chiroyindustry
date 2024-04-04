import { cn } from "@/lib/utils";
import { HTMLAttributes } from "react";

interface Props extends HTMLAttributes<HTMLParagraphElement> {}

const Text = ({ children, className, ...rest }: Props) => {
  return (
    <p className={cn("text-base text-[#666666]", className)} {...rest}>
      {children}
    </p>
  );
};

export default Text;
