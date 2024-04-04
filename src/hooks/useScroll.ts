import { useEffect, useState } from "react";

export const useScroll = (initialValue?: boolean) => {
  const [isScrolled, setIsScrolled] = useState(!!initialValue);

  const controlNavbar = () => {
    if (window.scrollY >= 300) {
      setIsScrolled(true);
    } else {
      setIsScrolled(false);
    }
  };

  useEffect(() => {
    window.addEventListener("scroll", controlNavbar);

    return () => {
      window.removeEventListener("scroll", controlNavbar);
    };
  }, []);

  return { isScrolled };
};
