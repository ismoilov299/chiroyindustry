import Section from "../ui/section";
import Text from "../ui/text";
import Title from "../ui/title";

const About = () => {
  return (
    <Section id="about">
      <div className="flex items-center sm:flex-row flex-col">
        <div className="sm:w-1/2">
          <div className="py-5 flex flex-col gap-y-8 items-center">
            <Title>About chiroyli</Title>
            <Text className="text-center">
              Lorem ipsum dolor sit, amet consectetur adipisicing elit. Totam
              laudantium aliquam nesciunt optio voluptatem consequatur
              asperiores nisi vel unde dolorem.
            </Text>
          </div>
        </div>
        <div className="sm:w-1/2">
          <div className="w-full flex justify-center">
            <div className="max-w-96 rounded-2xl overflow-hidden">
              <img
                src="https://preview.colorlib.com/theme/pato/images/our-story-01.jpg"
                alt="product"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      </div>
    </Section>
  );
};

export default About;
