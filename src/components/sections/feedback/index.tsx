import { Button } from "@/components/ui/button";
import Section from "@/components/ui/section";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { Navigation } from "swiper/modules";
import { Swiper, SwiperSlide } from "swiper/react";
import FeedbackCard from "./feedback-card";

const CustomArrowButton = () => (
  <div className="gap-[10px] z-10 flex sm:justify-end justify-center w-full mt-4">
    <Button
      size="icon"
      className="rounded-full feedback-prev-arrow"
      variant="ghost"
    >
      <ChevronLeft className="" />
    </Button>
    <Button
      size="icon"
      className="rounded-full feedback-next-arrow"
      variant="ghost"
    >
      <ChevronRight className="" />
    </Button>
  </div>
);

const Feedback = () => {
  return (
    <Section className="bg-slate-200" id="feedback">
      <div>
        <Swiper
          navigation={{
            nextEl: ".feedback-next-arrow",
            prevEl: ".feedback-prev-arrow",
          }}
          spaceBetween={30}
          breakpoints={{
            600: {
              slidesPerView: 3,
            },
          }}
          modules={[Navigation]}
        >
          <CustomArrowButton />
          {[1, 2, 3, 4].map(() => (
            <SwiperSlide>
              <FeedbackCard />
            </SwiperSlide>
          ))}
        </Swiper>
      </div>
    </Section>
  );
};

export default Feedback;
