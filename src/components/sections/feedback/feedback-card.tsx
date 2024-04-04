import Text from "@/components/ui/text";

const FeedbackCard = () => {
  return (
    <div className="max-w-[400px] group">
      <div className="flex flex-col sm:gap-y-3 gap-y-2">
        <div className="w-full rounded-lg overflow-hidden">
          <img
            src="https://preview.colorlib.com/theme/pato/images/intro-01.jpg.webp"
            alt=""
            className="w-full h-full object-cover group-hover:scale-105 transition-all duration-500"
          />
        </div>
        <h2 className="sm:text-xl text-lg font-semibold">
          ROMANTIC RESTAURANT
        </h2>
        <Text>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam,
          blanditiis.
        </Text>
      </div>
    </div>
  );
};

export default FeedbackCard;
