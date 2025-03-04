import React, { useContext } from "react";
import { useState } from "react";
import Chatbot from "./chatbot";
import { Link } from "react-router-dom";
import Navbar from "./Navbar";
import { StepContext } from "./context/StepContext";

import {
  MobileNav,
  Typography,
  Button,
  IconButton,
  Card,
} from "@material-tailwind/react";

function Home() {
  const context = useContext(StepContext);
  const [openNav, setOpenNav] = React.useState(false);
  const [data, setData] = useState([]);

  React.useEffect(() => {
    window.addEventListener(
      "resize",
      () => window.innerWidth >= 960 && setOpenNav(false)
    );
    window.scrollTo(0, 0);

    context.setStep1(false);
    context.setStep2(false);
    context.setStep3(false);
    context.setStep4(false);

    fetch("http://127.0.0.1:5000/api/services")
      .then((res) => {
        if (!res.ok) {
          throw Error("could not fetch");
        }
        return res.json();
      })
      .then((res) => {
        console.log(res);
        setData(res);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  const navList = (
    <ul className="mb-4 mt-2 flex flex-col gap-2 lg:mb-0 lg:mt-0 lg:flex-row lg:items-center lg:gap-6 ">
      <Typography
        as="li"
        variant="small"
        color="blue-gray"
        className="p-1 font-normal"
      >
        <a href="#" className="flex items-center">
          About
        </a>
      </Typography>
      <Typography
        as="li"
        variant="small"
        color="blue-gray"
        className="p-1 font-normal"
      >
        <a href="#" className="flex items-center">
          Services
        </a>
      </Typography>
      <Typography
        as="li"
        variant="small"
        color="blue-gray"
        className="p-1 font-normal"
      >
        <a href="#" className="flex items-center">
          Docs
        </a>
      </Typography>
    </ul>
  );

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-600 to-violet-600">
      <div className="py-12 relative z-10">
        <Typography
          variant="h2"
          color="white"
          className="font-bold text-4xl font-serif text-center text-white mb-2 "
          style={{
            fontFamily:
              ' "DM Serif Display", "Open Sans", "PT Sans", sans-serif',
            marginTop: "90px",
          }}
        >
          Tired of making legal documents?
        </Typography>
        <Typography
          color="white"
          className="font-normal text-center"
          style={{ fontFamily: '  "PT Sans", sans-serif' }}
        >
          This is your one-stop destination to get all your queries resolved!
        </Typography>
        <div className="md:max-w-3xl mx-auto mt-14 -mb-7 px-3">
          <Typography
            color="white"
            className="font-light text-center md:text-xl text-base"
            style={{ fontFamily: '  "PT Sans", sans-serif' }}
          >
            Now seamlessly draft your legal documents without knowing any legal
            jargons. Just answer some easy questions and get your documents
            drafted with custom editable feature.
            <br />
            Not sure which document to choose? Ask our AI-powered Chatbot!!
          </Typography>
        </div>
        {data.length > 0 && (
          <Typography
            variant="h2"
            color="white"
            className="font-bold text-4xl font-serif text-center text-white -mb-14 "
            style={{
              fontFamily:
                ' "DM Serif Display", "Open Sans", "PT Sans", sans-serif',
              marginTop: "90px",
            }}
          >
            Available Documents
          </Typography>
        )}
        {data.length > 0 ? (
          <section className="text-black w-full">
            <div className="container lg:px-16 md:px-9 px-5 py-24 mx-auto w-full">
              <div className="flex flex-wrap -m-4 w-full">
                {data.map((service) => (
                  <Link
                    to={`/service/${service.service_id}`}
                    className="p-4 md:w-1/3 cursor-pointer transform transition ease-in-out hover:scale-90 duration-500"
                    key={service.service_id}
                  >
                    <div className="h-full border-2 border-gray-200 border-opacity-60 rounded-lg overflow-hidden">
                      <img
                        className="lg:h-48 md:h-36 w-full object-cover object-center"
                        src={service.img_link}
                        alt="blog"
                      />
                      <div className="bg-[#E6E6FA] h-full">
                        <div className="p-6">
                          <h2 className="text-lg font-bold text-black mb-3 text-center">
                            {service.service_name}
                          </h2>
                          <div className="flex justify-center mb-3 ">
                            <p className="text-lg font-normal text-black text-justify">
                              {service.description}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </section>
        ) : (
          <div className="flex justify-center items-center h-full w-full">
            <p className="text-4xl text-white font-semibold">Loading...</p>
          </div>
        )}
        <div className="chat-bot">{/* div for chatbot */}</div>
      </div>
    </div>
  );
}

export default Home;
