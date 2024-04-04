import "swiper/css";
import Hero from "./components/sections/hero";
import Navbar from "./components/navbar";
import About from "./components/sections/about";
import Feedback from "./components/sections/feedback";
import Contact from "./components/sections/contact";

function App() {
  return (
    <>
      <Navbar />
      <Hero />
      <About />
      <Feedback />
      <Contact />
    </>
  );
}

export default App;
