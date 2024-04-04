import { Menu } from "lucide-react";
import { Button } from "./ui/button";

import { Sheet, SheetContent } from "./ui/sheet";
import { useState } from "react";
import { navLinks } from "@/constants/nav-links";
import { useScroll } from "@/hooks/useScroll";
import { cn } from "@/lib/utils";

const Navbar = () => {
  const [openMenu, setOpenMenu] = useState(false);
  const { isScrolled } = useScroll();

  return (
    <header
      className={cn(
        "fixed w-full top-0 left-0 right-0 z-50 transition-all duration-300",
        isScrolled ? "bg-white py-3 shadow-md" : "bg-transparent py-5"
      )}
    >
      <div className="container">
        <div className="flex justify-end">
          <Button
            variant="ghost"
            onClick={() => setOpenMenu(true)}
            className={isScrolled ? "" : "hover:bg-black"}
          >
            <Menu className={isScrolled ? "" : "text-white"} />
          </Button>
        </div>
      </div>
      <Sheet onOpenChange={setOpenMenu} open={openMenu}>
        <SheetContent>
          <nav className="mt-10 flex items-center gap-y-3 flex-col">
            {navLinks.map(({ label, url }) => (
              <a
                href={url}
                className="sm:text-lg text-base hover:underline"
                onClick={() => setOpenMenu(false)}
              >
                {label}
              </a>
            ))}
          </nav>
        </SheetContent>
      </Sheet>
    </header>
  );
};

export default Navbar;
