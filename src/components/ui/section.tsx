import { cn } from "@/lib/utils";
import { HTMLAttributes } from "react";

interface SectionProps extends HTMLAttributes<HTMLElement> {}

const Section = ({ children, className }: SectionProps) => {
  return (
    <section className={cn("py-10", className)}>
      <div className="container">{children}</div>
    </section>
  );
};

export default Section;
