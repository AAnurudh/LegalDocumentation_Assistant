import React from "react";

const About = () => {
  return (
    <>
      <div className="h-screen bg-gradient-to-r from-teal-400 to-cyan-500 flex items-center justify-center ">
        <div className="bg-white p-6 rounded-lg shadow-md ">
          <img
            src="https://res.cloudinary.com/dvgieawnp/image/upload/v1695017914/eac-pm-calls-for-codification-of-law-of-torts-punitive-damages-to-victims_yjmj3g.jpg" // Replace with your photo URL or import it
            alt="Law Photo"
            className="w-32 h-32 mx-auto rounded-full"
          />
          <h1 className="text-2xl font-semibold text-gray-800 mt-4 justify-center flex">
            About
          </h1>
          <h2 className="text-lg text-gray-600 mt-2 justify-center flex">
            LexAI-Legal document generating AI platform.
          </h2>
          <p className="text-gray-700 mt-4">
            We propose a web-based solution, where the user (i.e. small
            businesses or individuals) can prompt their situation or choose the
            type of legal document they wish to draft. Based on
            <br />
            the choice made, the user will be asked to answer a few required
            questions such as name of parties involved, date etc. The users will
            then be guided through a few essential questions, <br />
            like the names of parties involved. Then, our system seamlessly
            integrates their inputs into our comprehensive legal databases,
            streamlining the otherwise complex <br /> and time-consuming
            document drafting process.
            <br />
            <br />
            Additionally, our **AI-powered Legal Document Assistant** helps
            users for understanding the legal document by providing real-time
            responses to the queries. It ensures accuracy, <br />
            efficiency, and compliance, making legal document creation
            hassle-free and accessible to all.
          </p>
        </div>
      </div>
    </>
  );
};

export default About;
