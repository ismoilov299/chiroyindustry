import { cn } from "@/lib/utils";
import { HTMLAttributes } from "react";

interface SectionProps extends HTMLAttributes<HTMLElement> {}

const Section = ({ children, className, ...rest }: SectionProps) => {
  return (
    <section className={cn("sm:py-28 py-16", className)} {...rest}>
      <div className="container">{children}</div>
    </section>
  );
};

export default Section;
