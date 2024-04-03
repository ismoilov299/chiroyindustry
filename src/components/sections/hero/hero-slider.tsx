import { Swiper, SwiperSlide } from "swiper/react";
import { AnimatePresence, motion } from "framer-motion";
import "swiper/css/effect-fade";
import "swiper/css/navigation";
import "swiper/css/pagination";

import { EffectFade, Navigation, Pagination } from "swiper/modules";
import Title from "@/components/ui/title";
import { ChevronLeft, ChevronRight } from "lucide-react";

const heroImages = [
  "https://preview.colorlib.com/theme/pato/images/slide1-01.jpg.webp",
  "https://preview.colorlib.com/theme/pato/images/master-slides-01.jpg.webp",
];

const CustomPagination = () => (
  <div
    id="pagination-wrapper"
    className="flex justify-center gap-3 relative z-20 w-auto !bottom-10"
  ></div>
);

const CustomArrowButton = () => (
  <div className="gap-[10px] flex absolute top-1/2 z-10 -translate-y-1/2 w-full">
    <button className="hero-arrow-right arrow sm:size-12 size-10 disabled:opacity-50 disabled:cursor-default bg-black/80 z-10 cursor-pointer hover:bg-black/50 center-mode rounded-full sm:left-10 left-5 top-0 absolute">
      <ChevronLeft className="text-white" />
    </button>
    <button className="hero-arrow-left arrow sm:size-12 size-10 disabled:opacity-50 disabled:cursor-default bg-black/80 z-10 cursor-pointer hover:bg-black/50 center-mode rounded-full sm:right-10 right-5 top-0 absolute">
      <ChevronRight className="text-white" />
    </button>
  </div>
);

const HeroSlider = () => {
  return (
    <div className="h-screen relative">
      <Swiper
        effect="fade"
        navigation={{
          nextEl: ".hero-arrow-left",
          prevEl: ".hero-arrow-right",
        }}
        modules={[EffectFade, Navigation, Pagination]}
        pagination={{
          clickable: true,
          el: "#pagination-wrapper",
          bulletClass: "hero-bullet",
          bulletActiveClass: "hero-bullet-active",
        }}
        className="h-full"
      >
        <CustomPagination />
        <CustomArrowButton />
        {heroImages.map((image) => (
          <SwiperSlide key={image} className="h-full">
            {({ isActive }) => (
              <>
                <div className="w-full h-full absolute left-0 top-0">
                  <img
                    src={image}
                    alt="hero"
                    className="h-full w-full object-cover"
                  />
                </div>
                <div className="h-full center-mode relative z-10">
                  <AnimatePresence>
                    {isActive && (
                      <motion.div
                        initial={{ y: -20, opacity: 0 }}
                        animate={{ y: 0, opacity: 1 }}
                        exit={{ y: -20, opacity: 0 }}
                        transition={{
                          duration: 0.5,
                          type: "tween",
                          ease: "easeOut",
                        }}
                        className="max-w-lg truncate"
                      >
                        <Title className="text-red-50">Chiroyli</Title>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </>
            )}
          </SwiperSlide>
        ))}
      </Swiper>
    </div>
  );
};

export default HeroSlider;
